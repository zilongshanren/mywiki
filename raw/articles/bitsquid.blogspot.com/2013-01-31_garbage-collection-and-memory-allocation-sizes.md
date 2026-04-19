---
title: Garbage Collection and Memory Allocation Sizes
url: https://bitsquid.blogspot.com/2013/01/garbage-collection-and-memory.html
author: Niklas
published: '2013-01-31'
source_blog: 'bitsquid: development blog'
source_site: https://bitsquid.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

As a performance conscious programmer in a soft-realtime environment I've never been too fond of garbage collection.

Incremental garbage collectors (like the one in Lua) make it tolerable (you get rid of the horrible garbage collection stalls), but there is still something unsettling about it. I keep looking at the garbage collection time in the profiler, and I can't shake the feeling that all that time is wasted, because *it doesn't really do anything*.

Of course that isn't true. Garbage collection frees the programmers from a lot of busywork. And the time they gain can go into optimizing other systems, which leads to a net performance win.

It also simplifies some of the hairy ownership questions that arise when data is transferred between systems. Without garbage collection, those questions must be solved in some other way. Either by reference counting (error-prone) or by making local copies of the data to assume ownership (ugly and costly).

But still, there is that annoying performance hit.

I was pretty surprised to see that the developers [Go](http://golang.org/), a language that looks well-designed and targets low-level programmers, decided to go with garbage collection rather than manual memory management. It seemed like a strange choice.

But recently I've started to see things differently.

One thing I've noticed as I delve deeper and deeper into data-oriented design is that I tend to allocate memory in much larger chunks than before. It's a natural consequence of trying to keep things continuous in memory, treating resources as large memory blobs and managing arrays of similar objects together.

This has interesting consequences for garbage collection, because when the garbage collector only has to keep track of a small number of large chunks, rather than a large number of small chunks, it can perform a lot better.

Let's look at a simple example in Lua. Say we want to write a class for managing bullets. In the non-data-oriented solution, we allocate each bullet as a separate object:

```
function Bullet:update(dt)
self.position = self.position + self.velocity * dt
end
function Bullets:update(dt)
for i,bullet in ipairs(self.bullets) do
bullet:update(dt)
end
end
```

In the data-oriented solution, we instead use two big arrays to store the position and velocity of *all* the bullets:

```
function Bullets:update(dt)
for i=1,#self.pos do
self.pos[i] = self.pos[i] + dt * self.vel[i]
end
end
```

I tested these two solutions with a large number of bullets and got two interesting results:

The data-oriented solution runs

**50 times**faster.The data-oriented solution only needs

**half**as much time for garbage collection.

That the data-oriented solution runs so much faster shows what cache coherence can do for you. It is also a testament to how awesome LuaJIT is when you give it tight inner loops to work with.

Note that in this test, the *Bullet* code itself did not create any garbage. The speed-up comes from being faster at collecting the garbage created by *other systems*. And the reason for this is simply that with fewer, larger memory allocations, there is less stuff that the garbage collector has to trawl through. If we add in the benefit that the data-oriented solution will create fewer objects and generate less garbage, the benefits will be even greater.

So maybe the real culprit in isn't garbage collection, but rather having many small memory allocations. And having many small memory allocations does not just hurt the garbage collector, it is bad for other reasons as well. It leads to bad cache usage, high overhead in the memory allocator, fragmentation and bad allocator performance. It also makes all kinds of memory problems harder to deal with: memory leaks, dangling pointers, tracking how much memory is used by each system, etc.

So it is not just garbage-collected languages like Lua that would benefit from allocating memory in larger chunks, but manually managed languages like C++ as well.

Recently, I've come to think that the best solution to memory management issues in C++ is to avoid the kitchen-sink global memory allocator as much as possible and instead let each subsystem take a much more hands-on approach to managing its own memory.

What I mean by this is that instead of having the sound system (for example) send lots of memory requests to the kitchen-sink memory manager, it would only request a few large memory blocks. Then, it would be the responsibility of the system to divide that up into smaller, more manageable pieces that it can make practical use of.

This approach has a number of advantages:

Since the system knows the usage patterns for its data, it can arrange the memory efficiently. A global memory allocator has no such knowledge.

It becomes much easier to track memory use by system. There will be a relatively small number of global memory allocations, each tagged by system. It becomes obvious how much memory each system is consuming.

Memory

*inside*a system can be easily tracked, since the system knows what the memory*means*and can thus give useful information about it (such as the name of the object that owns it).When a system shuts down it can quickly and efficiently free all of its memory.

Fragmentation problems are reduced.

It actively encourages good memory behavior. It makes it easier to do good things (achieve cache locality, etc) and harder to do bad things (lots of small memory allocations).

Buffer overflows will tend to overwrite data within the same system or cause page faults, which will make them easier to find.

Dangling pointer access will tend to cause page faults, which will make them easier to find.


I'm tempted to go so far as to *only* allow *whole page allocations* on the global level. I.e., a system would only be allowed to request memory from the global manager in chunks of whole system pages. Then it would be up to the system to divide that up into smaller pieces. For example, if we did the bullet example in C++, we might use one such chunk to hold our array of *Bullet* structs.

This has the advantage of completely eliminating external fragmentation. (Since everything is allocated in chunks of whole pages and they can be remapped by the memory manager.) We can still get address space fragmentation, but using a 64-bit address space should take care of that. And with this approach using 64-bit pointers is less expensive, because we have fewer individually allocated memory blocks and thus fewer pointers.

Instead we get internal fragmentation. If we allocate the bullet array as a multiple of the page size (say 4 K), we will on average have 2 K of wasted space at the end of the array (assuming the number of bullets is random).

But internal fragmentation is a *much nicer* problem to deal with than external fragmentation. When we have internal fragmentation, it is one particular system that is having trouble. We can go into that system and do all kinds of things to optimize how its handling memory and solve the problem. With external fragmentation, the problem is *global*. There is no particular system that owns it and no clear way to fix it other than to try lots of things that we hope might "improve" the fragmentation situation.

The same goes for out-of-memory problems. With this approach, it is very clear which system is using too much memory and easy to fix that by reducing the content or doing optimizations to that system.

Dealing with bugs and optimizations on a system-by-system simplifies things enormously. It is quite easy to get a good grasp of everything that happens in a particular system. Grasping everything happens in the entire engine is a superhuman task.

Another nice thing about this approach is that it is quite easy to introduce it on a system-by-system basis. All we have to do is to change one system at a time so that it allocates its memory using the page allocator, rather than the kitchen-sink allocator.

And if we have some messy systems left that are too hard to convert to this approach we can just let them keep using the kitchen-sink allocator. Or, even better, we can give them their own private heaps in memory that they allocate from the page allocator. Then they can make whatever mess they want there, without disturbing the other systems.

The main reason Go uses garbage collection from what I gathered is to make it easier for developer to use the goroutines (which can capture variables etc.) and channels as well. Without this, you would have to do a lot of memory management yourself. This choice makes a lot of sense with this in mind :)



