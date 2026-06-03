import argparse
from PIL import Image
import os

def process_webp(input_path, output_path, speed_factor=1.0, quality=50, lossless=False):
    if not os.path.exists(input_path):
        print(f"Error: {input_path} not found.")
        return

    print(f"Reading {input_path}...")
    img = Image.open(input_path)
    
    frames = []
    durations = []
    
    try:
        while True:
            frames.append(img.copy())
            duration = img.info.get('duration', 100)
            durations.append(max(1, int(duration / speed_factor)))
            img.seek(img.tell() + 1)
    except EOFError:
        pass

    if frames:
        print(f"Processing {len(frames)} frames. Saving to {output_path}...")
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=img.info.get('loop', 0),
            lossless=lossless,
            quality=quality,
            method=4
        )
        print("Success!")
    else:
        print("No frames found")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process animated WebP (speed and compression)")
    parser.add_argument("input", help="Input WebP file")
    parser.add_argument("output", help="Output WebP file")
    parser.add_argument("--speed", type=float, default=1.0, help="Speed up factor (e.g. 2.0 for 2x faster)")
    parser.add_argument("--quality", type=int, default=50, help="Quality for compression (0-100), default 50")
    parser.add_argument("--lossless", action="store_true", help="Use lossless compression (increases file size)")
    
    args = parser.parse_args()
    process_webp(args.input, args.output, args.speed, args.quality, args.lossless)
