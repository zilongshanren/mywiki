---
title: 'Classic Tools Retrospective: The birth, death, and re-birth of Gamebryo 2'
url: https://www.gamedeveloper.com/audio/classic-tools-retrospective-the-birth-death-and-re-birth-of-gamebryo-2
author: David Lightbown
published: '2020-05-01'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Classic Tools Retrospective: The birth, death, and re-birth of Gamebryo 2

David Lightbown talks to Dan Amerson, Mike Daly, John Austin, and Tim Preston about the Gamebryo engine and tools. This article traces its history from NetImmerse, the Gamebryo rebranding, merger with Emergent, Lightspeed, and acquisition by Gamebase.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

# Introduction

In recent years, retrospectives of classic games have been well received at GDC, but there have been very few stories about classic game tools. This series of articles will attempt to fill that gap, by interviewing key people who were instrumental in the history of game development tools.

The first three articles in this series have featured [John Romero (about the TEd Editor)](https://www.gamasutra.com/blogs/DavidLightbown/20170223/289955/Classic_Tools_Retrospective_John_Romero_talks_about_creating_TEd_the_tile_editor_that_shipped_over_30_games.php), [Tim Sweeney (about the Unreal Editor)](https://www.gamasutra.com/blogs/DavidLightbown/20180109/309414/Classic_Tools_Retrospective_Tim_Sweeney_on_the_first_version_of_the_Unreal_Editor.php), and [Chris Norden (on tools for the original Deus Ex)](https://www.gamasutra.com/blogs/DavidLightbown/20181023/328687/Classic_Tools_Retrospective_The_tools_that_built_Deus_Ex_with_Chris_Norden.php).

For the fourth article, I am very excited to speak to Dan Amerson, Mike Daly, John Austin, and Tim Preston about the history of the Gamebryo game engine.

# Roundtable

John Austin joined NDL – the company that would go on to produce the Gamebryo engine – in 1998, at a time when they had only four customers. He was brought in as VP of engineering to give structure to the team.

Tim Preston joined NDL in 1999, initially working on the Mac port of the engine. After a short stint in particles and animation, he moved over to rendering, and was lead on the DirectX renderers and PC platform.

Dan Amerson joined in 2001. He worked as a Gamecube lead, Xbox 360 lead, and eventually technical director for rendering and runtime.

Mike Daly joined in 2004, right out of college. He met Dan while he was going to NC State. He started off working on exporters, and then worked on the toolchain.

![](../../assets/2df3ea662a69a8e1.img)


# RayTracing a path to the birth of NDL

The story of Gamebryo starts in the early 1980s.

In December of 1983, J. Turner Whitted and Robert Whitton founded Numerical Design Limited, or NDL. The company was based out of Chapel Hill, North Carolina, primarily staffed by grad students from the UNC Computer Graphics program.

Whitted was responsible for introducing recursive ray-tracing to the computer graphics world via a paper that he wrote in 1979, entitled “An improved illumination model for shaded display”.


![](../../assets/a301b83078a931a6.img)

![](../../assets/a74c01ed506081df.img)


Turner Whitted and a render from his 1979 paper


NDL’s first product was an off-line rendering engine called Rendition, and the main customer was AutoCAD. At that time, Autodesk was paying most of the bills.

In the 1990s, the first wave of VR started coming, and Intel had a real-time graphics software called 3D Worlds. They licensed it to NDL and, at the same time, invested in NDL through a convertible note. At that time, the graphics technology was known as NetImmerse.

![](../../assets/bd9e69a7037f2a26.img)

![](../../assets/13117db9048c3fa6.img)


The first few customers who used the NetImmerse real-time graphics engine were Prince of Persia, released in 1999, and Dark Age of Camelot released in 2001. NetImmerse was only a graphics engine at that time, and so everything else aside from the graphics engine was made by the developers who licensed NetImmerse.


# The Bright Age of MMORPGs

Due to the success of Mythic Entertainment’s “Dark Age of Camelot”, NetImmerse started to become associated with real-time MMORPGs, which – with the success of Ultima Online, Everquest, and Asheron’s Call – were very popular at that time.

This is ironic, as NetImmerse was purely a graphics engine, and had nothing to do with the networking code that made massively multiplayer games a reality. In the case of Dark Age of Camelot, Mythic Entertainment wrote all the networking code.

![](../../assets/72457e82cef0857b.img)

![](../../assets/6de1e2fb7dfaaaf5.img)


It’s possible that the word “Net” in “NetImmerse” had an influence on this. John says that “we had nothing to do with the multiplayer aspect of [Dark Age of Camelot]. All we were at that point was a graphics engine, but because that game happened to be in that genre, we picked up a bunch of customers in that space.”

Not only was it simply a graphics engine, but there were no editors at that point either. However, NetImmerse did come with a suite of very capable exporters.


We had nothing to do with the multiplayer aspect of [Dark Age of Camelot]. All we were at that point was a graphics engine, but because that game happened to be in that genre, we picked up a bunch of customers in that space



# Bringing an exporter to a .NIF fight

NetImmerse used the proprietary NIF file format. NIF files could be created using the exporters that came out of the box. Compared to the competition at the time, the exporters were quite capable. “Our exporters were probably the most fully featured in the industry and they did their best to make sure that what you saw in your 3d tool was exported into the engine”, Dan said.

They also included the ability to mark up your scene with game-specific information, which would allow you to downsize textures, set culling settings, and so on.



One of the factors that contributed to the quality of the exporters was that the team had set up an automated process where the exporters would export assets to PC, Playstation, and Xbox overnight, and then compare the results to test images to make sure that they kept their fidelity as closely as possible.

It’s worth noting how unusual it was to have powerful exporters out of the box in those days. There was no common interchange format, and DCC tools – such as 3ds max, Maya, and Softimage – were not architected to have exporters. “It was a non-trivial task to get data out of them at that time”, Mike added.


The exporters were very appealing to a large number of customers. Being able to use the DCC tools that everyone was already familiar with was one of the strong selling points of NetImmerse



It was worth it, though, because the exporters were very appealing to a large number of customers. Being able to use the DCC tools that everyone was already familiar with was one of the strong selling points of NetImmerse, and that continued to be the case for many years.


# ABC, Always Backwards Compatible

Backwards compatibility was also an important consideration for people working on NetImmerse. It did take some people time to come around to the idea, though.

“When I was the young guy in the company, I was the one arguing that we need to just ditch the backwards compatibility and have people re-export.” Dan said. “Then, I got on the ‘we have to be backwards compatible’ train because Tim convinced me that we have to, then Mike joined the company he was like ‘can we just make them backwards compatible?’ [laughs]”

A lot of energy was spent making everything backwards compatible. As a testament to the work that the team put into it, some NIF files from NetImmerse 1 could still be loaded into Gamebryo Lightspeed, over 10 years later.

It didn’t always work, though. Tim said, “We did break it once somewhere on NetImmerse 2 and that made [Mythic Entertainment] very unhappy, because they had a whole bunch of assets that they had already exported, and they didn’t have the master files for them anymore. They went back and wrote a NIF converter for that specifically. After that, we would deprecate features now and again, but we would always make sure that there was a NIF converter”

![](../../assets/2356ceaed3e7afb1.img)


Dan is fourth from the left, Tim is seventh from the left, and John is third from the right


# From Everything-Immerse to Gamebryo

One of the first real tools that was created was an animation tool. It was used to apply animations to different characters, to chain animations together, or even to morph animations from one to another. The other was a viewer for previewing .NIF files that had been exported. “Those were the only real tools we had for a long time”, Mike said.

It became a running joke internally that everything had the suffix “-immerse”: The exporters were called “MaxImmerse” and “MayaImmerse”. The Animation tool was called “AnImmerse”. There were even some other internal tools, such as an Excel plugin called “BizImmerse” and a tool for golf course visualization called “GolfImmerse”.

Most of the team didn’t like the name NetImmerse, or how the word “-immerse” was appended to all the product names. So, they started talking about a re-brand. They discussed names such as Typhoon or Hurricane.

Finally in 2003, with the assistance of the marketing firm CapStrat and Bennett Hazlip, the name “Gamebryo” was chosen. The NetImmerse engine was renamed to Gamebryo, though – under the hood – it was still the same rendering pipeline, runtime, exporters, as well as animation and viewer tools.

![](../../assets/615a3794c213ea22.img)

![](../../assets/4570c6756347c917.img)



# Morrowind AI and Playboy Physics

One of the most well-known customers of Gamebryo is, of course, Bethesda.

![](../../assets/762cce2799106faf.img)

![](../../assets/2c59f4a34f01d99b.img)


In 2002, Bethesda released Morrowind. It was one of the first open-world RPGs, and it was a massive hit. They followed this up with Oblivion in 2008. However, the open-world nature of the games did result in some technical challenges. “Oblivion started pushing floating point boundaries. There was that gnarly skinning bug that got us in the Special Thanks credits.”, Dan added.

At this time, Gamebryo was selling what are called “perpetual licenses”. “[Bethesda] was probably our biggest license deal, dollar-wise.” John said. “Cross-platform, multi-titles, source code. And then we had a healthy support agreement ongoing them.”

![](../../assets/ba63dd6291143468.img)

![](../../assets/03a4541c6774d994.img)


After Morrowind and Oblivion, Bethesda would go on to release Fallout 3, Skyrim, and Beyond. With each game, Bethesda would replace a little bit of Gamebryo’s code. Today, with Bethesda’s current “Creation Engine”, very little of Gamebryo remains. “I’d be surprised if there wasn’t still a few lines of Gamebryo code in there somewhere, though” Dan acknowledged.


I’ve always found it hilarious when enraged fanboys online say ‘Gamebryo AI sucks, look at Morrowind’. There’s no such thing as Gamebryo AI.



Despite this, Gamebryo would sometimes get blamed for bugs that were, in reality, caused by Bethesda. “I’ve always found it hilarious when enraged fanboys online say ‘Gamebryo AI sucks, look at Morrowind’. There’s no such thing as Gamebryo AI”, Tim said, laughing.

Another game running on Gamebryo got a lot of attention, but not for the same reasons. That game was Playboy: The Mansion, and it was would be the source of many entertaining Gamebryo support emails.

“I remember there were people getting emails and just dying laughing. You would turn around and say ‘what’s up’ and they would say ‘hang on, I’ll read you the support email: I got a new version of the exporter, and now my breasts don’t bounce correctly, what’s wrong?” Dan recalled, laughing.


![](../../assets/2c8f5b2e1bed422f.img)

![](../../assets/e29238f67daf0c95.img)


I got a new version of the exporter, and now my breasts don’t bounce correctly, what’s wrong?



# Editing Scenes and Visiting Teams

During the time that he was the technical director for rendering and runtime, Dan spent a lot of time visiting customers. A few examples of the companies using Gamebryo at that time were Red Orb, Irrational, Headfirst, Microids, Firaxis, and, of course, Bethesda and Mythic Entertainment.

It was sometimes hard to get good feedback from people who were already customers. “They had already evaluated the product, so they knew what they were getting into. It would have been better to talk to people who hadn’t bought the product.”

It was also at this point that the team started to get feedback from customers about what they wanted to see next from Gamebryo. Mike mentioned: “When sales guys were talking to potential customers, we got a lot responses along the lines of: the exporters and rendering stuff is great, but we’re trying to make a whole game, so what we really want is a complete tools suite”. Many teams were using the DCC as their level editor at that time.

![](../../assets/8d2f55e2d45900ac.img)

![](../../assets/bfcece3306741147.img)


Gamebryo Animation Tool (left) and the Scene Viewer (right)


Different teams had very different need, and so not everyone agreed, though. Some of the customers said that working on a scene editor would be wasting time. Bethesda had made significant changes to the rendering code and so didn’t ask for improvements to the rendering engine, while Firaxis wanted to have 1,000 characters on screen for their next project, titled “CivNext”, and so they were asking for big improvements to the rendering engine.

In the end, even though not every single customer wanted it, it was determined that a Scene Editor needed to be built. This was also another way for Gamebryo had to diversify its offering in an effort to stay competitive.

Around 2005, work started on the Scene Editor. The tool let users arrange NIFs relative to each other. However, right after it was completed, there was an unexpected shift in the company: NDL’s merger with Emergent Game Technologies.

![](../../assets/8a6c63985429824d.img)


Tim (right) at a Gamebryo User’s Group Meeting at GDC


# An Emergent merge emerges

Up until this point, NDL had been running a profitable business overall. Outside of the convertible note that Intel had given them in 1997, they ran solely on revenues. “There weren’t any Ferraris in the parking lot like there were down at Epic, but we were making payroll” John added. This is a noteworthy feat for any company at that time, as many other companies were burning through venture capital with nothing to show for it.


There weren’t any Ferraris in the parking lot like there were down at Epic, but we were making payroll



In 2002, the company decided to start trying to raise money. However, it was a very difficult time: right after the dot-com crash. So, they began looking at alternatives. John started talking to the big three DCC companies: Alias, Autodesk, and Softimage, the developers of Maya, 3ds max, and Softimage, respectively. The pitch was to get them to acquire and integrate Gamebryo, which would give them a competitive advantage over their other two competitors.

Conversations went on for a long time. Finally, in 2006, an offer was made to acquire the company. It was very close: The VP of engineering for the company who made the offer even sent an email, asking “send me everybody’s t-shirt size”. But, at the last moment, the deal fell apart, for reasons that are still unclear. This hurt NDL, as working on the acquisition meant that they had less time to focus on selling the product.

![](../../assets/0a9525afed8209da.img)


At this point, NDL fell on some tough times, and they were just making ends meet. However, there was a back-up plan: Another company, Emergent, had been part of the acquisition negotiations but had finished second. So, NDL went back to them after the deal fell through.

Emergent was founded in Shepherdstown, West Virginia. They were originally known as Butterfly.net, but in early 2005, they changed their name to Emergent Game Technologies, and moved their headquarters to Los Angeles. Emergent had an MMO engine, but little to no customers. They had also raised money. “Once you raise money once, it’s a lot easier to raise it a second time”, John added.

NDL considered a merger with Emergent. They had money, and a west-coast location, which was good to capture more potential customers. “It seemed like a good idea at the time. In any case, we didn’t have a ton of options”, John said.

So, in August of 2005, NDL and Emergent merged, and Gamebryo became Emergent Gamebryo.

![](../../assets/44a2d2108edb9345.img)


# Growing Pains

The acquisition helped keep Gamebryo alive, but it didn’t come without its share of challenges. For one, it meant starting the Scene Editor over from scratch, “but we carried over a lot of knowledge”, Mike said.

It also took a while for the two studios to align on a single product vision. For a while, the vision was that Emergent continue working on the MMO engine, while Gamebryo provided the customers. “It took a few years to realize that the path to getting the MMO stuff shipped was in increments, and that it had to be built on top of Gamebryo”, Mike said.

Getting 30 people on the west coast and 30 people on the east coast to align was a real challenge. Eventually the west coast engineering team moved to the east coast. To set a clear goal for everyone to drive towards, the decision was made to set a hard date for their next product. That product was Gamebryo Lightspeed.

![](../../assets/44c508ad6edb80ac.img)



# The Jump to Lightspeed

Gamebryo Lightspeed included a set of new tools: A revamped scene editor, an entity modeling tool, a simulation debugger, to name a few. It also added Lua support. However, the most exciting part about Lightspeed came from where it got its name. It was called “Lightspeed” because of its workflow philosophy: As you made changes in the tools, you would see them update in the game almost immediately.


![](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt8ac58eb4b3346f09/650eaae84d73ae2c3e558433/gamebryolightspeed(1).png/?width=1280&auto=webp&quality=80&disable=upscale)



This was a big deal for game developers, as iteration time is often connected to game quality. Before Lightspeed, it was very common for developers to spend a lot of their time simply waiting to build and update the game to see their changes. It could take anywhere from a few minutes to a few hours. Now, changes could be seen directly in the game.


# Building on Toolbench

At the core of Lightspeed was a platform called “Toolbench”.

The new Scene Editor was called “World Builder”, and it was built upon Toolbench. The World Builder was essentially a shell that loaded interconnected plugins. The Scene Editor was one of the big successes of Lightspeed, in that it had a really well thought out architecture, it was super modular, it had a plugin system that was easy to extend with reference examples and source code and integrated really well with the other tools.

![](../../assets/63fc4cc61725ec45.img)

![](../../assets/94a3d2d828ca04ff.img)


The Entity Modeling Tool was built on top of Toolbench. It allowed users to add components to determine the behavior of an in-game entity. For example, you could create an entity, add a physics component to it, then a game-specific component to determine which properties it has, and then override those properties. It was very similar to the components system that we take for granted in game engines like Unity today. The property overrides were done with a graph to represent the data-drive inheritance hierarchy.

![](../../assets/92909bd96b2947f2.img)

![](https://www.gamasutra.com/ckfinder/userfiles/27524733/gamebryosim2.jpg?width=1280&auto=webp&quality=80&disable=upscale)


The Simulation Debugger could connect to the game to show a visualization of what was loaded. It was possible to see a live status of all the properties and a history of functions that were invoked. This fit perfectly with the philosophy of Lightspeed, as it was all about rapid iteration: the game is connected live, and the developer can see the data and get immediate feedback on how it is affecting gameplay.

Lua support was also new to Lightspeed. Prior to Lightspeed, game logic was the job of the game developer. Now, anyone who could write a bit of Lua script was able to contribute to the game logic.

“Lightspeed was built on a lot of ideas that failed to take off.”, Mike said. “In the years since working at Insomniac, so many of the same exact concepts exist in our engine, and they have really flourished.”

“Lightspeed was also built on a lot of sound theories, it was just a question of getting it past the shaky 1.0 version. If it was released a year or two earlier, things could have been very different.”



Lightspeed was also built on a lot of sound theories, it was just a question of getting it past the shaky 1.0 version. If it was released a year or two earlier, things could have been very different.


![](../../assets/01e3e23a0eb8e807.img)


Mike Daly

# The Korean Connection

Around the same time, Gamebryo was getting a lot of business out of South Korea. The reseller Gamebase was capturing a huge portion of the South Korean middleware market. Dan travelled to South Korea twice.

![](../../assets/7cfce2a5cf6214c6.img)


On one trip, Dan was asked to write a tool to scan a game to see if it was using Gamebryo. This was due to the high number of game companies who pirated Gamebryo. “The idea was to get every game that comes out made by a South Korean company, see if it uses Gamebryo, and then send them a bill” Dan said. The tool saw some success, and they started contacting companies who had pirated the engine.

Dan also spoke at a conference in South Korea, where he and Tim Sweeney, CEO of Unreal, both got top billing. “It really said a lot about how well respected Gamebryo was at the time in South Korea”, Dan recalled.


![](../../assets/94ca1dd75c62fa70.img)


Dan (left) with fellow NSCU colleague Shaun Kime (right)


# Death and re-birth

Despite all its strengths, Lightspeed faced a lot of challenges.

The competition was getting fiercer. In the early days, the only competition was from Renderware who were doing the same thing: exporting scenes and rendering them. However, as time went on, there was more and more competition from products like Unreal, which had a more end-to-end pipeline: editors, physics, networking, AI, and so on. The Gamebryo team didn’t have the resources to catch up.

Also, performance was also starting to become a problem compared to other engines. Gamebryo carried a lot of baggage into the Playstation 3 and Xbox 360 timeframe. The big drawback was that it didn’t have a good processing pipeline in place, so it was hard to create efficient scenes that had performance that was competitive with games made with other engines. “You would get about 500 draw calls per gigahertz. There was a magic number that Microsoft said we needed to hit, and we were not batching all those draw calls together, managing states, and all those things you had to do”, Dan recalled.

There are few examples of this better than Bottlerocket’s 2005 game Splatterhouse, which ran on Gamebryo. In a [retrospective published by Polygon in 2010](https://www.polygon.com/features/2018/5/21/17370590/splatterhouse-2010-what-went-wrong), physics programmer Michael Seare is quoted saying “When it comes down to pushing bits around, it was terrible.”

To make things even more difficult, the games industry was changing under Gamebryo’s feet. The types of games that they could sell their technology to were not getting funded. At this time, the industry was splitting into two parts: Live Arcade games, and huge AAA titles like Assassin’s Creed and Call of Duty with $100 million budgets. “It was hard to sell a rendering engine for $75,000 when someone’s budget for the whole game is $500,000,” Dan said.


It was hard to sell a rendering engine for $75,000 when someone’s budget for the whole game is $500,000



At a certain point, the middle of the market fell out. Around the same time, Gears of War was a major showpiece for Unreal Engine, and it had just become available for licensing. “Because Gears showed so well, if there was a new game that used the Unreal Engine, journalists would put the word Unreal in the headline as evidence of how awesome it was going to be.” Dan added. Gamebryo tried to make an in-house game to do what Epic was doing. Lenguins and Daydreamer were two projects that were developed but never got funded, and so they never went beyond a vertical slice.


![](../../assets/d73dde7c15defb52.img)


The Daydreamer project, which was developed in collaboration with Killspace Entertainment


This was also around the subprime mortgage financial crisis. Games were selling on the iPhone for 99 cents. Gamebryo was under heavy pressure from Epic. The Unity game engine was starting to gather momentum as well, and were well positioned to service the growing mobile and indie game market.

Not long after, Dan and John left Gamebryo. Shortly after that, the office shut down and the employees who were left started working from home. Then, came the word in 2010 that all of Emergent’s assets – including Gamebryo – were going to be acquired by their loyal South Korean distributor Gamebase.

Development on Gamebryo continued for a few more years afterwards, but these days it is unclear if the engine is still in development or supported.


![](../../assets/da8c836d434ea61f.img)


John (mid-left, in the far back, standing), Dan (third from right, sitting), and Tim (far right)


# Advice for tools programmers

Finally, I asked Mike, Dan, John, and Tim to share some advice for people who are working in tools development today.

Mike offered, “Middleware carries an incredible weight that is a burden that’s often underestimated. When people buy a product, the code you send them needs to be readable, robust, documented, and supported. The amount of overhead that adds is really easy to underestimate. A common misstep is to not be ready for that burden, put a tool out there, and be crushed by it.” Dan added “What is written in the Mythical Man Month still holds true: Going from a piece of software to a software system, or to an API, is a 9-fold cost multiplier”.

“The most successful companies of that time were those who either did one thing really well – like Scaleform, Speedtree, or RAD game tools – or they were engine companies that were associated with a game, which gave them the focus for the product”, John said. “Also, they had the artists and the designers and everyone to provide that feedback in a very immediate way, and the revenue to do the development on the engine”.


You have to make sure you’ve got your artists and designers in the loop, and that they’re driving the feature development. At Epic, the artist was king. Gamebryo was very engineer-centric.



Dan said, “You have to make sure you’ve got your artists and designers in the loop, and that they’re driving the feature development. At Epic, the artist was king. Gamebryo was very engineer-centric. We had one artist on staff for the life of the product. He was awesome, but when you have one artist, he becomes the squeaky wheel. We never had enough content and users in-house to know whether what we were making was going to be useful.”

Tim added to this: “If you’re going to be making tools for artists designers, you need to actually use the tools and do something significant. Not just a toy, not just something that will demonstrate that the code does what it’s supposed to do, but something that shows that the workflow is what the artist and designers need to get the vision they want so that they actually want to go out with experiment with the tool, and not curse at you for making them go through hell every single day.”

“I’ve been in this industry for many, many years, and I feel like this is the lesson that keeps getting re-learned. Every team needs to stop and re-visit it”, Tim said.


If you’re going to be making tools for artists designers, you need to actually use the tools and do something significant […] I’ve been in this industry for many, many years, and I feel like this is the lesson that keeps getting re-learned. Every team needs to stop and re-visit it



# Where are they now?

Tim left Emergent in 2010 to work for Mythic Entertainment, where he worked on a few PC and mobile projects. After the studio closed, he moved to Austin, Texas, where he works at BioWare as a graphics programmer.

After leaving Emergent, Dan worked on middleware for Kinect at Activate 3D, which was acquired by Organic Motion. Now he works full-time as a martial artist instructor. “I teach people how to punch and kick now”, he joked.


![](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt8595a3afac08c57d/650eb47694b67198890a4105/gamebryodan.jpg/?width=1280&auto=webp&quality=80&disable=upscale)

![](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt2d179f6dfdbd198a/650eb46afcbd39610f9e8062/gamebryotim2.jpg/?width=1280&auto=webp&quality=80&disable=upscale)


Dan (left) and Tim (right) today


After leaving Emergent, Mike moved to Texas to work at Robot Entertainment (Age of Empires, Orcs Must Die, Hero Academy). However, right before leaving for Texas, he met a girl in North Carolina, and they started a long-distance relationship. After a time, he decided to move back to North Carolina, and he how works at the Durham branch of Insomniac Games.

John consulted for Emergent for a few months after leaving. In 2011, he became involved with a video game accelerator called Joystick Labs for a year, which then morphed into Groundwork Labs, a non-profit accelerator program that worked with startups in any sector. Today he is a senior director at the non-profit foundation NCIDEA, which helps startups across the state of North Carolina.


![](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/blt78969890358c5204/650eb474aa3e38717c67e8c4/gamebryomike.jpg/?width=1280&auto=webp&quality=80&disable=upscale)

![](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/bltb458dc714d419764/650eb46f843b5183ab4d8558/gamebryojohn.jpg/?width=1280&auto=webp&quality=80&disable=upscale)


Mike (left) and John (right) today


In addition to Dan, Mike, Tim, and John, many people who worked on Gamebryo continue to have an impact on the games industry. Here are just a few:

Chad Robertson - EA Bioware and Archetype Games

Lars Bishop - NVIDIA

Vince Scheib and Enne Walker - Google

Michael Noland, Nick Darnell, Katie Finin-McGovern, Shaun Kime – Epic

Matt Bailey, Joel Bartley, Paul McLauren – Insomniac

Paul McLauren – Red Storm

Jeremiah Washburn (staff artist) and Scott Sherman went on to found Grumpy Pixel.




# Special Thanks

I would like to thank Dan, Mike, Tim, and John for taking the time to speak with me to help preserve the history of game development tools.