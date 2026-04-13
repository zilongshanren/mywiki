---
title: 'USerial Library — v0.1.2010.12.26 :: nklein software'
url: http://nklein.com/2010/12/userial-library-v01/
author: Pat
published: '2010-12-27'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I am putting together a networking library atop [usocket](http://common-lisp.net/project/usocket/) for use in a multiplayer Lisp game. So far, I have implemented a library for serializing data into a byte buffer.

Here is a simple example of serializing some things into a buffer:

(make-bitfield-serializer :login-flags (:hidden :stay-logged-in))

(serialize* (:opcode :login

:uint32 sequence-number

:login-flags '(:hidden)

:string login-name

:string password) buffer)

You can unserialize those bits into existing places:

(unserialize* (:opcode opcode

:uint32 sequence-number

:login-flags flags

:string login-name

:string password) buffer)

...)

You can unserialize them into newly-created variables for use within a body:

:uint32 sequence-number

:login-flags flags

:string login-name

:string password) buffer

...)

Or, you can unserialize them into a list:

:uint32

:login-flags

:string

:string) buffer)))

...)

You can find out more about the serialization library [on my unet page](http://nklein.com/software/unet/).