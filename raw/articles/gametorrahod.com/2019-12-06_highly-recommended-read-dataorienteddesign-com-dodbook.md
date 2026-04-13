---
title: 'Highly recommended read : dataorienteddesign.com/dodbook'
url: https://gametorrahod.com/dodbook/
author: Sirawat Pitaksarit
published: '2019-12-06'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

An entire point of this post is just to point you to this one link : [http://www.dataorienteddesign.com/dodbook/](http://www.dataorienteddesign.com/dodbook/) and please read it all. Despite it's generic-sounding book name, the author almost always talks in game language. You will feel right at home reading it.

However, maybe you see that it is quite intimidating. I would like to convince you on a per-chapter basis what you will get, how that "hits home" to the problems you faced when trying to use [Entities library](https://docs.unity3d.com/Packages/com.unity.entities@latest) in Unity and don't know what to do.

These explanations require experience Unity DOTS, I assumed you have faced some frustrations already so you know what in this book will solve them.

In fact, after finishing this book I am very tempted to redo my data design again which I started last year when I knew nothing, as they are now naive and stupid. That says a lot about this book! I think it is a required reading that can't be filled with just Unity's [Entities documentation](https://docs.unity3d.com/Packages/com.unity.entities@latest) which is how to use the library. You want to use the library to design things mentioned in this book or else you could be doing OOP inside data-oriented. (e.g. not actually thinking how the data looks like and `Entity`

is now a synonym for an object.)

Though, I am not sure if reading this entirely before starting for the first time will be as effective or not, as I realized the book is useful because I can relate with my mistakes. That's why I decided to suicide my project into preview-DOTS since 2018 in the first place. I want to get a head start by making mistakes earlier than others to allow this kind of learning.

Actually I typed these down along the way as a way to keep myself focused, I'm going to just paste them now.

## Chapters

[Data-Oriented Design](http://www.dataorienteddesign.com/dodbook/node2.html): Convince you why OOP is only good for human programmer.[Relational Databases](http://www.dataorienteddesign.com/dodbook/node3.html): Proof there is a surefire way to answer "how should I model my data" if your mind is still with OOP. By borrowing techniques from DB people, each object can be untangled from its spaghetti of references and`null`

fields into a beautiful linear array, where you can then easily model with Unity's Entities library. There are multiple levels of normalization you can choose to do. When you linearize out the array field to a more data-oriented design or maybe with`DynamicBuffer`

member, you can now properly call it "[1NF](https://en.wikipedia.org/wiki/First_normal_form)".

[Existential Processing](http://www.dataorienteddesign.com/dodbook/node4.html)- How to "de-
`if`

" your code so you can just iterate on everything without`if`

guards or runtime checks, by data design. - Identify the
`if`

that really matters and essential. - The eternally popular demand to check for "subtype" (OOP concept) while iterating, but
`IComponentData`

is just that thing with no hierarchy. Using generics was not helping since each one became a completely new`IComponentData`

. Baking in an`enum`

or use by-value`ISharedComponentData`

to characterize them to replace subclassing is one solution that may come to you by common sense, this section expands on that so you feel it is not such a bad thing to do, compared to in OOP. - It is not weird to performs a check first then work on a chunk "blindly" after that one check, instead of the usual OOP way of checking for each object at the very last chance. This is essentially
`ISharedComponentData`

filtering, so you can kind of`switch case`

on any concrete value and get relevant data to work on. - Instead of runtime polymorphism (casting type, and there are some logic that change it behaviour depending on the current type), changing its archetype could also solve this. You will fear that data movement cost will be too much, but this article assures that that is in fact the norm in data-oriented.
- The event system : This is almost the bane of data-oriented design that you feel there is definitely no way out elegantly at first, and you were taking it for granted in OOP. There is a subsection for this, so you know you are not alone in finding this a problem. See how it relates to existential processing, I wasn't expecting this subsection to be here at first.

- How to "de-

[Component Based Objects](http://www.dataorienteddesign.com/dodbook/node5.html)- Finally it came to the C of ECS, previous sections wasn't even working with "components" but instead "just a data". So this section is very directly relatable to Entities package.
- It has an explicit mention to Unity and its classical components (the
`MonoBehaviour`

attachable component) that it is not yet the component in data-oriented way. - Harms of an object that impose its definition over its containing data (facts).
- How to deal with your
`Player`

uber-class where each things inside it sometimes talk to something inside it, and in the end you cannot take any of them out.


[Hierarchical Level of Detail](http://www.dataorienteddesign.com/dodbook/node6.html)- Or "HLOD". Unexpectedly, the book takes directly on rendering, a concept specific for games and similar media.
- It extends HLOD out of rendering concept though, you can "lod" just about anything such as simpler processing when accuracy is not needed.
- "Mementos" is an interesting term I first found here, but it is quite interesting. When LOD make the thing go to low definition, they should preserve some states so they could get back to it when they would become high definition again.
- Mementos deal with the occassional fear in Entities pacakge, of destroying
`Entity`

as a part of logic to make your system works the way you want to (not finding the entity anymore, therefore automatically do something/not doing things anymore, eliminating`null`

reference problems found in OOP), but you feel that "destroy" is a bit too much though there is no better clean way, and you start hacking in a flag or a boolean, then you have an`if`

. Adding tag component might help, but in some situation I think memento is a very clean and data-oriented way. For example adding a tag component requires modifying the system to account for it. (`None`

-query it) You will have a clearer strategy how to get that back dynamically. - The author not only removed rendering aspect from HLOD, but also the distance. You will realize that it is all about reducing works, a recurring theme in the Entities package and data-oriented design. This includes reducing instances of things, though the Entities package advertises it is fine with millions of things. It is then related to state complexity from the previous section, using LOD (axis of value) maybe a more data-way to determine what they should look right now than multitude of flags and booleans. This is as simple as refering to a stack of dishes as a single thing with an
`int`

how many dishes on it. This is already a HLOD because you reduced the details. Mind blown!


[Searching](http://www.dataorienteddesign.com/dodbook/node7.html)- This one also hits hard, it seems to be going against the flow in data-oriented to find something not already segmented (chunked) by components where previously you do something like LINQ query. Now you see inconveniences everywhere to allow searching : no longer parallelizable, manual work and tedious state maintenance, reduced performance, ugly code.
- Realize that the search is faster if the thing you are checking for is not interrupted by other things in between in terms of cache line, not just the complexity of search algorithm you use. How about a linear search that is faster than binary search because it travels in straight memory instead of jumping around thanks to data-oriented design? The key is in that 64 byte cache line size vs the size of each of your object, how much free stuff you can get in one read? Big O notation in shambles.
- Data-oriented search requires keeping in mind what would be your current cache line and get clever with it. For example on top of my head, separating a field to a new
`IComponentData`

for it to be linearly iteratable sounds good for speeding up search. - Get to know awesome algorithms that data-oriented design has advantage, such as
[Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter)or[B-Tree](https://en.wikipedia.org/wiki/B-tree). - Differentiate searching from sorting and hashing problems.
- It is possible to just modify the previous search result if you are aware when things are added or removed as an optimization, so you don't have to search again.


[Sorting](http://www.dataorienteddesign.com/dodbook/node8.html)- An another common need that feels wrong with Entities. You seems to be getting everything ordered randomly all the time caused by
`Entity`

removal and insertions. An unsettling experience coming from OOP world of hand-made`List<T>`

. - Think it through if there is any other way than sorting or not.
- The same with searching, data-oriented sorting should be aware of cache line and which linear memory to work in which order.
- Get to know data friendly algorithms such as
[Radix Sort](https://en.wikipedia.org/wiki/Radix_sort)or in-place[Bubble Sort](https://en.wikipedia.org/wiki/Bubble_sort)or[Sorting network](https://en.wikipedia.org/wiki/Sorting_network). There are several given to you in Entities package as well as an extension to work with`NativeArray`

.

- An another common need that feels wrong with Entities. You seems to be getting everything ordered randomly all the time caused by

[Optimisations](http://www.dataorienteddesign.com/dodbook/node9.html)- Making clear that which premature optimization is bad.
- Premature optimization is the root of all evils because in OOP and its instance based design abstracts so much you see everything as premature, until later when they show up, then you cannot optimize
*anyways*because OOP is getting in the way. In data-oriented you see the impact early and they looks no longer premature, therefore not evil then you can optimize it right away. Also you can fix it now, or improve them later. - Don't give in to hopeful optimizations. Determine, profile, make reports. We have the
[Performance Testing package](https://docs.unity3d.com/Packages/com.unity.test-framework.performance@latest)for this. It is great because as it take care of messy warm up step and report generation, exactly so the optimization isn't hopeful. - Give you several optimization examples on common problems.
- Several OOP optimization brought up here will hit home. You have done that before. How will that fare in data-oriented? Most of them reveal their weakness in cache line utilization.
- One part deal with data addition and deletion combined with multithreaded code. In this part you will appreciate that the system of Unity Entities manages that for you.
- "Don't delete" is a good advice so other concurrent system do not have to sync. They can continue to process values that ended up unused.


[Helping the compiler](http://www.dataorienteddesign.com/dodbook/node10.html): Needless to say, we are glad that most of this chapter are solved by C# Jobs limitations, Entities API design, and Burst, that we would otherwise have to face if coded pure in C++. But still useful to know about them.

[Maintenance and reuse](http://www.dataorienteddesign.com/dodbook/node11.html)- One of the bigger reason against using data-oriented approach that you can no longer subclass and infinitely build on the previous thing. This chapter make you feel better that there is more dimension in extending that is not inheritance.
- Why data-oriented cause less bug has been covered many times already but again here. The
`Entity`

query thing is already a protection against`null`

referencing in OOP since the work didn't even start if there is nothing to work for. - Convince you and remind you of your past OOP terror why data-oriented could make debugging faster. When he said a chain of
`if`

with multiple hidden`return`

in them, I immediately could relate to that one method I spent a day on creating and debugging. It wouldn't have to exist if it was data-oriented. - Different view on the word "reuse". You can indeed carry over something in a data-oriented project forward.
- Unit testing is hard in OOP because of setup step and that make us lazy to do it, you have to wire up objects. When it's just data, it is clear what to setup and what to look for : it's data. No more instantiating
`GameObject`

and placing in an imaginary world we can't even see because it is an Edit Mode test.


[What's wrong](http://www.dataorienteddesign.com/dodbook/node12.html)- This is actually a good first chapter to read. Answer questions as why you should drop OOP mindset.
- It reminds you about the current trend in OOP that is only good for you but bad for the machine and your players, and why data-oriented solve them.
- Explain why virtual calls that came as an ability in OOP are much more harmful (to data in your cache) than you think. Most devs thought that there is no way that the work in there is not worth the "tiny" virtual call cost, and that's what's wrong. As he talk how to avoid this problem, it ends with how about stop doing OOP altogether.
- Abstractions can help you solve problems, but in game development the problem is performance and that abstraction is of the wrong kind.
- The chapter can make you less carved for inheritance addiction.
- A more realistic view of "reusing" provided by OOP. Generic code is not as good as it sounds, it is only good on paper.


## How to read the web version better

You should support the author by purchasing a better formatted paperback or digital version : [https://www.amazon.com/dp/1916478700](https://www.amazon.com/dp/1916478700). But if that is not possible, there is a way to make the [web version](http://www.dataorienteddesign.com/dodbook) more accessible.

The only problem is that it has no style, and results in small fonts and a line length that is way too long. As soon as you realize there is an option for physical version, then you think "maybe a bit later I should order this, but not right now" as paying money is a friction in itself. Then a week later you forget you wanted to do it at all. Or the shipping cost outweight the book that make you hesitate. Then as you see the digital purchase version, you may think it would be not as good without a Kindle. I will show you some ways so you can start reading **now**. (Then continue in your preferred format later, etc.)

If you notice most good news website or magazines, they utilize margins or multiple columns to make characters per line at around 100 so your eye don't have to jump back and forth far horizontally. Reading is like a `for`

loop over thousands of lines, therefore you should optimize this data-oriented loop (heh) as much as possible so each line of text can be in one of your cache line fetch.

![](../../assets/9ebf19ec4e38fb46.png)

- Use a browser that has device simulation or CSS editing feature.
- Get your favorite fonts, I prefer serif font for long reads. Particularly a font that looks like the one in academic papers make me feel motivated to finish the read for some reason, so I choose the IM FELL font.
- Edit the CSS with
`font-family`

and`font-size`

to add in your own font from the machine. Additionally`line-height`

for some fonts. Do this again for each chapter, but each chapter is long enough. So have these CSS in your clipboard. - Use the screen width simulation to narrow down the line length, or use CSS paddings, so each line is approximately 100 characters. In Chrome, this device simulation mode also eliminates the sidebar appearing on scroll down, an improvement in focus since you are no longer aware of the total length of the article and can focus on learning.
- Use Night Shift or whatever tech that turns your screen yellow then enjoy the read at night. May looks ugly at first but you will get used to it after a chapter.
- The book flows better than you think. Once you actually
**start**reading for an hour, it gets exciting and harder to stop because you keep seeing familliar problems you faced being mentioned over and over, and you want to know how to approach them. So just start reading! - If you are still carving for Kindle as an excuse for delaying digital purchase. In fact you can try this with your laptop to suppress your desire. Though you need to scroll right for it to actually go down, and clicking the link to the next chapter can be a challenge :

![](../../assets/645c460e5aefcff0.jpg)