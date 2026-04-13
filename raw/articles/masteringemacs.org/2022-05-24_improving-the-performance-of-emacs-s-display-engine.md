---
title: Improving the performance of Emacs's Display Engine?
url: https://www.masteringemacs.org/article/improving-performance-emacs-display-engine
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I came across an [interesting thread](http://lists.gnu.org/archive/html/emacs-devel/2011-09/msg00350.html) on the GNU Emacs developer mailing list about an obscure variable called `redisplay-dont-pause`

and I figured I’d talk about it.

So, currently, if Emacs is busy redrawing the screen *any* input event (keyboard, mouse) will halt the redrawing and abort to handle the input event. The obvious benefit here is that the user will get a smoother typing experience, especially on older machines where display updates were slow. Nowadays, though, you could argue that this is an unnecessary and very conservative setting as it will cause screen tearing.

The variable `redisplay-dont-pause`

, when set to `t`

, will cause Emacs to fully redraw the display *before* it processes queued input events. This may have slight performance implications if you’re aggressively mouse scrolling a document or rely on your keyboard’s auto repeat feature. For most of us, myself included, it’s probably a no-brainer to switch it on.

Add this to your .emacs file to enable this functionality:

`(setq redisplay-dont-pause t)`