ReplyDeleteI think the method you're referring to for memory management in C++ is RAII (http://en.wikipedia.org/wiki/Resource_Acquisition_Is_Initialization)

ReplyDeleteNorton.com/Setup is best antivirus available in the market. If you want to protect your system online or locally from any unforeseen events Norton is is a must have software in your PC or Mac. Activate your Norton.com/Setup to protect yourself ad your data from your system from malware and antivirus. Browse internet without any hesitation norton will take care of all malicious antiviruses floating all over internet.


ReplyDeleteOffice.com/Setup is a software which is used by almost all company and business and even by individuals For all their office activities or for personal use. It has excels, word, add ppt as their constituent are most widely used apps. For any concern and help just visit website for

Office.com/Setup help and key activation. You can do it by yourself if you know how to install office.com/Setup on your PC or Mac or you can call third party companies as well who can do it on your behalf.up.

Missable Items in Final Fantasy 7

ReplyDeleteConvert FLAC Audio to MP3

Viewed your Whatsapp Profile

Use Dark Mode on Your Mac

The detoxification time frame is hard for the individual experiencing liquor fixation since it is joined by extraordinary withdrawal side effects. These side effects negatively affect the patient both genuinely and intellectually. Hence, a liquor rehab focus additionally gives close patient checking and help during this period.


ReplyDeletebeating addiction quotes

drug addiction recovery quotes

happy marriage anniversary di and jiju




ReplyDeletehappy anniversary uncle and aunty

The primary concern you'll see when you pull up YesPornPlease is, you gotten it, a great deal of porn. The screencaps don't move when you coast over them, yet they're all new, capable shots from colossal studios. Brazzers, Mofos, BangBros, and RealityKings are just two or three the indisputable names on the main page. It may be free, anyway you're not getting off-brand bitches snapping dicks behind a 7-11 for meth money. This is the worthy stuff.

ReplyDeleteyespornplease

yespornplease

ReplyDeleteyespornplease

It's really an amazing article post great to get the relatives information through your website posts for all the people, I appreciate your efforts and suggtions. Thank you for sharing your knowledge and experience with everyone. australia assignment help -

