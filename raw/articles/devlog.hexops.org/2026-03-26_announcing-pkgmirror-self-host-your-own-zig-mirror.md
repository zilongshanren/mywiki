---
title: 'Announcing pkgmirror: self-host your own Zig mirror'
url: https://devlog.hexops.org/2026/announcing-pkgmirror/
published: '2026-03-26'
source_blog: Hexops' devlog
source_site: https://devlog.hexops.org/
category: graphics
fetched: '2026-04-19'
---

' devlog

[pkgmirror](https://code.hexops.org/hexops/pkgmirror) is an open-source, self-hosted Zig toolchain and package mirror service so your builds no longer rely on third-party services or Microsoft GitHub.

[Mach](https://machengine.org) now hosts its own pkgmirror at [pkg.hexops.org](https://pkg.hexops.org).

## Features

**Zig toolchain mirroring**: acts as a caching reverse proxy for Zig toolchain downloads from ziglang.org**Package mirroring (optional)**- instead of writing GitHub URLs in your project’s`build.zig.zon`

, use your own server and have it mirror GitHub, Codeberg, or your project host of choice. No more Microsoft-induced downtime harming your builds.**Artifact mirroring (optional)**- mirror prebuilt binaries and CI artifacts the same exact way.**Nominated Zig support**- support for Mach’s[nominated Zig versions](https://machengine.org/docs/nominated-zig/): something less of a moving target than nightly Zig, but more frequently updated than Zig stable releases.**Proactive cache warming**- automatically fetches all stable and nominated Zig versions, for each OS/arch variant, so that your mirror is ready to go.**Automatic LetsEncrypt support**- Server can invoke acme.sh for you, no reverse proxy needed!**Single binary**- written in Zig, ~9 MB, super fast - no runtime dependencies beyond libc and acme.sh (optional)

## Why run a Zig toolchain mirror?

The Zig community maintains a [list of community mirrors](https://ziglang.org/download/community-mirrors/) for toolchain downloads which are used throughout the community.

For example, [setup-zig](https://codeberg.org/mlugg/setup-zig) is a GitHub Action that installs Zig and caches your build directory between runs, it cycles through the Zig mirror list automatically to reduce load on ziglang.org.

[anyzig](https://github.com/marler8997/anyzig) - which is probably the nicest way to seamlessly switch between Zig versions in your Zig projects, uses Zig mirrors as well.

Note: minisig verification is used to ensure you got a genuine ziglang.org binary, and not something malicious - these tools handle that verification for you automatically.

[pkgmirror](https://code.hexops.org/hexops/pkgmirror) is a Zig toolchain mirror server, written in Zig, so you can host a mirror of your own and contribute!

## Zig package mirrors

[pkgmirror](https://code.hexops.org/hexops/pkgmirror) goes beyond just simple Zig toolchain mirroring and allows mirroring *Zig packages* and binary artifacts, too. This is optional.

In [Mach](https://machengine.org/) for example, it’s really important to us that someone can check out an old repository with an old game/app that uses Mach, and be able to get it building quickly still: a key part of this is ensuring that all of Mach’s dependencies in `build.zig.zon`

are hosted through reliable URLs that won’t break or dissappear over time. Sure, we could link to a Github-hosted tarball of one of our libraries - but GitHub repositories get deleted, or Microsoft enshittification of GitHub may occur and [we have to move to a self-hosted forgejo instance, code.hexops.org](https://code.hexops.org/) (which we did recently) - so we need stable, long-term URLs our dependencies can be hosted at.

[pkgmirror](https://code.hexops.org/hexops/pkgmirror) allows configuring mirroring of Zig packages (and binary CI artifacts, too) that are hosted on GitHub, Codeberg, etc. - the approach is simple: pkgmirror caches the file on disk for you forever, and gives you a super stable URL to write in your `build.zig.zon`

file.

## Not everyone should run a mirror

Not everyone should run a Zig toolchain or package mirror: it’s a serious responsibility, you should handle backups, etc. especially if others are depending on your mirror to be stable.

But when you do want to host a Zig mirror, [pkgmirror](https://code.hexops.org/hexops/pkgmirror) is now a solid option for that - written in Zig unlike the myriad of other Go-based solutions out there.

## Special thanks

[pkgmirror](https://code.hexops.org/hexops/pkgmirror) would not be possible to write in Zig today if not for karlseguin’s [http.zig](https://github.com/karlseguin/http.zig) library, and our automatic LetsEncrypt support via acme.sh wouldn’t be possible without ianic’s excellent [tls.zig](https://github.com/ianic/tls.zig) library providing a TLS 1.3 server.

## Thanks

- You can now find pkgmirror and Mach itself on our self-hosted forgejo instance,
[code.hexops.org](https://code.hexops.org) - Join the
[Mach Discord server](https://discord.gg/XNG3NZgCqp)to follow development - Consider
[sponsoring our work](https://github.com/sponsors/emidoots)so we can do more of it!