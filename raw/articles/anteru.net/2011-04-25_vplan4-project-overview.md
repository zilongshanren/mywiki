---
title: 'VPlan4: Project overview'
url: https://anteru.net/blog/2011/vplan4-project-overview
published: '2011-04-25'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

## VPlan4

Fast-forward to 2010: I [started to use Linux](https://anteru.net/blog/2009/09/14/604/) for some of my development work, and I really wanted VPlan to run on Linux as well. In the meantime, all of the web-based tools have appeared with nice UIs, drag & drop, comfort functions etc. which VPlan lacked, so there was really some reason to give it another shot. This time around, I wrote down the requirements first before starting one line of code:

- Portability: Should run on Linux and Windows; the storage format should be platform-neutral
- Performance: Fast startup, little memory use.
- Features:
- Drag & drop in the tree-view
- ACID for all operations
- Per-task descriptions and priorities


For development, I used [Qt](http://qt.nokia.com/) this time around, as it is available under the LGPL and thus does not force me to publish the source (I didn’t set my mind on that yet.) It also supports sqlite, which gives me the ACID compliance, and should improve memory usage and performance quite a bit compared to WPF. With that much preparation, I went to coding.

## Implementation

I’m a strong believer that any crap can be refactored/polished until it’s good, as long as you have some crap to start with. Given my initial requirements, I didn’t spend too much time fleshing out an architecture, but went to implement a data model for all tasks so it could be bound to a [QTreeView](http://doc.qt.nokia.com/qtreeview.html) and write the corresponding SQL schema as I went along.

Get a basic UI with Qt turned out to be really simple using QtDesigner. A nice feature is that you can subclass any widget but still use QtDesigner to place it – something which turned out to be useful for my “deselecting tree-view”, a tree-view which deselects if you click the empty space.

I built the project with CMake, which works nicely with Qt once [you setup it properly](https://anteru.net/blog/2009/09/07/582/). Most coding was done in a single sprint: The feature set was limited and known up front and all I needed to do was to adapt the SQL backend into an abstract tree model. The rest is handled by Qt, including drag & drop and various other details.

Pretty late in the development cycle I decided to add translations. With Qt, all you need is to make sure that every string is wrapped with a macro and then run [QtLinguist](http://doc.qt.nokia.com/linguist-manual.html). The actual translation is pretty simple later on. One advantage of translating is that you can also generate proper plural form handling for English. That’s a nice polishing touch, and even though I assume that no VPlan user noticed it I always wanted to have this in an application since playing [Transport Tycoon](http://www.openttd.org/en/).

## Deployment

For deployment, I’m using [Wix](http://wix.sourceforge.net/) again. Wix is great for Windows deployment as it generates Microsoft Installer packages. One problem with Wix is that it’s verbose for small projects and thus takes some time to write. For larger projects, some I’m playing around with some automatic Wix generation but this has other issues (especially when it comes to the directory structure.) After each build, I’m storing the binaries and tagging the repository for each installer so I can exactly recreate the same file.

## Various unsolved issues

So much for the stuff that works. Some other details are not working yet which I’d definitely like to attack at some point. First of all, there is no automated testing for the UI and very limited testing for the backend. I guess that a script intermediate layer would be the easiest solution for that, but as it stands now, there is no good test coverage.

Crash handling is also an unsolved issue. For the latest version of my research engine, I’m using a crash handler and storing the PDBs along with the source and binaries so I can capture crashes and perform post-mortem debugging. As the user base seems to be minimal, this is enough for VPlan, but every larger project needs some mechanism to capture a minidump.

## Conclusion

So much for VPlan 4. This blog post has been a long time in the making, and I hope it shed some light on the development of VPlan4. So long, and thanks for all the fish!