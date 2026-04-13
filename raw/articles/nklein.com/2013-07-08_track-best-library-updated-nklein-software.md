---
title: 'Track-Best Library Updated :: nklein software'
url: http://nklein.com/2013/07/track-best-library-updated/
author: Pat
published: '2013-07-08'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I updated my [track-best](http://nklein.com/software/track-best-library/) library to allow you to keep all of the the things tied for best. The `WITH-TRACK-BEST`

macro now accepts the `:KEEP-TIES`

keyword parameter.

Here are some examples of using the `:KEEP-TIES`

option. For all of the examples, we will use the same sequence of `TRACK`

calls:

(track :one 1)

(track :uno 1)

(track :two 2)

(track :dos 2)

Here are some calls with `:KEEP-TIES`

as `NIL`

(the default):

=> (values :TWO 2)

(with-track-best (:keep 3 :keep-ties nil) (track-numbers))

=> (values (:TWO :DOS :ONE) (2 2 1))

Here are some calls with `:KEEP-TIES`

as `T`

:

=> (values (:TWO :DOS) (2 2))

(with-track-best (:keep 3 :keep-ties t) (track-numbers))

=> (values (:TWO :DOS :ONE :UNO) (2 2 1 1))