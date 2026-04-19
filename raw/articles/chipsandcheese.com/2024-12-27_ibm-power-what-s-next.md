---
title: IBM Power - What's Next?
url: https://chipsandcheese.com/p/ibm-power-whats-next
author: George Cozma
published: '2024-12-27'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# IBM Power - What's Next?

### An Interview with Bill Starke

Hello you fine Internet folks,

I had the opportunity to sit down and interview Bill Starke the Chief Architect of Power CPUs at IBM where we got to talk about the future of Power along with where he sees the industry going for future memory standards. But before the interview there is an introduction to IBM Power and the history of Power CPUs for the folks that don’t know what IBM’s Power is.

Hope y’all enjoy and the transcript of the interview is below the introduction.

**A Introduction to IBM Power**

Hello, you fine Internet folks. I'm back home from SC where I had an absolutely wonderful time and I cannot wait for SC25 next year in St. Louis.

And while at SC, I had the absolute pleasure to interview Bill Starke. Bill Starke is the chief architect of IBM's Power CPUs.

Now, some of you will know what IBM Power is, but some of you aren't. And this intro is more for you folks who don't know what IBM Power is. Now, IBM Power is one of two CPU lines that IBM makes. There's IBM Power and there's IBM Z. Now, IBM Z dates all the way back to the System 360 and is a very different lineage from the Power systems that Bill and I were talking about.

Power, as some of you may know, was used by Apple for a long time in the PowerPC series of MacBooks and Mac desktops.

So for some of you, Power is a known quantity. However, Power has been sort of out of the news as of late. There hasn't been a ton of talk about Power since the announcement of Power10 at Hotchips 2021.

So historically IBM has had an initial Power versions, so let's say POWER5 and then in between generations, so in between the POWER5 and the POWER6, they've had a POWER5+, which is an incremental update on the prior generation of Power. And with POWER9, seemingly IBM has dropped the + scheme [where] there was no POWER9+.

And with Power10, that seems to also be the case. There doesn't seem to be a Power10+ coming. Instead, what we're getting is the Power11.

And that is what Bill and I talk about along with what the future for Power holds and what decisions they may make for future architecture so, it wasn't explicitly said, but Power12.

Anyway, I hope this little preamble before the video does clear up some things and why these questions were asked as they were. And it's largely because there hasn't been a ton of news of Power. So I was very curious about what was happening with it and what does the future look like for Power? So, here's my interview with Bill Starke.

**Interview with Bill Starke**

*This transcript has been edited for readability and conciseness.*

George Cozma: Hello, you fine internet folks. We're still here at SC24 and instead of at the convention center, we're here at the Westin Peachtree with IBM and I have with me Bill Starke the Chief Architect of the Power division [at IBM]. Would you like to introduce yourself?

Bill Starke: Hello everybody, good to talk to you. Yeah, I'm Bill Starke. I'm the Chief Architect of our Power Microprocessors and happy to be here at SC24. It's been great. We had a little rain today, but you know, a little soggy, but other than that, you having a good time? I'm having a great time.

George Cozma: It's been a lot of fun, a lot of good discussions and a lot of filming and I see, I love your shirt, the Power 10 shirt.

Bill Starke: The 10 baby. It's good.

George Cozma: So speaking of Power, Power10 was the first to have a logo of all the Powers, the independent logo. Are we going to see a Power11 logo?

Bill Starke: I would expect so. I'm a little less involved in designing that than I am the actual processor, but Power 11 is kind of right around the corner, shall we say. Okay.

George Cozma: And what do you, so what is Power 11 going to look like in the sort of high level sense?

Bill Starke: Okay, yeah, just sort of stepping back, you know, if you've followed us over the years, you know, POWER7, POWER8, POWER9, Power10, we did a pretty big transformation, going from Power 9 to Power 10. You know, as we described it, we kind of tore the thing down from the core. We started up building a new one with the focus. We're always every generation, you know, looking at where our clients are, you know, we run enterprise. So I know a lot of people don't hear all the details about us. We're not super well known, but actually when you swipe something on your phone, you know, when you click something, most of the time it's running through a power computer, you know, hidden behind a curtain somewhere. You're running in, you know, all the world's top enterprises. But so as we went to Power 10, one of the big things, if you recall the discussion then, we really focused on AI being infused into the enterprise. And even prior to that, you know, we were playing a little more in the external accelerated AI. We were doing some really cool things with NVIDIA, which were really centered around big HPC and AI training.

