---
title: 'Semaphore Follow-Up: NTPL'
url: http://hacksoflife.blogspot.com/2010/12/semaphore-follow-up-ntpl.html
author: Benjamin Supnik
published: '2010-12-04'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[previous post](http://hacksoflife.blogspot.com/2010/12/performance-of-semaphore-vs-condition.html)on condition variables, etc. With

[NTPL](http://en.wikipedia.org/wiki/Native_POSIX_Thread_Library)(the pthreads implementation on Linux) a lot of the original issues I was trying to cope with don't exist. Some things NTPL does:

- pthread mutexes are spin-sleep locks, so they can be used as short-term critical sections without too much trouble. Given a moderately contested but shortly held lock, this is a win.
- sem_t semaphores have an atomic counter to avoid system calls in the uncontested case. When inited privately (sem_init) they appear to be lean and mean.
- All synchronization is done around
[futexes](http://en.wikipedia.org/wiki/Futex), ensuring that uncontested cases can be manged with atomic operations. (The OS X pthreads library at least uses spin locks around user space book-keeping for the uncontested case, but I think the futex code path is faster.)

## No comments:

## Post a Comment