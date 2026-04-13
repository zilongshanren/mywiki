---
title: null program
url: https://nullprogram.com/tools/
published: '2017-03-12'
source_blog: null program
source_site: https://nullprogram.com
category: graphics
fetched: '2026-04-13'
---

## Command Line Tools

Over the years I’ve developed and polished a number of command line tools,
most of which I use on a regular basis. Rather than leave them scattered
about, this page lists my most important tools. Each supports all the
major operating systems (Linux, Windows, BSD, macOS, etc.) and compiler
toolchains (GCC, Clang, MSVC), include complete documentation (man page,
etc.), and is readily installed and/or packaged with `make install`

or
similar.

On Windows, [w64devkit](https://github.com/skeeto/w64devkit) is an ideal development and build environment
for these tools.


Derives OpenPGP and SSH keys [from a master passphrase](/blog/2019/07/10/), effectively
allowing such keys to be memorized. No need to backup your keys, nor store
them at rest. Instead, generate keys on the fly as needed.

```
$ passphrase2pgp -u "Real Name <name@example.com>" | gpg --import
$ passphrase2pgp -u name@example.com -f ssh | ssh-add -
```


Source: [passphrase2pgp-1.3.0.tar.xz](https://github.com/skeeto/passphrase2pgp/releases/download/v1.3.0/passphrase2pgp-1.3.0.tar.xz)
([sig](https://github.com/skeeto/passphrase2pgp/releases/download/v1.3.0/passphrase2pgp-1.3.0.tar.xz.sig))


“*micro*-config” is a small, highly portable [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/) / [pkgconf](http://pkgconf.org/)
clone with [first-class Windows support](/blog/2023/01/18/). Integrated into
the [w64devkit](https://github.com/skeeto/w64devkit) toolchain, and a drop-in replacement on other platforms.
It is the most robust, most performant, most tested pkg-config available.

```
$ eval cc game.c $(pkg-config --cflags --libs sdl2)
```


Source: [u-config-0.33.1.tar.gz](https://github.com/skeeto/u-config/releases/download/v0.33.1/u-config-0.33.1.tar.gz) ([sig](https://github.com/skeeto/u-config/releases/download/v0.33.1/u-config-0.33.1.tar.gz.sig))


Encrypts [personal archives](/blog/2017/03/12/) for long-term storage and backup.
Zero build- nor run-time dependencies, trivially compiled, [highly
portable](/blog/2018/04/13/). Keys are asymmetric, which is scripting-friendly — a
password is never needed to encrypt an archive — and allows less-trusted
machines to encrypt files without the ability to decrypt them. Keys are
optionally derived from a master passphrase, so they never require backing
up.

```
$ enchive keygen --derive
$ enchive archive --delete backup.tar.gz
$ enchive extract <backup.tar.gz.enchive | gunzip | tar x
```


Source: [enchive-3.5.tar.xz](https://github.com/skeeto/enchive/releases/download/3.5/enchive-3.5.tar.xz) ([sig](https://github.com/skeeto/enchive/releases/download/3.5/enchive-3.5.tar.xz.sig))


Blazing fast hex dumper with color output. Highly portable.

```
$ hastyhex data.bin | less -R
```


Source: [hastyhex-1.0.0.tar.xz](https://github.com/skeeto/hastyhex/releases/download/v1.0.0/hastyhex-1.0.0.tar.xz) ([sig](https://github.com/skeeto/hastyhex/releases/download/v1.0.0/hastyhex-1.0.0.tar.xz.sig))


Wraps input into columns, automatically adjusting the column width as
needed. Fast, resource-efficient and highly portable. On some platforms
does not even require a C runtime.

```
$ seq 60 | cols -CW60
1 4 7 10 13 16 19 22 25 28 31 34 37 40 43 46 49 52 55 58
2 5 8 11 14 17 20 23 26 29 32 35 38 41 44 47 50 53 56 59
3 6 9 12 15 18 21 24 27 30 33 36 39 42 45 48 51 54 57 60
```



Converts CSV to/from a pipeline-friendly format processable by typical
unix command line tools. It’s not my original idea, but this is the
[fastest](/blog/2021/12/04/), leanest, strictest, and most portable implementation.

```
$ csvquote <data.csv |
awk -F, '{print $1 "," $2+$3}' |
csvquote -u >sum.csv
```



Attaches source scripts to PNG images so that [they do not become
separated](/blog/2021/12/31/). Behaves similar to archival programs like `tar`

. Highly
portable, with optional zlib dependency.

```
$ dot -Tpng graph.dot | pngattach graph.dot >graph.png
```



Prints ranges of IPv4 addresses like `seq`

. Also supports CIDR notation
inputs and outputs. Not my idea, but a much-improved, feature-complete,
drop-in clone of [the original](https://devel.ringlet.net/sysutils/prips/). This implementation is highly
portable, and on some platforms does not even require a C runtime.

```
$ prips -e ...255 192.168.1.0/24 |
xargs -n1 -P16 host |
grep -v NXDOMAIN
```



High performance base64 encoder and decoder. Compatible with and behaves
like a subset of the GNU `base64`

tool, but faster and far more portable.

```
$ gzip <data | race64 >data.gz.b64
$ base64 -d data.gz.b64 | gunzip >data
```


Source: [race64-1.0.0.tar.xz](https://github.com/skeeto/race64/releases/download/v1.0.0/race64-1.0.0.tar.xz) ([sig](https://github.com/skeeto/race64/releases/download/v1.0.0/race64-1.0.0.tar.xz.sig))