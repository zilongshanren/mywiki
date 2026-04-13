---
title: Full text searching in Info mode with Apropos
url: https://www.masteringemacs.org/article/full-text-searching-info-mode-apropos
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Most Emacs hackers quickly memorize the myriad of help commands available to them in Emacs. Among them, the humble `M-x apropos`

command, a full text regexp search command that searches all known Lisp symbols (functions, variables - you name it) and returns a list of matches.

In fact, there’s an apropos command for all occasions. They’re must-have commands if you can’t quite find what you are looking for. To find them all, why not use apropos: `C-h a apropos`

.

Nestled among all the other apropos commands is `M-x info-apropos`

, a full text search for Emacs’s documentation browser, `info`

(`C-h i`

.) It’s not limited to just your Emacs documentation either. The `info-apropos`

command handily searches all Info manuals Emacs is aware of and presents the matches as hyperlinked entries to their respective manual pages.

It’s not a commonly needed command, but when you do need it, you’ll be glad it’s there.