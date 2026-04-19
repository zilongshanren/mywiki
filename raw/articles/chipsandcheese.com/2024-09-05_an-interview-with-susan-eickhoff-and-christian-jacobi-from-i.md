---
title: An Interview with Susan Eickhoff and Christian Jacobi from IBM at Hot Chips
  2024
url: https://chipsandcheese.com/p/an-interview-with-susan-eickoff-and-christian-jacobi-from-ibm-at-hot-chips-2024
author: George Cozma
published: '2024-09-05'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# An Interview with Susan Eickhoff and Christian Jacobi from IBM at Hot Chips 2024

This is our second video interview from Hot Chips 2024 and this time I got to sit down with Susan Eickhoff and Christian Jacobi from IBM to talk about their brand new Telum II processor and Spyre AI cards from the development process to the architecture of said chips.

Note: This was the first video recorded with the new equipment so there were some audio issues, which at this point is becoming a running theme at this point. So a massive thanks to the folks that managed to recover the audio from the recording!

The transcript below has been edited for readability and conciseness.

George Cozma:

Hello, you fine Internet folks. We are here at Hot Chips, which is one of the premier architectural events for IEEE. And with me, I have Christian and Susan from IBM. Would you like to introduce yourself today?

Susan Eickhoff:

Hi. I’m Susan Eickhoff. I’m the director of IBM’s in processing development out in Poughkeepsie, New York.

Christian Jacobi:

And I’m Christian Jacobi. I’m an IBM fellow and the CTO for IBM Systems Development.

George Cozma:

So, a couple questions for y’all. Your new Telum II chip that you’re announced here at Hot Chips is going to your next gen Z Systems mainframe. Susan question for you, what was the development process from Telum I moving to Telum II? So what, what design choices were made from data that you’ve gathered from Telum I chips and customers?

Susan Eickhoff:

Yep, that’s a really good question. I think something that a lot of people don’t have visibility into. So for us overall, it’s a 5 year period for when we start concept until we’re able to actually offer a product there.

And given that what we are developing is for the mainframe, like you said, there are some consistent pillars that are always there, needing to have high reliability and scalability and performance. Sustainability has become a big pillar, recently. And then we also have this kind of rolling refactoring we do as every generation or processor we release so that we can balance innovating in the core, the nest, or the IO space and still keeping stability for clients. So kind of using those as, some high level tenets there. We start working with our internal architects and also different stakeholders within IBM.

So experts in the crypto space or in the AI space, and we heavily codevelop with clients as well. We have a very strong, active client base there that, you know, they know what’s working for them or areas they wanna develop in. So kinda using the standard areas we always look at. And then, like I said, working with different architects and clients, we start about 5 years early going through our concept phase and mapping out, what the design for Telum II or for Spyre is gonna be. But that being said, especially in the AI space, that is obviously rapidly evolving, so it’s hard to predict 5 years in advance exactly, what the client is gonna need or exactly where the industry is.

So while we have our design, the concept there laid out at the beginning, we still have to be adaptable and flexible and adjust to as we continue to hear back from clients. Because with the 5 year design cycle, the prior generation isn’t even out yet when we start on the next one. So it’s also still a flexible iterative process there.

George Cozma:

Speaking of Telum II, one of the new additions that you guys have added is a DPU. So why exactly, to you, Christian, what exactly is the DPU for, and why did you decide to put it on the processor side?

Christian Jacobi:

Yeah. Our clients, on mainframe systems are running enormous numbers of transactions through the system every day. And, of course, you can imagine that that level of scale also drives significant IO. And so we have very optimized enterprise class IO protocols for storage, network, etcetera, that that have sort of enterprise qualities when it comes to virtualization and error recovery scenarios, etcetera. We looked into how would we implement the next generation of that.

