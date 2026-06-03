import os
import tempfile
import subprocess
from PIL import Image, ImageDraw, ImageFont
import shutil
import argparse
import re

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    try:
        output = subprocess.check_output(cmd).decode('utf-8').strip()
        return float(output)
    except Exception as e:
        print(f"Erro ao obter duração do áudio: {e}")
        return None

def parse_srt(srt_path):
    with open(srt_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    blocks = re.split(r'\n\s*\n', content)
    subs = []
    
    for block in blocks:
        lines = block.split('\n')
        if len(lines) >= 3:
            time_line = lines[1]
            text = " ".join(lines[2:])
            
            m = re.match(r'(\d+):(\d+):(\d+),(\d+)\s*-->\s*(\d+):(\d+):(\d+),(\d+)', time_line)
            if m:
                h1, m1, s1, ms1, h2, m2, s2, ms2 = map(int, m.groups())
                start_sec = h1*3600 + m1*60 + s1 + ms1/1000.0
                end_sec = h2*3600 + m2*60 + s2 + ms2/1000.0
                subs.append({"start": start_sec, "end": end_sec, "text": text})
    return subs

def merge_webp_audio(webp_path, audio_path, output_mp4, srt_path=None):
    print(f"Lendo o vídeo webp: {webp_path}")
    img = Image.open(webp_path)
    
    subs = []
    if srt_path and os.path.exists(srt_path):
        subs = parse_srt(srt_path)
        print(f"Lidos {len(subs)} blocos de legenda. Vamos queimar direto nas imagens!")
    
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
    except:
        font = ImageFont.load_default()
        
    temp_dir = tempfile.mkdtemp()
    
    # === Sincronização Dinâmica (Linear Warping) ===
    total_frames = getattr(img, "n_frames", 1)
    audio_duration = get_audio_duration(audio_path)
    
    if audio_duration and audio_duration > 0:
        target_fps = total_frames / audio_duration
        print(f"Sincronização Elástica ativada: {total_frames} quadros em {audio_duration:.2f}s de áudio.")
        print(f"O FPS do vídeo foi reajustado para {target_fps:.2f} para garantir sincronia perfeita.")
    else:
        target_fps = 20.0
        print(f"Aviso: Não foi possível obter a duração do áudio. Usando FPS padrão: {target_fps}")
        
    try:
        frame_idx = 0
        while True:
            frame = img.convert("RGBA")
            
            # O momento em que este frame vai aparecer no vídeo final
            current_time_sec = frame_idx / target_fps
            
            # Checa se há texto para esse exato momento no vídeo
            current_text = None
            for sub in subs:
                if sub["start"] <= current_time_sec <= sub["end"]:
                    current_text = sub["text"]
                    break
            
            if current_text:
                txt_layer = Image.new("RGBA", frame.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(txt_layer)
                
                try:
                    text_bbox = draw.textbbox((0, 0), current_text, font=font)
                    text_w = text_bbox[2] - text_bbox[0]
                    text_h = text_bbox[3] - text_bbox[1]
                except AttributeError:
                    text_w, text_h = draw.textsize(current_text, font=font)
                
                x = (frame.width - text_w) / 2
                y = frame.height - text_h - 60
                
                draw.rectangle([x - 20, y - 10, x + text_w + 20, y + text_h + 10], fill=(0,0,0,180))
                draw.text((x, y), current_text, font=font, fill=(255,255,255,255))
                
                frame = Image.alpha_composite(frame, txt_layer)
            
            frame_path = os.path.join(temp_dir, f"frame_{frame_idx:05d}.png")
            frame.convert("RGB").save(frame_path, "PNG")
            
            frame_idx += 1
            
            try:
                img.seek(img.tell() + 1)
            except EOFError:
                break
                
        cmd = [
            "ffmpeg", "-y",
            "-framerate", str(target_fps),
            "-i", os.path.join(temp_dir, "frame_%05d.png"),
            "-i", audio_path,
            "-c:v", "libx264",
            "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            output_mp4
        ]
        
        print("Rodando ffmpeg final...")
        subprocess.run(cmd, check=True)
        print(f"Sucesso! Vídeo salvo em: {output_mp4}")
        
    finally:
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Junta arquivo WebP animado com Áudio em um MP4")
    parser.add_argument("webp_file", help="Arquivo .webp de entrada")
    parser.add_argument("audio_file", help="Arquivo .mp3 de entrada")
    parser.add_argument("output_file", help="Arquivo .mp4 de saída")
    parser.add_argument("--srt", help="Caminho opcional para arquivo de legenda (.srt)", default=None)
    
    args = parser.parse_args()
    merge_webp_audio(args.webp_file, args.audio_file, args.output_file, args.srt)
