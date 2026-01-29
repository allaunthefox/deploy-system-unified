#!/usr/bin/env python3
"""
Idempotent Porkbun DNS utility for GitHub Pages
Requires environment variables: PORKBUN_API_KEY, PORKBUN_SECRET
Optional flags: --domain DOMAIN --github-user USER --dry-run
"""

import os
import sys
import argparse
import time
import requests

API_BASE = "https://porkbun.com/api/json/v3"
GITHUB_PAGES_IPS = [
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153",
]


def api_post(path, payload):
    url = f"{API_BASE}{path}"
    r = requests.post(url, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


def list_records(domain, apikey, secret):
    resp = api_post(f"/dns/list/{domain}", {"apikey": apikey, "secretapikey": secret})
    if resp.get("status") != "SUCCESS":
        raise RuntimeError(f"Failed to list records: {resp}")
    return resp.get("records", [])


def create_record(domain, apikey, secret, name, typ, content, ttl=3600, dry_run=False):
    payload = {
        "apikey": apikey,
        "secretapikey": secret,
        "name": name,
        "type": typ,
        "content": content,
        "ttl": ttl,
    }
    if dry_run:
        print("DRY-RUN create:", payload)
        return None
    resp = api_post(f"/dns/create/{domain}", payload)
    if resp.get("status") != "SUCCESS":
        raise RuntimeError(f"Create record failed: {resp}")
    return resp.get("record", resp.get("response"))


def update_record(domain, record_id, apikey, secret, name, typ, content, ttl=3600, dry_run=False):
    payload = {
        "apikey": apikey,
        "secretapikey": secret,
        "name": name,
        "type": typ,
        "content": content,
        "ttl": ttl,
    }
    if dry_run:
        print("DRY-RUN update:", record_id, payload)
        return None
    resp = api_post(f"/dns/update/{domain}/{record_id}", payload)
    if resp.get("status") != "SUCCESS":
        raise RuntimeError(f"Update record failed: {resp}")
    return resp.get("record", resp.get("response"))


def find_record_id(records, name, typ):
    for r in records:
        rname = r.get("name") or ""
        if rname == name and r.get("type") == typ:
            return r.get("id") or r.get("recordId") or r.get("recordID")
    return None


def ensure_apex_a_records(domain, apikey, secret, dry_run=False):
    records = list_records(domain, apikey, secret)
    # normalize name for apex: use empty string '' or '@' depending on provider; Porkbun returns '' for apex
    existing = [r for r in records if (r.get("name") or "") == "" and r.get("type") == "A"]
    existing_ips = {r.get("content") for r in existing}

    for ip in GITHUB_PAGES_IPS:
        if ip in existing_ips:
            print(f"A record for apex already set to {ip}")
            continue
        # create missing A record
        print(f"Creating A record for apex -> {ip}")
        create_record(domain, apikey, secret, "", "A", ip, dry_run=dry_run)

    # Optionally, remove extraneous apex A records not in the set (not implemented automatically)


def ensure_www_cname(domain, github_user, apikey, secret, dry_run=False):
    records = list_records(domain, apikey, secret)
    desired = f"{github_user}.github.io"
    # find www CNAME
    for r in records:
        if (r.get("name") or "") == "www" and r.get("type") == "CNAME":
            if r.get("content") == desired:
                print("www CNAME already correct")
                return
            else:
                rid = r.get("id") or r.get("recordId") or r.get("recordID")
                print(f"Updating www CNAME to {desired}")
                update_record(domain, rid, apikey, secret, "www", "CNAME", desired, dry_run=dry_run)
                return
    # not found, create
    print(f"Creating www CNAME -> {desired}")
    create_record(domain, apikey, secret, "www", "CNAME", desired, dry_run=dry_run)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--domain", default=os.environ.get("DOMAIN"), help="Domain to update (e.g., lastingfirstsolutions.com)")
    parser.add_argument("--github-user", default=os.environ.get("GITHUB_USER"), help="GitHub username for CNAME target")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    apikey = os.environ.get("PORKBUN_API_KEY")
    secret = os.environ.get("PORKBUN_SECRET")
    if not apikey or not secret:
        print("PORKBUN_API_KEY and PORKBUN_SECRET must be set in the environment", file=sys.stderr)
        sys.exit(2)
    if not args.domain:
        print("--domain or DOMAIN env var required", file=sys.stderr)
        sys.exit(2)
    if not args.github_user:
        print("--github-user or GITHUB_USER env var required", file=sys.stderr)
        sys.exit(2)

    print(f"Ensuring DNS for {args.domain} (www -> {args.github_user}.github.io)")

    try:
        ensure_apex_a_records(args.domain, apikey, secret, dry_run=args.dry_run)
        ensure_www_cname(args.domain, args.github_user, apikey, secret, dry_run=args.dry_run)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()
