import os, json, urllib.request, html, collections, datetime
from pathlib import Path

username = os.environ.get("PROFILE_USER", "gowthame006-a11y")
token = os.environ.get("GITHUB_TOKEN", "")
def get(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "profile-metrics"}
    if token:
        headers["Authorization"] = "Bearer " + token
    with urllib.request.urlopen(urllib.request.Request("https://api.github.com/" + path, headers=headers), timeout=30) as response:
        return json.load(response)
user = get("users/" + username)
repos = []
page = 1
while True:
    batch = get(f"users/{username}/repos?per_page=100&page={page}")
    repos.extend(batch)
    if len(batch) < 100: break
    page += 1
owned = [r for r in repos if not r["fork"]]
languages = collections.Counter(r["language"] for r in owned if r["language"])
stars = sum(r["stargazers_count"] for r in owned)
forks = sum(r["forks_count"] for r in owned)
escape = lambda s: html.escape(str(s))
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="420" viewBox="0 0 1000 420" role="img" aria-label="Public GitHub metrics"><rect width="1000" height="420" rx="20" fill="#0d1117"/><style>text{font-family:Arial,sans-serif;fill:#c9d1d9}.title{fill:#58a6ff;font-size:23px;font-weight:bold}.label{fill:#8b949e;font-size:15px}.value{fill:#3fb950;font-size:32px;font-weight:bold}</style>']
parts += [f'<text x="36" y="49" class="title">{escape(user.get("name") or username)} / GitHub metrics</text>', '<text x="36" y="78" class="label">Public activity overview · live data snapshot</text>']
for i, (label, value) in enumerate([("Public repositories", user["public_repos"]), ("Stars received", stars), ("Forks received", forks), ("Followers", user["followers"])]):
    x = 36 + i * 235
    parts += [f'<rect x="{x}" y="105" width="215" height="100" rx="12" fill="#161b22"/>', f'<text x="{x+18}" y="140" class="label">{label}</text>', f'<text x="{x+18}" y="181" class="value">{value}</text>']
parts += ['<text x="36" y="246" class="title">Repository languages</text>']
for i, (lang, count) in enumerate(languages.most_common(4)):
    y = 277 + i * 27
    width = max(4, int(560 * count / max(sum(languages.values()), 1)))
    parts += [f'<text x="36" y="{y}" font-size="15">{escape(lang)}</text>', f'<rect x="190" y="{y-13}" width="{width}" height="14" rx="5" fill="#3fb950"/>', f'<text x="{205+width}" y="{y}" class="label">{count} repos</text>']
if not languages:
    parts += ['<text x="36" y="281" class="label">Language data will appear as source repositories are published.</text>']
parts += [f'<text x="36" y="399" class="label">Updated {datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")} · Languages count primary languages of owned public, non-fork repos.</text>', '</svg>']
Path("metrics.svg").write_text("".join(parts), encoding="utf-8")
