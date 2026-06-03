import os
import requests
import argparse
import base64
import json
from dotenv import load_dotenv

# Carrega as variáveis do .env na raiz do projeto
load_dotenv()

def format_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_srt(alignment, srt_file_path):
    characters = alignment.get('characters', [])
    start_times = alignment.get('character_start_times_seconds', [])
    end_times = alignment.get('character_end_times_seconds', [])
    
    # 1. Agrupar caracteres em palavras
    words = []
    current_word = ""
    word_start = -1
    
    for i, char in enumerate(characters):
        if word_start == -1 and char.strip():
            word_start = start_times[i]
            
        current_word += char
        
        # Fim de palavra num espaço ou último caractere
        if not char.strip() or i == len(characters) - 1:
            if current_word.strip():
                # Fim da palavra é o end_time do caractere anterior (se for espaço) ou do atual
                word_end = end_times[i] if char.strip() else end_times[i-1] if i > 0 else end_times[i]
                words.append({
                    "text": current_word.strip(),
                    "start": word_start,
                    "end": word_end
                })
            current_word = ""
            word_start = -1

    # 2. Agrupar palavras em legendas (chunks de ~8 palavras)
    with open(srt_file_path, "w", encoding="utf-8") as f:
        chunk_size = 8
        srt_index = 1
        
        for i in range(0, len(words), chunk_size):
            chunk = words[i:i+chunk_size]
            if not chunk:
                continue
                
            start_time = chunk[0]['start']
            end_time = chunk[-1]['end']
            text = " ".join([w['text'] for w in chunk])
            
            f.write(f"{srt_index}\n")
            f.write(f"{format_srt_time(start_time)} --> {format_srt_time(end_time)}\n")
            f.write(f"{text}\n\n")
            srt_index += 1

def generate_tts(text_file, output_file, model_id="eleven_flash_v2_5"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    # Lê o Voice ID do config.json (não é sensível, pode ir pro git)
    import json
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)
            voice_id = config.get("ELEVENLABS_VOICE_ID")
    except Exception as e:
        print(f"Erro ao ler config.json: {e}")
        return

    if not api_key or not voice_id:
        print("Erro: ELEVENLABS_API_KEY no .env ou ELEVENLABS_VOICE_ID no config.json não encontrados.")
        return

    if not os.path.exists(text_file):
        print(f"Erro: O arquivo de texto '{text_file}' não foi encontrado.")
        return

    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read().strip()

    if not text:
        print("Erro: O arquivo de texto está vazio.")
        return

    # Usar endpoint de timestamps
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    print(f"Chamando a API da ElevenLabs (modelo: {model_id})...")
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        res_json = response.json()
        audio_bytes = base64.b64decode(res_json["audio_base64"])
        alignment = res_json.get("alignment", {})
        
        with open(output_file, 'wb') as f:
            f.write(audio_bytes)
            
        print(f"Sucesso! Áudio premium gerado em: {output_file}")
        
        # Gerar legenda se houver alignment
        if alignment:
            srt_path = output_file.rsplit('.', 1)[0] + ".srt"
            generate_srt(alignment, srt_path)
            print(f"Legenda gerada com sucesso em: {srt_path}")
            
    else:
        print(f"Erro na geração do áudio. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gera áudio TTS usando a ElevenLabs com Legendas (.srt)")
    parser.add_argument("text_file", help="Caminho para o arquivo de texto base")
    parser.add_argument("output_file", help="Caminho para salvar o áudio (.mp3)")
    parser.add_argument("--model", default="eleven_flash_v2_5", help="Modelo da ElevenLabs a ser usado")
    
    args = parser.parse_args()
    generate_tts(args.text_file, args.output_file, args.model)
