---
title: The Top 5 Easter Eggs in Python - Alan Zucconi
url: https://www.alanzucconi.com/2015/10/29/the-top-5-easter-eggs-in-python/
author: Alan Zucconi
published: '2015-10-29'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Despite being a very serious language, Python is full of Easter eggs and hidden references. This post shows the top 5:

[Hello World…](https://www.alanzucconi.com#part1)[The Zen of Python](https://www.alanzucconi.com#part2)[Antigravity](https://www.alanzucconi.com#part3)[C-Style braces instead of indentation](https://www.alanzucconi.com#part4)[Monthy Python references](https://www.alanzucconi.com#part4)

I have covered the 5 most interesting features of Python in [this post](https://www.alanzucconi.com/2016/01/13/the-top-5-hidden-features/).

As a programmer, you should be familiar with **Hello World**. Python has a library that does that that.

>>> import __hello__ Hello World...

On Python 3 you get a slightly more enthusiastic message: `Hello world!`

. Reimporting the library doesn’t make the message reappear.

Another hidden library in Python is `this`

, which prints a poem by Tim Peters called **The Zen of Python**:

>>> import this The Zen of Python, by Tim Peters Beautiful is better than ugly. Explicit is better than implicit. Simple is better than complex. Complex is better than complicated. Flat is better than nested. Sparse is better than dense. Readability counts. Special cases aren't special enough to break the rules. Although practicality beats purity. Errors should never pass silently. Unless explicitly silenced. In the face of ambiguity, refuse the temptation to guess. There should be one-- and preferably only one --obvious way to do it. Although that way may not be obvious at first unless you're Dutch. Now is better than never. Although never is often better than *right* now. If the implementation is hard to explain, it's a bad idea. If the implementation is easy to explain, it may be a good idea. Namespaces are one honking great idea -- let's do more of those!

The most ~~in~~famous easter egg in Python is the antigravity one, which redirects to an [xkcd](http://xkcd.com/353/) strip:

import antigravity

![python](../../assets/eaf51697d4d00757.png)


![python](../../assets/eaf51697d4d00757.png)

Python is designed to be elegant; mandatory indentation is an essential part of this. The library `braces`

were supposed to change this, allowing to use C-Style braces instead of indentation. This is of course a joke, since attempting to import it produces a rather passive-aggressive “**not a chance**“.

>>> from __future__ import braces File "<stdin>", line 1 SyntaxError: not a chance

The name Python has nothing to do with reptiles. Rather the opposite, it comes from the BBC show “**Monty Python’s Flying Circus**”. As the official Python guide [suggests](https://docs.python.org/2/tutorial/appetite.html):

Making references to Monty Python skits in documentation is not only allowed, it is encouraged!


This has led developers to include several hidden references not only in the official documentation, but also in their code. For instance in Python, [metasyntactic variables](https://en.wikipedia.org/wiki/Metasyntactic_variable) takes the names of **spam and egg**, rather than the more traditionally used **foo and bar**. This is a clear reference to the Monty Python sketch [Spam](https://en.wikipedia.org/wiki/Spam_(Monty_Python)). You can see this, for example, in the official documentation ([Input and otuput](https://docs.python.org/2.7/tutorial/inputoutput.html)) in which there are many other references such as:

>>> print 'We are the {} who say "{}!"'.format('knights', 'Ni') We are the knights who say "Ni!"

From Coursera to Codeacademy, basically every serious Python tutorial make references to Monty Python.

## Leave a Reply Cancel reply