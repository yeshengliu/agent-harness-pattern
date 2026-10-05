"""Render original schematic animations; no source photos are modified."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math, subprocess

OUT = Path(__file__).parent
W, H, FPS, SECONDS = 1080, 1350, 24, 24
BG, INK, MUTED, LINE = '#101923', '#F1F5F9', '#A8BACB', '#35475A'
TEAL, AMBER = '#65DECF', '#F3B96A'
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'
def font(size, bold=False): return ImageFont.truetype(BOLD if bold else FONT, size)
def text(d, xy, s, size=30, color=INK, bold=False): d.text(xy, s, font=font(size,bold), fill=color)
def centered(d, xy, s, size=30, color=INK, bold=False):
    f=font(size,bold); box=d.textbbox((0,0),s,font=f); d.text((xy[0]-(box[2]-box[0])/2,xy[1]),s,font=f,fill=color)
def node(d, box, title, sub, active=False):
    d.rounded_rectangle(box, radius=18, fill='#19332F' if active else '#1B2836', outline=TEAL if active else LINE, width=3)
    cx=(box[0]+box[2])/2
    centered(d,(cx,box[1]+22),title,32,INK,True)
    centered(d,(cx,box[1]+67),sub,24,MUTED)
def edge(d, points, active=False, progress=0):
    d.line(points, fill=LINE, width=4, joint='curve')
    if active:
        lengths=[math.dist(a,b) for a,b in zip(points,points[1:])]; total=sum(lengths); at=progress*total
        for a,b,l in zip(points,points[1:],lengths):
            if at<=l:
                u=at/l if l else 0; x=a[0]+(b[0]-a[0])*u; y=a[1]+(b[1]-a[1])*u
                d.ellipse((x-10,y-10,x+10,y+10),fill=TEAL); break
            at-=l
    a,b=points[-2:]; theta=math.atan2(b[1]-a[1],b[0]-a[0]); x,y=b
    d.polygon([(x,y),(x-14*math.cos(theta-.5),y-14*math.sin(theta-.5)),(x-14*math.cos(theta+.5),y-14*math.sin(theta+.5))],fill=LINE)

CAP1=[('ONE FRONT DOOR','You ask. The dispatcher triages and delegates.'),('OWNERSHIP OUTLIVES A SESSION','A worklist records who owns each item.'),('SPECIALISTS START FRESH','Owners call reusable experts for bounded work.'),('AN OWNER EXITS','Its conversation ends. Its worklist claim stays.'),('A TIMER RESTARTS THE OWNER','Shared knowledge loads; other task chats stay out.'),('YOU REVIEW THE DECISION','Irreversible calls reach you as prepared work.')]
CAP2=[('COLLECT SIGNAL','Corrections / repeated mistakes / tickets / job failures'),('REQUIRE EVIDENCE','Verified correction or recurrence in two sessions'),('PROPOSE A SMALL EDIT','Facts refresh in memory; recurring procedures flag skills.'),('TRY TO PROVE IT WRONG','Independent refuter + held-out tests the loop cannot edit'),('PROMOTE AND MONITOR','Accepted prompt edit goes live; watch for recurrence.'),('ROLL BACK IF IT RETURNS','Restore the previous version and collect new evidence.')]
def frame(kind, t):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im); step=min(5,int(t/4)); p=(t%4)/4
    text(d,(70,55),'HARNESS NOTES  /  '+('01' if kind==1 else '02'),24,TEAL,True)
    title=['One conversation.','Three agent levels.'] if kind==1 else ['An agent harness','that learns carefully.']
    for i,s in enumerate(title): text(d,(70,112+i*66),s,57,INK,True)
    text(d,(70,265),'OWNERSHIP + RECOVERY' if kind==1 else 'EVIDENCE + REFUTATION + ROLLBACK',24,MUTED)
    if kind==1:
        node(d,(350,330,730,430),'YOU','One conversation',step==0 or step==5)
        node(d,(290,475,790,585),'L1 · Dispatcher','Triage / delegate / hook-enforced',step==0)
        node(d,(105,660,515,770),'L2 · Owner A','One work item',step in [1,3,4])
        node(d,(565,660,975,770),'L2 · Owner B','One work item',step==1)
        for x,a,b in [(80,'Investigator','Fresh call'),(390,'Reviewer','Fresh call'),(700,'Test fixer','Fresh call')]:
            node(d,(x,870,x+290,975),a,b,step==2)
        text(d,(80,830),'L3 · SPECIALISTS',23,MUTED)
        edge(d,[(540,430),(540,475)],step==0,p)
        edge(d,[(540,585),(540,620),(310,620),(310,660)],step==1,p)
        edge(d,[(540,585),(540,620),(770,620),(770,660)],step==1,p)
        for x in [225,535,845]: edge(d,[(310,770),(310,805),(x,805),(x,870)],step==2,p)
        if step==3:
            d.rounded_rectangle((105,660,515,770),18,fill='#392C23',outline=AMBER,width=3)
            centered(d,(310,684),'OWNER EXITED',30,AMBER,True)
            centered(d,(310,730),'Worklist claim remains',22,INK)
        if step==4: centered(d,(540,1003),'Timer → replacement owner → resume',27,TEAL,True)
        elif step==5: centered(d,(540,1003),'Uncertain → refuter | Irreversible → you',27,TEAL,True)
        else: centered(d,(540,1003),'Shared rules, skills, knowledge base & memory',25,MUTED)
        footer='30 / 47 dispatches started without a human*'
    else:
        boxes=[(70,355,480,465),(600,355,1010,465),(70,575,480,685),(600,575,1010,685),(70,795,480,905),(600,795,1010,905)]
        titles=[('Collect signal','Four sources'),('Verify evidence','Reject unsupported lessons'),('Propose prompt edit','Small, versioned change'),('Independent refuter','Protected held-out tests'),('Promote + monitor','Watch for the same mistake'),('Rollback','If the mistake returns')]
        for i,(box,(a,b)) in enumerate(zip(boxes,titles)): node(d,box,a,b,step==i)
        routes=[[(480,410),(600,410)],[(805,465),(805,520),(275,520),(275,575)],[(480,630),(600,630)],[(805,685),(805,740),(275,740),(275,795)],[(480,850),(600,850)],[(1010,850),(1040,850),(1040,315),(275,315),(275,355)]]
        for i,route in enumerate(routes): edge(d,route,step==i,p)
        centered(d,(540,955),'Failed evidence or tests → no promotion',27,AMBER)
        centered(d,(540,1001),'Facts → memory | Recurring procedures → skills',26,MUTED)
        footer='~1,950 resolved tickets → 11 manually edited skills*'
    cap=(CAP1 if kind==1 else CAP2)[step]
    d.line((70,1060,1010,1060),fill=LINE,width=2)
    text(d,(70,1090),f'{step+1:02d} / 06   '+cap[0],28,TEAL,True)
    # Caption wraps only at word boundaries.
    words=cap[1].split(); rows=['']
    for word in words:
        test=(rows[-1]+' '+word).strip()
        if d.textlength(test,font=font(30))>930: rows.append(word)
        else: rows[-1]=test
    for i,line in enumerate(rows): text(d,(70,1140+i*40),line,30)
    text(d,(70,1252),footer,25,INK,True)
    text(d,(70,1295),'*Author-reported results from the supplied draft.',20,MUTED)
    d.rectangle((0,H-6,int(W*t/SECONDS),H),fill=TEAL)
    return im

def render(kind):
    name='three-level-agents' if kind==1 else 'self-evolving-loop'
    args=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/(name+'.mp4'))]
    proc=subprocess.Popen(args,stdin=subprocess.PIPE)
    for i in range(FPS*SECONDS): proc.stdin.write(frame(kind,i/FPS).tobytes())
    proc.stdin.close()
    if proc.wait()!=0: raise RuntimeError('ffmpeg failed')
    frame(kind,8.5 if kind==1 else 12.5).save(OUT/(name+'-cover.png'))
    # Six-panel storyboard for visual QA.
    sheet=Image.new('RGB',(1080,900),BG)
    for i in range(6):
        img=frame(kind,i*4+2); img.thumbnail((360,450)); sheet.paste(img,((i%3)*360,(i//3)*450))
    sheet.save(OUT/(name+'-storyboard.jpg'))
    print(name+' rendered',flush=True)

if __name__=='__main__':
    render(1)
    render(2)
