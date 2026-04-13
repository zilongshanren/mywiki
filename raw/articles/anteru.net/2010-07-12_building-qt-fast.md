---
title: Building Qt -- fast
url: https://anteru.net/blog/2010/building-qt-fast
published: '2010-07-12'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

For building [Qt](http://qt.nokia.com), you typically have to reserve an hour or so. There’s a much faster way to build it though (besides the optimisations I already described) – build it using [jom](http://qt.gitorious.org/qt-labs/jom). Jom is a multi-threaded [nmake](http://msdn.microsoft.com/en-us/library/dd9y37ha.aspx) replacement. The only thing you have to keep in mind is to configure *without *`-fast`

for versions before 4.6.3; if you configure with `-fast`

, there’s [a bug which will lead to Qt being build with a single thread](http://bugreports.qt.nokia.com/browse/QTBUG-8562). So just configure as usual, and run `jom`

instead of `nmake`

, your build-times should be drastically reduced.