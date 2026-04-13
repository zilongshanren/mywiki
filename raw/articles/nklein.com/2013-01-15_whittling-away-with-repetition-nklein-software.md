---
title: 'Whittling Away with Repetition :: nklein software'
url: http://nklein.com/2013/01/whittling-away-with-repetition/
author: Pat
published: '2013-01-15'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I’ve now done the Bowling Game Kata from the [previous video](http://nklein.com/2013/01/bowling-game-kata-in-common-lisp) seven more times imperatively as I did in the video and two more times with a functional style.

Each time I did it imperatively, I decreased the overall size of the code. The functional code is smaller still and got smaller on my second try. The previous video was `bowling-20130102.lisp`

and the functional versions end in `-f.lisp`

.

70 bowling-20121230.lisp

70 bowling-20130102.lisp

64 bowling-20130106.lisp

62 bowling-20130107.lisp

64 bowling-20130109.lisp

66 bowling-20130110.lisp

62 bowling-20130113.lisp

54 bowling-20130113b-f.lisp

57 bowling-20130114.lisp

57 bowling-20130114b.lisp

51 bowling-20130114c-f.lisp

Total:

677

These SLOC numbers were generated using [David A. Wheeler’s ‘SLOCCount’](http://www.dwheeler.com/sloccount/). Straight up byte, word, and line counts follow the same trend.

Soon, I will record another run through the imperative style and a run through the functional style.

Here are the most recent versions of each style:

Appreciate the video. I also found your test framework NST interesting. I am a lisp novice but it would be nice if you ever covered NST package and its use a little more.

I’m glad you enjoyed the video, and I welcome you to Lisp.

NST is not a package I wrote (though, I do know the author). I will see if I can come up with a useful video for it. In the meantime, here is info from a presentation the author gave about NST: http://tclispers.org/nst-unit-testing-framework-common-lisp