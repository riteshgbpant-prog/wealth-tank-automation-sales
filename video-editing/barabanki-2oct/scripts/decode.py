"""Decode every saved Google Drive download (tool-result JSON) into raw/<original name>, skipping ones already done."""
import json, base64, glob, os
TR = "/root/.claude/projects/-home-user-wealth-tank-automation-sales/99c3a598-01bb-5fbc-af4b-e9e63c696d58/tool-results/"
os.makedirs("raw", exist_ok=True)
for p in sorted(glob.glob(TR + "mcp-Google_Drive-download_file_content-*.txt")):
    try:
        d = json.load(open(p))
    except Exception as e:
        print("bad", p, e); continue
    out = "raw/" + d["title"]
    if os.path.exists(out): continue
    open(out, "wb").write(base64.b64decode(d["content"]))
    print("saved", d["title"], os.path.getsize(out))
