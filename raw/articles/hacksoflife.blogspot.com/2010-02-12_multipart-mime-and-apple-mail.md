---
title: Multipart MIME and Apple Mail
url: http://hacksoflife.blogspot.com/2010/02/multipart-mime-and-apple-mail.html
author: Benjamin Supnik
published: '2010-02-12'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

I finally figured out why attachments from our bug report script don't have icons in Apple mail: Apple mail requires multipart/mixed as the MIME type, while Thunderbird will accept multipart/related.


Apple mail also cares about Content-disposition; it will show an icon for "attachment"-style disposition, even for text files, but it will show the text (with no markings showing it is an attachment) for "inline" style. Thunderbird shows the full text, with horizontal rules, no matter what.

## No comments:

## Post a Comment