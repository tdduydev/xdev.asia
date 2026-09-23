"""Generate public product narration, with resumable output and bounded requests."""
import asyncio,json
from pathlib import Path
import edge_tts
ROOT=Path(__file__).resolve().parents[1]
async def main():
 sem=asyncio.Semaphore(4)
 async def narrate(lang,voice,i,s):
  async with sem:
   out=Path('/tmp/xdev-video')/lang;out.mkdir(parents=True,exist_ok=True)
   audio=out/f'{i:02}.mp3';meta=out/f'{i:02}.jsonl';done=out/f'{i:02}.done'
   if done.exists():return
   for attempt in range(3):
    try:
     await edge_tts.Communicate(s['narration'],voice,rate='+0%').save(str(audio),str(meta));done.touch();break
    except Exception:
     if attempt==2:raise
     await asyncio.sleep(2)
   print(lang,i,s['slug'],flush=True)
 await asyncio.gather(*(narrate(lang,voice,i,s) for lang,voice in [('vi','vi-VN-HoaiMyNeural'),('en','en-US-JennyNeural')] for i,s in enumerate(json.loads((ROOT/f'docs/video/script.{lang}.json').read_text()))))
asyncio.run(main())
