---
title: Coding For Two Audiences
url: http://hacksoflife.blogspot.com/2010/01/coding-for-two-audiences.html
author: Benjamin Supnik
published: '2010-01-05'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

All code is written for two audiences.Ha! You could put that in a fortune cookie. Seriously though, that is the truth, and it is the driving motivation behind my style guidelines for headers.

The first audience for your code is, of course, the compiler. The compiler is a tool that writes your application - your code is a set of instructions to the compiler about what you want it to do. Since compilers aren't very creative (at least we hope) you have to be very precise, and the compiler tends to be very picky. A compiler gets all bent out of shape when you write things like:

`viod set_flaps(int position);`


No imagination, those compilers. They also aren't real good at catching things like this:`if (x=0) init_subsystem();`


(Not quite fair - compilers now do catch some of the more knuckleheaded things you can do - but look at the C++-tagged posts in this blog for examples of what the compiler thinks isn't a bad idea.)So lots of books have been written about how to write code that won't confuse the compiler and you'll find engineers who insist on writing if (0 == x) and such. That serves the first audience well. But what of the second audience?

The second audience is the humans who will have to read the code in the future in order to use or change it. That includes future you, so for your own sake, be nice to this audience. Code says something to people, not just to compilers. Consider this:

`typedef void * model_3d_ref;`

model_3d_ref load_model_from_disk(const char * absolute_file_path);

void draw_model(model_3d_ref the_model, float where_x, float where_y, float where_z);

void deallocate_model(model_3d_ref kill_this);


Without knowing what the hell we're doing, if you know C and have worked as a computer programmer a few years, you probably already have a rough idea of what I'm trying to do with those declarations. Humans read code, and humans infer things from the code that will be necessary to work on it.The compiler doesn't read your code like this - the following code is exactly the same to a compiler:

`void * load_model_from_disk(const char *);`

void draw_model(void *, float, float, float);

void deallocate_model(void *);


As humans though, the above is a lot more like gibberish.**Header Nazi**

And that is why I am a header Nazi. Here's how I do the math: if you write code that is useful, bug free, and reasonably well encapsulated/insulated, then people are going to spend a lot more time looking at the header to understand the interface than they will spend looking at the implementation. (In fact, it should be unnecessary to look at the implementation at all to use the code.)

For this reason, I want my headers to be clean, clean, clean. I want them to read like a book , because that's what they are: the user's manual for this module to the humans who will use it. This tick comes out in a few forms:

- I prefer physical insulation (putting code in the cpp file) to logical encapsulation (putting things in the private: part of an object) because it gets the implementation details out of sight. It keeps the human readers from being distracted by how the module works, and helps keep inexperienced programmers from mistaking implementation for interface.
- If I have to inline for performance, I keep the inline out-of-class at the bottom of the header so it doesn't detract from readability.
- Bulk comments about usage go in the header to form a document.
- Any semantics about calling conventions go in the header so that examining source is not necessary.

## No comments:

## Post a Comment