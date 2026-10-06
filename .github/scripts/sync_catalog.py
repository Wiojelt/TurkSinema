import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = "CloudStream/4.0"
TIMEOUT = 12

def process_file(json_path: Path) -> bool:
    if not json_path.exists():
        return False

    try:
        content = json_path.read_text(encoding="utf-8")
        data = json.loads(content)
    except Exception as e:
        print(f"Failed to read {json_path}: {e}")
        return False

    if not isinstance(data, list):
        return False

    modified = False

    for item in data:
        name = item.get("name", "Unknown")
        url = item.get("url")
        if not url:
            continue

        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                if resp.status != 200:
                    continue
                body = resp.read()
                actual_size = len(body)
                if actual_size < 512:
                    continue
                sha_hex = hashlib.sha256(body).hexdigest()
                actual_hash = f"sha256-{sha_hex}"

                cur_size = item.get("fileSize")
                cur_hash = item.get("fileHash")

                item_changed = False
                if cur_size != actual_size:
                    item["fileSize"] = actual_size
                    item_changed = True
                if cur_hash != actual_hash:
                    item["fileHash"] = actual_hash
                    item_changed = True

                if "?v=" in url:
                    parsed = urllib.parse.urlparse(url)
                    qs = urllib.parse.parse_qs(parsed.query)
                    short_hash = sha_hex[:12]
                    if qs.get("v") != [short_hash]:
                        qs["v"] = [short_hash]
                        new_query = urllib.parse.urlencode(qs, doseq=True)
                        item["url"] = urllib.parse.urlunparse(parsed._replace(query=new_query))
                        item_changed = True

                if item_changed:
                    print(f"Updated {name}: size={actual_size}, hash={sha_hex[:10]}...")
                    modified = True
                else:
                    print(f"Verified {name} (OK)")
        except Exception as e:
            print(f"Skipped {name} ({e})")

    if modified:
        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Saved updates to {json_path}")

    return modified

def main():
    root = Path(".").resolve()
    targets = [
        root / "plugins.json",
        root / "catalogs" / "live" / "plugins.json",
    ]

    total_changed = False
    for target in targets:
        if target.exists():
            print(f"\nProcessing {target}...")
            if process_file(target):
                total_changed = True

    if total_changed:
        print("\nManifest sync complete: updates applied.")
    else:
        print("\nManifest sync complete: all packages up to date.")

if __name__ == "__main__":
    main()
