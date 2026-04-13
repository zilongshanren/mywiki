---
title: Rate my API
url: http://c0de517e.blogspot.com/2014/06/rate-my-api.html
published: '2014-06-03'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Metal, Mantle, OpenGL's ADZO, GL|ES, DirectX 12... Not to mention the "secret" console ones. It's good to be a graphics API these days... And everybody is talking about them.

As I love to be "on trend" now you get my take on all this from hopefully a slightly different perspective.


To be honest, I initially wrote an article as a rant in reaction to the excellent post on

As I love to be "on trend" now you get my take on all this from hopefully a slightly different perspective.

To be honest, I initially wrote an article as a rant in reaction to the excellent post on

[modern OpenGL by Aras](http://aras-p.info/blog/2014/05/31/rant-about-rants-about-opengl/)(Unity 3d) but then after Metal and some twitter chats I became persuaded I should write something a bit more "serious". Or at least, try...


**- When is a graphics API sexy?**

Various smart people are talking with nice detail about the technical merits of certain API design decision (e.g. Ryg and Timothy's exchanges on OpenGL:

[original](http://timothylottes.blogspot.ca/2014/06/bindless-and-descriptors.html),[reply](http://fgiesen.wordpress.com/2014/06/01/bindless-chain-letter/),[re:re:](http://timothylottes.blogspot.ca/2014/06/bindless-chain-letter-re-bound.html)and[another one](http://timothylottes.blogspot.ca/2014/06/bindless-blog-chain-cached.html)) so I won't add to that right now. I want instead to cast these discussion in a different and to me more relevant point of view. What do we really want from a API (or really any piece of software)?
First and foremost will consider to adopt a technology if it's useful. It might seem obvious but apparently it's not. How many times have you seem projects that don't really work, yet spend time on aesthetic improvements?

Ease of use, documentation, great design, simplicity. All these attributes are completely irrelevant if the software doesn't do some compelling work. We can learn undocumented stuff, we can write our own tools, we are engineers and if there is something we need and there is a road open to obtaining it, we can achieve what we need. Of course we'd rather prefer not to endure pain, but pain is better than just not being able to do what we need to. Easy is better than hard, but hard is better than impossible.

Of course after we have something that does something we could be interested in, then if we'll adopt it or not depends on how much we want it divided how hard it is to achieve it. Cost/Benefit, unsurprisingly. To recap we want an API that is:

- Working. Is actually implemented somewhere, the implementation actually works. If it's written on paper but it's not reliably deployed, we can safely ignore its existence. This is actually part of "useful" or of the benefits, but it's important enough I'd like to remark it here.
- Useful. Does something that we need, in a market we're interested in. If I'm a AAA company and you make a great API that enables incredible graphics on a device that sold ten thousands units, that's not useful. If you provide a big speed improvement on a platform that is not performance bounds on my products, that's not so useful either. And so on.
- Easy. Do I need to change my entire engine or workflow to adopt this API? That's the most pressing question. Then it comes documentation and support. Then tools. Then in general how nice the API design is. APIs usually work in a realm that is well-separated from the rest of the software, if your API requires to sacrifice a (virtual) goat each time I have to call it, it's probably still not going to make all my project bad, it's not going to "spread". If the bad API design "spreads" to the engine or the entire software then that's changing the workflow, so it goes back to the first, most important attribute.

Now we can go through a few graphics API on the table these days and see how they fare (in my humble opinion) according to this (obvious but sometimes forgotten) metric.

**- OpenGL and AZDO**

OpenGL has a long history, once upon a time was winning the graphics API war, started to lose ground and by the time DirectX9 was around, pretty much all games switched (a good history lesson was

That didn't stop the

OpenGL took years to catch up with a variety of patches to DirectX11 (

[posted a while ago on stackoverflow](http://programmers.stackexchange.com/questions/60544/why-do-game-developers-prefer-windows/88055#88055)).That didn't stop the

[downward spiral](http://www.tomshardware.com/reviews/opengl-directx,2019.html), to the point that around the time DirectX11 came (2008, shipped with Windows 7 in 2009) even multi-plattform CG software (Maya, Max and the likes) moved to DirectX on Windows as the preferred frontend.OpenGL took years to catch up with a variety of patches to DirectX11 (

[g-truc reviews are awesome](http://www.g-truc.net/project-0032.html#menu)) and even longer to see robust implementation of these concepts. Still today the driver quality and the number of extensions supported varies wildly across vendors and OS ([some](http://www.g-truc.net/post-0655.html#menu)[examples](https://app.box.com/s/nrbuq10rra5cg955vkyj)[here](https://medium.com/@michael_marks/opengl-for-real-world-games-7d0f4d35891c)), ironically (and to make things worse) the platform where OpenGL has the best drivers across vendors today is Windows (that though doesn't even ship by default with OpenGL drivers but only an ancient OpenGL 1.1 to Dx layer) while OSX which is the best use-case for OpenGL in many ways, has drivers that tragically lag behind (but at least they are guaranteed to be updated with the OS!).
But,

[for all the faults it has](http://www.joshbarczak.com/blog/?p=154), today OpenGL is offering something very worth considering, which is what[cool people call AZDO](http://gdcvault.com/play/1020791/)(instance rendering on steroids): a way to reduce draw-call overhead by orders of magnitude by shifting the responsibility of working with resources from the CPU, generating commands that set said resources into the command buffer, to the GPU, that in this model follows a few indirections starting from a single pointer to tables of resources in memory.
To a degree AZDO is more a solution "around" OpenGL, rather than fixing OpenGL by creating an api that allows fast multithreaded command buffer generation, it provides a way to draw with minimal API/driver intervention.

In a way is a feat of engineering genius, instead of waiting for OpenGL to evolve its multithreading model it found a minimal set of extensions to work around it, on the other hand this probably will further delay the multithreading changes...

In a way is a feat of engineering genius, instead of waiting for OpenGL to evolve its multithreading model it found a minimal set of extensions to work around it, on the other hand this probably will further delay the multithreading changes...

Results seem great, the downside of this approach is that all other modern competitors (DirectX12, Mantle, XBox One and PS4 libGNM) allow both to reduce CPU work by offloading state binding to GPU indirection and support fast CPU command buffer generation via multithreading and lower-level concepts, which map to more "conventional" engine pipelines a bit more easily. There is also a question about if the more indirect approach is always the fastest (i.e. when dealing with draws that generate little GPU work) but that's yet up to debate (as AZDO is very new and I'm not aware of comparisons pitting it against the other approach).

**For AAA games**. Today for most companies this means consoles first, Windows second, anything else is much less important. For these games having more performance on a platform that is not the primary authoring one and that is not often a performance bottleneck, at the cost of significant engine changes doesn't seem attractive at all (and with no debug tools, little documentation and so on...), especially considering that DirectX12 is coming, an alternative that promises to be as good but easier, better supported and that will also target Xbox One, thus covering two of the three target platforms.

A notable exception though are free-to-play games hugely popular in Asia that are not only usually Windows exclusive, but where Windows XP is still very relevant, which means no DirectX11 and even less DirectX12. For these games I guess OpenGL could be a great option today.

Note also that AZDO is currently not fully supported on Intel hardware (no bindless, MDO software emulated) so you'll probably need a fallback renderer as well, as Intel hardware is quite interesting for games at the lower end.

Note also that AZDO is currently not fully supported on Intel hardware (no bindless, MDO software emulated) so you'll probably need a fallback renderer as well, as Intel hardware is quite interesting for games at the lower end.

**For applications**. Most CGI applications are the worst-case scenarios for GPU efficiency, they tend to do lots of draws with very little actual work (wireframe drawing, little culling) and in not very optimized ways as well due to having to work with editable, unoptimized data and often also carrying legacy code or code not thought to achieve the best GPU performance.

Also, shipping on multiple platforms is the norm while working across multiple vendors is less of a concern, NVidia has the golden share among CG studios and Intel is completely out of the picture, even only NVidia/Linux is probably a compelling enough target to consider "modern OpenGL there" and even more as Windows would benefit as well.

These things considered I would expect modern OpenGL to be something most applications will move towards, even if it might be a significant effort to do so.

These things considered I would expect modern OpenGL to be something most applications will move towards, even if it might be a significant effort to do so.

*Some more links:*

*APITest*[https://github.com/nvMcJohn/apitest](https://github.com/nvMcJohn/apitest)*Steam Dev Days - OpenGL presentations*[http://steamdevdays.com/](http://steamdevdays.com/)*Valve VOGL and TOGL*[https://github.com/ValveSoftware/vogl](https://github.com/ValveSoftware/vogl)[https://github.com/ValveSoftware/ToGL](https://github.com/ValveSoftware/ToGL)*Lottes on OpenGL texture binding*[http://timothylottes.blogspot.ca/2014/01/modern-opengl-texture-usage.html](http://timothylottes.blogspot.ca/2014/01/modern-opengl-texture-usage.html)*Opengl 4.4 reference card*[https://www.opengl.org/sdk/docs/reference_card/opengl44-quick-reference-card.pdf](https://www.opengl.org/sdk/docs/reference_card/opengl44-quick-reference-card.pdf)*Opengl 4 online searchable reference*[http://opengl.anteru.net/](http://opengl.anteru.net/)*OpenGL Superbible*[http://www.openglsuperbible.com/](http://www.openglsuperbible.com/)*Op**enGL Insights*[http://openglinsights.com/#menu](http://openglinsights.com/#menu)



**- Mantle**

AMD's Mantle is an clear example of a nice, good, easy API (exaggerated, but interesting praise

[here](http://www.joshbarczak.com/blog/?p=99)) that fails (in my opinion) to be really useful for shipped titles. On the technical level there's nothing to complain, it seems very reasonable and well done.**For AAA games**. Today Mantle works only on Windows with AMD hardware. That's a bit little, then again especially when DirectX12 is coming and AZDO is an alternative too. While it's most probably easier to deploy than AZDO (and I bet AMD is going to be willing to help, even if right now there might be no tools and so on), is also much less useful. Worse even if you consider that even on AMD hardware only certain CPU/GPU combinations are

[CPU limited](http://www.anandtech.com/show/7728/battlefield-4-mantle-preview).

It simply covers too little ground, I hoped at the beginning that AMD would come out sooner and with a PS4 layer as well, thus getting deployed by many projects that were looking for an easier way to target PS4 than figuring out libGNM. It didn't happen and that I think is the end of it. Some people were thinking it could have been a new cross-vendor standard, but it will -never- happen.

They did though score with Frostbite's support which pretty much means all EA games. But I would be very surprised if they didn't have to pay for that, and wonder how long it will last (as it's still a cost to support it, as it is supporting any platform)...

They did though score with Frostbite's support which pretty much means all EA games. But I would be very surprised if they didn't have to pay for that, and wonder how long it will last (as it's still a cost to support it, as it is supporting any platform)...

**For applications**. It's a bit more interesting there, as if you remove the consoles from your target then you're increasing the surface occupied by Windows. Also it's not unreasonable to think that Mantle could be ported on Linux. Unfortunately though NVidia is more popular than AMD for CG studios and that pretty much kills it.

**For the people**. There is something thought that needs to be praised a lot: AMD also has lots of great, public documentation about the working of its GPUs (Intel is not bad as well, NVidia is absolutely terrible, a sad joke) and tools that show the actual GPU shader working (i.e. shader disassembly) which is really great as it allows everybody to talk and share their findings without fearing NDAs.

This creates a positive ecosystem where everybody can work "close to the metal" and Mantle is part of that. Historically it just happens that the more people are able to hack, the most amazing things get created. See what happened after twenty years of C64 hacking (

I expect all graphic researchers to focus on GCN from now on.



[some](http://www.studiostyle.sk/dmagic/gallery/gfxmodes.htm)[examples](https://www.youtube.com/watch?v=pD234-SY_xg)[here](https://www.youtube.com/watch?v=cQNT9Whg4r4)).I expect all graphic researchers to focus on GCN from now on.

**- DirectX12**

It's hard to criticize DirectX11, especially if you consider that it was presented in 2008 and what was the state of the other APIs at that point. It changed everything, mapping better to modern GPU concepts, introduced Tessellation and Compute Shaders, looks great and easy, is reasonably well documented and supported, and it's very successful.

Arguably DirectX9 had better tools (VSGD is horrible AND they killed Pix that was actually working fine), but that's hardly a fault of 11 and rather due to the loss of interest in PC gaming, nowadays things are getting much better. Consider that only now we're starting really to play with Compute Shaders for example, because next-gen consoles arrived, but we had them for five years now! It was so ahead of time that it needed only rather minor updates in 11.1 and 11.2.

The only, big issue with 11 is that Microsoft wants to make things simpler than they really should be, for no great reason. So 11 shipped with certain "contracts" in its multithreading model that don't seem really useful or needed but hugely impacted the performance of multithreaded drivers to the point where multithreading is useful only if your application and not the driver is the bottleneck.

If your code is fast enough, multithreaded Dx11 will actually be slower than single-threaded, which is clearly an issue. I suspect it could still be technically possibly to carve "fast paths" for applications swearing not to exercise the API in certain ways but probably it was simply not important enough for the PC gaming market and now 12 is coming, probably just in time...

**For everything Microsoft**. DirectX won on windows and it also ships on Microsoft consoles. I can't comment much on 12 and it's not finished yet. Hardly it will be displaced on Windows though, especially for games.

**- Metal**

Metal is Apple's Mantle. On my very personal biased poll from the reactions I've read on my twitter feed, it has not been received with the same enthusiasm as AMD's initiative. Some explained to me it's because Mantle promised to be a multi-vendor API while Metal didn't. Oh Apple, outclassed at marketing from AMD, you don't know how to appeal the engineers, next time say it's designed to be open...

I've also seen many people complaining this is foul play designed only to create vendor lock-in, a mere marketing move. I don't agree, and if you think it's only marketing then you should prove that's possible to write an equally fast driver in today's OpenGL|ES.

I believe that's not technically possible and I believe OpenGL|ES is plagued by many of the same defects of desktop OpenGL, only much worse as it has no AZDO and it ships on platforms that are very resource constrained, so where performance and efficiency matters even more!

It would have probably been possible to carve fast-paths and patch ES with proprietary extensions that would have been a bit more friendly to the ecosystem (extension often get incorporated into the standard down the line), but if it reaches the point where most of the rendering would have gone through extensions what's the point, really?

Actually this might be for the best even for the overall ecosystem, as it's a bigger kick-in-the-nuts than everything else could have been, and when many vendors on Android are shipping drivers that are just the -worst- software ever and Khronos shows to be slow to evolve and ridden with politics, a hard kick is what's most needed.

It's very new as we speak and I haven't had an in depth look into it, so I might edit this section later on.

**For games**. iOS has still the golden share of mobile gaming, with many more exclusives and games shipping "first" of that system than the competitor, but the gap is not huge. Also, most games are still 2d and not too demanding on the hardware, so for a lot of people a degree of portability will matter more than a magnitude improvement in drawcall performance.

But, for the games that do care about performance, Metal is just great, iOS is big enough that even if your game is not exclusive, it's very reasonable to think about spending money to implement unique features to make your game nicer on it.

It's true that Metal won't be available on older Apple hardware but Apple has always succeeded in giving people reasons to update both their software and their hardware, so that's not probably a big concern.




Learn AZDO, play with Mantle, ship with DirectX.


If you're doing an indie title do use a rendering library or engine (I keep pointing at


If a market is interesting enough for a given application and the vendors there decide on their own API, like it's happening for Metal and happened for DirectX, I'd welcome that.


The problem with many of the APIs we're seeing is not that they divide the market, but that they try to do so in segments that are too small and uninteresting to specifically target. If for example Linux decided on its own 3d API for games I doubt that would be at all interesting...

If AMD shipped Mantle on consoles and PC then it could have been big enough of a segment to target, PC-only is not. If NVidia GameWorks offered a compelling solution on consoles, guess what, it would see a bigger adoption as well, while right now I suspect it will be used only on projects where NVidia is directly involved.


Most projects already have to ship with an abstraction layer of sorts, many of these are available, in practice the idea of using OpenGL directly to ship products across platforms doesn't exist (except for very small projects and some research code).

It's always best to have to write (or use via third-party libraries) lower-level code on things that we understand that have to fight with very opaque, wildly different implementations of a supposedly standard API.


In fact I bet that practically no (a very tiny number) gamedev knows even the basics of what a driver does and why certain API decisions led to slow CPU performance. Also the number of people not using third-party game engines especially for indie work is dwindling.


In theory a single API is better, in practice, today, it isn't and that's why the emergence of these low-level libraries is not just a marketing plot but actually a reasonable technical solution.

**- Conclusions**Learn AZDO, play with Mantle, ship with DirectX.

If you're doing an indie title do use a rendering library or engine (I keep pointing at

[https://github.com/bkaradzic/bgfx](https://github.com/bkaradzic/bgfx)but it's just an example) so you'll still ship with the best API for each platform and with the least amount of headaches. If you really love toying with the graphics API directly then I guess a flavor of OpenGL that is supported across platforms could be nice (3.3 if you care about Intel/Linux right now).If a market is interesting enough for a given application and the vendors there decide on their own API, like it's happening for Metal and happened for DirectX, I'd welcome that.

The problem with many of the APIs we're seeing is not that they divide the market, but that they try to do so in segments that are too small and uninteresting to specifically target. If for example Linux decided on its own 3d API for games I doubt that would be at all interesting...

If AMD shipped Mantle on consoles and PC then it could have been big enough of a segment to target, PC-only is not. If NVidia GameWorks offered a compelling solution on consoles, guess what, it would see a bigger adoption as well, while right now I suspect it will be used only on projects where NVidia is directly involved.

Most projects already have to ship with an abstraction layer of sorts, many of these are available, in practice the idea of using OpenGL directly to ship products across platforms doesn't exist (except for very small projects and some research code).

It's always best to have to write (or use via third-party libraries) lower-level code on things that we understand that have to fight with very opaque, wildly different implementations of a supposedly standard API.

In fact I bet that practically no (a very tiny number) gamedev knows even the basics of what a driver does and why certain API decisions led to slow CPU performance. Also the number of people not using third-party game engines especially for indie work is dwindling.

In theory a single API is better, in practice, today, it isn't and that's why the emergence of these low-level libraries is not just a marketing plot but actually a reasonable technical solution.

## 29 comments:

"Historically it just happens that the more people are able to hack, the most amazing things get created. See what happened after twenty years of C64 hacking (some examples here).



I expect all graphic researchers to focus on GCN from now on."

I don't think that applies to 3D graphics. C64 hacking is done for fun, not because the demos and games they make are actually remotely competitive with any modern platforms.

Likewise, yes you can try to learn GCN inside-out and hack away at it... but by the time your understanding of the architecture is good enough to actually do something useful with it, GCN will long have been rendered irrelevant by newer, much more powerful architectures, which break all the rules you were trying to learn about GCN in the first place.

I don't think so, you would be surprised how much people can hack GPUs, figuring them even better than the vendors themselves...




Part is because the community is big and there is a lot of interest, part of it is because GPUs are less "settled" in terms of architecture compared to CPUs so many details are not too predictable, vendors know that they can expert certain improvements when doing certain changes but often the best possible paths and performance characteristics are not that easy.

As for the time concerns, a console generation is not that short, there is plenty of time. Even for vendors that are not on consoles certain things carry over from a GPU to the next.

Also consider that apart from AMD all other vendors don't even show the actual GPU code generated from shaders by the drivers, so you're basically coding very high performance loops in a language a few translations steps apart from the hardware...

"As for the time concerns, a console generation is not that short, there is plenty of time."






We're not talking about consoles here. Consoles have their own APIs anyway. We're talking about how useful it is to have something like Mantle on PC, and studying the GPU at a low level.

"Also consider that apart from AMD all other vendors don't even show the actual GPU code generated from shaders by the drivers, so you're basically coding very high performance loops in a language a few translations steps apart from the hardware..."

This is done for a good reason: so that you don't paint yourself into a corner, the way it happened with x86 for example.

By keeping an abstraction layer between application code and GPU, you can easily change the GPU architecture underneath.

Just figure: AMD's initial DX11 architecture wasn't very good... they had to move to GCN quite recently, to have an architecture that is more in line with nVidia's Fermi and newer derivatives.

GCN is VERY different from their earlier architectures... And I think it's naive to think that GCN is the 'final' GPU architecture, and no big changes will ever come to GPU architectures again.

Quite the contrary, I'd say... if you look at PowerVR for example... Firstly they are doing things differently anyway, with their TBDR... Secondly, they're adding raytracing to the mix.

On consoles you can get away with studying the GPU's internals, because you know the console will be on the market for many years, and the effort pays off.

But on PCs, it doesn't pay off to spend a few years studying and optimizing for one specific GPU. Firstly because there are 3 major GPU vendors on the market anyway... Secondly, because the update cycle of PC hardware is faster than that of consoles.

Thanks, I'm very uninformed in this, so it's good to get some perspective. One thing I would add regarding Metal though:








I get the impression (no proof) that the majority of iOS games are built with engines from vendors. Obviously Unity, but also Apple's Sprite Kit & Scene Kit, and then many others such as Corona & open source options, etc.

So, a studio wanting to ship a cross platform mobile game will want to author in their favourite tool.

Engine vendors want to make their solution as attractive as possible. That means consistency over platforms, and also getting the best performance on platforms.

It seems to make a lot of sense for them to provide backends that utilise the low level drivers available on each platform.

I think it is very likely that Unity will update their iOS engine to use Metal, and all the Unity games that ship on iOS will benefit.

I'd go as far as saying that Metal was primarily developed for Unity and for Apple's internal use in driving the iOS (and perhaps OS X) interface.

Other users are crowdsourced bug hunters :-)

Does Metal have yet another shader language? :(

> even multi-plattform CG software (Maya, Max and the likes) moved to DirectX on Windows as the preferred frontend.






In the case of Maya the only reason involved for a DirectX viewport is to allow video game vendors to work with their shaders directly in viewport (mainly for asset visualisation).

The graphic API is not the problem here.

FYI.

Regards,

Dorian

Scali, the point IMHO is that as long as the consoles will be around, then GCN will be relevant, even on PC.





If on PC they switch architecture (and AMD won't, it would be a stupid decision to do so) still graphic researchers should stick to GCN so their results are directly interpretable on the console platforms (and they won't be worse for PC as there most vendors are opaque anyways)

About the good reasons to avoid assembly. There might be good reasons to not have people directly write assembly, but there are ZERO good reasons to avoid people -see- the generated assembly so they know what they are doing with their code!

And it's not a matter of spending a few years to understand a PC GPU, that would surely help and as I wrote, because of the consoles you can be sure at least GCN will be well studied, but even for a non-console architecture being as opaque as vendors are these days means that you could be doing absolutely stupid things for their HW and you'll never know unless they send their support guys to analyze your application with their proprietary tools... Which is often bad anyways because it happens at the end of a project when you already made all the design decisions (blindly) and changing stuff might be hard...

"Scali, the point IMHO is that as long as the consoles will be around, then GCN will be relevant, even on PC."














Apparently we don't agree on that.

"If on PC they switch architecture (and AMD won't, it would be a stupid decision to do so) still graphic researchers should stick to GCN so their results are directly interpretable on the console platforms (and they won't be worse for PC as there most vendors are opaque anyways)"

I don't get this. Firstly, why would it be a stupid decision for AMD to switch from GCN to something newer? Clearly GCN is not the ultimate architecture, so it would be stupid to stick with that when newer, better architectural ideas come around. And they will, soon.

As for consoles... How do consoles make outdated videocards relevant on PC? GCN already has a very small marketshare on PC today anyway (about 17% of all DX11-capable cards are GCN).

When newer cards arrive, this will only get smaller. Why develop for such a small subset of the total market? Especially if you're not even interested in consoles (as this post is NOT about consoles, but about APIs on PC and smartphone).

"About the good reasons to avoid assembly. There might be good reasons to not have people directly write assembly, but there are ZERO good reasons to avoid people -see- the generated assembly so they know what they are doing with their code!"

As I say: it is irrelevant.

Just like nobody will check the native code that Java or .NET will generate for their CPUs. You just profile and optimize your code at a higher level, where it makes a lot more difference anyway.

"And it's not a matter of spending a few years to understand a PC GPU, that would surely help and as I wrote, because of the consoles you can be sure at least GCN will be well studied, but even for a non-console architecture being as opaque as vendors are these days means that you could be doing absolutely stupid things for their HW and you'll never know unless they send their support guys to analyze your application with their proprietary tools..."

You're looking at it the wrong way.

D3D and OpenGL are standardized ways to access GPUs.

It is not our job to try and figure out how to shoehorn these APIs into their GPUs.

It is their job to design GPUs that handle these APIs in an efficient and intuitive way.

It doesn't make sense to design a GPU that suddenly works completely differently from everything that went before. That would also mean that all legacy applications would be unoptimized for this architecture.

The same goes for x86. Pentium 4 was not all that bad if you hand-optimized assembly for it. But it was horrible at legacy-code which was mostly optimized for Pentium or Pentium Pro/II/III.

That's what made the Pentium 4 a bad CPU.

The same goes for AMD's Bulldozer/etc architecture now. You may be able to get reasonable performance out of it if you hand-tune your code for this specific CPU, but it is horrible at legacy code.

And since the majority of CPUs on the market need different optimizations, new software generally won't get optimized for Bulldozer either.

I hope this opens your eyes somewhat. A PC is not a console, and should not be treated as such. A PC is a device that speaks x86 and D3D/OGL, and CPUs and GPUs should be designed to handle x86 and D3D/OGL code as efficiently as possible.

"It doesn't make sense to design a GPU that suddenly works completely differently from everything that went before. That would also mean that all legacy applications would be unoptimized for this architecture."



I'd like to clarify that "works completely differently" means different optimization rules in this context.

It's fine to have a GPU that works completely differently under the surface, as long as it is still efficient at running existing code as well (such as how the GeForce 8800 was a completely different architecture from earlier DX9 cards, yet it was more efficient at running DX9 code as well... or GCN being better than the VLIW-based architectures that AMD used before).

So do not interpret this as "AMD should stick with GCN", obviously.

"Firstly, why would it be a stupid decision for AMD to switch from GCN to something newer?"






Because 99.99% of the AAA games happen on console first today, and AMD won big by having its GCN chip on both XBox and PS4 (and WiiU has some similarities too).

By keeping the architecture consistent they will keep reaping benefits as console games are cycle-optimized on their GPUs, thus PC ports will similarly be much much more optimized for their hardware for free. If they diverge then even if they keep all the documentation open for the new architectures, optimizing for them will need different code paths and time and money, which very rarely today is something that AAA devs do for PC ports.

Basically if they stick with GCN-ish architectures on PC they will get console-like efficiency for free, which is a super smart thing to do. They should over and over again try to capitalize on PC the power they have on the consoles, e.g. making all sort of GCN middleware that can be "sold" because of the consoles but goes "for free" on PC as well...

"Just like nobody will check the native code that Java or .NET will generate for their CPUs."

If you write in Java or .NET a kernel that is run on millions of data points, like shaders are, and you don't care about cycle-optimizing it, it's your problem. FWIW I remember when we were doing Java demos a long ago, we did know how the (at that time Microsoft) JVM did translate code. Like today if you're writing performance-sensitive code even in JS you should (and people -do-) know how the various JS engines execute code.

If you don't it's your decision, for sure it's false that "nobody" does because at least -I- do and people in the companies I've worked in -do- and I can tell in actual shipped games, having that low-level knowledge of a GPU does make a difference. Full. Stop.

"You're looking at it the wrong way."

No I'm not. That's how I work. You're free to work in a different way.

"It is not our job to try and figure out how to shoehorn these APIs into their GPUs."

It's my job (when I am in charge of optimization) to make my game as fast and smooth as possible when it ships on the target platforms that it ships. That's the reality of things, it's not that if your game runs at 1fps because it's hitting a slow-path in the driver or GPU then you just cross your arms and say, I'm writing wonderful DirectX code, it's the GPU and drivers that sucks. Or -you- are free to do it, but if that attitude shows from someone working on my projects I won't be happy.

"It is not our job to try and figure out how to shoehorn these APIs into their GPUs."

It's my job (when I am in charge of optimization) to make my game as fast and smooth as possible when it ships on the target platforms that it ships. That's the reality of things, it's not that if your game runs at 1fps because it's hitting a slow-path in the driver or GPU then you just cross your arms and say, I'm writing wonderful DirectX code, it's the GPU and drivers that sucks. Or -you- are free to do it, but if that attitude shows from someone working on my projects I won't be happy.

"I hope this opens your eyes somewhat."


Such arrogance is unwelcome here, keep it out of my comments section please.

"Because 99.99% of the AAA games happen on console first today, and AMD won big by having its GCN chip on both XBox and PS4 (and WiiU has some similarities too)."












The PC world moves a lot faster than the console world.

The GPU architectures used in the XBox 360 and PS3 did not remain relevant for very long on the PC either. They were replaced almost immediately by DX10-capable architectures (which were so much faster and more efficient that no amount of optimization would make any DX9-architecture come anywhere close). GCN isn't anything special, so I see no reason why it should stick around longer than the average architecture does on PC. Note also that GCN was already on the market for 2 years before the consoles launched.

"Basically if they stick with GCN-ish architectures on PC they will get console-like efficiency for free, which is a super smart thing to do."

No, it is a mega-stupid thing to do when your competitor comes out with a much more efficient architecture (which they will).

An outdated architecture with 'console-like efficiency' will not be able to match a state-of-the-art architecture with regular D3D/OGL efficiency.

"FWIW I remember when we were doing Java demos a long ago, we did know how the (at that time Microsoft) JVM did translate code."

I've written software renderers in Java myself, and I did know how they translated code.

I also know that it's rather useless to try and tweak it for a specific CPU, especially when it is your goal to run on all available CPUs.

"That's the reality of things, it's not that if your game runs at 1fps because it's hitting a slow-path in the driver or GPU then you just cross your arms and say, I'm writing wonderful DirectX code, it's the GPU and drivers that sucks."

That depends... In the case of GeForce FX the GPU *did* in fact suck. It was my choice to not try and bother with SM2.0 at all on those things.

Sure, if I would get paid enough, I could cook up a specially optimized path for it... but since that didn't happen, I just didn't target the card. If people thought it was too slow, just run an SM1.x path on it.

The problem quickly solved itself when nVidia's next generation was as good at running SM2.0 code as ATi's hardware was.

"Such arrogance is unwelcome here, keep it out of my comments section please."

It was not meant as arrogance. I am merely pointing out that you have a one-sided view on the situation (and very console/AMD-centric at that).

I'm saying that CPUs and GPUs are disposable. Yes, I've studied more CPU and GPU architectures than I care to remember, and coded them on the bare metal and all that... But in the long run it doesn't get you much.

Bad CPU/GPU architectures will be replaced with good ones soon enough, and in the long run, the only code that is really worth the effort is the 'generic' x86/D3D/OGL code path that runs well on a wide variety of hardware, rather than those few niche-optimizations for a small subset that is rendered irrelevant within a few years anyway.

I guess I should clarify that despite the AMD APUs in the consoles, nVidia GPUs are still out-selling AMD GPUs by about 2:1, and only a very small subset of the installed base of DX11-capable (or even DX12-capable GPUs, since Fermi+ supports DX12) is GCN-based.



So GCN is only about 17% of all DX11-GPUs today, and it is not likely to suddenly tip into AMD's favour in the near future (especially with such cards as the GTX750Ti, which really hit the performance/watt and bang-for-buck sweet spots).

I'd rather spend most of my time getting the code to run as well as possible on the other 83% first.

Let's face it, even if you have a console-optimized version of your code, it's only going to take you so far, because your code will be tuned specifically for the performance level and memory capacity of the console. PC cards may be based on the same GCN architecture, but because of all the variation in CPU and GPU parameters, there's no single catch-all path in terms of efficiency.

"No, it is a mega-stupid thing to do when your competitor comes out with a much more efficient architecture (which they will)."

You are assuming it's impossible for the years to come to make GPUs that competitive while keeping the same set of fast-paths as current GCN. Note that you don't have to keep exactly the same design at all, just make sure that whatever was optimal on GCN stays optimal or still among the best solutions for a task on the new architecture and you'll still reap the benefits of having engineers cycle-optimize for the console GCN.

"I also know that it's rather useless to try and tweak it for a specific CPU, especially when it is your goal to run on all available CPUs."

Which is not the goal of a game, the goal of a game is to run the best on the (popular, targeted) architectures available when it ships.

"Bad CPU/GPU architectures will be replaced with good ones soon enough"

Soon enough is irrelevant, when a game comes out it has to work great at that point in time, not after some years. So you want it optimized as much as possible right there and then if even the optimizations are not too valid for the new generations of GPUs it doesn't matter much also because raw power will eat that efficiency gap.

"Yes, I've studied more CPU and GPU architectures than I care to remember, and coded them on the bare metal and all that... But in the long run it doesn't get you much."

I guess what you "studied" is not what I saw at all, because in the world I live and shipped game on, you could get order-of-magnitude improvements by just minor changes in the code paths, minor changes that though are hard to do if you don't know exactly how the architecture you're coding on works.

Take GCN that has public documentation, there you see you have a quite limited number of shader registers (vgpr/sgpr), very small changes to a shader (one more sampler for example) can bump it into the next occupancy level and significantly degrade performance, so you would in general know to pay attention to said resources. And that by the way has been a AMD design constraint since forever, well before GCN, while NVidia doesn't work the same way.

So here it's a simple example of a small detail that makes a huge difference in performance and has been constant for more than seven years now? And that's just a simple example, the only one I could think of right now that doesn't infringe any NDA.

But if you still think you're right go ahead, keep doing what you're doing and I'll keep doing what I'm doing, it's not that I want to persuade you to work like me, nor I pretend to open your eyes.

"You are assuming it's impossible for the years to come to make GPUs that competitive while keeping the same set of fast-paths as current GCN."
















Now you're turning it around. You're assuming that it is impossible for a new architecture to render GCN irrelevant overnight.

I'm saying I'm not putting all my eggs in one basket, certainly not the GCN-basket, with such small marketshare.

"and you'll still reap the benefits of having engineers cycle-optimize for the console GCN."

Is that even true anyway? I mean, from what I know of Mantle, it just uses HLSL as the shader language. So there won't be any shader-level optimizations that you can't just use in vanilla D3D anyway.

The gains of Mantle are on the CPU-side. It's not making the GPU render faster, it's just trying to reduce the idle time between rendering.

Something that is much less relevant on PC than on consoles anyway... and DX12 will also offer these things, but on all architectures/vendors, instead of just GCN/AMD.

"the goal of a game is to run the best on the (popular, targeted) architectures available when it ships."

I disagree. Yes, I meant popular/targeted available architectures... but not just at shipping time, also in the future.

I don't want to write yet another Glide-game which people won't be able to run in 5 years time, because no hardware supports Glide anymore.

"Soon enough is irrelevant, when a game comes out it has to work great at that point in time, not after some years. So you want it optimized as much as possible right there and then if even the optimizations are not too valid for the new generations of GPUs it doesn't matter much also because raw power will eat that efficiency gap."

Problem is when it takes a few years to develop the game. The hardware available at the start of development is not the same as time of shipping.

Aside from that, as I say, I'm not one to write 'disposable' code. I prefer a bit of longevity.

Perhaps you and I are just working in slightly different industries... Or perhaps you are just in the 'Gaming Evolved' programme? In which case there's no point in discussing in the first place.

"I guess what you "studied" is not what I saw at all, because in the world I live and shipped game on, you could get order-of-magnitude improvements by just minor changes in the code paths, minor changes that though are hard to do if you don't know exactly how the architecture you're coding on works."

'Order-of-magnitude'... that's quite a stretch.

Perhaps you should give some real-world examples of such then...

Because I can name various examples where knowing things about the architecture matters... But in most cases, most of the gains come from high-level optimizations, such as choosing the right algorithms, ordering your data the right way, and that sort of thing.

I haven't seen order-of-magnitude gains on strictly architectural level optimizations, ever.

Not even Geforce FX was 'orders of magnitude' faster when you replaced float code with int code (which doesn't even count as an optimization, but rather as moving the goal posts), and that is one of the most extreme examples I can think of (driver bugs aside... but I don't count those since I just report those and have them fixed in a few weeks time usually. Working around driver bugs has nothing to do with CPU or GPU architecture anyway).

"So here it's a simple example of a small detail that makes a huge difference in performance"

'Huge'? 'Orders-of-magnitude'?

You're being completely unrealistic here. Yes, you get a speed hit, but it's not super-dramatic.

"But if you still think you're right"

If this is just about being right or wrong for you, you're talking to the wrong person.

It seems that an in-depth technical discussion is too much to ask for.

By the way, you also ignored my earlier statement:



"Let's face it, even if you have a console-optimized version of your code, it's only going to take you so far, because your code will be tuned specifically for the performance level and memory capacity of the console. PC cards may be based on the same GCN architecture, but because of all the variation in CPU and GPU parameters, there's no single catch-all path in terms of efficiency."

You still reiterate: "you'll still reap the benefits of having engineers cycle-optimize for the console GCN."

If you're really so knowledgeable of CPU and GPU architectures, you know that cycle-optimizing only holds for a very specific configuration. For example, some GCN-based cards have much more shader capacity than the consoles, and relatively little memory bandwidth... Others may have relatively high bandwidth compared to their shader power... Etc.

So as I already said, your cycle-optimized console isn't a catch-all solution on PC.

But I'm sorry if I'm trying to make the discussion technical again.

Why are you talking Mantle now? I wrote already in the article that Mantle is good to study, not to use, so.




If you were talking about Mantle all this time, sorry, we were not on the same level, I was just talking about GCN being open and AMD giving tools to look at assembly and so on.

"It seems that an in-depth technical discussion is too much to ask for."

Nothing you said is in my eyes and "in-depth technical discussion". Sorry.

"some GCN-based cards have much more shader capacity than the consoles, and relatively little memory bandwidth... Others may have relatively high bandwidth compared to their shader power... Etc.











So as I already said, your cycle-optimized console isn't a catch-all solution on PC."

Of course not but it still makes a big difference not falling in the weaknesses of a given architecture.

An optimized console GCN code might be not 100% the -best- way of doing things on a given PC GCN card but it will be much closer to be efficient than code running on an opaque architecture of which you know nothing about.

Many design decisions do carry over and do stay constant even after years, I already made a specific example, do you want more? Just some random examples on top of my head:

- Geometry shaders. AMD and NVidia implement them in quite different ways which matter for performance in ways that are constant among all their cards

- VS Interpolators. Is it better to pack, compress vertex outputs and pay a price to decompress it on the PS or not (e.g. is it better to compute the bitangent in PS or pass it along?

)? Architecture dependent again. Also applies to VS inputs and constants.

- Constant indexing, how is it implemented in shaders?

- What does disable early-Z? Early-Z makes an order-of-magnitude difference and the conditions under which is disabled are architecture dependent

- How is Z/Stencil and early-z/early-stencil packed? What causes compressed Z to be decompressed? Is it better to read the Z or to emit a copy in a MRT? If reading Z forces a decompress and then you keep rendering into the decompressed Z you get a big performance hit

I get the impression that either you're trolling or you really don't know how much understanding the GPU under your API matters.



Either way I'm wasting too much time on this.

Bye.

"Of course not but it still makes a big difference not falling in the weaknesses of a given architecture."










Yes, obviously.

However, that is done by profiling your code more than studying assembly. Looking at the assembly won't tell you how efficiently the code is being executed.

"it will be much closer to be efficient than code running on an opaque architecture of which you know nothing about."

This seems to be the problem in our communication here.

To me, "not being able to look at the native assembly" is something completely different as "not knowing anything about the architecture".

All vendors publish lots of presentations and other documentation on how to optimize for a given architecture or how to best use an API.

"I already made a specific example, do you want more?"

I want an example that actually makes "orders of magnitude" of a difference, with actual code so I can verify your claims on real hardware.

But I think we both know that your claims were WAY overestimated here.

"I get the impression that either you're trolling or you really don't know how much understanding the GPU under your API matters."

And you call me arrogant? You're the one who put a link to my blog in your article the first place, trying to use it to support your point in a way I don't agree with (see my first comment).

If you read my blog, you should have an idea of how deep my understanding of hardware and APIs goes.

"All vendors publish lots of presentations and other documentation on how to optimize for a given architecture or how to best use an API."




But I'd like to elaborate on that, getting back to what I said earlier:

For PCs, a 'good' GPU is one that runs a wide range of existing software efficiently.

This implies that all GPUs should follow roughly the same optimization rules. Which implies that you don't need to study GPUs in all that much detail in general (just like how in the x86-world, with the exception of the Pentium 4, the same rules of optimization that applied for Pentium Pro, mostly still apply for the latest Core i7's today).

There are some exceptions... One that I covered on my blog was the difference in tessellation performance between Fermi and Evergreen/Northern Islands for example.

But that's not a case of optimization: the AMD cards simply weren't good at tessellation, regardless of how much you wanted to optimize your code.

So it all just boiled down to having AMD cards run at a lower tessellation setting than nVidia cards.

Scali: The consoles count. This is the big truth. Learn how GCN works is a must, because this will lead to better games on XO and PS4.


I think Mantle is a good tool to learn what's possible on GCN. Personally I'm amazed how much better this architecture, than anything I worked before.

While I may not use Mantle on PC, it is definitely help me to understand the next era of graphics.

Mantle will help the PC industry. It is much harder to make a Triple-A game with D3D/OGL, then doing some fancy graphics stuff. With the low-level push we may port our next-gen game to PC in the end of 2015.

This is largely a business related thing. We don't have reasource and time for doing a PC port to D3D11/OGL. But D3D12/Mantle is so much elegant that it will give as a chance to achieve our performance targets much sooner and much easier than an older API.

"Scali: The consoles count. This is the big truth. Learn how GCN works is a must, because this will lead to better games on XO and PS4."






Consoles count when you're developing for consoles. But this article is about APIs on PC and mobile platforms, not consoles.

It's pretty obvious that games targeting a particular console are optimized for that console. That's the whole point of consoles: fixed hardware, relatively long life.

"While I may not use Mantle on PC, it is definitely help me to understand the next era of graphics."

GCN is 2.5 years old, it's 'last era', not 'next era'.

"Mantle will help the PC industry. It is much harder to make a Triple-A game with D3D/OGL"

How exactly is Mantle going to help? You still need to write D3D/OGL code because the majority of the hardware (including AMD's own DX11 hardware) does not support Mantle.

"Scali: Consoles count when you're developing for consoles. But this article is about APIs on PC and mobile platforms, not consoles."





It doesn't matter. Everybody who I known research new things for the consoles, and then port them some way to PC (and mobile if possible).

"GCN is 2.5 years old, it's 'last era', not 'next era'."

GCN is a very forward looking architecture. It's a very good concept what should be a GPU in the next era. Personally I think every vendor will follow this road.

"You still need to write D3D/OGL code because the majority of the hardware (including AMD's own DX11 hardware) does not support Mantle."

Who will finance it? Because our publisher won't. So I just want to write a code for D3D12, and maybe Mantle for Linux. It won't run on every hardware, but the port will be cheap. The big money is in the consoles, so the PC is just an extra.

"Personally I think every vendor will follow this road."


Actually, GCN is basically AMD changing to a more Fermi-like architecture, if anything.

So nVidia was already on this road before AMD was (which is also why nVidia will have a much larger installed base for DX12).

Please don't turn this comment section in a AMD vs NVidia vs Intel war.



I will delete posts if this gets into a flamewar (and arguably it might already be).

Scali: I removed the link to your blog and linked directly to Anandtech. Bye again.

Metal Shading Language is interesting because






it has taken OpenCL and added graphics

shadeers and textures.

and put it in c++11.

It uses LLVM to speed and pre-comiple.

It has vector and matrix maths.

So in a way Apple has updated OpenCL with graphics, hidden the targeting of multiple cpu and gpu. hidden the C cruft.

So this could be the future of OpenCL if industry chooses to it.

On the other hand, looking at Mantle

number AMD posted in their blog,

I see 40% gain FPS for CPU bound games, 30% gain for dual GPU systems and only 10% gain for GPU bound games.

Post a Comment