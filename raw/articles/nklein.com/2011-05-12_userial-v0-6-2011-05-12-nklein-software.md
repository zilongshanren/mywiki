---
title: 'USerial — v0.6.2011.05.12 :: nklein software'
url: http://nklein.com/2011/05/userial-v0-6-2011-05-12/
author: Pat
published: '2011-05-12'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

The latest release of my [USerial](http://nklein.com/software/unet/userial/) library provides a way to make a simple serialize/unserialize pair for a list where every item can be serialized using the same key.

(make-list-serializer :list-of-integers :uint32)


(with-buffer (make-buffer)

(serialize :list-of-integers '(1 2 3 4 5 6 7))

(buffer-rewind)

(reduce #'+ (unserialize :list-of-integers))) => 28

(with-buffer (make-buffer)

(serialize :list-of-integers '(1 2 3 4 5 6 7))

(buffer-rewind)

(reduce #'+ (unserialize :list-of-integers))) => 28

Here is the latest:

- Code
[userial_0.6.2011.05.12.tar.gz](http://nklein.com/wp-content/uploads/2011/05/userial_0.6.2011.05.12.tar.gz), and - Signature
[userial_0.6.2011.05.12.tar.gz.asc](http://nklein.com/wp-content/uploads/2011/05/userial_0.6.2011.05.12.tar.gz.asc)