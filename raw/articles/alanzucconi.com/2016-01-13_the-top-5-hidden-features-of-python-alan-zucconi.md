---
title: The Top 5 Hidden Features of Python - Alan Zucconi
url: https://www.alanzucconi.com/2016/01/13/the-top-5-hidden-features/
author: Alan Zucconi
published: '2016-01-13'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Python aims to be an elegant and expressive language; this post includes its **top 5 hidden features**:

The term *hidden* is loosely used to indicate features which are generally unique to Python, or not very well known. I covered the most interesting Easter eggs which are *really* hidden in Python in [this post](https://www.alanzucconi.com/2015/10/29/the-top-5-easter-eggs-in-python/).

Python has the ability to slice list using the `[start:end]`

notation. Given a list a, `a[start:end]`

returns the sublist from the `start`

-th to the `end`

-th element.

>>> a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'] >>> a[2:6] ['c', 'd', 'e', 'f']

![list2_6](../../assets/897e42d30e371ee1.png)

Python allows to omit `end`

to indicate the last element:

>>> a[2:len(a)] ['c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'] >>> a[2: ] ['c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

![list2_end](../../assets/b6dd4b58b73b7aba.png)

You can also omit `start`

, which is equivalent to use `0`

instead:

>>> a[0:6] ['a', 'b', 'c', 'd', 'e', 'f'] >>> a[ :6] ['a', 'b', 'c', 'd', 'e', 'f']

![list0_6](../../assets/e9a34bd158c4d8e9.png)

One of the most annoying things when it comes to lists and arrays is to work with their last elements. Python allows to use negative indices, which behaves exactly like positive ones but on the right side:

>>> a[2:len(a)-4] ['c', 'd', 'e', 'f'] >>> a[2: -4] ['c', 'd', 'e', 'f']

![list2_-4](../../assets/958718f9e923a7fc.png)

For loops are often used to search for a specific element within a list. When this is the case, a flag is usually used to indicate if it has been found or not:

found = False for i in foo: if i == 0: found = True break if not found: print("i was never 0")

Python offers the **for…else construct**, which replaces the code above with the more expressive:

for i in foo: if i == 0: break else: print("i was never 0")

The else statement is executed if the loop has been completed without ever invoking `break`

.

In Python there is the concept of **iterator**. Lists, strings and `range`

s are all iterators. They allows to drive for loops, such as:

s = "Hello World..." # Loops over the characters of the string for a in s: print a,

Technically speaking, they are classes which:

- Have a
`__init__`

method - Have a
`__iter__`

method which return`self`

- Have a
`next`

method (`__next__`

in Python 3)

For instance, the following class is an iterator that counts up to a certain value:

class firstn(object): def __init__(self, n): self.c = 0 # Current element self.n = n # Max element def __iter__(self): return self def next(self): if self.c < self.n: cur = self.c self.c = self.c +1 return cur else: raise StopIteration() # Stops the iterator # Python 3 compatibility def __next__(self): return self.next()

As you can see, iterators are extremely tedious to create; something as easy as counting to n suddenly requires dozens of lines of code. **Generators** are the solution to this problem: they are methods which invoke the **yield statement**. The same class can be rewritten as a generator like this:

def firstn(n): for i in range(0,n): yield i

Both iterators and generators can be used in for loops and other functions which takes sequences:

for i in firstn(1000): ... sum( firstn(100) )

Languages such as C and Java only support single assignment. One variable equal one vale. Python allows to have multiple assignments on the same line.

>>> one = 1 >>> two = 2 >>> one, two = 1, 2

This also allows for the infamous **in-line swap**:

>>> a, b = b, a

Multiple assignments in Python is just a clever way of packing and unpacking variables. Python natively supports **list and tuples unpacking**:

>>> t = [1, 2, 3] >>>> one, two, three = t

List unpacking fails when used on a function; Python doesn’t natively unpack a list or a tuple when is passed to a function. This is because it may cause ambiguity: it’s up to the developer to specify when this has to be done. For instance:

def function(x,y,z): ... t = [1, 2, 3] function(t[0], t[1], [2])

is equivalent to the more compact:

function(*t)

The magic is done by the **star operator**. Python also has the **double star operator**, which is used to semantically unpack dictionaries:

def function(x,y,z): print x,y,z d = {'z':30, 'y':20, 'x':10 } function(**d)

In this case, Python will match the keys of the dictionary with the name of the arguments in the function. In order for this to work, the keys in the dictionary must match the name of the arguments.

## Leave a Reply Cancel reply