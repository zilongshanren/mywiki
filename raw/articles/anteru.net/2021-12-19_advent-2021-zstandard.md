---
title: 'Advent 2021: Zstandard'
url: https://anteru.net/blog/2021/advent-2021-zstd
published: '2021-12-19'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

Yet another library that has appeared recently and really changed how I do things is [Zstandard](https://facebook.github.io/zstd/) – a compression library. Compression is an interesting area of computer science which hasn’t seen much innovation for a long time. When I started programming, there were dozens of competing algorithms and tools: RAR, UHARC, ACE, ARJ, ZIP, and a few more exotic ones. After a while, things seemed to settle down on ZIP and 7z, with ZIP being the clear leader (ZIP using [deflate compression](https://en.wikipedia.org/wiki/Deflate) – ZIP itself is just the container, but I’s pretty much universally used with `deflate`

. The canonical library for that is [ zlib](https://www.zlib.net/)). More recently, a few new algorithms started to crop up:

[Brotli](https://github.com/google/brotli),

[LZ4](https://lz4.github.io/lz4/), and

[Snappy](https://google.github.io/snappy/). Those were attacking the compression problem from new angles, and I ended up using LZ4 a lot of compression of data sets as it is incredibly easy to add, but they all remained fairly niche.

Fast forward a few years and a new contender entered the ring: Zstd. Zstd provided a great blend of compression quality and performance, being as good as standard ZIP at much higher speed, or being dramatically faster at slightly lower compression ratios. Especially in the age of NVMe drives which can read at GiB/s rates, you really don’t want a compression algorithm which can’t decompress at that speed. Additionally, it’s scalable: It can go extremely fast at reduced compression, or achieve very high compression rates at significantly higher cost.

For me, Zstd replaced most uses of LZ4 and `zlib`

by now. I compress data sets using Zstd as it’s much faster and has no downsides, by being a better algorithm. I also use it for backups and other long-term archival storage as it doesn’t seem to go away anytime soon. The next frontier here will be hopefully a replacement for ZIP (the package format!) as that one hasn’t aged very well, but it still ubiquitous and often times the only supported built-in format. I’m optimistic though – there’s a good reason to develop a new on-disk format now (if only to support the latest advances in compression) and I wouldn’t be surprised if we’ll see a ZIP replacement in the coming years. Till then, I’ll continue to use Zstd where I already can!