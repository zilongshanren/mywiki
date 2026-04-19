---
title: Chips and Cheese Interviews Ronak Singhal
url: https://chipsandcheese.com/p/chips-and-cheese-interviews-ronak-singhal
author: George Cozma
published: '2024-09-30'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Chips and Cheese Interviews Ronak Singhal

For today’s article we have another video interview for you folks, this time with Ronak Singhal from Intel where we talk about Granite Rapids AP.

Before we get into the video and the transcript, I would just like to give a massive thank you to all of you who have subscribed to the Chips and Cheese YouTube Channel. We now have over 1,000 subscribers which is mind blowing to me. When I decided that I wanted to some video content I didn’t know how it would be received by the community and I am so glad to see that you guys have liked our video content and I can’t wait to bring more video content out for you guys to enjoy!

The transcript below has been edited for readability and conciseness.

**George Cozma:**

Hello, you fine Internet folks. We’re here at Intel’s Enterprise Tech Tour, where we were finally introduced to Xeon 6 and where Granite Rapid SKUs have been announced. That is the all-P core SKUs, and in particular, the 128 core SKUs with three compute dies, two IO dies, which was formerly codenamed “Granite Rapids AP”. And with me, I have…

**Ronak Singhal:**

Hi, I’m Ronak Singhal, Intel’s Senior Fellow. I work on Xeon on our long-term roadmap and overall technology strategy.

**George Cozma:**

So, getting into the questions, because that’s the most important part. Starting with the high level and moving in, the Granite Rapids memory system [can support up to] 6400 DDR5 with 12 channels for the AP version but SP is 8 channels, correct?

**Ronak Singhal:**

That is correct. Yeah, so we’ll have two separate platforms. One platform is a higher TDP platform, the AP one, 500 watts, 12 channels of memory, just like you said. That’s AP what we’re launching now. And then SP will come Q1 next year, that’ll be 8 channels with lower TDPs.

**George Cozma:**

Okay. So, 6400 DDR support. However, only one DIMM per channel, one DPC. Why was that chosen? Why one DPC instead of what we’ve been used to with two DPC?

**Ronak Singhal:**

Yeah, that’s a great question. And so, on the one that will launch next year in Q1 and next year, we will have two DIMM per channel support. On this platform, we actually went through a lot of internal debate on the one DIMM per channel versus two DIMM per channel answer. And what we said is, we really want to support, first of all, highest memory speed, highest bandwidth for these SKUs. These are our beefiest compute SKUs. We need the need for the bandwidth.

So, what we ended up seeing is that most of our customers were still going to deploy a single DIMM per channel to get that bandwidth, whether it was the 6400 or to do it with the MRDIMM, which only comes in one DIMM per channel anyway. So, once you see that, then the support and the ability for us to really limit the number of configurations that we need to validate, that we need to support going forward, that became a trade-off versus how many customers are actually planning to deploy two DIMMs per channel. So, we made the decision to go with a single DIMM per channel on this platform. But like I said, you’ll see on the SP platform, you’ll still see two DIMMs per channel.

**George Cozma:**

Okay, cool. And so, you sort of touched on MRDIMMs, but how are we going to sort of make up that capacity loss with sort of the removal of two DPC?

**Ronak Singhal:**

So, I think the place, it’s a great question because where do we see people going after high capacity? So, one of the things is the AP platform will be our either one socket or two socket platform. The SP platform next year will be also the platform where we support not just one socket and two socket, but also four socket and eight sockets. And that’s where we tend to see people really grow that capacity. Now, on the AP platform, if people want to go after a much higher capacity, then again, you’re getting 12 DIMMs already. So, if you compare that versus what you have today, you’re already not in a bad shape. But what we do see people looking at is expanding their memory by using memory attached to CXL. And there you can grow the amount of capacity you have independent of the number of DIMMs per channel that we have on the system. So we have some different options and flexibility depending on where people want to be on bandwidth and capacity.

**George Cozma:**

And then, MRDIMMs. Now these are not your previous generation MCRDIMMs. These are what’s going to become part of the JEDEC standard, if I remember correctly. But that standard hasn’t been released yet. So how do you design a platform for a technically unreleased specification?

**Ronak Singhal:**

Yeah. So just to clarify, this is the first generation that’s supporting any of this technology. No generation, either ourselves or anybody else has supported that. I mean, it’s a testament to the work that we do with the memory ecosystem, with the memory vendors, to be able to be the first one out on a standard like this. To work closely with them, partner with them through not just the specification, the design, and then the validation of these, their parts with our parts. And be able to say on the day we launch, we have these available in the ecosystem. All right. So it’s really that close partnership.

**George Cozma:**

Do you expect a lot of your customers to sort of move towards this MRDIMM technology moving forward?

**Ronak Singhal: **

