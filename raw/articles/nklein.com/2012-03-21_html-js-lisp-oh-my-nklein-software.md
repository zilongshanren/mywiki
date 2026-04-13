---
title: 'HTML + JS + LISP. Oh My. :: nklein software'
url: http://nklein.com/2012/03/html-js-lisp-oh-my/
author: Pat
published: '2012-03-21'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I started a Javascript + HTML application some time back. I decided that I wanted to get some Lisp on. So, it was time to pull out Hunchentoot, CL-WHO, and Parenscript.

It’s been awkward slogging so far. I still don’t have a good user-model of when exactly I need to wrap something in a `(cl-who:str ...)`

or when Parenscript will expand my macro rather than convert it into a function call or how I managed to get the `cl-who:*attribute-quote-char*`

to finally stick for a few REPLs.

The other half of the awkwardness is that I started writing the application in idiomatic javascript with prototype-based objects.

this.myfirst = undefined;

this.myarray = [ ];

}

MyClass.prototype.mymethod = function (arg1, arg2) {

this.myfirst = arg1;

this.myarray.push(arg2);

};

This makes for some awkward javascript when converted directly into Parenscript because:

- The method
`mymethod()`

will try to return the result of`Array.push()`

(which, technically, is fine, but not really the intent of the method). - Almost every statement on the Lisp side ends up wrapping just about everything in
`(parenscript:chain ...)`

. (**Edit:**Of course, I discovered right after posting this that the dot is left untouched in the Parenscript symbol conversion, so I can do`(this.myarray.push arg2)`

instead of`(parenscript:chain this my array (push arg2))`

. I’m certainly pleased with the brevity, but it pegs mysomething’s fishy here, Batman

meter.) - I have an aversion to using any package other than
`COMMON-LISP`

, so everything is way clunkier than all of the tutorials and examples online.

I think that I’m going to scratch all of the Javascript and Parenscript code that I have right now and start over with a mindset of How would I do this if it were just in Lisp? Now, what extra hoops do I need to get Parenscript to make usable Javascript?

rather than How would I do this in Javascript? Oh, and then, how can I make Parenscript say exactly that?

And, I may bite the bullet and `(use-package ...)`

both CL-WHO and Parenscript.

this.myarray.push is read in as one symbol, so if push is a macro, it won’t get macro expanded, and if myrarray is a symbol macro, it won’t be expanded either. That might be why your macros are not expanding, and why I made the “.” syntax unsupported (Parenscript should issue a warning every time it sees such a symbol). It’s possible to modify the readtable to treat “.” dots properly, but the dot character is already used for dotted lists in the standard CL readtable. I might provide that as an optional readtable that people can use with their code.

About CL-WHO, I just recommend going with straight HTML templates. It’s easier to work with and more flexible (you can have your templates writing out to a stream or returning strings in any way you want). And no more confusion about exactly what the output should look like. CL-Interpol actually makes a good solution: http://paste.lisp.org/display/118522

The only problem with that approach is that there is no mode for emacs that will indent HTML mixed with s-expression properly (yet).

I mentally discarded HTML-TEMPLATES off the top because I expect to have a bunch of DIV’s that have similar but not identical content and it just felt easier to do in Lisp than in TEMPLATE loops.

The CL-Interpol idea is interesting. I’ll keep that in mind.

Thanks.

One thing I have never had a good sense about is “what if my parenscript doesn’t work?” How do I debug parenscript-generated javascript? How do I patch it? Do I have to keep crashing my web app and starting over? Am I back to a variant of the old write-compile-test loop?

I know how to get a rudimentary REPL for developing in ordinary JavaScript — do I have to give it up to use Parenscript?

If you get this all figured out, give a talk about it at TC Lispers!

It seems possible to patch it through as a rudimentary REPL, but it would take a bit of work on both ends.

For my web application, I don’t expect it to be incredibly deep. So, the penalty for having to start over should be small. I suspect one of two things will happen:

Now accepting bets (or bribes).

Aw, heck. I’m already hooked. I’ll still take bribes, but it’s gonna be number 2.