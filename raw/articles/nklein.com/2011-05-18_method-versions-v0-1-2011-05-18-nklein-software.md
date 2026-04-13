---
title: 'Method Versions — v0.1.2011.05.18 :: nklein software'
url: http://nklein.com/2011/05/method-versions-v0-1-2011-05-18-2/
author: Pat
published: '2011-05-18'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

Edit:After re-reading some of the ContextL papers, I believe that I am actually just going to use ContextL as it’s a much more flexible superset of this library. I will probably still keep this library published as an example of a non-trivial, but glarkable, method combination.

I am releasing a new library that allows one to dispatch generic methods based on the value of a global parameter.

There are situations where one might like to dispatch a method on some information other than the required parameters of the method. For many situations, it is sufficient to switch between those methods based on some external parameter. The [method-versions](http://nklein.com/software/method-versions/) library allows one to do just that.

- The home page:
[http://nklein.com/software/method-versions/](http://nklein.com/software/method-versions/) - The tar-ball:
[method-versions_0.1.2011.05.18.tar.gz](http://nklein.com/wp-content/uploads/2011/05/method-versions_0.1.2011.05.18.tar.gz) - The GPG signature for the tar-ball:
[method-versions_0.1.2011.05.18.tar.gz.asc](http://nklein.com/wp-content/uploads/2011/05/method-versions_0.1.2011.05.18.tar.gz.asc) - The main git repository:
[http://git.nklein.com/lisp/libs/method-versions.git](http://git.nklein.com/lisp/libs/method-versions.git) - A browsable mirror of the git repository:
[http://github.com/nklein/method-versions](http://github.com/nklein/method-versions)

In this example, we do a silly form of internationalization. To that end, we will use English as the default language and define some other languages.

(method-versions:define-method-version pig-latin)

(method-versions:define-method-version french latin)

(method-versions:define-method-version spanish latin)

We will prepare a language parameter and a welcome method that is versioned on the language.

(defparameter *language* nil)

(defgeneric welcome ()

(:method-combination method-versions:method-version-method-combination

*language*))

And, we define welcome methods for the various languages (accidentally forgetting `spanish`

).

(defmethod welcome :latin () :velkominum)

(defmethod welcome :pig-latin () :elcomeway)

(defmethod welcome :french () :bonjour)

Then, we will try each of the languages in turn.

(let ((*language* ll))

(welcome)))

'(nil :latin :pig-latin :french :spanish))

=> (:welcome :velkominum :elcomeway :bonjour :velkominum)

This looks like a stripped-down version of ContextL. Can you compare your library to that one?

Indeed, on the main page, I mention ContextL. I would say, is quite accurate.

The big thing, for me, was that I read all I could find about ContextL and still didn’t understand how to do reflective layer stuff where turning on layer B automatically turns on layer A, first. Additionally, I didn’t see a need for keeping slots in layers. ContextL seemed like overkill for my problem and like its academic documentation seemed out of sync with its current implementation.

Definitely, for some projects soon, I will likely use ContextL or Filtered Functions or both. But, for the serialization, networking, and binary logging applications that I have on hand, the only part I need/want is version numbers for some of my methods.

I updated the library main page with a list of some of the features of ContextL.

And, now I’ve re-read this paper on reflective layer activation and will probably end up using ContextL instead of this library for my serialization, networking, logging needs. Once I’ve actually played with it and verified that I grok it, I’ll make a new post describing what I’ve learned.