But once again, we're an enterprise business. So we kind of needed to make sure you could train models so that later on you can run them and inference them in your enterprise workflows. By the time we went to Power 10, we pivoted strongly back towards let's focus on the inference now that we know that the world can do training properly. And, you know, that's been a huge area we've been venturing into. And I feel like with Power 10, you know, we not only hit the workloads of the day and what we needed to get done, but we got the workloads of the future, you know, much better addressed. So sorry, that's a really long preamble to what are we doing with Power 11?

What we found in the field is Power 10 has, you know, even outpaced our expectations. You know, looking in the rearview mirror, it was exactly what we needed and it's better future facing. So Power 11, we are not burning it all to the ground and starting with a lot of new DNA. We're actually going to kind of extend those capabilities, those architectural features that you see in Power 10 and we're going to augment them. And I can give a few examples, but I got to let you get a word in as wise as you're the interviewer. But I can give some examples of that if you like.

George Cozma: So yeah, some examples. So the Power 11 core, is it derived off of the Power 10 core?

Bill Starke: Yes

George Cozma: What are the sort of biggest micro architectural changes there?

Bill Starke: Not a whole lot of change into the core itself. I mean, the Power 10 core knocked it out of the park. So yes, it's going to run faster. Yes, we're going to be able to enable, you know, more cores. But, you know, fundamentally think of it as evolutionary from an architecture standpoint. And where we're really looking is as we talk to our clients, you know, what are capabilities beyond just those raw speeds and feeds that you need to get? Or what are other aspects of the system where we can provide more value? Yeah.

George Cozma: So, but Power 11 is its own independent core is it not?

Bill Starke: Oh, it's a new core.

George Cozma: The reason why I asked that is because in some LLVM commits, it was just, it was Power11 was essentially labeled as Power 10. So a lot of people had questions of is it a new core or not?

Bill Starke: So like in terms of any ISA changes, you know, any new instructions, anything like that. No, the ISA is the same as a Power 10 ISA. So kind of in the software-ish world, you know, you're going to see like, hey, this looks the same. Well, yeah, you know, you want to have continuity in your ISA. We didn't see any things where it's like, oh, we better add that new thing to it. I mean, and then when I said with Power 10, we feel like we addressed not only the present, but the future very well. You know, that kind of goes hand in hand with that.

George Cozma: Okay. So I know that there was a roadmap a few days ago published and the future Power chip looks a lot like AMD's, Rome and Milan set up where you have a single IODI and then multiple [compute] chiplets.

Bill Starke: Yes.

George Cozma: What drove you to that sort of design?

Bill Starke: So we've been evaluating for many years, you know, when is that time going to come with Moore's Law, where like, yep, we have to augment just doing new chips with packaging. And as you pointed out, we've seen that with our friends at AMD. We've seen that with our friends at Intel. We've seen that with our friends other places. People are evolving toward chiplet architectures to kind of overcome the physics limitations that Moore's Law, which was once our good friend, is not so much our friend anymore. So we need to do those things. So we determined for power that the new thing we come out with after Power 11. I'm not going to say the name because we have to have official naming, but I'll let you guess the name after Power 11. Maybe that's 12. Well, I can either confirm nor deny that. But whatever that next thing is called, we are going to go to a chiplet architecture. And part of the reason we wanted to spell that out is we get that question all the time. I mean, it's, gee, when are you guys going to get there? What are the factors? Now, what's really cool, if you'd like, I can talk about some of what we've discovered as we evaluate these architectures. And you ask specifically, yeah, we look a little bit like the thing AMD did. You know, AMD had to make tradeoffs in what they did. Intel had to make tradeoffs in what they did.

