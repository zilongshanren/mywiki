---
title: LOGO Interpreter - Adrian Courrèges
url: http://www.adriancourreges.com/projects/logo-interpreter/
author: Adrian Courrèges
published: '2015-11-02'
source_blog: Adrian Courrèges
source_site: http://www.adriancourreges.com/
category: graphics
fetched: '2026-04-13'
---

![LOGO turtle](../../assets/a5b3baa09577e73b.png)


Its main goal was to introduce beginners to the concept of
algorithm or programs.


The turtle robot, which was actually an on-screen cursor, was one of the most famous features.
Thanks to a very easy syntax it was possible to make the turtle move, rotate or draw figures.
By providing immediate visual feedback the language was very accessible and easy to debug.


The interpreter I wrote can process a simplified version of the LOGO language.

It understands the following key-words and operators:

DEF, BEGIN, END, IF, THEN, ELSE, REPEAT, CALL, MOVE, JUMP, COLOR, FILL, NOFILL sin, cos, tan, *, +, -, /, =, <=, <, >=, >, &&, ||, not

The interpreter is written in CaML, you can find more information by reading the documentation below. (in French)

Playing with some fractal rendering code can be really fun.

### Screenshots

![LOGO Screenshot](../../assets/f21a7adaf84e6ad1.png)

![LOGO Screenshot](../../assets/082fe0788376d5ca.png)

![LOGO Screenshot](../../assets/2932345cbc493134.png)

![LOGO Screenshot](../../assets/8afe07b1b095f99e.png)


### Examples

The syntax of LOGO is quite simple.

Here is the definition to draw a square of dimension ‘n’:

DEF SQUARE (n) BEGIN REPEAT (4) BEGIN MOVE (n) ROTATE (90) END END

And here is how to draw a circle:

DEF CIRCLE (r) BEGIN REPEAT (1000) BEGIN MOVE (r/1000) ROTATE (360/1000) END END

Many other more complex algorithms can be found in the archive containing the source code.