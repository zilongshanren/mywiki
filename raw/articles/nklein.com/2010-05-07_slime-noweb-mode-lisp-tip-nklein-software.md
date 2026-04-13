---
title: 'SLIME/noweb-mode/Lisp tip :: nklein software'
url: http://nklein.com/2010/05/slimenoweb-modelisp-tip/
author: Pat
published: '2010-05-07'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

Just a quick tip here if you use SLIME for Lisp and use Lisp as a noweb-code-mode…. Either change `slime-auto-connect`

to `'ask`

or `'always`

or just remember to start slime before you wander into a Lisp code chunk. If you don’t, noweb-mode gets all confused and won’t code-highlight your Lisp or switch back to doc-mode when you leave that chunk.

I spent a long time just thinking noweb-mode was entirely broken if there were single quotes or less-than signs in any document chunk. Alas, it just needed SLIME to stop chucking a Not connected

error.