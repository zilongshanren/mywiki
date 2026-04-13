---
title: 'Dusting off my Growl Library :: nklein software'
url: http://nklein.com/2011/12/dusting-off-my-growl-library/
author: Pat
published: '2011-12-22'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I’ve spent the last few hours dusting off my [Common Lisp Growl client library](http://nklein.com/software/cl-growl/). The last time I worked on it was before the Mac Growl Application supported GNTP (Growl Notification Transport Protocol).

Today, working on it, I’m not quite sure what’s up, but I am not succeeding in communicating with the server using encryption. I’ll have to look more closely. Last time that I worked on it, I extended [Ironclad](http://method-combination.net/lisp/ironclad/), but I never got those changes pushed fully into Ironclad’s main line. But, I think I’m using the same version of Ironclad that I was using when I tested against the Windows Growl Application. *shrug*

I’ve also run into a snag with the Callbacks. Essentially, your Lisp program could get a callback when the user has clicked on your Growl notification. This actually works except for the fact that I am calling `READ-SEQUENCE`

into a buffer that is longer than the message. The server, I believe, is supposed to close the socket after the callback. But, it does not. So, I am stuck waiting for more bytes that will never come.

Now, I either have to do one of the following:

- refactor it to use
`READ-LINE`

instead - switch from using
[USocket](http://common-lisp.net/project/usocket/)to using[IOLib](http://common-lisp.net/project/iolib/)(and hope that`:dont-wait`

works as expected) - extend USocket to support
`SOCKET-RECEIVE`

even on TCP sockets

Anyone have a preference?

Are you having trouble using encryption with the Mac version or with the Windows version? The Mac version does not yet support encryption, so encrypted notifications will fail and should return the appropriate GNTP error response. The Windows version still supports all of the specified encryption options and should work fine if it was working fine before.

When I wrote the library, the Mac version didn’t support GNTP at all. Then, I tested on my son’s Win 7 laptop. This time around, I was testing on my Mac.

I was getting an error message, but it was not the correct one. It said:

Response-Action: REGISTER

Error-Description: (null)

Error-Code: 2

I suppose none of the listed Error-Codes in the GNTP doc really fit, but “(null)” and “2” gave me no clue what went wrong, if it was my fault, how to get more info, etc.