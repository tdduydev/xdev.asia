"""Combine drawn frames with narration, preserving scene time and captions."""
import json,subprocess,shutil,zipfile
from pathlib import Path
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'src/assets/ai-studio/story';WORK=Path('/tmp/studio-story-v3');RENDER=Path('/tmp/story-render');FF=imageio_ffmpeg.get_ffmpeg_exe()
def run(args):subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*map(str,args)],check=True)
for lang in ['vi','en']:
 d=json.loads((OUT/f'manifest.{lang}.json').read_text());parts=[]
 for i,s in enumerate(d['scenes']):
  wav=WORK/f'{lang}-{i}-padded.wav';run(['-i',WORK/f'{lang}-{i}.mp3','-af','adelay=450:all=1,apad','-t',s['duration'],'-ar',48000,'-ac',1,wav]);parts.append(wav)
 concat=WORK/f'{lang}-concat.txt';concat.write_text(''.join(f"file '{p}'\n" for p in parts))
 run(['-f','concat','-safe',0,'-i',concat,'-c:a','aac','-b:a','128k',OUT/f'narration.v2.{lang}.m4a'])
 run(['-i',RENDER/f'story.{lang}.mp4','-i',OUT/f'narration.v2.{lang}.m4a','-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart','-t',d['duration'],OUT/f'story.v2.{lang}.mp4'])
 run(['-ss',d['scenes'][-1]['start']+9,'-i',OUT/f'story.v2.{lang}.mp4','-frames:v',1,OUT/f'poster.v2.{lang}.png'])
 shutil.copyfile(RENDER/f'story.{lang}-grid.jpg',ROOT/f'docs/video/story/contact.{lang}.jpg')
 shutil.copyfile(RENDER/f'story.{lang}-render.json',ROOT/f'docs/video/story/render.{lang}.json')
 print(lang,d['duration'],flush=True)
with zipfile.ZipFile(OUT/'source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in OUT.iterdir():
  if p.name in ['narration.vi.m4a','narration.en.m4a']:continue
  if p.suffix in ['.js','.html','.woff2','.svg','.txt','.m4a','.json','.vtt']:z.write(p,p.name)
