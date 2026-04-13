---
title: Emacs's switch to Git
url: https://www.masteringemacs.org/article/emacss-switch-to-git
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

After nearly ten months of hard work, Eric S Raymond (esr) has finished the transition from Bazaar to Git, and in the process cleaned up 29 years of ossified CVS references and other source control flotsam. ESR calls it “geologic strata” and he’s not even kidding. 29 years of continued development makes it unavoidable. If you haven’t been keeping up I suggest you read his article on [the conversion](http://esr.ibiblio.org/?p=5634).

The move to Git, I think, is a big one. Like it or not, but it won the source control fight. Bazaar lost (not that it ever had a chance of winning); Mercurial lost too (and it did have a chance of winning.) Git’s the right choice; it will significantly reduce the barrier to entry for new developers — well, you still need to sign over your code to the FSF, but it’s easi*er*.

Lars Ingebrigtsen has [written a great tutorial](http://lars.ingebrigtsen.no/2014/11/13/welcome-new-emacs-developers/) for newcomers interested in contributing to Emacs. I had no idea it was *that* easy to find and push bug fixes out. There’s a fancy Emacs package, `debbugs`

, that makes it easy to do so (obviously.)

I hope the switch to git will renew interest in committing to Emacs.