I think that’s probably an open question. We would like to see it. And we’ve seen significant interest on the technology. I think the biggest question that some of our customers have, rightfully so, is where will that end up pricing wise? Because memory pricing is so critical to them. Again, I think this will be a function of as some of the larger customers start to invest in MRDIMMs, then you start to get the volume, you’ll start to see the prices move on it. But I think time will tell. Memory pricing is always, as you know, very fluid. Very volatile.

**George Cozma: **

So again, now moving a bit into the actual package and talking about how you’re connecting all five dies, but the three main dies within the compute cluster, that is still using EMIB, correct?

**Ronak Singhal:**

That’s correct.

**George Cozma:**

And you now have those three packages, but you have at the top end 128 cores. How exactly are you splitting that?

**Ronak Singhal:**

Yeah. So just like you were describing, and make sure that all your viewers know, we have two IO dies, one at the top, one at the bottom. That’s where we have our PCIe, our CXL, our UPI.

**George Cozma:**

And that is also not where you have your memory controllers. The memory controllers are on the compute dies, which is a bit different to what some of your competitors are doing.

**Ronak Singhal:**

That’s right. And so then we have the compute dies that have our x86 cores that were the L2 cache or L3 cache. And then like you just said, that’s also where the memory controllers reside. So for the case of AP, where we have the 12 memory channels with three compute dies, you have four memory channels per compute die. Now your question was, all right, how do I take something like the 128 core part and have that split across the three different dies? You’ll end up with 43 cores, 43 cores, 42 cores for that kind of scenario.

**George Cozma:** So for yield reasons, could it potentially be 42-43-43, 43-42-43, 43-43-42 for just in the packaging, or will it always be a set [configuration]?

**Ronak Singhal:**

We have flexibility and in truth, we’ll see what we end up with if it’s always the same or not. I think the thing to keep in mind is the 128, that’s clearly the top line SKU. That’s going to be the SKU with the highest throughput. You’re going to see a range of different core counts deployed by our customers. So if you go see what a typical cloud vendor will provide, will they do a 128? Maybe they might also do something that’s a little bit lower to get a higher performance per core. So you’ll see a range of those SKUs being deployed.

**George Cozma:**

And speaking of the mesh, how do you deal with sort of different column and row sizes when it’s not perfectly square, so to speak?

**Ronak Singhal:**

Yeah. So first of all, like you’re alluding to, we still have a fully connected mesh as our interconnect between the cores. So all cores have access to all of the L3 cache. They’ve access to all the memory controllers. They have low latency interconnect to talk to each other. When we do that with something like the 43, typically the way we build it, as you can imagine, is that you do have, I’ll call it a perfect rectangle between rows and columns. But some of those may not be cores. Some of those may be mesh stops for things like your memory. Some of those may be cores that we don’t turn on. So we have the ability to, you can call them dummy stops on the mesh or other things like that, but we have the ability to deal with less than perfect rectangular numbers when we’re building this.

**George Cozma:**

And sort of continuing on, sort of a mix of the two, you now have this newish mode called SNC3, which is Sub-NUMA Clustering 3. And that’s because you have the three compute dies. Now why was that added? So why not just stick with what is now being called HEX mode, which was previously known as SNC1, which is where it’s all just one big compute pile essentially.

**Ronak Singhal:**

Yeah, that’s a great question. So just like you said, our hex mode is when you allocate your memory, you stripe it across all 12 channels. And so your average core is going to talk to each of those 12 channels equally. What you see is two factors here. First of all, as you’re growing the core count, like I said, we have a fully connected mesh. So you are growing the distance between points. So that grows your latency. Second of all, we have the three different compute dies. And there is latency to cross the compute dies over that EMIB, even though it is a low latency interface, you still have to potentially hop four different times. If you’re going from the top die to the bottom die and back.

So what we looked at is for some workloads, you need to have that because that’s their characteristic. But there are a lot of other workloads that have NUMA optimization properties. And so we can take advantage of that and really focus on allocating memory that’s nearest to the cores. So like you said, I have four channels of memory per compute die. If I stripe that memory to the cores that are doing the compute, I can cut down the average latency that I see both for cache accesses and for memory accesses.

**George Cozma:**

Now, when building a mesh this big on your slides, you’re showing essentially about a 20 nanosecond difference between SNC3 and HEX mode. Now, that’s quite a big uptick is part of that because of how you have to design a mesh that’s well over 128 stops because you have to account for the memory, as well as all your EMIB connections to not only your IOD dies but also to the other compute dies. Does that one is that a factor in that latency hit as well as is there also a mesh penalty for that, for building it that big?

**Ronak Singhal:**

Yeah, mesh clock penalty. Yeah, I think it’s multi-fold, just like you’re talking about. One is exactly what you said. As I grow the mesh, I’m growing the number of hops. We talked about the physical interface that we have as well. The last part is you want to be able to manage the power of this mesh because the mesh is growing bigger and bigger and that interface is growing. How do I modulate the power? So how fast am I running this at and what’s the tradeoff between power and performance I’m making on that?

