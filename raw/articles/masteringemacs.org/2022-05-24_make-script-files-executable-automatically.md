---
title: Make script files executable automatically
url: https://www.masteringemacs.org/article/script-files-executable-automatically
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

You can force Emacs to make a file executable (respecting your `umask`

settings) if Emacs considers it a script. To determine if it is a script, Emacs will look for the *hash-bang* notation in the file and treat it as a script if it finds it.

Add this to your init file and Emacs will then make the file executable if it is a script.

```
(add-hook 'after-save-hook
'executable-make-buffer-file-executable-if-script-p)
```