"""Create bilingual narrated Hive films from synthetic-data UI captures.

Run with the isolated environment described in docs/hive/README.md.
Public product narration is sent to Edge TTS. Content-addressed cache allows retries.
"""
import asyncio
import hashlib
import json
import math
import os
import shutil
import subprocess
import textwrap
from pathlib import Path
import edge_tts
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'src/assets/hive/video'
WORK=Path(os.environ.get('HIVE_VIDEO_WORK','/tmp/xdev-hive-video'))
FF=shutil.which('ffmpeg')
FONT=Path(os.environ.get('HIVE_VIDEO_FONT','/System/Library/Fonts/Supplemental/Arial.ttf'))
BOLD=FONT.with_name('Arial Bold.ttf')
FPS=24

def command(args):
 subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],check=True)
def stamp(t):
 ms=round(t*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'
def font(size,bold=False):return ImageFont.truetype(str(BOLD if bold else FONT),size)
def wrapped(draw,text,xy,width,size,color,bold=False,spacing=1.3):
 words=text.split();lines=[];line='';f=font(size,bold)
 for word in words:
  candidate=(line+' '+word).strip()
  if draw.textlength(candidate,font=f)>width and line:lines.append(line);line=word
  else:line=candidate
 if line:lines.append(line)
 x,y=xy
 for line in lines:draw.text((x,y),line,font=f,fill=color);y+=round(size*spacing)
 return y

def frame(lang,i,s,count):
 im=Image.new('RGB',(1280,720),'#f7f9fc');d=ImageDraw.Draw(im)
 logo=Image.open(OUT/'brand.png').convert('RGBA')
 im.paste(logo,(32,6),logo)
 d.text((1000,42),'xdev.asia / hive',font=font(17),fill='#586a83')
 d.line((36,92,1244,92),fill='#dce4ef',width=1)
 if s['image']:
  d.text((42,124),f"{s['chapter']:02} / 07",font=font(16,True),fill='#0759ed')
  y=wrapped(d,s['chapter_title'],(42,155),300,19,'#586a83')
  y=wrapped(d,s['title'],(42,y+28),315,38,'#17243d',True,1.15)
  wrapped(d,s['description'],(42,y+26),305,22,'#586a83')
  shot=Image.open(ROOT/f"src/assets/hive/{s['image']}.{lang}.png").convert('RGB');shot.thumbnail((832,554),Image.Resampling.LANCZOS)
  x=400+(832-shot.width)//2;y=119+(554-shot.height)//2
  d.rounded_rectangle((x-1,y-1,x+shot.width+1,y+shot.height+1),radius=8,fill='#dce4ef');im.paste(shot,(x,y))
 else:
  d.rounded_rectangle((35,115,1245,647),radius=24,fill='#102544')
  wrapped(d,s['title'],(76,150),1100,54,'#ffffff',True,1.18)
  wrapped(d,s['description'],(78,294),1050,25,'#b5c9e5')
  if s['slug']=='problem':
   labels=['Repo / instructions','Chat / decisions','Task / owner'] if lang=='en' else ['Repo / quy chuẩn','Chat / quyết định','Task / người nhận']
  else:labels=['Claim','Build','Review','Learn'] if lang=='en' else ['Nhận việc','Xây dựng','Review','Học hỏi']
  gap=20;w=(1080-gap*(len(labels)-1))//len(labels)
  for j,label in enumerate(labels):
   x=80+j*(w+gap);d.rounded_rectangle((x,405,x+w,494),radius=12,fill='#1d3a60',outline='#47709f',width=1)
   d.text((x+20,431),label,font=font(22,True),fill='white')
  d.text((80,553),'Claude Code   /   Codex   /   Gemini CLI   /   Cursor',font=font(24),fill='#80b8ff')
  d.text((80,597),'MCP  ·  Desktop  ·  Web hub',font=font(18),fill='#b5c9e5')
 note='Giao diện demo · Giọng đọc tổng hợp' if lang=='vi' else 'Demo interface · Synthetic narration'
 d.line((36,676,1244,676),fill='#dce4ef',width=1);d.text((42,687),note,font=font(13),fill='#586a83')
 d.text((1140,687),f'{i+1:02} / {count:02}',font=font(13),fill='#586a83')
 target=WORK/lang/f'{i:02}.png';im.save(target)
 return target

async def narrate(lang,i,s):
 work=WORK/lang;work.mkdir(parents=True,exist_ok=True)
 voice='vi-VN-HoaiMyNeural' if lang=='vi' else 'en-US-JennyNeural'
 audio=work/f'{i:02}.mp3';meta=work/f'{i:02}.jsonl';cache=work/f'{i:02}.hash'
 digest=hashlib.sha256((voice+s['narration']).encode()).hexdigest()
 if not(audio.exists() and cache.exists() and cache.read_text()==digest):
  for attempt in range(3):
   try:
    await asyncio.wait_for(edge_tts.Communicate(s['narration'],voice,boundary='WordBoundary').save(str(audio),str(meta)),timeout=60)
    cache.write_text(digest);break
   except Exception:
    if attempt==2:raise
    await asyncio.sleep(2)
 print('Narration',lang,i+1,flush=True)

async def prepare():
 # Bounded concurrency avoids hammering the speech service.
 sem=asyncio.Semaphore(2)
 async def one(lang,i,s):
  async with sem:await narrate(lang,i,s)
 await asyncio.gather(*(one(lang,i,s) for lang in ['vi','en'] for i,s in enumerate(json.loads((ROOT/f'docs/hive/script.{lang}.json').read_text()))))

def build(lang):
 slides=json.loads((ROOT/f'docs/hive/script.{lang}.json').read_text());work=WORK/lang
 chapters=[];cues=[];offset=0;last=None
 for i,s in enumerate(slides):
  audio=work/f'{i:02}.mp3'
  duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(audio)]))
  length=math.ceil((duration+.9)*FPS)/FPS
  picture=frame(lang,i,s,len(slides));frames=round(length*FPS)
  # A restrained camera push plus short fades gives held UI shots readable motion.
  vf=f"zoompan=z='min(1.018,1+on*0.018/{frames})':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={frames}:s=1280x720:fps={FPS},fade=t=in:st=0:d=0.25,fade=t=out:st={length-.25}:d=0.25"
  command(['-i',str(picture),'-i',str(audio),'-vf',vf,'-af','apad','-t',str(length),'-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-ar','48000','-threads','2',str(work/f'{i:02}.mp4')])
  if s['chapter']!=last:
   chapters.append({'title':s['chapter_title'],'start':round(offset,3),'time':f'{int(offset)//60:02}:{int(offset)%60:02}'});last=s['chapter']
  words=[json.loads(line) for line in (work/f'{i:02}.jsonl').read_text().splitlines() if json.loads(line)['type']=='WordBoundary']
  for n in range(0,len(words),7):
   group=words[n:n+7];start=offset+group[0]['offset']/1e7;end=offset+(group[-1]['offset']+group[-1]['duration'])/1e7
   cues.append(f"{stamp(start)} --> {stamp(min(offset+length,end))}\n{' '.join(q['text'] for q in group)}\n")
  s['start']=round(offset,3);s['duration']=length;offset+=length
  print('Encoded',lang,i+1,flush=True)
 concat=work/'concat.txt';concat.write_text(''.join(f"file '{work}/{i:02}.mp4'\n" for i in range(len(slides))))
 metadata=[';FFMETADATA1','title=xDev Hive — Product story','artist=xDev']
 for i,c in enumerate(chapters):
  end=chapters[i+1]['start'] if i+1<len(chapters) else offset
  metadata.extend(['[CHAPTER]','TIMEBASE=1/1000',f'START={round(c["start"]*1000)}',f'END={round(end*1000)}',f'title={c["title"]}'])
 meta=work/'metadata.txt';meta.write_text('\n'.join(metadata)+'\n')
 command(['-f','concat','-safe','0','-i',str(concat),'-i',str(meta),'-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(OUT/f'hive.{lang}.mp4')])
 shutil.copyfile(work/'00.png',OUT/f'poster.{lang}.png')
 (OUT/f'captions.{lang}.vtt').write_text('WEBVTT\n\n'+'\n'.join(cues))
 data={'language':lang,'duration':round(offset,3),'duration_label':f'{int(offset)//60}:{int(offset)%60:02}','voice':'vi-VN-HoaiMyNeural' if lang=='vi' else 'en-US-JennyNeural','chapters':chapters,'slides':slides}
 (OUT/f'manifest.{lang}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('Completed',lang,data['duration_label'],flush=True)

if __name__=='__main__':
 assert FF and FONT.exists(),'Install ffmpeg and set HIVE_VIDEO_FONT to an Arial-compatible TTF font.'
 OUT.mkdir(parents=True,exist_ok=True);WORK.mkdir(parents=True,exist_ok=True)
 asyncio.run(prepare())
 for locale in ['vi','en']:build(locale)
