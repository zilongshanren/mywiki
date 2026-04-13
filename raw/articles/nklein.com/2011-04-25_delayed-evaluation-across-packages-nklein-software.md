---
title: 'Delayed Evaluation Across Packages :: nklein software'
url: http://nklein.com/2011/04/delayed-evaluation-across-packages/
author: Pat
published: '2011-04-25'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

For my [networking layer library](http://nklein.com/software/unet/), I wanted to provide ubiquitous logging. At the same time, I did not want to tie the application to my choice of logging library. I wanted the user to be able to pass me a function where I could give them a logging category and something to log.

(defvar *logger-function* nil)

(defmacro log-it (category thing-to-log)

`(when *logger-function*

(funcall *logger-function* ,category ,thing-to-log)))

This seems simple enough, right? Now, throughout my code, I can do things like:

(log-it :list-of-unacked-packets (get-list-of-unacked-packets))

(etc)

The application can register a `*logger-function*`

something like this:

(cl-log:log-message category thing-to-log))

Here’s the problem though: most (all?) logging libraries are good about not evaluating any arguments beyond the `category`

unless something is actually listening for messages of that category. This makes it reasonable to do stuff like this and only take the speed hit when it’s actually important to do so:

(mapcar #'get-excrutiating-detail (append everyone everything)))

With my macro above, I have no way of knowing whether something is listening on a particular category or not. Further, most logging libraries don’t offer a way to query that sort of information.

### What to do?

What I wanted to do was to pass a macro from the application package into my networking library instead of passing a function. I spent way too long trying to find a way to make this work (especially considering I ran into the same trouble in [October, 2009](http://nklein.com/2009/10/lisp-troubles-fabricating-a-closure/) trying to use some combination of `(macroexpand ...)`

and `(eval ...)`

to let the caller decide which forms to execute).

All it took was posting to [comp.lang.lisp](http://groups.google.com/group/comp.lang.lisp/browse_thread/thread/a63a10394350cc7e/c06e26bb6dc1a20e#c06e26bb6dc1a20e) to answer my own question: **Closures**. I changed my macro to create a closure:

`(when *logger-function*

(funcall *logger-function* ,category #'(lambda () ,thing-to-log))))

Now, the application’s logger function changes slightly and my forms are only evaluated when the logging library evaluates them:

(cl-log:log-message category (funcall thing-to-log-generator))

Hopefully, I will remember next time I run into this.

Be aware that there is some cost in generating closures. Some implementations optimise generating the closure (so it isn’t very expensive) but accessing the closed-over variables is a bit slower than non-closed-over. Other implementations optimise variable access (so it’s no slower for a closed-over variable) but the cost of creating the closure will then be much higher. You mileage will vary.

– nick

Neat treatment!

I adapted to my own logging function by placing the FUNCALL inside the macro:

`(when *verbose*

(format *verbose* (funcall (lambda() (format nil ,message ,@parameters))))))

which makes the logging statements less verbose.

Any reason why you placed the FUNCALL as a parameter to the macro?

And why use the “#'” in front of the LAMBDA? Style?

The reason that I used a

`lambda`

at all was to keep it from evaluating just because`*verbose*`

was true. I wanted to some other part of the code decide when to do the`funcall`

.I think in your case here, you should probably instead be doing:

`(when *verbose*

(format *verbose* ,message ,@parameters)))

The

`when`

will take care of only evaluating the parameters when needed.And, yes… the

`#'(lambda`

is mostly a matter of reinforcing to the reader (lisp and human) that I really want to be passing in the function, not the result of calling it.