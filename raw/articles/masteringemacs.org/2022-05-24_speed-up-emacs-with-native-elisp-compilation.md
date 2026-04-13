---
title: Speed up Emacs with native elisp compilation
url: https://www.masteringemacs.org/article/speed-up-emacs-libjansson-native-elisp-compilation
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Cyril Northcote Parkinson wrote in his book *Parkinson’s Law* that “work expands so as to fill the time available for its completion.” If you squint your eyes, you’ll see that this is also the case for modern software, and in particular Emacs.

For every incrementation in performance, there will be a new gizmo to dial it back down again. Common sources of performance bottlenecks include completion frameworks; the Emacs client libraries that talk to *Language Servers*; and other highly trafficked code paths used widely in Emacs’s many packages.

**Emacs 30 Update**: `libjansson`

is out; it’s been replaced with a builtin JSON encoder and decoder that is much faster still. If you’re compiling Emacs 30+, you can safely disregard the `libjansson`

instructions below.

There are some ministrations that balm the performance pains, though: Emacs 27 now supports `libjansson`

, a C library for working with JSON. If you’re a heavy user of *lsp-mode* or *eglot* then I highly recommend you upgrade for that reason alone.

As of Emacs 28 you can now benefit from the hard work by [Andrea Corallo](http://akrl.sdf.org/gccemacs.html) who discovered that you can use GCC to compile Emacs Lisp. That idea graced the minds of many smart Emacs hackers in the past, but the work of actually making it happen took years of Andrea’s time! It’s an incredible feat of engineering.

**Emacs 30 Update**: Native compilation is enabled by default, provided you meet the requirements. This does not factually change anything in the instructions below, though.

The only teensy-tiny downside is the effort of having to compile Emacs yourself, as it’s unlikely you have the tools installed for Emacs’s configure system to automatically enable native compilation. But, rest assured, it’s really quite easy to get working on Linux. (On other platforms, the level of pain required ranges from a light pinch to the vice-like jaw of a bear.)

## Common Errors

So if you encounter `Does Emacs have native lisp compiler? no`

during a compile step then your Emacs is not compiled with native compilation. Ditto if `M-: (native-comp-available-p)`

returns `nil`

.

Another common error is `elisp native compiler was requested, but libgccjit was not found.`

and `emacs was not built with native compilation support`

which is much the same reason. That’s almost always because `libgccjit`

is either not installed or you haven’t paired up the right `gcc`

version with the right `libgccjit`

library – but that’s also easy to solve, as you’ll see below.

## Enabling Native Compilation on Ubuntu

First update your package repository lists and clone Emacs. It’ll default to `master`

which is the bleeding edge of Emacs. Most of us that without trouble, but if you do, roll back a few revisions or check out a tagged release.

Next, you’ll need a couple of packages. You probably have all of them already, but just in case:

Now we need to add a `ppa`

that contains `libgccjit`

. That is the library that Emacs needs for this to work. I’m also installing `gcc-10`

(but use whatever the latest version on your system is) as **must** have the same version of `gcc`

and `libgccjit`

installed.

Now you need to edit `/etc/apt/sources.list`

and uncomment all the `deb-src`

entries. We’ll need them as a shortcut to installing all the specific dependencies Emacs needs, in addition to the specialist ones to get native compilation working.

Once you have done that, you can install `emacs`

’s build dependencies:

If you want `libjansson`

for fast JSON (you do!) you’ll need this also:

Now you need to tell `make`

what C compiler to use. As I installed `gcc-10`

earlier, that is what I specify in `CC`

:

Now you can do the usual configure-make rigmarole:

I strongly recommend you do `./configure --help`

and ensure you pick the options you want. But this is usually good enough to get you started.

Now build Emacs:

The `make install`

command may need root to install to your `/usr/local`

directories.

And you’re done!

## Dockerfile Example

FROM ubuntu:20.04
# We assume the git repo's cloned outside and copied in, instead of
# cloning it in here. But that works, too.
WORKDIR /opt
COPY . /opt
LABEL MAINTAINER "Mickey Petersen at mastering emacs"
# Needed for add-apt-repository, et al.
#
# If you're installing this outside Docker you may not need this.
RUN apt-get update \
&& apt-get install -y \
apt-transport-https \
ca-certificates \
curl \
gnupg-agent \
software-properties-common
# Needed for gcc-10 and the build process.
RUN add-apt-repository ppa:ubuntu-toolchain-r/ppa \
&& apt-get update -y \
&& apt-get install -y gcc-10 libgccjit0 libgccjit-10-dev
# Needed for fast JSON and the configure step
RUN apt-get install -y libjansson4 libjansson-dev git
# Shut up debconf as it'll fuss over postfix for no good reason
# otherwise. If you're doing this outside Docker, you do not need to
# do this.
ENV DEBIAN_FRONTEND=noninteractive
# Cheats' way of ensuring we get all the build deps for Emacs without
# specifying them ourselves. Enable source packages then tell apt to
# get all the deps for whatever Emacs version Ubuntu supports by
# default.
RUN sed -i 's/# deb-src/deb-src/' /etc/apt/sources.list \
&& apt-get update \
&& apt-get build-dep -y emacs
# Needed for compiling libgccjit or we'll get cryptic error messages
# about failing smoke tests.
ENV CC="gcc-10"
# Configure and run
RUN ./autogen.sh \
&& ./configure --with-native-compilation --with-mailutils
ENV JOBS=2
RUN make -j ${JOBS} && make install
ENTRYPOINT ["emacs"]


The whole process may take a while. Native compilation is, as of Emacs 28.1, automatic, and runs in the background. **There is nothing for you to do to make it work** as it will compile stuff in the background while you’re using Emacs.

To test that *both* the fast JSON *and* native compilation is working you can evaluate the following elisp in Emacs:

```
(if (and (fboundp 'native-comp-available-p)
(native-comp-available-p))
(message "Native compilation is available")
(message "Native complation is *not* available"))
```


And for the JSON:

```
(if (functionp 'json-serialize)
(message "Native JSON is available")
(message "Native JSON is *not* available"))
```


And.. that’s that. Enjoy your souped-up Emacs.