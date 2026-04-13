---
title: 'Iterators in C#: yield, IEnumerable & IEnumerator - Alan Zucconi'
url: https://www.alanzucconi.com/2017/01/22/iterators-c-yield-ienumerable-ienumerator/
author: Alan Zucconi
published: '2017-01-22'
source_blog: Alan Zucconi
source_site: https://www.alanzucconi.com/
category: game programming
fetched: '2026-04-13'
---

Iterating over lists in C# is often done using `for`

loops. This tutorial shows how the `foreach`

construct can be coupled with the `yield`

statement to create more elegant and safe code.

[Introduction](https://www.alanzucconi.com#introduction)- Part 1.
[Implementation](https://www.alanzucconi.com#part1) - Part 2.
[The yield Statement](https://www.alanzucconi.com#part2) - Part 3.
[Limitations](https://www.alanzucconi.com#part3) [Conclusion](https://www.alanzucconi.com#conclusion)

If you are familiar with C#, chances are you might have used the `List`

class. Like most of the modern data structures available in .NET, the elements within a `List`

can be **iterated** in many way. The most common uses a `for`

loop and and index `i`

to access the elements sequentially.

List<int> list = new List<int>(); ... for (int i = 0; i < list.Count; i ++) Debug.Log(list[i]);

C# introduces a new way to loop over the elements of a list: `foreach`

construct.

List<int> list = new List<int>(); ... foreach (int n in list) Debug.Log(n);

This new syntax allows to explicitate the intention of the programmer. The stress now is on the fact that you want to iterate the elements of a list; not about incrementing indices. This is particularly helpful when there are nested loops. Indices like `i`

and `j`

can be easily swapped by mistake, and edge conditions are sometimes hard to get right on the first try.

Classes that can be iterated using `foreach`

make such a behaviour possible by implementing the `IEnumerable`

interface ([MSDN](https://msdn.microsoft.com/en-us/library/9eekhta0(v=vs.110).aspx)). Inside, it contains a method called `GetEnumerator`

that must be used to create and return an **iterator**. Like the name suggests, iterators are data structures that can be iterated upon. They implement the interface `IEnumerator`

([MSDN](https://msdn.microsoft.com/en-us/library/78dfe2yb(v=vs.110).aspx)), which provides an API to iterate over a sequence of element. `IEnumerator`

contains:

`MoveNext`

: A method that forces the iterator to fetch the next element in the list. It returns`true`

if there is a next element;`false`

if the sequence has terminated.`Current`

: This**getter**is used to return the current element of the iterator.

After having understood how an iterator class is implemented, it’s easy to see how those two code snippets are equivalent:

// Foreach foreach (int i in list) Debug.Log(i); // Iterator IEnumerator<int> iterator = list.GetEnumerator(); while (iterator.MoveNext()) { int n = iterator.Current; Debug.Log(n); }

Iterators are awesome. However, they are a pain to code. Recording the position of the current object and moving it at each subsequent call of `MoveNext`

is not the most natural way to iterate over a sequence. This is why C# allows a more compact way to write classes that are compatible with `foreach`

. This is done thanks to a new keyword: `yield`

.

Let’s imagine that we want to create an iterator that produces the elements `0`

, `1`

, `2`

, and `3`

. We can either create a class that implements the `IEnumerable`

interface, instancing an `IEnumerator`

that uses `MoveNext`

and `Current`

to produce the desired list.

Or, we can create the following function:

IEnumerator<int> OurNewEnumerator () { yield return 0; yield return 1; yield return 2; yield return 3; }

The compiler will take this piece of code and convert it in a proper `IEnumerator`

. With this new syntax, is incredibly easy to loop over the object the sequence:

foreach (int n in OurNewEnumerator()) Debug.Log(n);

If we want the instance of the class that contains `OurNewEnumerator`

to be automatically recognised as an iterator in a `foreach`

loop, what we have to do the following:

public class OurClass : IEnumerable<int> { ... IEnumerator<int> IEnumerable.GetEnumerator() { return OurNewEnumerator(); } }

Now we can use the class itself as the list argument of the `foreach`

loop:

OurClass list = new OurClass(); ... foreach (int n in list) Debug.Log(n)

Iterators are very handy. However, they have some pretty strong limitations. The most obvious one is that elements should not be removed in the body of a `foreach`

loop. Most lists detect and prevent this. On top of being an **anti pattern** ([Wikipedia](https://en.wikipedia.org/wiki/Anti-pattern)), removing elements, one by one, on a list is generally extremely inefficient. When an element is removed from an array-based list, for example, it causes most elements to be rearranged to fill the gap it left behind. Repeating this multiple times is inefficient.

Removing elements from a list is, generally speaking, a “controversial” topic. A common solution is to iterate elements in reverse with a traditional `for`

loop. Most .NET data structures comes with a function `RemoveAll`

that can be used to safely remove all elements that match a certain condition.

This post introduced the concept of `foreach`

loop, as a safer and more elegant approach to traditional index-based `for`

loops. To sum up:

- The
`foreach`

loop can be used to iterate data structures; `IEnumerable`

is the interface that iterable data structures should implement. It contains:`GetEnumerator`

: must return an instance of`IEnumerator`


`IEnumerator`

is the interface that abstracts the process of iterating elements. It contains:`MoveNext`

: Advances the state of the iterator and returns true if there is a next element available;`Current`

: A getter used to retrieve the current element being iterated upon.


## Leave a Reply Cancel reply