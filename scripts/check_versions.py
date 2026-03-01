# =============================================================================
# Audit Event Identifier: DSU-PYS-500119
# Last Updated: 2026-02-28
# =============================================================================
import urllib.request
import json
import re
import sys
import ssl

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

def get_docker_hub_tags(namespace, image):
    url = f"https://hub.docker.com/v2/repositories/{namespace}/{image}/tags/?page_size=100"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            return [res["name"] for res in data.get("results", [])]
    except Exception as e:
        return []

def get_ghcr_tags(namespace, image):
    auth_url = f"https://ghcr.io/token?service=ghcr.io&scope=repository:{namespace}/{image}:pull"
    try:
        with urllib.request.urlopen(auth_url) as response:
            token_data = json.load(response)
            token = token_data["token"]
        
        list_url = f"https://ghcr.io/v2/{namespace}/{image}/tags/list"
        req = urllib.request.Request(list_url)
        req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
            return data.get("tags", [])
    except Exception as e:
        return []

def is_stable(tag):
    tag_lower = tag.lower()
    
    if any(x in tag_lower for x in ["beta", "alpha", "rc", "test", "nightly", "develop", "unstable", "pr-", "build", "sha-", "sha256", "dependabot", "docs", "latest"]):
        return False
        
    if tag_lower.startswith(("amd64", "arm", "linux-", "windows-", "arch-")):
         return False
    
    if re.match(r"^20\d{6}", tag): # YYYYMMDD
        return False

    if not re.search(r"\d+\.\d+", tag):
        return False

    return True

def parse_version(tag):
    clean = tag.lower()
    clean = re.sub(r"^[v]|version-", "", clean)
    clean = re.sub(r"-ls\d+.*$", "", clean)
    clean = re.sub(r"-r\d+.*$", "", clean)
    
    match = re.match(r"(\d+)\.(\d+)(\.(\d+))?", clean)
    if match:
        groups = match.groups()
        v = [int(groups[0]), int(groups[1]), int(groups[3]) if groups[3] else 0]
        return tuple(v)
    return (0,0,0)

def check_image(name, registry="docker", image_path=""):
    app_name_lower = name.lower()
    parts = image_path.split("/")
    if registry == "docker":
        if len(parts) == 2:
            tags = get_docker_hub_tags(parts[0], parts[1])
        else:
            tags = get_docker_hub_tags("library", parts[0])
    elif registry == "ghcr":
         tags = get_ghcr_tags(parts[0], parts[1])
    else:
        tags = []

    candidates = [t for t in tags if is_stable(t)]
    candidates.sort(key=parse_version, reverse=True)
    
    final_tag = "latest"
    
    if candidates:
        if "transmission" in app_name_lower:
            v4 = [c for c in candidates if parse_version(c)[0] == 4]
            if v4: candidates = v4
        
        # Additional filter for Plex (look for public releases, plex tags are messy often uuid)
        # Plex tags example: 1.40.1.8227-c0dd5a73e
        # We want the numeric part mostly.
        
        final_tag = candidates[0]
        
    print(f"{name}|{image_path}|{final_tag}")

images = [
    ("Jellyfin", "docker", "jellyfin/jellyfin"),
    ("Radarr", "docker", "linuxserver/radarr"),
    ("Sonarr", "docker", "linuxserver/sonarr"),
    ("Lidarr", "docker", "linuxserver/lidarr"),
    ("Prowlarr", "docker", "linuxserver/prowlarr"),
    ("Jellyseerr", "docker", "fallenbagel/jellyseerr"),
    ("Navidrome", "docker", "deluan/navidrome"),
    ("Transmission", "docker", "linuxserver/transmission"), 
    ("Homarr", "ghcr", "ajnart/homarr"),
    ("Vaultwarden", "docker", "vaultwarden/server"),
    ("Wastebin", "docker", "quxfoo/wastebin"),
    ("Plex", "docker", "plexinc/pms-docker"),
    ("Readarr", "docker", "linuxserver/readarr"),
]

for name, registry, path in images:
    check_image(name, registry, path)
