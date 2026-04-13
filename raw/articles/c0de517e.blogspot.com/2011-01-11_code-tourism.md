---
title: Code Tourism
url: http://c0de517e.blogspot.com/2011/01/code-tourism.html
published: '2011-01-11'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

**Intro**:

I've always liked the analogies between the art of computer programming and classical arts, many have been made by various authors but the most famous are surely the essays "

[Hackers and Painters](http://www.paulgraham.com/hp.html)" by Paul Graham and "

[The Cathedral and the Bazaar](http://en.wikipedia.org/wiki/The_Cathedral_and_the_Bazaar)" by Raymond.

And it's not about some sort of self-indulgent flattery, as being proficient in some scientific field is still seen as a less culturally valid than having technical expertise in one of the "classical" ones. No, the fact is that I really believe that coding is an amazingly creative process and that we are still really bad at it. We should learn more from the other creative arts, it's striking how badly "engineered" our process is.

A painter gathers references (papers), draws studies (exploratory programming), then starts drawing (design), roughing in blocks and detailing areas (top-down coding). All this keeping a great control over his vision, and for most of the work he does... can we say that we do the same when coding our average tasks?

Now most of this has to do with the process itself, with our cumbersome workflow. It's harder for us to learn, to become proficient in these skills to the level that artists reach because our process is so far removed from our products. We don't interact with our creations, nor it's as-easy to visually assess their qualities.

I've wrote about this in some older posts, and I'm a strong advocate of live-coding and visualization techniques, but that's not what I wanted to write today (even if I already wrote quite a bit)...




**Tourism**:Today I want to focus on another aspect, that is how we learn our art. How did you learn to program? I guess the story is the same for everyone, we probably started to read a book or study a language, then we went to do some exercises maybe, and we started to... program. Then more reading, more programming, maybe talking to other people, working together, sharing ideas.

All this is fine, but aren't we missing something? I mean, you might bet that artists share a similar education, maybe they learn about techniques, maybe they have some mentors or teachers, and they start drawing. True. But they also do another thing. They leverage on their history. They study the masters. Visit cities, look at the architecture, visit galleries, get inspired by other people's work, or by their surroundings.

I started thinking about this while reading "

[the ultimate code kata](http://www.codinghorror.com/blog/2008/06/the-ultimate-code-kata.html)"; I bet when you started coding you did look at other people's source-code. Maybe got involved in a few projects, started tweaking stuff. Reading and understanding other people's ideas. But it's something that often we quickly dismiss after we get a bit more experienced.Why? Well one of the reasons is that on average we think too highly of ourselves, but another is that is really a time consuming process. Starting to understand the code in a project can take quite some effort, and how can we know if there is anything interesting for us to look at anyway?

We need code galleries! We need tourist information offices, guided tours, sightseeing. If you are in charge of a opensource project, or so, you should think about this, maybe adding a page to your wiki with some "entry points" (for example, see

[this](http://stackoverflow.com/questions/1010724/what-parts-of-linux-kernel-can-i-read-for-fun)).Some projects are by themselves more "touristic", neatly made examples of great code (but also, as touristic cities tend to be, they can be less livable, like

[boost](http://www.boost.org/)), some others contain great treasures, but they are hidden from the casual viewers (like my hometown[Naples](http://wikitravel.org/en/Naples), that can be pretty hostile to tourists).But this is not really only about opensource, I think it would be a great practice for a company too.

Usually one of the first things I do when I start working on a new project is to start understanding the main rendering flow, and usually there is no documentation about it, so I end up writing a wiki page with pointers to where to start, what functions are the main, most interesting ones, documenting a tour of the main "streets".

But it could be more than that... why not having a "gallery" of links and short introductions to interesting bits of code and functionality in your project? People could be interested, and even start learning across disciplines. Same goes for "notable snippets" maybe they can come from code reviews, maybe the lead or the TD can write some notes when looking at the changelists...

So where do we start?

*If you have suggestions, send some links to files/functions in the comments!*
## 6 comments:

My 1cent: https://github.com/paulhodge/EASTL/blob/master/include/EASTL/vector.h

If you develop this idea further, just enough to make public the code. Will be required and source criticism.

Who will determine that the code is worth attention? :)

KestaL: I don't understand your comment, sorry.

Sorry me English is poor and I tray translate a post with Google translator :). Now I rewrite post by me self and try explain.

I will say: if we look at programming like at art is not enough just make programming code (like paintings in art) public, and share for all. Who decide code (or project structure) write good or bad? In art we have art historians and reviewers. Who not make art, but analyze him. Who will due this jab on programming?

Anyway I agree software developing is art. And will be look at programming from this corner.

I always look at other source codes for different things, here some examples:


- for basic wxwidget stuff I look at the editor of the spin-x-engine (http://www.spinxengine.com/). With that I easily got a basic editor working.

- eastl for container-stuff (is eastl reentrant?) or stdcxx

- imgui and "immediate mode" stuff (http://www.johno.se/?tab=software)

- mmorpg sourcecode (ryzom or http://massiv.ow2.org/)

- multithreaded job management (http://software.intel.com/en-us/articles/nulstein/)

- game tool framework (https://github.com/HeliumProject/Helium)

great idea, keep them coming ;)

1. The closed source world is a very bad place to learn from.



2. The old world economics is based on the concept, that information hiding is good. Or at least if is not possible then to own ideas by use of patents.

3. My idea is that every software project should be structured like an interactive (software) book. The documentation and the project are the same. If you want you can jump to a page of code and can interactively execute a certain part and the result is visualized. All initialization is done by the "software book interactive environment" so that you do not have to configure anything just you are able to concentrate on a specific topic.

Post a Comment