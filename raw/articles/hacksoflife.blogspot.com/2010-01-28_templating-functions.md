---
title: Templating Functions
url: http://hacksoflife.blogspot.com/2010/01/templating-functions.html
author: Benjamin Supnik
published: '2010-01-28'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Template parameters can be either parameterized by type (typename T) or by value (int X).

The "traditional" C++ way of templating a piece of code is to use a functor - that is, the code is in an object, and the object thus gives the code unique type.

When working with traditional functions, this technique doesn't work well, because a change in type doesn't indicate a specific function - rather it specifies only the signature of many possible functions. So:

`template`

int do_op(int a, int b, OP op)

{

return op(a,b,);

}

int add(int a, b) { return a + b; }

...

int c = do_op(4,5,add);


Isn't equivalent to the functor case. In this example, do_op is instantiated for all function pointers whose signature is int X (int, int). The compiler would have to be pretty aggressive to fully inline this case. (I wouldn't rule it out though, as compiler optimization has gotten pretty advanced.)One way to tell that this code doesn't quite do what we want is:

`int (* func_ptr)(int, int) = add;`

int c = do_op(4,5,func_ptr);


is still legal, and clearly this is not getting inlined. To get full inlining, we need to template by value, so the function is fully available in the template.`typedef int(*binary_int_op)(int, int); // signature for all params`

template int add(int a, int b) { return op(a,b); }

int add(int a, b) { return a + b; }

...

int c = do_op(4,5);


In this case, each instantiated version of do_op is instantiated with a specific function already available. Thus we expect the code for do_op to look a lot like "return a + b". (Lisp programmers, stop your smurking!)We can also confirm that this is closer to what we want because this:

`int (* func_ptr)(int,int) = add;`

int c = do_op(4,5);


will fail to compile. GCC says: "error: 'func_ptr' cannot appear in a constant-expression. In other words, I can't fully expand do_op because you haven't given me enough info at compiler time to know what our op is.So if the second example is really fully inlining our op, and the first is not, what good is the template? What is it doing? The answer is: type coercion. This riff on the first example will work:

`template`

int do_op(int a, int b, OP op) { return op(a,b); }

float fadd(float a, float b) { return a+b; }

...

int c = do_op(4,5,fadd);


That example will work! (I am not suggesting it is good C++ but...) What has happened is do_op has been templated around the signatures of the various functions, and each separate instantiation will write different type coercion code. So the instantiated code for do_op with fadd looks something like:- convert a and b from int to float.
- call the function ptr op with float a and float b.
- convert the result back to int and return it.

(OT)

ReplyDeleteI'm pretty sure you are aware of it, but HTML is taking over all '<' and '>'s in your posted code segments. I'd say sample template code is quite damaged if you omit everything between angle brackets, right?!

It's ruining an otherwise useful post.

I know, and apparently blogger trashed the original code. :-( I'll see if I can fix it. :-(

ReplyDelete