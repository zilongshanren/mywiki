---
title: Rapidhash Unity port · Aras' website
url: https://aras-p.info/blog/2026/03/07/Rapidhash-Unity-port/
published: '2026-03-07'
source_blog: Aras' website
source_site: https://aras-p.info/
category: graphics
fetched: '2026-04-13'
---

Ten years ago I was writing about various
[non-cryptographic hash functions](https://aras-p.info/blog/2016/08/09/More-Hash-Function-Tests/). Back then
[xxHash](https://xxhash.com/) was new (introduced in 2014)! However, quite some things have changed
since then. xxHash itself got a new [“XXH3” version](https://fastcompression.blogspot.com/2019/03/presenting-xxh3.html)
(2020); [“wyhash”](https://github.com/wangyi-fudan/wyhash) appeared (2020+), and eventually evolved into
[ “rapidhash”](https://github.com/Nicoshev/rapidhash) (2024+). Many others too, but this is about

*rapidhash*.

It is *small* and *beautiful*. Yes, current (V3) version is over 500 lines of C code, but that is *three* hash
function variants and several tweaking options.

I ported it to C# (Unity/Burst) and the full core `rapidhash`

implementation is barely over 100 lines of code.

- Full repository:
(MIT license).**UnitySmolRapidhash on github** - The actual source file:
**SmolRapidhash3.cs** - It uses Unity’s Burst to get access to 128 bit multiply function, and the code itself has
`[BurstCompile]`

on it. - API is similar to
`Unity.Collections.xxHash3`

class, except it returns 64 bit value directly instead of an`int2`

, and has helper entry points for hashing a single struct or various arrays:`static ulong Hash64<T>(ref T key) where T : unmanaged; static ulong Hash64<T>(T[] key) where T : unmanaged; static ulong Hash64<T>(Span<T> key) where T : unmanaged; static ulong Hash64<T>(NativeArray<T> key) where T : unmanaged; static ulong Hash64(void* key, long length);`


### Performance

Burst approaches native (C) performance of rapidhash at larger input sizes, nice!

- The calling benchmark program is just a C# (not Burst) script tested in the editor; might be cause of some overhead for small input sizes.
- Curiously, C#/Burst port of XXH3 (as provided by
`Unity.Collections`

package) is 30-40% slower than native (C) implementation. This slowdown is not there for rapidhash.

Rapidhash is always faster than XXH3; the difference is more pronounced on arm64.

Ryzen 5950X / Windows / Visual Studio 2022 (17.14.23): **rapidhash reaches 38GB/s**. Native XXH3 version is similar
for large input sizes (slower for small sizes). However the C#/Burst version of XXH3 only reaches 24GB/s.
![](../../assets/914a8c0670fb3e99.png)


Apple M4 Max / macOS / Xcode 16.1: **rapidhash reaches 67GB/s**. Native XXH3 version reaches 50GB/s, and C#/Burst
version of XXH3 reaches only 30GB/s.
![](../../assets/f9da4023522f4d53.png)


*That’s it!*