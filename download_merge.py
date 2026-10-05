#!/usr/bin/env python3
"""
Download and merge anime episode with German audio + German subtitles
"""

import subprocess
import os
import sys
import json
from pathlib import Path

def download_version(url, language, output_dir):
    """
    Download a specific version (German Dub or German Sub) using aniworld package
    """
    print(f"Downloading {language} from {url}...")
    
    # Use aniworld CLI to download
    cmd = [
        "aniworld",
        "--no-menu",
        "--language", language,
        "--output", output_dir,
        url
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Successfully downloaded {language}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {language}: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def extract_subtitles(video_path, output_srt_path):
    """
    Extract subtitles from video file using ffmpeg
    """
    print(f"Extracting subtitles from {video_path}...")
    
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-map", "0:s:0",  # Extract first subtitle track
        "-c:s", "srt",
        output_srt_path,
        "-y"  # Overwrite if exists
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully extracted subtitles to {output_srt_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error extracting subtitles: {e}")
        return False

def merge_audio_subtitles(video_path, srt_path, output_path):
    """
    Merge video with new subtitles using ffmpeg
    """
    print(f"Merging {video_path} with {srt_path}...")
    
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-i", srt_path,
        "-c", "copy",
        "-c:s", "mov_text",
        "-metadata:s:s:0", "language=ger",
        output_path,
        "-y"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully merged to {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error merging: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python download_merge.py <aniworld_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = Path("downloads")
    output_dir.mkdir(exist_ok=True)
    
    # Download German Dub version
    dub_success = download_version(url, "German Dub", str(output_dir))
    if not dub_success:
        print("Failed to download German Dub version")
        sys.exit(1)
    
    # Download German Sub version (for subtitles)
    sub_success = download_version(url, "German Sub", str(output_dir))
    if not sub_success:
        print("Failed to download German Sub version")
        sys.exit(1)
    
    # Find the downloaded files
    dub_files = list(output_dir.glob("*Dub*.mp4")) + list(output_dir.glob("*Dub*.mkv"))
    sub_files = list(output_dir.glob("*Sub*.mp4")) + list(output_dir.glob("*Sub*.mkv"))
    
    if not dub_files or not sub_files:
        print("Could not find downloaded files")
        sys.exit(1)
    
    dub_video = dub_files[0]
    sub_video = sub_files[0]
    
    # Extract subtitles from subbed version
    srt_path = output_dir / f"{sub_video.stem}.srt"
    if not extract_subtitles(str(sub_video), str(srt_path)):
        print("Failed to extract subtitles")
        sys.exit(1)
    
    # Merge German audio with German subtitles
    output_path = output_dir / f"{dub_video.stem}_merged.mkv"
    if not merge_audio_subtitles(str(dub_video), str(srt_path), str(output_path)):
        print("Failed to merge")
        sys.exit(1)
    
    print(f"\n✅ Success! Merged video saved to: {output_path}")
    
    # Output the path for GitHub Actions to capture
    print(f"OUTPUT_PATH={output_path}")

if __name__ == "__main__":
    main()
