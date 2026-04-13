---
title: 'CL-Growl client library released :: nklein software'
url: http://nklein.com/2010/04/cl-growl-client-library-released/
author: Pat
published: '2010-04-12'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

[Growl](http://growl.info/) is a notification system for Mac OS X. You run a Growl server on your machine. Then, applications can send notifications that will be displayed on your desktop. Growl supports a thin network protocol called [Growl Talk](http://growl.info/documentation/developer/protocol.php) that programs can use to send notifications to the Growl server (and hence, to your desktop).

Growl is incredibly useful for any program that operates asynchronously with the user. If you want to be notified when some portion of your job completes or when there is a critical error in your web application, Growl is a great tool to have at your disposal.

I wrote an implementation for Common Lisp of the client protocol. Here is a simple example of how you might use it:

(growl:*growl-default-host* "localhost")

(growl:*growl-default-password* "my-growl-password"))

(growl:register :enabled (list "Warn" "Error")

:disabled (list "Info"))

(growl:notify "Program starting up..."

:notification "Info")

(unless (connect-to-database ...)

(growl:notify "Cannot connect to database!"

:title "Critical Error!"

:notification "Error"

:sticky t

:priority 2)))

For more complete usage information and to learn how to obtain the library, see [the CL-Growl web page](http://nklein.com/software/cl-growl/).

Sort of a Lisp noob but I cannot seem to be able load this. I installed this, MD5, and Ironclad through ASDF and while I can require the latter two all calls to

fail as if the package doesn’t exist. I am running SBCL through MacPorts on Snow Leopard, if that makes a difference.

Hmm. Did you ASDF-Install it? If not, where did you install it? And, what is the value of asdf:*central-registry* when you are in SBCL?

This was a problem with the tar file that I had uploaded. Try doing ASDF-INSTALL again.

Apparently, ASDF-Install gets confused if I tar things up as ./FOO-BAR-BAZ instead of just FOO-BAR-BAZ.

I did the install through ASDF. I just did a re-install and it works fine. Thanks!