And the concept of DPUs is something that’s now widespread in the industry. So we looked at what we could do with DPUs. And as we were investigating that, we realized that the best place for a DPU for our use case, sort of on our side of the PCI interface so that the communication that happens between the main workloads and the IO protocols, we can shorten that by coherently attaching the DPU into the cache architecture.

And so now the DPU and the main processors can talk sort of at cache latency and cache bandwidth instead of talking through the PCI interface. And then the DPU kind of becomes that middle piece where all these protocols get implemented and then connect through the PCI bus to the actual network adapters or storage adapters. But, that’s the essence of it is that the DPU can implement those protocols with firmware and optimize the latency between the main workloads.

George Cozma:

Speaking of Telum’s cache hierarchy, you guys have a very unique cache hierarchy. You have a private L2 that also acts as a virtual L3. And then moving on to sort of the CPU drawer that you have in, in the Z system, virtual L4. Susan, what drove those decisions sort of in the first place? Was that customer driven data or is that IBM internal data or was that sort of a combination of them?

Susan Eickhoff:

Combination of both. In the end, always an iterative process there. Some of the things that we had mentioned is always needing to get more performance. So being able to grow our cache is allows us to get to get better performance there, but then also being able to utilize, you know, what is kind of a, by default, the L1, L2 cache, then you can have this virtual L3 [and] L4 cache, which are innovations that we can continue to enhance and optimize with each generation as we go on.

George Cozma:

And to you, Christian, what what’s the if there is an added complexity to having a virtual L3 versus just sort of a your older version, z14, z13, where you had just a standard L3 level cache? So there’s pros and cons in in any design point, of course.

Christian Jacobi:

Right? The way we had designed the cache architecture previous to Telum I, including the z15 generation, was that we had dedicated physical L3 and L4 caches, and we managed them as inclusive caches, meaning that whatever is in the cache, say, the L1 is also in the L2 and in the L3 and what’s in the L2 is also in the L3 and L4.

And because the caches got so big, the L2s got really big, the L3s got really big. You’re basically just storing the same data multiple times, and you’re not really getting the effectiveness of all of that physical cache space. And so when we invented the, the virtual cache hierarchy where we say, okay, all the physical caches are level 2 caches to the cores and now the DPU, but we know that not all cores are using their level 2 cache at the same rate at any point in time. So we can kind of donate space from 1 core to another as we, through heuristics, figure out which caches are hot and which caches are colder. We could actually optimize the redundancy of cache lines in the overall cache real estate.

And in that way, get a much more effective, larger cache, than we could with the with the prior design point. And so on Telum I, we ended up with, like, a 2 gigabyte virtual L4, which is more than double what we had on z15. And now we’ve grown it to 2.8 gigabytes on Telum 2. It just shows that that sort of platform that we’ve built from which we can iteratively innovate. Like Susan was saying, that has really worked out for us.

George Cozma:

Continuing on with that, I noticed that you have 10 36 megabyte L2 slices. However, only none appear to be attached to a direct core to the DPU. That is that 10th there for redundancy, or is it there for just sort of an act just to make everything square?

Christian Jacobi:

It’s additional cache capacity. Right? If you think about how the virtual L3 concept really works. If you just had a regular L3, like a physical dedicated L3, depending on which core is how active, the cores would take sort of different slices out of that cache dynamically. And we’re trying to replicate that same mechanism with the virtual L3 where through, like I mentioned, heuristics, when a core needs to cast out a cache line, we bring something new in, something else needs to go. It can look around and see, is there some other L2 cache that’s not as busy that could become my cast out partner where I can push that cache line into? And now we have this 10th L2 on the chip, and it just doesn’t get any traffic from its nonexistent core.

So it will always look like a relatively cold cache, and therefore, we can become sort of the cast out partner that consumes, cache lines that other L2s are pushing out. And then, of course, by pushing cash lines into that 10th L2, it kind of warms up itself, and then it gets balanced out with all the other caches on the chip.

George Cozma:

