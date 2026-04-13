---
title: 'A Currying Pipeline :: nklein software'
url: http://nklein.com/2010/11/a-currying-pipeline/
author: Pat
published: '2010-11-20'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I have been reading a great deal about Haskell and thinking a great deal about a networked Lisp game that I intend to work on soon. For the Lisp project, I will need to serialize and unserialize packets to send them over the network. I re-read the chapter on parsing binary files in Practical Common Lisp and started to think about how I could make readers and writers that worked on buffers. Thanks to the Haskell influence, I was also trying to do this serialization without side effects.

### The Goal

I wanted to accomplish something like this without all of the **SETF** action and verbiage:

(setf vv (serialize 'real xx vv))

(setf vv (serialize 'real yy vv))

(setf vv (serialize 'real zz vv))

vv)

### The First Attempt

Well, also thanks to Haskell, my instinct was to make a **CURRY-PIPELINE** macro that gets called something like this:

(serialize 'real xx)

(serialize 'real yy)

(serialize 'real zz))

and expands into something like this:

Unfortunately, this changes the order of evaluation of **xx**, **yy**, and **zz** entirely. So, this was suboptimal. It also involved a fifteen-line macro with macro recursion and two conditionals.

### Slightly Cleaner

My next attempt was about a ten-line macro with one conditional that turned it into a bunch of nested **LET** statements.

(let ((#:V-1 (serialize 'real xx #:V-1)))

(let (#:V-1 (serialize 'real yy #:V-1)))

(let (#:V-1 (serialize 'real zz #:V-1)))

#:V-1))))

### Cleaner Still

Then, I realized that most of my simple examples would be simplest if I curried into the first argument instead of the last. (In fact, it would have even fixed my order of evaluation problem in the initial version.) And, I realized that I could abandon the nested **LET** if I used a **LET***. Now, I have a six-line macro that I really like.

(let ((vv (gensym "VARIABLE-")))

(labels ((curry-and-store (line)

`(,vv (,(first line) ,vv ,@(rest line)))))

`(let* ((,vv ,initial)

,@(mapcar #'curry-and-store body))

,vv))))

So, here is an example that does one of those grade school magic tricks. Pick a number, multiply by five, add six, multiply by four, add nine, and multiply by five. Tell me the answer. I subtract 165 and divide by one hundred to tell you your original number.

(let ((rube (curry-pipeline n

(* 5)

(+ 6)

(* 4)

(+ 9)

(* 5))))

(curry-pipeline rube

(- 165)

(/ 100))))

### Back to the Original Problem

Now, my serialize functions can simply take a buffer and return a buffer which is the concatenation of the input buffer and the bytes required to encode the given value. The unserialize is not as nice since I will have to return both a buffer and a value, but I am sure I can work something out using a **CONS** as an accumulator. And, heck, it is going to kill my performance anyway if I really copy the buffer every time I want to add another item to it. I am probably going to ditch the functional aspect anyway. *shrug*

### A New Tack

If you don’t like currying or need to have more control over where the accumulator goes in each step of the chain, you can still get the same kind of chaining if you require a declaration of the variable. And, it simplifies the macro:

`(let* ((,var ,initial)

,@(mapcar #'(lambda (line) `(,var ,line)) body))

,var))

(defun magic-trick (n)

(let ((rube (let-pipeline (r n)

(* 5 r)

(+ 6 r)

(* 4 r)

(+ 9 r)

(* 5 r))))

(let-pipeline (a rube)

(- a 165)

(/ a 100))))

From there, it is not too big of a leap to allow **MULTIPLE-VALUE-BIND** instead. To accomplish the unserialize, as I mentioned, I will need to track multiple values. I am now down to a four line macro:

`(multiple-value-bind ,vars ,call

,(if rest-pipeline

`(mv-pipeline ,rest-pipeline ,@body)

`(progn ,@body))))

Here is an easy to follow example that returns the first five Fibonacci numbers:

(f2) (+ f1 f0)

(f3) (+ f2 f1)

(f4) (+ f3 f2))

(list f0 f1 f2 f3 f4))

Now, my unserialize case might look something like this:

(mv-pipeline ((xx buffer) (unserialize 'real buffer)

(yy buffer) (unserialize 'real buffer)

(zz buffer) (unserialize 'real buffer))

(values (vector xx yy zz) buffer)))

### Conclusion

Luckily, I am not paying myself based on lines of code per hour. Almost every time I have done more work, I have reduced the number of lines of code. I am reminded of this quote from Blaise Pascal: I have made this letter longer, because I have not had the time to make it shorter.