#!/usr/bin/env python3
"""
Hourly Domain Sync & Validator for CloudStream Repositories
===========================================================
Automatically rotates and verifies live domains in domains.json:
- Number increments (+1..+10) & decrements (-1..-2)
- TLD permutations (.com, .net, .org, .to, .xyz, .top, .live, .sbs, etc.)
- Gateway HTTP 301/302, meta refresh & JS window.location redirects
- Content verification (filters out parking, ISP block, and Cloudflare challenge pages)
"""

import os
import sys
import re
import json
import urllib.parse
from datetime import datetime
import warnings

import requests
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

DOMAINS_FILE = "domains.json"

COMMON_TLDS = [
    ".com", ".net", ".org", ".to", ".xyz", ".top", ".live",
    ".sbs", ".cfd", ".is", ".site", ".pw", ".me", ".cc",
    ".diy", ".ltd", ".co", ".pro", ".online", ".tv", ".app", ".nl", ".beer"
]

NEGATIVE_MARKERS = [
    "bu siteye erişim engellenmiştir",
    "mahkeme kararıyla",
    "erişim engeli",
    "domain satılıktır",
    "domain for sale",
    "buy this domain",
    "parked domain",
    "namesilo",
    "godaddy",
    "cloudflare ray id",
    "attention required! | cloudflare",
    "just a moment...",
    "404 not found",
    "default web site page",
    "apache2 default page"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache"
}

def log(msg: str):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}", flush=True)

class DomainChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.session.verify = False

    def is_alive(self, url: str) -> tuple[bool, str]:
        try:
            resp = self.session.get(url, timeout=(3.0, 5.0), allow_redirects=True)
            if resp.status_code != 200:
                return False, url

            text_lower = resp.text.lower()
            if len(resp.text) < 400:
                return False, url

            for marker in NEGATIVE_MARKERS:
                if marker in text_lower:
                    return False, url

            final_url = resp.url
            if not final_url.endswith("/"):
                final_url += "/"
            return True, final_url
        except Exception:
            return False, url

    def extract_redirect_target(self, gateway_url: str) -> str | None:
        try:
            resp = self.session.get(gateway_url, timeout=(3.0, 5.0), allow_redirects=False)
            if resp.status_code in (301, 302, 303, 307, 308):
                loc = resp.headers.get("Location")
                if loc:
                    return urllib.parse.urljoin(gateway_url, loc)

            if resp.status_code == 200:
                text = resp.text
                meta_match = re.search(r'content=[\'"][0-9]+;\s*url=([^\'"]+)[\'"]', text, re.I)
                if meta_match:
                    return urllib.parse.urljoin(gateway_url, meta_match.group(1))

                js_match = re.search(r'(?:window\.location(?:\.href)?|location\.href)\s*=\s*[\'"]([^\'"]+)[\'"]', text, re.I)
                if js_match:
                    return urllib.parse.urljoin(gateway_url, js_match.group(1))
        except Exception:
            pass
        return None

    def generate_mutations(self, original_url: str) -> list[str]:
        candidates = []
        parsed = urllib.parse.urlparse(original_url)
        scheme = parsed.scheme or "https"
        netloc = parsed.netloc

        if not netloc:
            return []

        host = netloc.split(":")[0]
        has_www = host.startswith("www.")
        raw_host = host[4:] if has_www else host

        parts = raw_host.rsplit(".", 1)
        if len(parts) == 2:
            domain_name, cur_tld = parts[0], "." + parts[1]
        else:
            domain_name, cur_tld = raw_host, ""

        def build_url(d_name: str, tld: str) -> str:
            prefix = "www." if has_www else ""
            return f"{scheme}://{prefix}{d_name}{tld}/"

        numbers = list(re.finditer(r'\d+', domain_name))
        if numbers:
            last_num_match = numbers[-1]
            num_str = last_num_match.group(0)
            num_val = int(num_str)
            start_idx, end_idx = last_num_match.span()

            for delta in range(1, 11):
                new_num_str = str(num_val + delta).zfill(len(num_str))
                new_d_name = domain_name[:start_idx] + new_num_str + domain_name[end_idx:]
                candidates.append(build_url(new_d_name, cur_tld))

            for delta in range(1, 3):
                if num_val - delta > 0:
                    new_num_str = str(num_val - delta).zfill(len(num_str))
                    new_d_name = domain_name[:start_idx] + new_num_str + domain_name[end_idx:]
                    candidates.append(build_url(new_d_name, cur_tld))

        for tld in COMMON_TLDS:
            if tld != cur_tld:
                candidates.append(build_url(domain_name, tld))

        if numbers:
            last_num_match = numbers[-1]
            num_str = last_num_match.group(0)
            num_val = int(num_str)
            start_idx, end_idx = last_num_match.span()
            for delta in [1, 2]:
                new_num_str = str(num_val + delta).zfill(len(num_str))
                new_d_name = domain_name[:start_idx] + new_num_str + domain_name[end_idx:]
                for tld in [".com", ".net", ".org", ".to", ".xyz", ".top", ".live", ".sbs"]:
                    candidates.append(build_url(new_d_name, tld))

        seen = set([original_url.rstrip("/") + "/"])
        unique_candidates = []
        for c in candidates:
            c_clean = c.rstrip("/") + "/"
            if c_clean not in seen:
                seen.add(c_clean)
                unique_candidates.append(c_clean)

        return unique_candidates

    def find_working_domain(self, source_name: str, current_candidates: list[str], gateways: list[str]) -> str | None:
        for url in current_candidates:
            alive, final_url = self.is_alive(url)
            if alive:
                log(f"[{source_name}] Aktif domain: {final_url}")
                return final_url

        log(f"[{source_name}] Mevcut domain kapalı, taranıyor...")

        for gw in gateways:
            target = self.extract_redirect_target(gw)
            if target:
                alive, final_url = self.is_alive(target)
                if alive:
                    log(f"[{source_name}] Gateway ({gw}) yönlendirmesi bulundu: {final_url}")
                    return final_url

        for base_url in current_candidates:
            mutations = self.generate_mutations(base_url)
            for cand in mutations:
                alive, final_url = self.is_alive(cand)
                if alive:
                    log(f"[{source_name}] Rotasyonda YENİ domain bulundu: {final_url}")
                    return final_url

        log(f"[{source_name}] ⚠️ Yeni domain bulunamadı.")
        return None

