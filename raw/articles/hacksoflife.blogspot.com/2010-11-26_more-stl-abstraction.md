---
title: More STL Abstraction
url: http://hacksoflife.blogspot.com/2010/11/more-stl-abstraction.html
author: Benjamin Supnik
published: '2010-11-26'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[STL is not an abstraction](http://hacksoflife.blogspot.com/2010/02/stl-is-not-abstraction.html)because the specification it implements is so specific with regard to performance that it's really just an implementation. Response was swift and furious, and my contrast of the STL to something like an SQL query may have been lost.

Which begs the question: why is anyone reading this? What the heck? Chris and I have been terrified to find anything from this blog on the first page of a Google search or reposted somewhere. So if you're reading this: there will be no refunds at the end of this article if you feel you've lost 5 minutes of your life you'll never get back. You have been warned.

Anyway, I was looking at one case of the STL where you actually don't know what kind of performance you'll get unless you know things about your specific implementation. When you insert a range into a vector, the insert code has two choices:

- Iterate the range once, incrementally inserting. This may cause excess reallocation (since we don't know how much more memory we need until we're done), and that reallocation may in turn call excess copy construction and destruction.
- Measure the distance of the range. This lets us do one allocation and a minimum number of copies, but if the iterator doesn't have random access differencing, it would mean the range is iterated twice.

I have seen other cases where you can't quite guess what STL performance might be. For example, some implementations cache list size for O(1) list::size() while others do not cache and have to actually traverse the list. The SGI STL documentation does declare what the worst behavior is, so I have no right to complain if the list size isn't cached.

My argument isn't that the STL should always do the right thing by reading my mind. My argument is that because the STL is such a low level of abstraction, and because it serves such a low level purpose in code, the performance of the implementation matters. There may not be one right container for the job, and in trying to decide between a vector and list, whether I get single-allocate-insert on vector or constant-time size on the list might matter.

Fortunately in real development this turns out to be moot; if performance matters, we'll run an adaptive sampling profiler like Shark on the app, which will tell us whether for our particular usage and data the STL is under-performing. In a number of cases, our solution has been to toss out the STL entirely for something more efficient; as long as that's on the table we're going to have to profile, which will catch STL implementation differences too.

Ben, the point I think you might be missing is that STL is an example of


ReplyDeletegeneric programming(and not of OO). It is not meant to hide detail, as such! Generic programming is the style/study/practice of encoding algorithms in an abstract representation so you can apply them without change on different data structures.For more info, see this Stepanov interview:

http://www.stlport.org/resources/StepanovUSA.html

Christer, that's a GREAT interview!!! I think Stepanov is a hair over-the-top in his attack on OOP, but it's still fun to hear him articulate it. OOP vs. generic programming will have to be another blog post.





ReplyDeleteRe: hiding details...I need to think about this ... Stepanov formulates what he's trying to abstract in a very different way than OO, and it made me realize that my terminology in trying to describe what thie STL is and isn't is horribly imprecise.

So I suppose the real question is: how much fluctuation is there in STL implementations between advertised performance and actual performance. For example, I did not realize that having list-size cached is a requirement (and I have in the past used STLs, I think it was an older gcc-toolchain one, where list size was linear, although this is definitely fixed now).

It may be that my perception of ambiguity in the STL's performance spec comes from a bumpy road to implementations meeting the spec (I've been using C++ templates since the dark days when they often simply didn't work right) and not actually a design issue at all.

It certainly sounds like Stepanov has a clear idea of what he wants: the time performance IS the spec...that's something I can live wihth. :-)