import os, json, urllib.request, html, datetime
from pathlib import Path
USER = "gowthame006-a11y"
def api(url, data=None):
    headers = {"Authorization": "Bearer " + os.environ["GITHUB_TOKEN"], "User-Agent": "gowtham-profile", "Accept": "application/vnd.github+json"}
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r: return json.load(r)
result = api("https://api.github.com/graphql", {"query": 'query($login:String!){user(login:$login){name followers{totalCount} contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount color}}}}}}', "variables": {"login": USER}})
if result.get("errors"): raise RuntimeError("GitHub contribution query failed: " + str(result["errors"]))
user = result["data"]["user"]
calendar = user["contributionsCollection"]["contributionCalendar"]
repos = []
page = 1
while True:
    batch = api(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}")
    repos += batch
    if len(batch) < 100: break
    page += 1
owned = [r for r in repos if not r["fork"]]
e = lambda value: html.escape(str(value))
s = ['<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="650" viewBox="0 0 1200 650" role="img" aria-labelledby="title description"><title id="title">Gowtham E. GitHub 3D contribution dashboard</title><desc id="description">Public GitHub contributions rendered as isometric columns. Column height indicates daily contribution count.</desc><rect width="1200" height="650" rx="24" fill="#0d1117"/><style>text{font-family:Arial,sans-serif;fill:#c9d1d9}.muted{fill:#8b949e}.blue{fill:#58a6ff}.green{fill:#3fb950}</style>']
def text(x,y,value,size=16,cls=""):
    s.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}">{e(value)}</text>')
text(36,52,"GOWTHAM E.",30,"blue")
text(36,82,"AI Engineer / Data Analyst / Software Developer",18)
text(36,111,"B.Tech AI & DS 2027 · Chennai",15,"muted")
stats=[("Contributions / last year",calendar["totalContributions"]),("Public repos",len(repos)),("Stars / owned repos",sum(r["stargazers_count"] for r in owned)),("Followers",user["followers"]["totalCount"])]
for i,(label,value) in enumerate(stats):
    x=36+i*288
    s.append(f'<rect x="{x}" y="140" width="270" height="88" rx="12" fill="#161b22" stroke="#30363d"/>')
    text(x+16,168,label,14,"muted")
    text(x+16,209,value,31,"green")
text(36,268,"3D CONTRIBUTION CALENDAR",19,"blue")
text(36,294,"One column per day · height represents contributions · last 12 months",14,"muted")
def poly(points,fill):
    s.append('<polygon points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y in points)+'" fill="'+fill+'" stroke="#0d1117" stroke-width=".6"/>')
# Draw back to front along the increasing projected screen Y.
cells=[]
for week_index,week in enumerate(calendar["weeks"]):
    for day_index,day in enumerate(week["contributionDays"]):
        x=85+week_index*17+day_index*17
        y=330+week_index*2.65-day_index*8
        cells.append((y,x,day))
for y,x,day in sorted(cells):
    count=day["contributionCount"]
    height=min(72,3+count*6) if count else 0
    color=day["color"] if count else "#21262d"
    a=(x,y);b=(x+15,y+2.3);c=(x+30,y-4.8);d=(x+15,y-7.1)
    s.append(f'<g><title>{e(day["date"])}: {count} contributions</title>')
    if height:
        poly([a,b,(b[0],b[1]-height),(a[0],a[1]-height)],"#0e4429")
        poly([b,c,(c[0],c[1]-height),(b[0],b[1]-height)],"#006d32")
    poly([(px,py-height) for px,py in [a,b,c,d]],color)
    s.append("</g>")
text(36,512,"PROJECTS",19,"blue")
text(36,542,"SSAGI V2 · Multi-agent analysis",16)
text(430,542,"MetaTagger AI · Content analysis",16)
text(825,542,"BasketIQ · Retail analytics",16)
text(36,581,"Current work: CAPIQ · PURSUIT AI 2.0 · Personal portfolio",16,"muted")
text(36,622,"Updated "+datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")+" · Public GitHub data · Column heights capped at 72px",13,"muted")
s.append("</svg>")
Path("docs").mkdir(exist_ok=True)
Path("docs/profile-3d.svg").write_text("".join(s),encoding="utf-8")
