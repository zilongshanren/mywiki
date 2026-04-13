---
title: Stop over-engineering static websites
url: https://apoorvaj.io/stop-overengineering-static-websites
published: '2025-10-04'
source_blog: apoorvaj.io
source_site: https://apoorvaj.io/
category: graphics
fetched: '2026-04-13'
---

I’ve used several static website generators over the years for this blog, and they’ve all failed me in various ways:

Over the years, I had also accumulated complexity in my website build
pipeline, where I pushed my changes to a git branch, which would trigger
a hook on [Netlify](https://www.netlify.com/), which would
start a Linux virtual machine, which would clone my repository, install
Astro, build the website, and deploy it to Netlify’s CDN.

I realized while building [papaya.io](https://papaya.io/)
that things don’t have to be this insane.

Just build and deploy from your local computer. CDN companies want you to sell you their worker VMs, but there’s no need for this. Cloudflare provides a tool called Wrangler that you can install locally to publish to their CDN. Other solutions (like self-hosting an HTTP server) can be done similarly, without a builder or a VM. One less computer to worry about.

If you’re happy to write in HTML, but don’t want to constantly
re-write shared content like headers and footers, you can literally
`fetch`

HTML and [insert it at run-time](https://mxb.dev/blog/buildless/). This
is like `#include`

for the web. Sure it’ll be a few more web
requests, but maybe the lowered complexity is worth it.

If you want to write in Markdown (like I do), then use [Pandoc](https://pandoc.org/), which is an executable, and also
a Python library, to transform Markdown into HTML. It even supports HTML
templates, math notation, and syntax highlighting.

Here’s my solution. It builds markdown to HTML, serves the result on
localhost, has a file-watcher for local development, and even builds the
RSS feed. And of course, it’s fully configurable, because it’s just a
Python file that I vibe-coded. It uses [bun](https://bun.sh/)
to serve files locally, but hey, you can use whatever you want,
including Python’s built-in HTTP server.

The web doesn’t have to be complicated or brittle. Get rid of complexity, and reclaim your independence.

#!/usr/bin/env python3
import os
import sys
import subprocess
import signal
import time
import argparse
import fnmatch
import shutil
from pathlib import Path
import pypandoc
# ANSI color codes
class Colors:
HEADER = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
def print_help():
print(f"{Colors.BOLD}{Colors.CYAN}Papaya Controller{Colors.ENDC}")
print(f"{Colors.YELLOW}Usage:{Colors.ENDC} ./run.py <command>")
print()
print(f"{Colors.GREEN}Available commands:{Colors.ENDC}")
print(f" {Colors.BLUE}serve{Colors.ENDC} - Start servers")
print(f" {Colors.BLUE}deploy{Colors.ENDC} - Deploy to Cloudflare Pages (dev branch)")
print(f" {Colors.BLUE}deploy --production{Colors.ENDC} - Deploy to Cloudflare Pages (main branch)")
print(f" {Colors.BLUE}help{Colors.ENDC} - Show this help message")
print()
# Load environment variables from a file.
def load_env(env_file='.env'):
if not os.path.exists(env_file):
print(f".env file doesn't exist. Creating a default .env file, set up for {Colors.BOLD}{Colors.RED}local development{Colors.ENDC}")
default_content = """
HTTP_SERVER_PORT=8000
# If you're someone with access to deploy secrets, add these:
PPY_CLOUDFLARE_PROJECT_NAME=█████
PPY_CLOUDFLARE_API_TOKEN=█████
PPY_CLOUDFLARE_ACCOUNT_ID=█████
"""
with open(env_file, 'w') as f:
f.write(default_content)
try:
with open(env_file, 'r') as f:
for line in f:
line = line.strip()
# Skip empty lines and comments
if line and not line.startswith('#'):
key, value = line.split('=', 1)
os.environ[key.strip()] = value.strip()
except FileNotFoundError:
print(f"{Colors.YELLOW}Warning: {env_file} file not found{Colors.ENDC}")
print()
def build_post(md_file):
"""Build a single post from a markdown file. Returns post metadata dict or None."""
with open(md_file, 'r') as f:
content = f.read()
# Parse front-matter
if content.startswith('---'):
parts = content.split('---', 2)
if len(parts) >= 3:
front_matter = parts[1].strip()
text_content = parts[2].strip()
# Extract title and date from front-matter
title = None
date = None
starred = False
for line in front_matter.split('\n'):
line = line.strip()
if line.startswith('title:'):
title = line.split(':', 1)[1].strip().strip('"')
elif line.startswith('date:'):
date = line.split(':', 1)[1].strip()
elif line.startswith('starred:'):
starred_value = line.split(':', 1)[1].strip().lower()
starred = starred_value == 'true'
# Create URL from filename (remove .md extension)
url = md_file.stem
# Convert markdown to HTML using pandoc with template
html_content = pypandoc.convert_text(
text_content,
'html',
format='md',
extra_args=[
'--template=src/post-template.html',
f'--metadata=title:{title}',
f'--metadata=date:{date}',
'--highlight-style=pygments',
'--katex'
]
)
# Write HTML file
output_path = Path(".output") / f"{url}.html"
with open(output_path, 'w') as f:
f.write(html_content)
return {
'title': title,
'date': date,
'url': url,
'text': text_content,
'starred': starred
}
else:
print(f"{Colors.RED}Error: {md_file.name} should start with front-matter{Colors.ENDC}")
return None
def build_index(posts):
from datetime import datetime
# Sort posts by date (newest first)
sorted_posts = sorted(posts, key=lambda p: datetime.strptime(p['date'], '%d %B %Y'), reverse=True)
# Build index.html
# Read the index template
with open('src/index-template.html', 'r') as f:
template = f.read()
# Generate blog post rows
post_rows = []
for post in sorted_posts:
star = '∗' if post.get('starred', False) else ''
post_rows.append(f'<tr class="block mb-2">\n<td class="postStar">{star}</td>\n<td>\n<a href="/{post["url"]}">{post["title"]}</a>\n</td>\n</tr>')
blog_posts_html = '\n'.join(post_rows)
# Replace the placeholder with actual posts
output = template.replace('{{BLOG_POSTS}}', blog_posts_html)
# Write the output
with open('.output/index.html', 'w') as f:
f.write(output)
# Build RSS feed
rss_items = []
for post in sorted_posts:
# Parse date and convert to RFC 822 format (RSS pubDate format)
date_obj = datetime.strptime(post['date'], '%d %B %Y')
# Format: "Thu, 18 Sep 2025 00:00:00 GMT"
rss_date = date_obj.strftime('%a, %d %b %Y 00:00:00 GMT')
rss_items.append(
f'<item>'
f'<title>{post["title"]}</title>'
f'<link>https://apoorvaj.io/{post["url"]}/</link>'
f'<guid>https://apoorvaj.io/{post["url"]}/</guid>'
f'<pubDate>{rss_date}</pubDate>'
f'</item>'
)
rss_content = (
'<?xml version="1.0" encoding="UTF-8"?>'
'<rss version="2.0">'
'<channel>'
'<title>apoorvaj.io</title>'
'<description>Apoorva Joshi\'s Blog</description>'
'<link>https://apoorvaj.io/</link>'
+ ''.join(rss_items) +
'</channel>'
'</rss>'
)
with open('.output/rss.xml', 'w') as f:
f.write(rss_content)
def watch_for_changes():
"""Watch for changes in posts/, static/, and src/ directories and rebuild accordingly"""
posts_dir = Path("posts")
static_dir = Path("static")
src_dir = Path("src")
posts_mtimes = {}
static_mtimes = {}
src_mtimes = {}
# Initialize file modification times for posts/
for md_file in posts_dir.glob("*.md"):
posts_mtimes[md_file] = md_file.stat().st_mtime
# Initialize file modification times for static/
for static_file in static_dir.rglob("*"):
if static_file.is_file():
static_mtimes[static_file] = static_file.stat().st_mtime
# Initialize file modification times for src/
for src_file in src_dir.rglob("*"):
if src_file.is_file():
src_mtimes[src_file] = src_file.stat().st_mtime
# Keep script running and watch for file changes
while True:
time.sleep(0.5)
# Check for modified or new files in posts/
for md_file in posts_dir.glob("*.md"):
current_mtime = md_file.stat().st_mtime
if md_file not in posts_mtimes or posts_mtimes[md_file] != current_mtime:
print(f"{Colors.CYAN}File changed: {md_file.name}{Colors.ENDC}")
posts_mtimes[md_file] = current_mtime
# Rebuild this post
build_post(md_file)
# Rebuild index page (need to re-read all posts for sorting)
posts = []
for f in posts_dir.glob("*.md"):
post = build_post(f)
if post:
posts.append(post)
build_index(posts)
print(f"{Colors.GREEN}Rebuilt {md_file.name}{Colors.ENDC}")
# Check for deleted files in posts/
deleted_posts = [f for f in posts_mtimes.keys() if not f.exists()]
for deleted_file in deleted_posts:
print(f"{Colors.YELLOW}File deleted: {deleted_file.name}{Colors.ENDC}")
del posts_mtimes[deleted_file]
# Remove corresponding HTML file
output_path = Path(".output") / f"{deleted_file.stem}.html"
if output_path.exists():
output_path.unlink()
# Rebuild index page
posts = []
for f in posts_dir.glob("*.md"):
post = build_post(f)
if post:
posts.append(post)
build_index(posts)
print(f"{Colors.GREEN}Removed {deleted_file.name}{Colors.ENDC}")
# Check for modified or new files in static/
for static_file in static_dir.rglob("*"):
if not static_file.is_file():
continue
current_mtime = static_file.stat().st_mtime
if static_file not in static_mtimes or static_mtimes[static_file] != current_mtime:
print(f"{Colors.CYAN}Static file changed: {static_file.relative_to(static_dir)}{Colors.ENDC}")
static_mtimes[static_file] = current_mtime
# Copy the file to .output maintaining directory structure
relative_path = static_file.relative_to(static_dir)
output_path = Path(".output") / relative_path
output_path.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(static_file, output_path)
print(f"{Colors.GREEN}Copied {relative_path}{Colors.ENDC}")
# Check for deleted files in static/
deleted_static = [f for f in static_mtimes.keys() if not f.exists()]
for deleted_file in deleted_static:
relative_path = deleted_file.relative_to(static_dir)
print(f"{Colors.YELLOW}Static file deleted: {relative_path}{Colors.ENDC}")
del static_mtimes[deleted_file]
# Remove corresponding file in .output
output_path = Path(".output") / relative_path
if output_path.exists():
output_path.unlink()
print(f"{Colors.GREEN}Removed {relative_path}{Colors.ENDC}")
# Check for modified or new files in src/
for src_file in src_dir.rglob("*"):
if not src_file.is_file():
continue
current_mtime = src_file.stat().st_mtime
if src_file not in src_mtimes or src_mtimes[src_file] != current_mtime:
print(f"{Colors.CYAN}Source file changed: {src_file.relative_to(src_dir)}{Colors.ENDC}")
src_mtimes[src_file] = current_mtime
# Do a full rebuild
print(f"{Colors.YELLOW}Doing full rebuild...{Colors.ENDC}")
build_full()
print(f"{Colors.GREEN}Full rebuild complete{Colors.ENDC}")
# Re-initialize all mtimes after full rebuild
posts_mtimes.clear()
for md_file in posts_dir.glob("*.md"):
posts_mtimes[md_file] = md_file.stat().st_mtime
static_mtimes.clear()
for static_file in static_dir.rglob("*"):
if static_file.is_file():
static_mtimes[static_file] = static_file.stat().st_mtime
break # Break the src file loop to avoid multiple rebuilds
def build_full():
if os.path.exists("./.output"):
shutil.rmtree("./.output")
# Create output directory
os.makedirs("./.output", exist_ok=True)
# Copy static/ folder contents to .output
shutil.copytree("static", ".output", dirs_exist_ok=True)
# Parse all markdown posts
posts = []
posts_dir = Path("posts")
for md_file in posts_dir.glob("*.md"):
post = build_post(md_file)
if post:
posts.append(post)
build_index(posts)
print(f"Built {len(posts)} posts")
def run_serve():
"""Start servers and keep them running until interrupted"""
build_full()
# HTTP server
# -----------
port = os.environ.get("HTTP_SERVER_PORT", "8000")
processes = {
'static': subprocess.Popen(["bunx", "serve", ".output", "-p", port, "--no-clipboard"])
}
# Cleanup: stop servers on script exit
def cleanup(signum, frame):
if processes['static']:
processes['static'].terminate()
processes['static'].wait()
print()
sys.exit(0)
signal.signal(signal.SIGINT, cleanup)
try:
watch_for_changes()
except KeyboardInterrupt:
cleanup(None, None)
def run_deploy(is_production=False):
# Check if production deployment is allowed
if is_production:
try:
current_branch = subprocess.run(
["git", "branch", "--show-current"],
capture_output=True,
text=True,
check=True
).stdout.strip()
if current_branch != "prod":
print(f"{Colors.RED}Error: Production deployment is only allowed from 'prod' branch{Colors.ENDC}")
print(f"Current branch: {current_branch}")
sys.exit(1)
except subprocess.CalledProcessError:
print(f"{Colors.RED}Error: Unable to determine current git branch{Colors.ENDC}")
sys.exit(1)
# Determine branch name
branch = "prod" if is_production else "dev"
# Get environment variables
cf_api_token = os.environ.get("PPY_CLOUDFLARE_API_TOKEN")
cf_account_id = os.environ.get("PPY_CLOUDFLARE_ACCOUNT_ID")
cf_project_name = os.environ.get("PPY_CLOUDFLARE_PROJECT_NAME")
# Check required environment variables
if not cf_api_token:
print(f"{Colors.RED}Error: PPY_CLOUDFLARE_API_TOKEN environment variable not set{Colors.ENDC}")
sys.exit(1)
if not cf_account_id:
print(f"{Colors.RED}Error: PPY_CLOUDFLARE_ACCOUNT_ID environment variable not set{Colors.ENDC}")
sys.exit(1)
if not cf_project_name:
print(f"{Colors.RED}Error: PPY_CLOUDFLARE_PROJECT_NAME environment variable not set{Colors.ENDC}")
sys.exit(1)
print(f"{Colors.GREEN}✔ Artifacts cleared{Colors.ENDC}")
build_full()
print(f"{Colors.GREEN}✔ Build done{Colors.ENDC}")
# Deploy using wrangler
deploy_cmd = [
"bunx", "wrangler", "pages", "deploy", ".output",
"--commit-dirty=true",
f"--project-name={cf_project_name}",
f"--branch={branch}"
]
# Set environment variables for wrangler
env = os.environ.copy()
env["CLOUDFLARE_API_TOKEN"] = cf_api_token
env["CLOUDFLARE_ACCOUNT_ID"] = cf_account_id
try:
result = subprocess.run(deploy_cmd, env=env)
if result.returncode == 0:
print(f"{Colors.GREEN}Successfully deployed to Cloudflare Pages ({branch} branch){Colors.ENDC}")
else:
print(f"{Colors.RED}Deployment failed{Colors.ENDC}")
sys.exit(1)
except FileNotFoundError:
print(f"{Colors.RED}Error: wrangler CLI not found. Please install it first.{Colors.ENDC}")
print("Install with: bun install")
sys.exit(1)
def main():
# Load env vars and populate global variables based on them
load_env()
# Check if running in nix shell
if not os.environ.get('IN_NIX_SHELL'):
print(f"{Colors.YELLOW}Warning: Not running in a nix shell environment. Run `nix develop`.{Colors.ENDC}")
print()
if len(sys.argv) < 2:
print(f"{Colors.RED}Error: No command specified{Colors.ENDC}")
print_help()
sys.exit(1)
command = sys.argv[1]
if command == "serve":
run_serve()
elif command == "deploy":
is_production = len(sys.argv) > 2 and sys.argv[2] == "--production"
run_deploy(is_production)
elif command == "help":
print_help()
else:
print(f"{Colors.RED}Error: Unknown command '{command}'{Colors.ENDC}")
print_help()
sys.exit(1)
if __name__ == "__main__":
main()