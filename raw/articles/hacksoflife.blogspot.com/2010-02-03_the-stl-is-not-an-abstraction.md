---
title: The STL Is Not An Abstraction
url: http://hacksoflife.blogspot.com/2010/02/stl-is-not-abstraction.html
author: Benjamin Supnik
published: '2010-02-03'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

The STL is not an abstraction; it is a shortcut.In computer programming, an abstraction is something that hides the details. Abstractions let us get stuff done, and most of the time they

[leak](http://www.joelonsoftware.com/articles/LeakyAbstractions.html). Is the STL the leakiest abstraction in the universe?

No. It's not an abstraction at all. Abstractions hide implementation from you - the STL simply

*provides*implementation.

An indication that the STL is an abstraction would be that you could change the implementation of an STL algorithm or container and not notice. Does the STL meet that criteria? I don't think so, at least not in any sane way.

With the STL, you need to know

*all*of the fine print for any algorithm or class you do. Picking the type means picking an algorithm or data structure for its strengths and weaknesses. For example, if you pick vector, you are picking the following:

- A simple, compact representation.
- Blazingly fast random access iteration.
- The copy constructor of your data is going to be called a gajillion times.
- Mutating the size of the vector is going to hose outstanding iterators.
- Non-far-end insertion and deletion cost a fortune.

*prescribes*what will happen, pretty exactly.

And that's okay; typing vector

In 99% of the cases, you can't possibly build everything from zero - that is where STL helps, and STL does help a lot.



ReplyDeleteBtw, picking up suitable container (vector? deque? map? )does require an understanding of what container does and doesn't, in what area it shines etc are fair enough.

I dont agree with you complaining about copy constructor being called gazillion times. You can simply create a vector of pointers.

Dude, when you have to code in Java for your day job, you will realize just how lucky you were to be burned by STL all those years.

ReplyDeleteWhile I agree that it is not an abstraction, I would say that it is a _great_ thing that the STL doesn't abstract away the runtime complexities of the dictionary operations on each of these components. When you are looking at C++ as a language, runtime is a priority. The STL designers understood and made sure that these parameters are ingrained into the interfaces/guarantees that the library provides.

ReplyDeleteThe STL is an abstraction in the vane that all containers follow the container concept. Meaning you need to implement everything proposed by the concept in order to use your own container with STL algorithms. C++0x was supposed to fix this I believe with the introduction of concepts but it appears that has been scrapped for the time being. Unfortunately, the concept addition would have allowed performant code to work well with compile time interfaces. Since this doesn't seem to be coming anytime soon, errors will persist when the developer forgets to implement one of the requirements of the container concept.

ReplyDeleteexactly; google for scott meyers, effective stl, item 2, "Beware the illusion of container-independent code"

ReplyDeleteAt least C++0x's move semantics will solve the copy constructor issue.

ReplyDeleteOf course the STL is an abstraction. That's why you have no idea, for example, what datastructure underlies a std::map<>. You *can* change the implementations and not notice.


ReplyDeleteThe problem here is simple: you don't know what you're talking about. (Same reason you keep getting burned.)

StoneCypher: I think the point he was trying to make was that you can't just think about the specific abstractions the STL provides (iterators/containers, algorithms) and expect them to work together in all cases without looking into the details of each case. Type constraints (concepts) would have made this less of an issue of course, as they would guide programmers along the correct path. The issue is C++ doesn't provide what the STL requires to make their abstractions work properly. Performance was a higher priority for them, and the broken abstractions was the tradeoff.

ReplyDeleteStoneCypher: compare STL containers and algorithms to an SQL search query.





ReplyDeleteThe SQL search query is a leaky abstraction: it hides how it will do its magic, most of the time it works, because there's a crazy optimizer down there being clever, and every now and then the optimizer won't be clever enough and your DB admin will have to go put in an index or something.

Compare this to the STL; the spec for the containers tells you exactly what you get. The performance characteristics of the STL classes are not at all abstracted away.

My statement on the original post re: implementation is incorrect...what would be more correct is:

- For most of the STL containers, by the time you get to the actual container, the spec has so many requirements that there is only one sane available implementation.

- For all of the STL containers, the spec requirements on the specific containers are so specific that you are effectively picking an implementation.

You could argue that the hash table is a little bit abstract in that there are multiple ways to code a hash table, and you could argue that map is a little bit abstract because there are multiple ways to code a tree. I have yet to see a map that isn't a tree internally.