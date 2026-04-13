---
title: 'Building the language up to you :: nklein software'
url: http://nklein.com/2013/05/building-the-language-up-to-you/
author: Pat
published: '2013-05-05'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

One of the things that’s often said about Lisp is that it allows you to [build up the language](http://dunsmor.com/lisp/onlisp/onlisp_5.html) to you. Here are two examples that really drive home that point, for me.

## The Problem Domain

I read [an article about Treaps](http://pavpanchekha.com/blog/treap.html) on reddit yesterday. The article used pretty direct pylisp to present Treaps.

I thought it would be fun to go through the exercise in Common Lisp instead. Pylisp made a number of things awkward that would melt away in Common Lisp.

I began by defining a node structure to encapsulate the information at a given node:

(priority (random 1.0d0) :type real :read-only t)

(key 0 :read-only t)

(value 0 :read-only t)

(left nil :type (or null node) :read-only t)

(right nil :type (or null node) :read-only t))

Then, I defined a top-level structure to hold the root node, track the function used to sort the tree, and track the function used to create a key from a value. I used the convention that two keys are equivalent if neither is less than the other.

(root nil :type (or null node) :read-only t)

(less-than #'< :read-only t)

(key #'identity :read-only t))

## The First Build Up

The article was using a functional style. As you may have guessed by the liberal use of `:read-only t`

in those `DEFSTRUCT`

clauses, I also used a functional style.

When working with functional data structures, one often needs to copy a whole structure with only slight modifications. Here, Lisp’s keyword arguments made everything simple and clean. I made this functions:

(key (node-key node))

(value (node-value node))

(left (node-left node))

(right (node-right node)))

(make-node :priority priority

:key key

:value value

:left left

:right right))

Now, for any node, I could copy it and only have to specify the fields that I wanted to change. Here is a left-rotation using this:

(let ((left (node-left node)))

(copy-node left

:right (copy-node node

:left (node-right left)))))

What other languages let you do anything like that so simply? You could pull it off in Perl if you were willing to have your node be a hash (which, admittedly, you probably are if you’re writing Perl). What other language lets you do anything like that? Even other languages with named arguments don’t let you have the defaults based on other arguments.

## The Second Build Up

As with any binary tree, you find yourself having to deal with four specific cases over and over again with Treaps.

- You ran out of tree
- Your key is less than the current node’s key
- Your key is greater than the current node’s key
- Your key is equivalent to the current node’s key

I wrote myself a `TREAP-CASES`

macro that streamlines all of these checks. It also validates to make sure you don’t have duplicate cases or cases other than these four. It makes sure that no matter which order you write the cases (or even if you leave some out), they end up organized in the order listed above. The four cases are mutually exclusive so the order doesn’t matter except that you want to make sure you haven’t run out of tree before doing comparisons and that once you’re beyond the less-than and greater-than cases you already know you’re in the equivalence case.

With this macro, my `TREAP-FIND`

function looks like this:

(check-type treap treap)

(labels ((treap-node-find (root)

(treap-cases (key root treap)

(null (values nil nil))

(< (treap-node-find (node-left root)))

(> (treap-node-find (node-right root)))

(= (values (node-value root) t)))))

(treap-node-find (treap-root treap))))

The little DSL makes writing and reading the code so much easier. All of the mess of comparing the key to the node’s key is hidden away.

With years of practice and days of debugging, you might be able to pull off some quasi-readable control construct like this using C++ templates. With enough therapy, you could convince yourself you can get a close-enough effect with C-preprocessor macros. In Lisp, it’s the work of minutes (without lying to yourself).

Here is the `TREAP-CASES`

macro for reference/completeness.

(validate-treap-case-clauses clauses)

(let ((k (gensym "KEY-"))

(tr (gensym "TREAP-"))

(r (gensym "ROOT-"))

(t< (gensym "<-")))

`(let* ((,k ,key)

(,tr ,treap)

(,r ,root)

(,t< (treap-less-than ,tr)))

(cond

((null ,r) ,@(rest (assoc 'null clauses)))

((funcall ,t< ,k (node-key ,r)) ,@(rest (assoc '< clauses)))

((funcall ,t< (node-key ,r) ,k) ,@(rest (assoc '> clauses)))

(t ,@(rest (assoc '= clauses)))))))

I suppose I should also include `#'VALIDATE-TREAP-CASE-CLAUSES`

, too, but it’s what you’d expect:

(let ((all-choices '(null < > =)))

(flet ((assert-all-choices-valid ()

(dolist (c clauses)

(unless (member (first c) all-choices)

(error "Unrecognized clause type: ~S" (first c)))))

(assert-no-duplicates ()

(dolist (c all-choices)

(unless (<= (count c clauses :key #'first) 1)

(error "Duplicate ~S clause not allowed." c)))))

(assert-all-choices-valid)

(assert-no-duplicates))))