---
title: How to Exfiltrate Code from Bitbucket
url: https://etodd.io/2021/07/21/how-to-exfiltrate-code-from-bitbucket/
published: '2021-07-21'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# How to Exfiltrate Code from Bitbucket

Every year or so, something compels me to start over with a fresh OS image. Most recently, that something was an unfortunate water bottle incident. Once again, I need to pull down my digital life from the internet.

The code and assets for this blog currently live in a 500 MB Git repository, which was hosted on Bitbucket until earlier today. Let's try cloning it!

```
evantodd@HW-0063 ~ % git clone git@bitbucket.org:etodd/etodd.io.git
Cloning into 'etodd.io'...
remote: Enumerating objects: 2237, done.
remote: Counting objects: 100% (2237/2237), done.
remote: Compressing objects: 99% (1885/1903)
# hang
```


No worries, we can clone over HTTPS!

```
git clone https://etodd@bitbucket.org/etodd/etodd.io.git
Cloning into 'etodd.io'...
Password for 'https://etodd@bitbucket.org':
remote: Enumerating objects: 2237, done.
remote: Counting objects: 100% (2237/2237), done.
remote: Compressing objects: 100% (1903/1903), done.
Receiving objects: 22% (507/2237), 20.75 MiB | 278.00 KiB/s
# hang
```


No worries, we can [shallow clone](https://github.blog/2020-12-21-get-up-to-speed-with-partial-clone-and-shallow-clone/)!

```
evantodd@HW-0063 ~ % git clone --depth 1 git@bitbucket.org:etodd/etodd.io.git
Cloning into 'etodd.io'...
remote: Enumerating objects: 928, done.
remote: Counting objects: 100% (928/928), done.
remote: Compressing objects: 100% (895/895), done.
# hang
```


No worries, we can shallow clone over HTTPS!

```
evantodd@HW-0063 ~ % git clone --depth 1 https://etodd@bitbucket.org/etodd/etodd.io.git
Cloning into 'etodd.io'...
remote: Enumerating objects: 928, done.
remote: Counting objects: 100% (928/928), done.
remote: Compressing objects: 100% (895/895), done.
error: RPC failed; curl 56 LibreSSL SSL_read: SSL_ERROR_SYSCALL, errno 54
fetch-pack: unexpected disconnect while reading sideband packet
fatal: early EOF
fatal: index-pack failed
```


No worries, we can download a zip from the web interface!

![](../../assets/42775bbba48a36f4.png)

Alright, Bitbucket, I see how it is. Time for me to hit the "Give feedback" button. But what's this?

![](../../assets/0744a5d199565a07.png)

50 free build minutes?? I bet I could get up to some mischief in that time. I wonder what templates they have available...

![](../../assets/d8ae01660421e698.png)

Jackpot. Crucially, the little web installer for setting up my first pipeline lets me edit the pipeline YAML file right in the browser and commit it directly. Good thing, since I can't clone this repository to be able to commit to it. After deleting a bunch of npm nonsense, I'm left with this pipeline YAML:

```
image: node:10.15.3
pipelines:
default:
- step:
name: Exfiltrate!!
script:
- pipe: atlassian/aws-s3-deploy:0.4.4
variables:
S3_BUCKET: 'etodd.io'
LOCAL_PATH: '.'
```


5 minutes later I've got an S3 bucket and a fresh AWS IAM user. Plug that baby into the repository settings.

![](../../assets/a894f41bd8383ca5.png)

Let's try it out!

![](../../assets/dae46d1ee9146276.png)

Holy cow it worked.

![](../../assets/ee8e5129e4a64f62.png)

No way! It even copied the `.git`

directory!

Time to pull it down.

```
evantodd@HW-0063 ~ % mkdir etodd.io
evantodd@HW-0063 ~ % AWS_ACCESS_KEY_ID=xxx AWS_REGION=us-west-1 AWS_SECRET_ACCESS_KEY=xxx aws s3 cp s3://etodd.io/ ./etodd.io --recursive
evantodd@HW-0063 ~ % cd etodd.io
evantodd@HW-0063 etodd.io % git status
Refresh index: 100% (899/899), done.
On branch master
Your branch is up to date with 'origin/master'.
nothing to commit, working tree clean
```


I can't believe this is working. Let's push it to Github:

```
evantodd@HW-0063 etodd.io % git remote rm origin
evantodd@HW-0063 etodd.io % git remote add origin git@github.com:etodd/etodd.io.git
evantodd@HW-0063 etodd.io % git push --set-upstream origin main
Enumerating objects: 1353, done.
Counting objects: 100% (1353/1353), done.
Delta compression using up to 12 threads
Compressing objects: 100% (976/976), done.
Writing objects: 100% (1353/1353), 324.57 MiB | 1.17 MiB/s, done.
Total 1353 (delta 340), reused 1353 (delta 340), pack-reused 0
remote: Resolving deltas: 100% (340/340), done.
To github.com:etodd/etodd.io.git
! [remote rejected] main -> main (shallow update not allowed)
error: failed to push some refs to 'github.com:etodd/etodd.io.git'
```


Of course! The Bitbucket build agent cloned the repo using `--depth 50`

, so it doesn't have the full Git history.
But maybe now that I have most of the repo downloaded, I can fetch the rest from Bitbucket?

```
evantodd@HW-0063 etodd.io % git fetch --unshallow https://etodd@bitbucket.org/etodd/etodd.io.git
Password for 'https://etodd@bitbucket.org':
remote: Enumerating objects: 1035, done.
remote: Counting objects: 100% (1035/1035), done.
remote: Compressing objects: 100% (642/642), done.
error: RPC failed; curl 56 LibreSSL SSL_read: SSL_ERROR_SYSCALL, errno 54
fetch-pack: unexpected disconnect while reading sideband packet
fatal: early EOF
fatal: index-pack failed
```


So close! Turns out you can also deepen a shallow clone without going all the way with `git fetch --depth N`

.
Through trial and error I keep increasing the depth, downloading the repo bit by bit. Finally, one last `git fetch --unshallow`

and it's done.

I write this post, commit, push to Github, point Netlify at the new repo, and now you are caught up on things.

I hope this is helpful if you ever need to get code out of Bitbucket.