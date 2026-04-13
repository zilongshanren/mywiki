---
title: 'Binary Logging with CL-Log :: nklein software'
url: http://nklein.com/2011/04/binary-logging-with-cl-log/
author: Pat
published: '2011-04-07'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

One of the things that my current work does better than anywhere I’ve worked before is logging. When something goes wrong, there is a log file that you can dig through to find all kinds of information about what you were doing and how things were going.

As I move forward programming a game with my [UNet](http://nklein.com/software/unet/) library, I want to make sure that I can easily log all the network traffic during testing runs at least.

In looking through the various [Lisp logging](http://cliki.net/logging) packages out there, I decided on Nick Levine’s [cl-log](http://www.nicklevine.org/cl-log/) library.

I installed it in no time with [quicklisp](http://quicklisp.org/).

Then, I set to work trying to figure out how I could use it to log binary data.

Here’s what I ended up with. If you want to do something similar, this should give you a good starting point.

### Serializing, unserializing, and categorizing

With my [USerial](http://nklein.com/software/unet/userial/) library, I defined a serializer to keep track of the different categories of log messages. And, I made corresponding categories in cl-log.

(defcategory :packet)

(defcategory :error)

(defcategory :warning (or :error :warning))

(defcategory :info (or :warning :info))

### Specializing the classes

There are two major classes that I specialized: **base-message** and **base-messenger**. For my toying around, I didn’t end up adding any functionality to the **base-message** class. I will show it here though so that you know you can do it.

())

(defclass serialized-messenger (base-messenger)

((filename :initarg :filename :reader serialized-messenger-filename)))

Then, I overrode the **messenger-send-message** generic function to create a binary header with my [USerial](http://nklein.com/software/unet/userial/) library and then write the header and the message out.

(message serialized-message))

(let ((header (make-buffer 16)))

(serialize* (:uint64 (timestamp-universal-time

(message-timestamp message))

:log-category (message-category message)

:uint64 (buffer-length :buffer (message-description message)))

:buffer header)

(with-open-file (stream (serialized-messenger-filename messenger)

:direction :output

:if-does-not-exist :create

:if-exists :append

:element-type '(unsigned-byte 8))

(write-sequence header stream)

(write-sequence (message-description message) stream))))

### Using it

To get things going, I then made a log manager that accepts my **serialized-message** type and started one of my **serialized-messenger** instances.

(make-instance 'log-manager

:message-class 'serialized-message))

(start-messenger 'serialized-messenger :name "binary-logger"

:filename "/tmp/binary-log.dat")

Once these were started, I made a little utility function to make it easy for me to make test messages and then invoked **log-message** a few times.

(serialize :string string :buffer (make-buffer)))

(log-message :warning (make-info "Warning"))

(log-message :info (make-info "This is info"))

### Conclusions

In all, it has taken me about four times as long to write blog post as it did to install cl-log with quicklisp, peek through the cl-log documentation and source code enough to figure out how to do this, and write all of the code.

To really use this, I will probably separate out the category of a message from the serialized type of the message. This will probably involve adding a field to the **serialized-message** class to track the message type, adding an **initialize-instance :before** method for that class to look through the **arguments** to pull out the type, and then adding the type as an extra argument to **log-message**.

Sorry for the tangent, but the exclusive use of DIV for styling means that people who read the article somewhere other than your website (e.g. on planet lisp) don’t see preformatted code as preformatted code, but as plain text. It might be easier to read if you used e.g. PRE or CODE instead of DIV.

Hmm. That is all being done via a WordPress plugin. I’ll see if it’s customizable enough to change the tags it’s using. If not, I’ll see about forking off a version.

Hmm… I swear my posts used to look better on Planet Lisp than they do now. I wonder if they used to use

codetags and switched todivin one of the recent updates. Hmm.I think I fixed this now, but it involved editing the source to a plugin. I’ll probably break it next time I upgrade that plugin. Kick me again if that happens.