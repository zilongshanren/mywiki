---
title: The Dangers of Super Smart Compilers
url: http://hacksoflife.blogspot.com/2015/12/the-dangers-of-super-smart-compilers.html
author: Benjamin Supnik
published: '2015-12-19'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

For the first time today, I ran an optimized DSF render using RenderFarm (the internal tool we use to make the global scenery) compiled by Clang.

The result was a segfault, which was a little bit surprising (and very disheartening) because the non-optimized debug build worked perfectly, and the optimized build works perfectly when compiled by GCC. When -O0 revealed no bug (meaning the bug wasn’t some #if DEV code) it was time for a “what did the optimizer do this time session.”

After a lot of printf and trial and error, it became clear that the optimizer had simply skipped an entire block of code that went roughly like this:


So…WTF? Well, buddy isn’t a pointer - it’s a smart handle, so operator== isn’t a pointer compare it’s code. We can go look at that code, let’s see what’s in it.

The handle turns out to just be a wrapper around a pointer - it’s operator* returns *m_ptr. Operator== is defined out of line and has a case specifically designed to make comparison-with-null work.


Reference cannot be bound to dereferenced null pointer in well-defined C++ code; comparison may be assumed to always evaluate to false.

Oh @#. Well, there’s our problem. This operator==, like plenty of other semi-legit code, is “unpacking” the handle wrapper by using &* to get a bare pointer to the thing being wrapped. In practice, the & and * cancel each other out and you get the bare pointer that is secretly inside whatever you’re working with.

Except that Clang is sooooo clever. It goes “hrm - if &*rhs == NULL then what was *rhs? It’s a NULL reference (because rhs is NULL and we dereferenced it). And since NULL objects by reference are illegal, this must never have happened - our code is in undefined behavior land as soon as *rhs runs.

Since our code is in undefined behavior land (if and only if *rhs is a “null object” if such a thing exists, which it doesn’t) then the compiler can do whatever it wants!

If *rhs is not a NULL object, &*rhs won’t ever equal NULL, and the result is false. So if one side of the case returns false and the other side is undefined, we can just rewrite the whole function.


The short term “fix” (and I use the term loosely) is to do this:



Newer versions of CGAL* have fixed this by taking advantage of the fact that a custom operator->() returns the bare pointer underneath the iterator, avoiding the illegal null reference case. (This technique doesn’t work in the general case, but the CGAL template is specialized for a particular iterator.)

In Clang’s defense, the execution time of the program was faster until it segfaulted!


The result was a segfault, which was a little bit surprising (and very disheartening) because the non-optimized debug build worked perfectly, and the optimized build works perfectly when compiled by GCC. When -O0 revealed no bug (meaning the bug wasn’t some #if DEV code) it was time for a “what did the optimizer do this time session.”

After a lot of printf and trial and error, it became clear that the optimizer had simply skipped an entire block of code that went roughly like this:

```
for(vector<mesh_mash_vertex_t>::iterator pts =
ioBorder.vertices.begin(); pts !=
ioBorder.vertices.end(); ++pts)
if(pts->buddy == NULL)
{
/* do really important stuff */
}
```


The really important stuff was being skipped, and as it turns out, it was really important.So…WTF? Well, buddy isn’t a pointer - it’s a smart handle, so operator== isn’t a pointer compare it’s code. We can go look at that code, let’s see what’s in it.

The handle turns out to just be a wrapper around a pointer - it’s operator* returns *m_ptr. Operator== is defined out of line and has a case specifically designed to make comparison-with-null work.

```
template < class DSC, bool Const >
inline
bool operator==(const CC_iterator<DSC, Const> &rhs,
Nullptr_t CGAL_assertion_code(n))
{
CGAL_assertion( n == NULL);
return &*rhs == NULL;
}
```


Of course, Clang is way smarter than I am, and it actually has commentary about this very line of code!Reference cannot be bound to dereferenced null pointer in well-defined C++ code; comparison may be assumed to always evaluate to false.

Oh @#. Well, there’s our problem. This operator==, like plenty of other semi-legit code, is “unpacking” the handle wrapper by using &* to get a bare pointer to the thing being wrapped. In practice, the & and * cancel each other out and you get the bare pointer that is secretly inside whatever you’re working with.

Except that Clang is sooooo clever. It goes “hrm - if &*rhs == NULL then what was *rhs? It’s a NULL reference (because rhs is NULL and we dereferenced it). And since NULL objects by reference are illegal, this must never have happened - our code is in undefined behavior land as soon as *rhs runs.

Since our code is in undefined behavior land (if and only if *rhs is a “null object” if such a thing exists, which it doesn’t) then the compiler can do whatever it wants!

If *rhs is not a NULL object, &*rhs won’t ever equal NULL, and the result is false. So if one side of the case returns false and the other side is undefined, we can just rewrite the whole function.

```
template < class DSC, bool Const >
inline
bool operator==(const CC_iterator<DSC, Const> &rhs,
Nullptr_t CGAL_assertion_code(n))
{
return false; /* there I fixed it! */
}
```


and that is exactly what Clang does. Thus if(pts->buddy == NULL) turns into if(false) and my important stuff never runs.The short term “fix” (and I use the term loosely) is to do this:

```
for(vector<mesh_mash_vertex_t>::iterator pts =
ioBorder.vertices.begin(); pts !=
ioBorder.vertices.end(); ++pts)
if(pts->buddy == CDT::Vertex_handle())
{
/* do really important stuff */
}
```


Now we have operator== between two handles:```
template < class DSC, bool Const1, bool Const2 >
inline
bool operator!=(const CC_iterator<DSC, Const1> &rhs,
const CC_iterator<DSC, Const2> &lhs)
{
return &*rhs != &*lhs;
}
```


This one is also doing illegal undefined stuff (&* on a null ptr = bad) but Clang can’t tell in advance that this is bad, so the optimizer doesn’t hammer our code. Instead it shortens this to a pointer compare and we win.Newer versions of CGAL* have fixed this by taking advantage of the fact that a custom operator->() returns the bare pointer underneath the iterator, avoiding the illegal null reference case. (This technique doesn’t work in the general case, but the CGAL template is specialized for a particular iterator.)

In Clang’s defense, the execution time of the program was faster until it segfaulted!

- You can make fun of me for not updating to the latest version of every library every time it comes out, but given the time it takes to update libraries on 3 or 4 compilers/build systems and then deal with the chain of dependencies if they don’t all work together, you’ll have to forgive me for choosing to get real work done instead.

Your post should be named The danger of code having undefined behavior.

ReplyDeleteTotally true! It's not an easy transition for old-timers like me who used to think we knew what the 'undefined' behavior was actually doing. With compiler technology 15 years ago, you could probably know what code would be generated for your target architecture and you might go "well, that's fine."


DeleteClearly now is not then and Clang is just going to astonish us with wizardry until we all shape up. :-)

I'm not sure whether that's your goal, but if you'd like to obtain the underlying object's address, why not simply use std::addressof instead?


ReplyDeletehttp://en.cppreference.com/w/cpp/memory/addressof

It wouldn't matter - the thing we're taking an address of is -already- a null reference (because we applied * to a nullptr_t) and thus we are already in undefined-bizarro-land.

DeleteI forgive you

ReplyDeleteInteresting post -- thanks for that!




ReplyDeleteNot sure if any of the techniques described here would have helped in your case, but there's a good overview of how clang deals with undefined behavior at:

http://blog.llvm.org/2011/05/what-every-c-programmer-should-know_21.html

Some more interesting docs about how clang optimizes const objects:


Deletehttps://docs.google.com/document/d/112O-Q_XrbrU1I4P-oiLCN9u86Qg_BYBdcDsmh7Pn9Nw/mobilebasic

I didn't know we already got at least one "post-classical" compiler in the wild as described by Raymond Chen:

ReplyDeletehttps://blogs.msdn.microsoft.com/oldnewthing/20140627-00/?p=633/ His description quite fits...

That's a great Raymond post. And yep...clang/llvm is -very- post classical. :-) This is the first time in production code that I've seen this kind of "undefined code? we'll optimize by nuking the entire code block" type behavior.

DeleteGCC has done the same thing before. It broke one of SPEC 2006 tests by optimizing a function into a infinite loop:

Deletehttp://blog.regehr.org/archives/918

However GCC developers decided to "fix" that optimization just before release.

Hah! You've got to love Clang. It's telling you it's all your fault, which you can't deny! I do worry about this development because it means programmers must become language lawyers to prevent things from breaking willy-nilly. A lot of programmers don't care very much, let alone know all the rules.


ReplyDeleteI also question the use of making things like signed integer overflow undefined. I think it was originally put there to deal with some signed formats and trapping hardware (although that could be implementation-defined). Does it have to be repurposed like that? Sure, it allows for some optimizations, but it's not quite as obvious what's going on when it works perfectly fine until the optimizer sees an opportunity. That kind of 'undefined' is bound to cause obscure bugs.

Another interesting case:









ReplyDelete// Global definition

struct Thing { char a[3]; };

// One file

ptrdiff_t subtract(struct Thing *a, struct Thing *b) { return a - b; }

// Another file

char data[1];

printf("%td\n", subtract((struct Thing *)(data + 1), (struct Thing *)data));

No optimization: 0

Full optimization: 0

Optimization but no link-time optimization: -6148914691236517205

Alternatively, you could do this:

struct Thing thing;

printf("%td\n", subtract(&thing + 4000000000000000000, &thing));

No optimization: -2148914691236517205

Full optimization: -2148914691236517205

Optimization but no link-time optimization: 4000000000000000000

You're welcome. Happy new year!

just a minor correction



ReplyDeleteit seems the problem is not in rhs, but in this,

"operator* returns *m_ptr"

operator* return a reference, and it can't be null

so clang evaluates == null as always false

in the solution to the problem clang has no choice but to evaluate both operands