**George Cozma:**

Okay. And how much was that latency impacted by the increasing cache per L3 slice?

**Ronak Singhal:**

The cache is a very modest amount of the latency. That’s not a driver really on those latency. Okay. Okay. Because as you saw, in the SNC case, our latencies are actually quite comparable to prior generation, but we still have a larger cache.

**George Cozma:**

Moving from the cache and more into the core, previous generations, so your specifically Golden Cove and the version of Golden Cove that was in Elmore Rapids had a vector register that was not fully 512 bit. And what I mean by that is you had approximately 320 entries that were 256 bit and 220 of those also had that extra 512 extension. Has that changed with the Redwood Cove in Granite Rapids?

**Ronak Singhal:**

Yeah, so Redwood Cove, I’ll call it a modest update over the cores that you saw in Sapphire Rapids and Emerald Rapids. There are improvements. There are changes for microarchitecture performance and really for power efficiency and power reduction. On the vector side, it’s going to be a very similar implementation.

**George Cozma:**

How different is it… So in terms of what’s changed for the client versus the data center, how much has changed from Meteor Lake’ implementation to Granite Ridge’ implementation beyond AMX and the re-addition of AVX-512?

**Ronak Singhal:**

Those are the biggest changes. Okay. So it’s really, when we look at, we share the majority of that IP common between the client side and the data center side. Like you said, we will have things like the AMX unit for AI acceleration that the client team doesn’t have. And then we have the ability obviously to take advantage of AVX-512.

**George Cozma: **

And so there is no additional necessarily like RAS features within the core. Those are the two big changes?

**Ronak Singhal:**

Those are the two big ones. There are reliability capabilities, for instance, that we may only use in the data center version. Right. There’s the power management. We will tune for the data center. The prefetchers will tune for the data center. So there are things of that nature. But if you’re looking at a dive photo of the two cores, really the big major difference you’re going to see is AMX.

**George Cozma:**

And sort of how much complexity does it add to a design when you’re sort of adding and subtracting these things? Because I know that when you have to do validation, every single little change you make, you have to revalidate because you don’t know what could cause the entire core to just go, “Nope, I’m not going to boot now.” So how much complexity does that add to the design to make it that flexible and sort of scalable?

**Ronak Singhal:**

Yeah, I think our teams have done a great job to make it actually fairly easily for us to do what we think of almost as just dive chops. Right. We are able to chop off that AMX unit. Right. The rest of the core basically operates the same without it. You know, everything else, you know, like I said, there are some minor tweaks or minor features that can be different between them. So there is some incremental validation. But again, the vast majority of the testing and validation that’s done on the core applies to both the client version and the data center version. So we’re able to amortize that very nicely between the two.

**George Cozma: **

Okay. And speaking of the amortization, how much more validation do you need to actually add that sort of third die for Granite Rapids AP? Is that a significant validation increase or is it sort of a wad of the sort of groundwork was already set when you’re doing the initial validations?

**Ronak Singhal: **

Yeah, you know, so really our focus with this modular design where I can aggregate one, two or three compute dies is that you set the interfaces to be standard between them. And then so once you can you can validate that protocol, that interface, you’re in very good shape. Now, do you still have to go and say, when I increase the core count by another, you know, 30 percent, does that introduce any new issues? Does that put stress on any buffers that I may not have seen before? So there is additional testing, but it’s not a complete full validation that’s required.

**George Cozma: **

Okay. And wrapping up this interview, sort of a final question, what is your favorite type of cheese?

**Ronak Singhal:**

Oh my, you know, I could give you all sorts of cheese stories. My family is huge on cheese. My daughter, in fact, who’s nine, there’s nothing in the world she loves more than cheese. For one of her birthdays, we went to a place that’s no longer here in Portland called the Cheese Bar, which is literally a bar that serve cheese. So we were just in vacation in Europe in August and we went to a place that was similar to that where it is a restaurant with conveyor belts and the conveyor belts bring you cheese that’s paired with something. That’s a huge which kind of cheese you want to have. My personal favorite cheese is a blue cheese from Spain called Val Dione.

**George Cozma:**

Awesome. Blue cheese is not necessarily my favorite cheese, but I can respect it. I can respect it.

**Ronak Singhal:**

So if you want to do a whole other interview on cheese, I’m there for it.

**George Cozma:**

Well, thank you so much for having this interview. Unfortunately, I have to shill hitting the like and subscribe buttons. And there will be a transcript of this on the Chips and Cheese website with links down below. There’s also a [Patreon](https://www.patreon.com/ChipsandCheese) and a [PayPal](https://www.paypal.com/donate?hosted_button_id=4EMPH66SBGVSQ) if you would like to toss us a few bucks if you like what we do and have a good one, folks. Thank you.