def main():
    if not os.path.exists(DOMAINS_FILE):
        log(f"Hata: {DOMAINS_FILE} bulunamadı.")
        sys.exit(1)

    with open(DOMAINS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    checker = DomainChecker()
    changed = False

    if "sources" in data and isinstance(data["sources"], dict):
        # TurkSpor schema
        for name, cfg in data["sources"].items():
            candidates = cfg.get("candidates", [])
            gateways = cfg.get("gateways", [])
            working = checker.find_working_domain(name, candidates, gateways)
            if working:
                if not candidates or candidates[0].rstrip("/") != working.rstrip("/"):
                    log(f"🔄 [{name}] Domain güncellendi: {candidates[0] if candidates else 'yok'} -> {working}")
                    cfg["candidates"] = [working] + [c for c in candidates if c.rstrip("/") != working.rstrip("/")]
                    changed = True
    else:
        # TurkSinema schema: { "Provider": ["url1", "url2"] }
        for name, urls in list(data.items()):
            if not isinstance(urls, list):
                continue
            working = checker.find_working_domain(name, urls, [])
            if working:
                if not urls or urls[0].rstrip("/") != working.rstrip("/"):
                    log(f"🔄 [{name}] Domain güncellendi: {urls[0] if urls else 'yok'} -> {working}")
                    data[name] = [working] + [u for u in urls if u.rstrip("/") != working.rstrip("/")]
                    changed = True

    if changed:
        with open(DOMAINS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        log("✅ domains.json yeni domainlerle güncellendi.")
    else:
        log("Tüm domainler zaten güncel.")

if __name__ == "__main__":
    main()