It was interesting for me to see because we kind of made the plan years ago. And as we saw, oh, here's what they're doing, here's what they're doing, we got to see the things that we conjectured for ourselves play out in the realities of what they're building. And we got to see, oh, how does this confirm or deny what our engineering analysis said it would? And basically, it's kind of matching our judgment. I mean, I don't know that I should make too many comments on what the competitors do. You know, it's just my guesses. I don't want to say anything negative about anybody. But I would argue both AMD with their architecture and Intel with like Sapphire Rapids, they had to make certain tradeoffs. I can see wisdom in what they both did. And they're very different, you know, to address certain things. And I can see compromises they needed to make. And it just so happened that within the realm we play, which we're playing in a different world. We're playing in enterprise and we're playing, you know, especially we have our large system enterprise heritage.

If you look at how those kinds of approaches might map, the thing we came up with just happens to look a little more like the thing AMD came up with. And I mean, I can go into more detail. I will say where I'm super excited is the areas I see they had to make compromises. That's some areas where we have some differentiation where I feel like I'm getting the value of a chiplet architecture without having to make some of the negative compromises. So, yeah, so what I guess what client workloads drove you to more of a I.O. with disaggregated compute, single I.O. with disaggregated compute rather than say single unified compute and disaggregated I.O. So one aspect of that is just to build a large system. The worst thing you could do from a latency standpoint is do the compute at the center and disaggregate I.O. Think of building a topology. It's not about building the socket. It's about building the connectivity across all sockets and internal to the socket. I like to call it the silicon radius. I need to engineer to the absolute lowest latency to get from one end of the silicon to the furthest end of the silicon in the system, not at a socket level. I also have to do that one aggregating as much silicon as I can. So those are at odds with each other. So hence it's a fun engineering problem.

George Cozma: So we just saw the announcement from Azure and AMD about the MI300C chip. Now, what did what do you think of it [because] it looks like a mix of what Intel did with Sapphire Rapids and what AMD was doing so do you see that as fewer compromises in terms of trade offs? Because I know that a large trade off that AMD had to make was you can't you couldn't directly communicate between chiplets [and L3 Caches].

Bill Starke: Can we maybe suggest maybe they had to make some latency compromises and some bandwidth compromises? Yeah, because of the kind of signaling as opposed to if you looked at a Sapphire Rapids and all the small bump edge edge stuff. Intel, I believe, was saying we're going to build our full highway systems that run across this. And so I think what you're seeing is an evolution of AMD saying some of those latency bandwidth compromises we made, we're going to make improvements to that. However, that leads to some of the compromises Intel made. So it's interesting. They're balancing somewhere between where they've been and where Intel is. And the thing that for myself, for us there, from our signaling technology that we use in our hub and surrounded by compute model, the signaling technology is not requiring me to make bandwidth compromises. That's a twofold thing. One is just the capability of the kinds of unpackaged SERDES. My engineering team is able to do so as I map out the highways, I didn't get like, oh, we have to cut the lanes out. No, it's pretty much what I would have built on ship. But the other piece is because of a memory interface, we're not surrounding our hub chip with all these horribly inefficient DDR ports to talk to memory. We have our own my memory architecture that takes the signaling overhead for memory very low and enables us to put bandwidth in for other things. So it's a combination of really good quality signaling and the ability to get more of it in there. I don't have to make that compromise. It also helps me in latency because the best thing you can do for latency is be outside of the silicon. The wires in the substrate run 10 to 50 times faster than in silicon wires. So the worst thing you can have is a big, big, big pile of silicon with, you know, staying in the silicon and latency, I think, in my world probably matters more to me than any of these other folks because I have to build really large 16 socket systems. I'm not trying to just build a single socket optimize or a couple sockets optimize. So it's different tradeoffs that you're making for the different kinds of spaces. And so I don't mean to be I'm not being critical of anybody. I'm just saying we have to do different things. And I really admire what both what AMD and Intel have done with the constraints.

George Cozma: No, absolutely. It really was a question of what did you think of the blending? And I really liked your OMI if you want to talk more about OMI because that's a major differentiator for not just Power, but also for any IBM system.

