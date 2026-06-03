import os
import argparse
import subprocess
import sys

def run_command(cmd_list):
    print(f"\n[ORQUESTRADOR] Rodando: {' '.join(cmd_list)}")
    subprocess.run(cmd_list, check=True)

def generate_documentation(script_txt, webp_video, output_mp4):
    print("==================================================")
    print(" INICIANDO GERAÇÃO DE DOCUMENTAÇÃO AUTOMATIZADA")
    print("==================================================")
    
    # Nomes temporários e saídas
    base_name = os.path.splitext(os.path.basename(script_txt))[0]
    assets_dir = os.path.dirname(script_txt)
    
    # 1. Gerar o Áudio + SRT a partir do roteiro
    audio_mp3 = os.path.join(assets_dir, f"{base_name}_audio.mp3")
    srt_file = os.path.join(assets_dir, f"{base_name}_audio.srt")
    
    # Chama o script do tts-tools
    run_command([
        sys.executable, 
        ".agents/skills/tts-tools/scripts/elevenlabs_tts.py", 
        script_txt, 
        audio_mp3
    ])
    
    # 2. Fazer o merge do vídeo webp com o áudio e a legenda gerada
    # Chama o script do video-tools
    run_command([
        sys.executable,
        ".agents/skills/video-tools/scripts/merge_audio_video.py",
        webp_video,
        audio_mp3,
        output_mp4,
        "--srt", srt_file
    ])
    
    print("==================================================")
    print(f" SUCESSO! O VÍDEO DOCUMENTADO FOI GERADO:")
    print(f" -> {output_mp4}")
    print("==================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orquestrador para gerar vídeos de documentação automaticamente")
    parser.add_argument("script_txt", help="Arquivo do roteiro da documentação (.txt)")
    parser.add_argument("webp_video", help="Gravação em vídeo da tela bruta (.webp)")
    parser.add_argument("output_mp4", help="Nome do arquivo de saída em MP4")
    
    args = parser.parse_args()
    generate_documentation(args.script_txt, args.webp_video, args.output_mp4)
