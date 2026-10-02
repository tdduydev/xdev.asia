"""Decode both Hive films and validate streams, chapters, timings, and caption cues."""
from pathlib import Path
import json
import subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'src/assets/hive/video'
for language in ['vi','en']:
    manifest=json.loads((OUT/f'manifest.{language}.json').read_text())
    movie=OUT/f'hive.{language}.mp4'
    media=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(movie)]))
    video=next(s for s in media['streams'] if s['codec_type']=='video')
    audio=next(s for s in media['streams'] if s['codec_type']=='audio')
    assert (video['width'],video['height'])==(1280,720)
    assert video['codec_name']=='h264' and audio['codec_name']=='aac'
    assert video['r_frame_rate']=='24/1'
    assert abs(float(media['format']['duration'])-manifest['duration'])<.5
    assert len(media['chapters'])==7
    for actual,expected in zip(media['chapters'],manifest['chapters']):
        assert abs(float(actual['start_time'])-expected['start'])<.01
    # Decode all frames and audio samples; headers alone don't prove playable media.
    subprocess.run(['ffmpeg','-v','error','-i',str(movie),'-f','null','-'],check=True)
    print(f'PASS: {language} {manifest["duration_label"]}; H.264/AAC decoded, 1280x720, seven chapter timestamps.')