Bill Starke: Yeah, our Z systems use OMI as well. And I mean, so there's another whole realm there. I just described the value of OMI in terms of it provides all this signaling, you know, beachfront resource to do other high bandwidth signaling. That's one element. That's just because it is so beachfront area efficient because you're essentially running a really high speed series instead of running a really low speed DDR interface, relatively speaking. The pin counts are so much lower. But the other thing with OMI, well, there's multiple. I could talk forever here. I don't know how much time we have, but I'll hit the high points. Reliability, ultra reliability. One of the weakest components of any system is a DIM connector and running a DDR protocol over a DIM connector. You know, it's got to run, you know, down through the modules, through the motherboard up over the DIM connector up under the DIM, hit the DRAM chips as DRAM speeds are trying to go faster and faster and faster with these single ended DDR protocols. I don't know how they're even going to do DDR6. I think the industry is kind of in for a nasty wake up call here. I know they're dealing with it. I know people have a lot of trouble in this area with the DDR5 signal integrity. Yeah. And so I don't have that. I'm not running a DDR protocol that way. I'm running this beautiful high speed series. If I have a problem, I do a replay. It's a really intelligent protocol, just like PCI. You know, you got to resend a packet, you take a CRC fail, you replay it. I also can steer around lanes. So if a lane goes bad or if there's something flaky on the DIM connector, I can get around it, keep the system up and running. That matters for what we're doing in our Z systems, in our power systems, especially power like our big SAP HANA workloads. You got tens of terabytes of memory that can never afford to go down.

This is part of our secret sauce of how we get there. Now, the other thing, that's reliability. Also, because I'm able to run this so much more efficiently off the processor, I'm not stuck only putting like eight DDR ports or maybe 12 behind a socket. I have 32 DDR5 ports behind my new memory architecture on a single socket. So much higher bandwidth. I can get to like three, four X types of bandwidth, three, four X types of capacities. Capacity is big, too. Yeah, absolutely. Especially in the SAP HANA world where it's in memory databases and those databases can be eight 16 terabytes in size or larger. We're sort of much bigger than that. But yes, I think I'm the right way like in the past and we still have eight socket systems and it was almost specifically designed for SAP HANA work.

George Cozma: So I guess moving forward, there is going to be Power.

Bill Starke: Oh, Power definitely exists. So here's the other beauty. So we talked about power 11. We talked about and then beyond that, we moved to a chiplet architecture for that thing that comes next that might be named like power 11 plus one.But once you're on that chiplet architecture, the other thing we see is a path forward. We see how to iterate within that architecture with the hub and the compute chips around. You can see how you can incrementally change things. You can see, first of all, allows you to get more silicon area in a socket. Well, those are tiny little compute chiplets. You can see how those can grow as you need. You can see how you don't have to refresh the whole thing. So there's there is a growth path and there's a set of development economics around that that I will tell you as a chief architect, I've been doing this for almost 30 years, not as a chief architect, but an engineer working on the processors. I can see clearly further forward into the future than I ever have before, just because of, you know, seeing, well, I could do this for the thing after, you know, power 11. I can do for the thing after that. I'll do this twist for the thing after that. I'll do this twist. And I can see getting there in a much more economical way from a development standpoint.

George Cozma: Well, I guess they just have one final question for you, what's your favorite type of cheese?

Bill Starke: You know, I guess I love a Danish blue is really good with a nice glass of red wine.

George Cozma: So we still have some more SC stuff coming out, hopefully, I think. Depends on when this video comes out. But hit that like button, hit the subscribe. I hate shilling it, but I have to. And have a good one, folks.

Bill Starke: Hey, thanks so much for having me.

George Cozma: Thank you so much.

If you like the content then consider heading over to the [Patreon](https://www.patreon.com/ChipsandCheese) or [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks to Chips and Cheese. Also consider joining the [Discord](https://discord.gg/TwVnRhxgY2) and subscribing to the [Chips and Cheese Youtube channel](https://www.youtube.com/@chipsandcheesecc).

I can't even read the transcript, YOU KNOW. Comes up 35 times.

>It also helps me in latency because the best thing you can do for latency is be outside of the silicon. The wires in the substrate run 10 to 50 times faster than in silicon wires.

Can someone explain what he's talking about here, in more detail? I though the whole point of staying monolithic is because on-chip communication is faster and generally better than chip-to-chip communication, no? If what he's saying is true, why aren't we just still building processors on PCBs from discrete transistors? What metric is it that is 10-50 times faster? Surely not the signal propagation speed?