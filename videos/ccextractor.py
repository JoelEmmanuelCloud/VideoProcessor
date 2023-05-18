import subprocess

def extract_subtitles(video_path):
    # Run ccextractor binary with appropriate arguments to extract subtitles
    cmd = ['./ccextractor', video_path, '-o', 'subtitles.srt']
    subprocess.run(cmd, check=True)
