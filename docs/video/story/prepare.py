"""Synthesize public narration with content-addressed caching and bounded concurrency."""
import asyncio,json,subprocess,math,hashlib
from pathlib import Path
import edge_tts,imageio_ffmpeg
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'src/assets/ai-studio/story';WORK=Path('/tmp/studio-story-v3');WORK.mkdir(exist_ok=True)
data=json.loads((Path(__file__).parent/'script.json').read_text())
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
async def main():
 sem=asyncio.Semaphore(1)
 async def voice(lang,i,s):
  async with sem:
   stem=WORK/f'{lang}-{i}';audio=stem.with_suffix('.mp3');meta=stem.with_suffix('.jsonl');cache=stem.with_suffix('.hash');fingerprint=hashlib.sha256(s['narration'].encode()).hexdigest()
   if not audio.exists() or not cache.exists() or cache.read_text()!=fingerprint:
    for attempt in range(4):
     try:
      await asyncio.wait_for(edge_tts.Communicate(s['narration'],'vi-VN-HoaiMyNeural' if lang=='vi' else 'en-US-JennyNeural').save(str(audio),str(meta)),90)
      cache.write_text(fingerprint);break
     except Exception:
      if attempt==3:raise
      await asyncio.sleep(5*(attempt+1))
   raw=subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(audio),'-f','s16le','-ac','1','-ar','24000','-'])
   s['duration']=math.ceil((len(raw)/48000+1.5)*24)/24;print(lang,i,s['kind'],s['duration'],flush=True)
 await asyncio.gather(*(voice(lang,i,s) for lang,scenes in data.items() for i,s in enumerate(scenes)))
 for lang,scenes in data.items():
  offset=0;captions=[]
  for i,s in enumerate(scenes):
   s['start']=offset
   for line in (WORK/f'{lang}-{i}.jsonl').read_text().splitlines():
    q=json.loads(line)
    if q['type'] in ('SentenceBoundary','WordBoundary'):
     a=offset+.45+q['offset']/1e7;b=a+q['duration']/1e7;captions.append(f'{stamp(a)} --> {stamp(b)}\n{q["text"]}\n')
   offset+=s['duration']
  manifest={'language':lang,'duration':offset,'fps':24,'scenes':scenes}
  (OUT/f'manifest.{lang}.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(OUT/f'data.{lang}.js').write_text('window.STORY = '+json.dumps(manifest,ensure_ascii=False)+';\n');(OUT/f'captions.{lang}.vtt').write_text('WEBVTT\n\n'+'\n'.join(captions))
asyncio.run(main())