A big topic here at Hot Chips and sort of around the industry is, of course, artificial intelligence, AI. And in Telum I, you had the you added a AI processor to the Telum I chip. Susan, how often do your customers use AI in their workloads? How why was it changing to be architected with a single accelerator for the entire chip instead of, say, one accelerator per core.

Susan Eickhoff:

Right. So, I mean, as you said, we introduced that on Telum I. And so, again, going back to you have a 5 year design cycle. Right? You’re many years back now at this point when we were going through the concept phase for Telum I. And at that point, sure, you start to get we have as a mainframe, you have tremendous amounts of data that’s going there, transactions that are going through there. So, again, you look at the everything going on in the AI space and that additional, intelligence analytics that that, you know, could potentially bring to clients seemed like a very fertile space for to innovate there.

So we had added that on to for Telum I. And, you know, like I said, it’s a for the first question there, there’s, innovations that the engineers do, but then there’s also feedback that we get from clients. So with Telum I, we have a 175 clients with over 200 different use cases that they’re using, and some of that is still prototype, but some of those are actually being used out on their customer workloads. And so as we again get feedback from them, what is working, how do we need to tailor that, 2 clear themes that came back where we need more AI compute capacity, and we need the ability to support large language models. So that’s it fed into how we design Telum II and then also the addition of the Spyre AI accelerator.

George Cozma:

Speaking to having a single AI accelerator on a chip, Christian, how do you do time slicing? Because if one core needs access and then another bird needs access, do you sort of split compute, or can you do some other method?

Christian Jacobi:

Yeah. [Although] I wanna step back and set the context a little bit more. Right? Mainframes are executing data serving and transaction processing workloads. Right? They process, like, 70% of the world’s financial transactions. And our goal is to enrich to enable our clients to enrich those workloads with AI. But that doesn’t mean that AI is the primary workload.

The primary workload is databases, transaction processing, etcetera. And then AI becomes a part of that. And so when we defined Telum I, we were looking at, should we add an AI engine to every core? And when we looked at that, well, if you’re running whatever 90% of your time in database and transaction processing code and maybe 10% of your time you’re doing AI, once you have it only in the you know, spread around in every core, then that workload would only get its share in terms of total compute capacity. Instead, what we said is, let’s not do that.

Let’s put a consolidated area on the chip as the AI engine. And then when the software needs to do AI, it gets that full compute capacity, not only one end of it that would be allocated to the core, but the complete compute is available. And that’s how we can minimize the latencies for when these workloads do AI somewhat sporadically spread out through the rest of the workload. The downside is if now your AI takes on a significant percentage of the total workload that you get into sort of this time slicing question that you’re asking. Right?

And the way we did this on Telum I is we said, well, we’re kind of early, and the adoption is gonna grow over time, but it’s not gonna be, like, instantaneous that many, many clients have tons and tons of AI. So we said, okay. We’ll just time slice when a second core comes in and wants to do AI. It has to wait for the current operation, not the whole AI inference, but the current operation of, like, a matrix multiplication to finish before the second core gets access to the accelerator. Now that we see increased demand for AI and we have forecast that it’s gonna keep growing faster and faster, we did 2 things for Telum II.

We quadrupled the compute capacity of each AI accelerator on the chip. But then to address the time slicing question, we also enable now to use neighboring chips’ AI capabilities. So when a core comes in and the local AI engine is busy, it can use the cache fabric that interconnects all the chips to kind of attach to a neighboring AI accelerator and perform its AI function there. And so in essence, we’re making the pool much broader, much larger pool of AI compute that each core can tap into, to further reduce the probability of ever running into such a time slicing issue.

George Cozma:

Question for you, Susan. Can you continue on with that? Larger pool of AI and with your new Spyre AI accelerator, you can have up to 8 in a pool essentially with up to 1 terabytes of memory. Was that essentially that memory design decided in order to be able to fit bigger models onto these accelerators?

Susan Eickhoff:

Yes. I mean, in a nutshell, yes.

George Cozma:

And sort of where do you see your clients’ models moving towards in terms of size? So like 10 billion, 30 billion, or say 200 billion.

Susan Eickhoff:

I’ll let CJ field that one.

Christian Jacobi:

So we’re seeing we’re seeing really 2 kinds of use cases that we’ve designed Spyre for. Right?

We have the first use case, which is the ensemble method of AI, where you combine a traditional AI model like a, you know, LSTM or CNN, that runs on the Telum II Processor. And then when that has low confidence in its prediction, say, it’s not entirely sure, maybe only 90% sure whether a credit card transaction is fraudulent or not, you would then, do a second screening of the transaction, on a more complex model, and that could be, for example, like a 100 million parameter BERT model. Those are still relatively small models in the in the grand scheme of things, but they are much more capable in terms of accuracy than the very small traditional AI models. But then we have the second use case of, generative AI where we want to use, for example, large language models for code generation or code explanation, code transformation. And so that’s when we can cluster up to 8 cards, as you were saying, to get [increased] memory size, but maybe more importantly to the compute capacity and the memory bandwidth that gets aggregated across those 8 cards to get to a nice user experience in terms of tokens per second.

And that’s where that design comes from, that we that we have relatively small models that can run on single Spyre cards, well, then the generative models that can run on clusters of Spyre cards.

George Cozma:

Question for you Susan is, was spire developed roughly at the same time as telling to in terms of the sort of development process or were they, sort of, segregate in terms of where they started, and now they’re sort of coming together at the same time.

Susan Eickhoff:

Yeah. I mean, I’ll say, segregated, although they started to come together towards the end.

So, I mean, that that base piece of IP that’s on the Telum I AI Accelerator, on Telum II, on Spyre, that is all common there. And so we knew, again, all the way starting back with Telum I and now Telum II, we would continue to make enhancements there and improve that that base core there. But then I said as we got more feedback from clients on needing to add even additional AI compute capacity and the large language models that generated AI that we had, it made sense to broaden that partnership that we had with our research team to take the prototype, I’ll call it, that they had been working on, you know, what became Spire, and actually work with them to get that to the enterprise grade level that we need for our clients, and codevelop that to actually get that to productize in concert with Telum II.

George Cozma:

And are you seeing any customers that are buying Telum II as well as buying Spyre alongside it in the next generate like, is that what your prediction is? Is that they’re going to buy both the next generation of z that has Telum II as well as a cabinet of Spyre?

Susan Eickhoff:

I mean, we tailor very much to whatever our individual client needs are. So we have or the next generation z, you’ll have a 192 PCIe slots, which are filled with an array of networking and storage and the Spyre AI cards. So combinations and, again, very tailored to what that client’s needs are.

George Cozma:

So what you’re saying is that not all z systems are it may be z systems as a whole, but there are different models z.

Susan Eickhoff:

There’s different configurations.

George Cozma:

So just like the classic server realm where there’s multiple configurations of a server. Well, I guess I have only 2 questions, one for each of you, and that is, what’s your favorite type of cheese?

Susan Eickhoff:

What’s my favorite type of cheese? I did not see that question coming. I’m not gonna lie.

George Cozma:

I am obligated to ask.

Susan Eickhoff:

I’m gonna go with Gruyere at the moment.

Christian Jacobi:

Parmigiano.

George Cozma:

Good choices. Well, that wraps up our interview with IBM. Thank you so much, Susan and Christian. And if you would like some more interviews. Unfortunately, I have to shill hitting the like button and subscribe button. We are also going to have a transcript of this interview on the website. And if you’d like to donate, there’s a [Patreon](https://www.patreon.com/ChipsandCheese) and a [PayPal](https://www.paypal.com/donate?hosted_button_id=4EMPH66SBGVSQ). As well as, one more interview or a few more interviews from hot chips. So look forward to that. Have a good one y’all.