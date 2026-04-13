---
title: The Emacs 27 Edition of Mastering Emacs is out now
url: https://www.masteringemacs.org/article/the-emacs-27-edition-of-mastering-emacs-out-now
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

I have updated the [ Mastering Emacs book](https://www.masteringemacs.org/book) so it covers Emacs 26 & 27.

Both versions of Emacs highlight just how much momentum there is in Emacs core and in the community: Emacs is bursting at the seams with cool, new features (as you can read about in [What’s new in Emacs 27](https://www.masteringemacs.org/article/whats-new-in-emacs-27-1) and [What’s new in Emacs 26](https://www.masteringemacs.org/article/whats-new-in-emacs-26-1).) And the community itself has changed and grown a lot, too. I believe Atom and VSCode helped stimulate a more earnest debate about IDE features and their role in Emacs.

If you’ve ever been curious at all about Emacs, then now is absolutely the right time to jump in. If you already own the book (*thank you!*) then head on over to the download area for your free update. I recommend you read it in Emacs this time using the excellent [nov.el](https://github.com/wasamasa/nov.el) EPUB reader mode in Emacs.

I’ve included the opening chapter *2020 Edition Update* from the book below.

## 2020 Edition Update

It’s been ten years since I started my blog where I shared detailed articles on areas of Emacs I felt warranted people’s interest. And it’s been five years since I published the first edition of this book.

In those five years, entire text editors have come out of nowhere and exploded in popularity, only to wane in the face of even newer upstart challengers. Meanwhile, Emacs users are still using Emacs, learning from the advances (and retreats…) of other editors. But there were plenty of advances in the last five years for Emacs users to benefit from.

*Microsoft VSCode* deserves a special mention for standardizing something that should have been agreed on and implemented *decades* ago in the software community: a protocol for exposing – or re-implementing, where that is not possible – the internals of compilers, interpreters and other programmable engines in a format that enables a tool, like Emacs, to support high-level features familiar to anyone who has used a closed-source IDE: automatic refactoring; syntax and error highlighting; code completion; documentation lookup, and more. Microsoft, perhaps surprising to some, has won the argument with the *Language Server Protocol*, an open JSON-RPC standard. Before the advent of said protocol most IDEs and editors had insular, homegrown implementations that varied in breadth, depth and quality. It’s a major win for Emacs and its users especially: they will benefit from the collective works of people who build these *Language Servers*.


Language Servers in EmacsThere are two implementations of note: LSP mode and EGlot. LSP mode offers a complete IDE experience out of the box, with EGlot preferring a more ascetic, Emacs-centric approach. You should try both and pick the one you like best.

Both products are under active development, and as such they are rapidly changing. They support a large variety of both tools and languages.


Better IDE-like features does raise Emacs’s profile, but one inescapable fact about learning Emacs is, once it’s second nature, you tend to forget what a rough time you had learning it. That is one thing non-users seize on as it is skin-deep and easy to critique: that the terminology is baroque; the UI brutalist; and the key bindings byzantine. True. But this is Emacs: you can change all of that. But I believe there is a kernel of truth to these complaints: a prettier UI is a quick win; changing some of Emacs’s more obscure defaults is another, despite the risk of upsetting a few vocal, ornery graybeards.

But first impressions count: people make snap judgments based on fitness and form; if the editor doesn’t code complete but another free editor does, then that might just mean they’ll never try Emacs. The curb appeal of all-in-one packages like *Spacemacs* and *Doom Emacs* – two kitchen sink kits for Emacs – are a testament to the importance of first impressions and the value of sensible defaults. Many jump straight into Emacs using either of those kits, and just as many then graduate to their own Emacs configuration when the shine wears off: but at that point they’re Emacs users for life.

This book details how to learn Emacs, and learn it you will: Emacs’s terminology predates modern computing, but it is easy to learn, as there are but a handful of terms that distinguishes it from the UI terminology used elsewhere. The key bindings and commands are harder to learn, but then that gets us to the crux of what Emacs is.

Emacs is a complex piece software, and it will take you time and hard work to learn. But, if you do, you will have an editor for life. It has an active, friendly community that will seize on any advances made in other editors and bring them into the fold. And that excludes – as you’ll see in the rest of the book – the untold benefits that other editors cannot even begin to match.

The Emacs maintainers know this, and are tirelessly working on Emacs’s core behind-the-scenes, with the aim of incrementally improving Emacs for everybody, while keeping backwards compatibility. They are excellent stewards, carefully balancing the need to respect the GNU project’s philosophy and Emacs’s heritage and commitment to stability, with advances in technology and feedback from their users.

Your patient mastery of Emacs is well-rewarded. I assure you.

There are no comments. Why not write one?