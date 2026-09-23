"""Encode reproducible narrated MP4s and timestamped captions/chapters."""
import concurrent.futures,json,math,shutil,subprocess,wave
from pathlib import Path
import imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[1];FF=imageio_ffmpeg.get_ffmpeg_exe();OUT=ROOT/'src/assets/ai-studio/video';OUT.mkdir(parents=True,exist_ok=True)
def run(args):subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],check=True)
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
def build(lang):
 slides=json.loads((ROOT/f'docs/video/script.{lang}.json').read_text());work=Path('/tmp/xdev-video')/lang;durations=[]
 for i,s in enumerate(slides):
  assert (work/f'{i:02}.done').exists(),f'Narration incomplete: {lang}/{i}'
  wav=work/f'{i:02}.wav';run(['-i',str(work/f'{i:02}.mp3'),str(wav)])
  with wave.open(str(wav)) as w:durations.append(w.getnframes()/w.getframerate())
 # Keep both localized editions inside the requested 5–7 minute interval.
 raw=sum(durations)+len(slides)*.35
 rate=raw/400 if raw>415 or raw<305 else 1
 assert .75<=rate<=1.35, f'Narration needs editorial adjustment: {raw:.1f}s, rate {rate:.2f}'
 lengths=[math.ceil((d/rate+.35)*20)/20 for d in durations]
 def encode(i):
  duration=lengths[i]
  run(['-loop','1','-framerate','20','-i',str(work/f'{i:02}.png'),'-i',str(work/f'{i:02}.wav'),'-vf',f'fade=t=in:st=0:d=0.22,fade=t=out:st={duration-.22:.2f}:d=0.22','-af',f'atempo={rate:.6f},apad','-t',str(duration),'-c:v','libx264','-preset','veryfast','-tune','stillimage','-crf','24','-pix_fmt','yuv420p','-c:a','aac','-b:a','96k','-ar','48000','-threads','2',str(work/f'{i:02}.mp4')])
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(encode,range(len(slides))))
 concat=work/'concat.txt';concat.write_text(''.join(f"file '{work}/{i:02}.mp4'\n" for i in range(len(slides))))
 chapters=[];cues=[];offset=0;last=None;metadata=[';FFMETADATA1','title=AI Studio — Product tour','artist=xDev']
 for i,s in enumerate(slides):
  if s['chapter']!=last:
   chapters.append({'title':s['chapter_title'],'start':round(offset,3),'time':f'{int(offset)//60:02}:{int(offset)%60:02}'});last=s['chapter']
  for line in (work/f'{i:02}.jsonl').read_text().splitlines():
   cue=json.loads(line)
   if cue['type'] not in ['SentenceBoundary','WordBoundary']:continue
   start=offset+cue['offset']/1e7/rate;end=min(offset+lengths[i],start+cue['duration']/1e7/rate)
   cues.append(f'{stamp(start)} --> {stamp(end)}\n{cue["text"]}\n')
  offset+=lengths[i]
 for i,c in enumerate(chapters):
  end=chapters[i+1]['start'] if i+1<len(chapters) else offset
  metadata.extend(['[CHAPTER]','TIMEBASE=1/1000',f'START={round(c["start"]*1000)}',f'END={round(end*1000)}',f'title={c["title"]}'])
 meta=work/'metadata.txt';meta.write_text('\n'.join(metadata)+'\n')
 run(['-f','concat','-safe','0','-i',str(concat),'-i',str(meta),'-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(OUT/f'ai-studio.{lang}.mp4')])
 (OUT/f'captions.{lang}.vtt').write_text('WEBVTT\n\n'+'\n'.join(cues))
 shutil.copyfile(work/'00.png',OUT/f'poster.{lang}.png')
 manifest={'language':lang,'voice':'vi-VN-HoaiMyNeural' if lang=='vi' else 'en-US-JennyNeural','duration':round(offset,3),'duration_label':f'{int(offset)//60}:{int(offset)%60:02}','playback_rate':rate,'chapters':chapters,'slides':slides}
 (OUT/f'manifest.{lang}.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 print(lang,manifest['duration_label'],f'rate {rate:.3f}',flush=True)
for language in ['vi','en']:build(language)