ReplyDeleteAssignment Help Melbourne -

Assignment Help Perth

I will be looking forward to your next post. Thank you

ReplyDeleteเอ ศุภชัย ประชันความสวยมุมเดียวกับ อั้ม พัชราภา

I will be looking forward to your next post. Thank you

ReplyDeletewww.blogspot.com

This post was very amazing. Yellowstone stone

ReplyDeleteSuggest good information in this message, click here.

ReplyDeleteบอล ต่อ

เลข ใต้ดิน

google 1159

ReplyDeletegoogle 1160

google 1161

google 1162

google 1163

google 1164





ReplyDeletejoker123

ronmg dopo

Hello! This is my first visit to your blog! We are a group of volunteers and starting a



ReplyDeletenew initiative in a community in the same niche. Your blog provided us

valuable information to work on. You have done a marvellous

job! 바카라사이트

Iwas more than happy to find this site. 스포츠토토

ReplyDeleteI want

to to thank you ffor your time for this particularly

wonderful read!! I definitely savored every little bit of it and i also have yyou saved

aas a favorite to check out new stuff in your website.

토토사이트 Completely awesome posting! Bunches of helpful data and motivation, both of which we all need!Relay welcome your work



ReplyDeleteWhen I read your article on this topic, the first thought seems profound and difficult. There is also a bulletin board for discussion of articles and photos similar to this topic on my site, but I would like to visit once when I have time to discuss this topic. 먹튀검증업체I think it would be nice if you come to if you can solve my problem.




ReplyDeleteThis is very useful for me and I think your post is also useful for the world. Keep working hard if you want to advance in the future. Thanks again for the great post.

ReplyDeleteigoal88 กีฬา

토토사이트




ReplyDelete스포츠토토티비

토토

This is a very good article. I see the greatest contents on your blog and I extremely love reading them.

토토




ReplyDelete배트맨토토

배트맨토토프로

Thank you so much for ding the impressive job here, everyone will surely like your post.

I really enjoy reading and also appreciate your work.

Hello Everyone! I'm Ronald Frankeliene, an Online Dissertation Help expert who has been offering online Dissertation assistance for a long time duration. Many students have problems with their dissertations and are seeking help. If you're one of those who are facing the same issues, get in touch with us immediately. We have a team of experts to assist you in resolving your issue.


ReplyDeleteAs a heterosexual male, all you want is to body to body spa near me be touched by a female who can make you go crazy and at the same time gives you the best relaxing massage of all time.

ReplyDeleteFor sharing this, I'm grateful. Both of those things were true. So please accept my gratitude for the time and effort you spent producing this essay. By reading this post, you may check your click speed here for free without downloading any additional software. Click here for more information speed test 10 second.

ReplyDeleteThis comment has been removed by the author.

ReplyDeleteThese differ across nations and cultures body to body massage centres in hyderabad

ReplyDeleteand some are famous for their local experiences.

Stress Reduction: Mindful Massage induces female to male body massage in chennai a state of deep relaxation, reducing stress and anxiety.

ReplyDeleteIf "Rungu Massage" is associated with female to male body massage centres hyderabad a specific culture or tradition, it's important to approach it with cultural sensitivity and respect for its origins. Indigenous practices often hold deep cultural significance and should be honored in their proper context.

ReplyDeletePain and stress can also be associated to post surgery. A head massage can focus on decreasing pain and relieving emotions female to male massage at home near me of stress. A head massage can be used as an effective stress reliever after surgery or injury.

ReplyDeleteMental health can be divided into two massage parlour near me groups called "neurotic" or "psychotic". Neurotic mental health covers severe symptoms of "normal" emotions such as depression, anxiety or panic

ReplyDeleteConsent and boundaries are often female to male full body massage centres near me spoken about in tantric workshops and individual therapy sessions.

ReplyDeleteOnce I hop out, I feel an endorphin body to body massage in pune rush and am quickly awake and alert to start the day.”



ReplyDeletegood and female to male spa near me 24 hours entertaimenn

ReplyDeleteAre you feeling overwhelmed or tired, or just looking for a little pampering? Don't look any further! Our top female to male massage in chennai is designed to refresh your mind So, come and relax with our professional therapist

ReplyDeleteamazing postb2b massage near me

ReplyDeleteawesome

ReplyDeleteb2b massage spa near me

amazing

ReplyDeletemassage centres nearby me

I found this post incredibly helpful! Your advice is spot-on, and it’s exactly what I was looking for.

ReplyDeleteThank you so much for sharing this informative post. Really i got exact information what i was searching massage spa near me to know about our service.

ReplyDelete