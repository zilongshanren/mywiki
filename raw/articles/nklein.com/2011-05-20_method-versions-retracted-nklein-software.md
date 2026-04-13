---
title: 'Method Versions — Retracted :: nklein software'
url: http://nklein.com/2011/05/method-versions-retracted/
author: Pat
published: '2011-05-20'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

When I wrote the [method-versions library](http://nklein.com/software/method-versions/), I had read about [ContextL](http://common-lisp.net/project/closer/contextl.html) and decided that I only wanted a very small subset of it and wanted it to be very easy to use. It turns out that I didn’t quite understand the complexity-level of ContextL. It is actually very similar to what I had wanted.

With my library, you set up some versions and a variable to track the current version:

(method-versions:define-method-version :v1.1 :v1.0)

(declaim (special *protocol-version*))

(defparameter *protocol-version* :v1.0)

In ContextL, you just set up some layers:

(contextl:deflayer :v1.1 (:v1.0))

In my library, you then set up a generic function that uses a special method combination that keys off of the special variable:

(:method-combination method-versions:method-versions-method-combination

*protocol-version*))

In ContextL, you declare a layered function:

In my library, you then declare different methods using the version as a method qualifier.

(send-string (login-name cmd))

(send-string (login-password cmd)))

(defmethod send-cmd :v1.0 ((cmd login-cmd))

(send-string (login-name cmd))

(send-string (login-password cmd))

(send-string (login-location cmd)))

In ContextL, you declare layered methods specifying which layer the functions belong to:

(send-string (login-name cmd))

(send-string (login-password cmd)))

(contextl:define-layered-method send-cmd :in :v1.0 ((cmd login-cmd))

(send-string (login-name cmd))

(send-string (login-password cmd))

(send-string (login-location cmd)))

In my library, you set your special variable appropriately and invoke the method:

(send-cmd cmd))

In ContextL, you declare which layer you want to be active when you go to invoke the method:

(send-cmd cmd))

My library does not let you specify other method qualifiers like `:around`

or `:after`

. ContextL does.

I am going to leave my library published because I think it is a reasonably understandable, yet non-trivial, use of non-standard method combinations. However, I am going to end up using ContextL for the projects that I had intended for my library.