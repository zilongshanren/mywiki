---
title: 'USerial — v0.7.2011.05.24 :: nklein software'
url: http://nklein.com/2011/05/userial-v0-7-2011-05-24-2/
author: Pat
published: '2011-05-24'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I am releasing a new version of my [USerial](http://nklein.com/software/unet/userial/userial) library. This version cleans up many messes from earlier releases. Unfortunately, in that process, it breaks compatibility with earlier releases.

#### Obtaining

Getting the USerial library:

- The home page:
[http://nklein.com/software/unet/userial/](http://nklein.com/software/unet/userial/) - The tar-ball:
[userial_0.7.2011.05.24.tar.gz](http://nklein.com/wp-content/uploads/2011/05/userial_0.7.2011.05.24.tar.gz) - The GPG signature for the tar-ball:
[userial_0.7.2011.05.24.tar.gz.asc](http://nklein.com/wp-content/uploads/2011/05/userial_0.7.2011.05.24.tar.gz.asc) - The main git repository:
[http://git.nklein.com/lisp/libs/userial.git](http://git.nklein.com/lisp/libs/userial.git/) - A browsable mirror of the git repository:
[http://github.com/nklein/userial](http://github.com/nklein/userial/)

#### Differences

The differences between this version and earlier versions of this library include:

- Use of
[ContextL](http://common-lisp.net/project/closer/contextl.html)layered functions instead of CLOS methods - Elimination of
`:buffer`

parameter in favor of using the`*buffer*`

special variable - Cleaning up macros which no longer required the
`:buffer`

parameter - Serializers for arbitrarily large integers and unsigned integers
- Serializer for raw sequence of bytes
- New
`make-list-serializer`

macro

By using ContextL layered functions, one has the ability to define a serializer and/or unserializer in a particular ContextL layer. This can be used to create new versions of the serializer without losing the ability to use the older version when required.

In the process, I have created macros to assist in creating completely custom serializers. This both streamlines their definition and should allow any future modifications to the USerial library to fly under the radar. Code that before looked like this:

&key (buffer userial:*buffer*) &allow-other-keys)

... some code ...

buffer)

(defmethod unserialize ((key (eql :foo))

&key (buffer userial:*buffer*) &allow-other-keys)

(values (progn ... some code ...)

buffer))

Should now look like this:

... some code ...)

(define-unserializer (:foo)

... some code ...)

And, when you find you need to add a new version of your `:foo`

serializer but you don’t want to lose the old one, you can add:

(define-serializer (:foo (value foo-struct) :layer new-version)

... some new code ...)

Without the `:buffer`

parameter everywhere, code that used to look like this:

(buffer-rewind :buffer buf)

(unserialize-slots* (:string name :uint8 age) object :buffer buf)

Should now look like this:

(serialize* :string aa :uint8 bb)

(buffer-rewind)

(unserialize-slots* object :string name :uint age))

There are now `:int`

and `:uint`

serializers that encode arbitrarily large integers and unsigned integers, respectively. There is also a serializer that copies a sequence of bytes as is without any prefix or suffix. To unserialize, you either have to provide a buffer of the appropriate length with the `:output`

parameter or provide appropriate `:start`

and `:end`

keywords.

(end (length uchar-array)))

(unserialize :raw-bytes &key output

(start 0)

(end (length output)))

And, if you have a serialize/unserialize pair for type `:foo`

you can use the `make-list-serializer`

macro to create a serialize/unserialize pair for a list of items that can be serialized with the `:foo`

serializer.

(serialize :list-of-int8 '(0 1 1 2 3 5 8 13 21 34 55 89))

At the USerial home page, you can find [more complete documentation](http://nklein.com/software/unet/userial/userial).