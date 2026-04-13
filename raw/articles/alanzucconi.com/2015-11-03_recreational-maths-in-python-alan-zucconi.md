---
title: Recreational Maths in Python - Alan Zucconi
url: https://www.alanzucconi.com/2015/11/03/recreational-maths-python/
author: Alan Zucconi
published: '2015-11-03'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

This post is for all the developers and mathematicians out there that are curious to explore and visualize the bizarre properties of numbers. Although Maths plays an important role in today’s technology, many people likes to ~~ab~~use it for **recreational purposes**. Part of the appeal of [Recreational Maths](https://en.wikipedia.org/wiki/Recreational_mathematics) lies in the challenge to discover something new. Despite what many believe, finding mathematical patterns is very easy; it’s discovering something useful that is incredibly challenging. If you’re up for such a challenge, this tutorial will teach you how to use Python to calculate some of the most ~~in~~famous numerical sequences.

- Part 0.
[Unlimited precision](https://www.alanzucconi.com#part0) - Part 1.
[Working with digits](https://www.alanzucconi.com#part1)(Narcissistic numbers, Kaprekar numbers) - Part 2.
[Working with sequences](https://www.alanzucconi.com#part2)(Happy numbers) - Part 3.
[Visualising graphs](https://www.alanzucconi.com#part3)(Melancoil loop) - Part 4.
[Parallel computation](https://www.alanzucconi.com#part4) [Conclusion](https://www.alanzucconi.com#conclusion)

If you are familiar with Python, it is not uncommon to discover native features which would be challenging to replicate in other languages. One of the most intriguing is the way Python handles `long`

integers. While standard `int`

s have a 32bit precision, `long`

s can store arbitrarily big integers. This feature is native in Python, and does not requires any additional piece of code: when an `int`

becomes too large, it is automatically cast to `long`

. Compared to Java or C#, Python is perfect to work with very long numbers. The best hidden features of Python have been discussed in the tutorial [The Top 5 Hidden Features of Python](https://www.alanzucconi.com/?p=3392).

Many numerical sequences which are classified as *recreational Maths* work by manipulating the digits of a number. Converting a number in the list of its digits is surprisingly easy in Python:

def int_to_list (n): return map(int,str(n))

The number is firstly converted into a string using `str(n)`

; it is then passed into `map`

which converts each character of the string into an integer.

>>> int_to_list (1234567890); [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

#### Narcissistic numbers

Let’s use this to calculate [Narcissistic numbers](http://mathworld.wolfram.com/NarcissisticNumber.html) (OEIS [A005188](http://oeis.org/A005188)); a number of ![Rendered by QuickLaTeX.com d](../../assets/e3e196f6915d0ca1.png)

![Rendered by QuickLaTeX.com d^{th}](../../assets/7b9365c0eaee9cce.png)

![Rendered by QuickLaTeX.com 153](../../assets/52a0702ae04485a5.png)

![Rendered by QuickLaTeX.com 153=1^3+5^3+3^3](../../assets/d3dfbaa617ee11be.png)

*very suitable for puzzle columns and likely to amuse amateurs, but there is nothing in them which appeals to the mathematician*” ([G. H. Hardy](https://en.wikipedia.org/wiki/G._H._Hardy), 1993).

The following code checks whether a number is narcissistic or not:

def is_narcissistic (n): d = int_to_list(n) e = 0 for x in d: e = e + x ** len(d) return e == n

The for loop can be replaced by a `map`

function, which calculates the ![Rendered by QuickLaTeX.com d^{th}](../../assets/7b9365c0eaee9cce.png)


def is_narcissistic (n): d = int_to_list(n) e = sum( map(lambda x : x**len(d), d) ) return e == n

To calculate the sequence you can simply leave this piece of code running:

n = 1 while True: if is_narcissistic(n): print n, n = n+1

#### Kaprekar numbers

A slightly more interesting sequence is the one made of [Kaprekar numbers](http://mathworld.wolfram.com/KaprekarNumber.html) (OEIS[ A006886](http://oeis.org/A006886)). Consider an ![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n](../../assets/ac810e78c43cd7c0.png)

![Rendered by QuickLaTeX.com n-1](../../assets/43204d5a42f66088.png)

![Rendered by QuickLaTeX.com 9](../../assets/a5c506f91ef8c84f.png)

![Rendered by QuickLaTeX.com 9^2=81](../../assets/4947ff61302a3339.png)

![Rendered by QuickLaTeX.com 8+1= 9](../../assets/c8adefda75ed50c0.png)

![Rendered by QuickLaTeX.com 297^2=88209](../../assets/4436edf6311bc872.png)

![Rendered by QuickLaTeX.com 88+209=297](../../assets/7f41a34c5e13a4b6.png)


What makes it more interesting is that it requires to split a number into digits and then to join them. Once again, Python offers a very elegant way of doing this:

def list_to_int(ns): return int(''.join(map(str, ns)))

What we have to do now is to split the left and right side of the digits into two separate lists. To get the left `n`

elements of a list `d`

in Python one can write `d[:-n]`

; for the right `n`

elements `d[-n:]`

can be used instead.

def is_kaprekar (n): nn = len( int_to_list(n) ) # Digits original numbers d = int_to_list(n**2) # Square d_l = d[:-nn] # Left side d_r = d[-nn:] # Right side # Right term can't be zero (by convention) if d_r == 0: return False return n == list_to_int(d_l) + list_to_int(d_r)

Some numbers requires a more complex approach. This is the case for [happy numbers](https://en.wikipedia.org/wiki/Happy_number) (OEIS [A007770](https://oeis.org/A007770)). Finding if a number is happy or sad (not happy) requires an iterative computation. Let’s start with the **happification**, a process in which you take the digits of a number, square and sum them up:

![Rendered by QuickLaTeX.com \[happy\left( 13\right)=1^2+3^2=10\]](https://www.alanzucconi.com/wp-content/ql-cache/quicklatex.com-e29bef2a2eebe3b5021c4a614715aa7f_l3.png)


A number is happy if repeating this process leads to ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com 13](../../assets/745ea9772487eeb7.png)

![Rendered by QuickLaTeX.com happy\left( 10\right)=1](../../assets/8def9d605285ec7e.png)

![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)

![Rendered by QuickLaTeX.com 4](../../assets/0725b22597534378.png)

![Rendered by QuickLaTeX.com 16](../../assets/b3c71617c0c82a02.png)

![Rendered by QuickLaTeX.com 37](../../assets/57d25732b553f5fe.png)

![Rendered by QuickLaTeX.com 58](../../assets/7b3198fafa4b1736.png)

![Rendered by QuickLaTeX.com 89](../../assets/c32479adcb1e2c16.png)

![Rendered by QuickLaTeX.com 145](../../assets/0d088c7e65e4d202.png)

![Rendered by QuickLaTeX.com 42](../../assets/a8535dee2979cfc1.png)

![Rendered by QuickLaTeX.com 20](../../assets/fff5321e87cc6c2f.png)

[Numberphile](https://www.youtube.com/watch?v=_DpzAvb3Vk4) has covered this in a video in which [Matt Parker](https://twitter.com/standupmaths) coined the term **melancoil**.

The function `is_happy`

determines whether a number is happy or not; it keeps happifying the number until it gets ![Rendered by QuickLaTeX.com 1](../../assets/da6d507f7a2bceae.png)


def is_happy (n, l=[]): seen_numbers.append(n) # End of tree if n == 1: return True ns = int_to_list(n) s = sum(map(lambda x : x**2, ns)) # We are looping! if s in seen_numbers: l.append(s) return False # Recursive step return is_happy(s, l)

It’s important to remember that despite Python’s ability to work with arbitrarily large numbers, the function `is_happy`

cannot. This is because Python has a recursion depth limit. You can extend it using:

import sys sys.setrecursionlimit(10000)

Another alternative is to avoid recursion altogether:

def is_happy(n): seen_numbers = set() while n > 1 and (n not in seen_numbers): seen_numbers.add(n) ns = int_to_list(n) n = sum( map(lambda x: x**2, ns) ) return n == 1

Since we are storing the numbers in a list, the function is again limited by the amount of memory available. A further improvement is to remove any memory requirement by hard-coding the melancoil numbers in the function:

def is_happy(n): melancoil = [4, 16, 37, 58, 89, 145, 42, 20] while n > 1 and (n not in melancoil): ns = int_to_list(n) n = sum( map(lambda x: x**2, ns) ) return n == 1

The above function works only because all the sad numbers eventually end up in the melancoil loop.

The happification process naturally links numbers to each other. The result is a network graph which can be hard to see within the Python console. The best way to show the relationships between them is to visualise them with a graph. This is discussed in the tutorial [Interactive Graphs in the Browser](https://www.alanzucconi.com/?p=3460). **You can see the result in the interactive graph below:**

You can find a high resolution version (2000x2000px, first 1000 numbers) here: [PNG](https://drive.google.com/file/d/0B4nCcaMlgxV2UWVEREdUYUV0SVk/view?usp=sharing), [SVG](https://drive.google.com/file/d/0B4nCcaMlgxV2SUxhakdWTU1lcmM/view?usp=sharing), [HTML](https://www.alanzucconi.com/extra/d3/melancoil_1000/).

If the sequence you are trying to calculate works on very big numbers, it might take longer and longer to run. Calculating several numbers in parallel can help speed up the process, especially if you have multiple cores. There are several ways to implement **parallel computation** in Python; this example relies on the `joblib`

package:

from joblib import Parallel, delayed if __name__ == '__main__': tasks = 4 with Parallel(n_jobs=tasks) as parallel: n = 1 while True: # Calculate results = parallel(delayed(function_to_calculate)(n+i) for i in range(tasks)) # Print for i, result in enumerate(results): print n+i, "\t", result n = n +tasks

**Line 5** opens a `with`

section which creates four parallel processes. Every process has overhead, so it’s important to use a reasonable number; using too many processes can actually slow down your calculations. Within the parallel block, the computation is done with the function `parallel`

, which is fed four tasks. The function `delayed`

allows the user to specify the name of the function that will be executed separately. Evaluating results forces the program to wait until all of the processes are completed.

It is important to notice that in order for this code to work, everything has to be inside a `__main__`

section; this is because when the processes start they will execute the current file again.

### 📚 Recommended Books

This tutorial has shown how Python can be used effectively to calculate numerical sequences of arbitrary length. Recreational Maths is a very intriguing field, which can sometimes produce beautiful things such as [Conway’s Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). I strongly encourage you to explore the bizarre properties of numbers, and see if you can find something new.

If you are interested in this topic, you might also find the following tutorials interesting:

## Leave a Reply Cancel reply