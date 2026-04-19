---
title: An Interview with Intel’s Arik Gihon about Lunar Lake at Hot Chips 2024
url: https://chipsandcheese.com/p/an-interview-with-intels-arik-gihon-about-lunar-lake-at-hot-chips-2024
author: George Cozma
published: '2024-09-02'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# An Interview with Intel’s Arik Gihon about Lunar Lake at Hot Chips 2024

For today’s article we have another video interview for you folks, this time with Arik Gihon from Intel where we talk about Lunar Lake.

Before we get into the video and the transcript, I would just like to give a massive thank you to all of you who have donated to Chips and Cheese. Without y’all we would have not been able to afford to get the camera equipment as well as the audio equipment needed to film this interview as well all of the future interviews we do!

The transcript below has been edited for readability and conciseness.

**George Cozma:**

Hello, you fine Internet folks. Today, we have Arik from Intel who gave a presentation, as of the recording of this video, yesterday about Lunar Lake. Arik, would you like to tell the audience what you do at Intel and what part of Lunar Lake you, were a part of?

**Arik Gihon:**

Yeah so, I work at Intel, as an SoC architect. I’m leading the SoC architect team that brings all the definition to the client CPUs. We worked at Lunar Lake for the last 3 years as a team. I was leading the team, the architecture team, definitions from the early definition of Lunar Lake till the execution, the project, and now we are at high volume manufacturing.

**George Cozma:**

Awesome. Now just jumping straight into it, starting from the cores. You decided to use a version of Lion Cove that doesn’t have SMT. And we’ve heard from other folks in the industry that SMT is a good way to get more performance for the same power. So why was SMT removed if that is in fact the case or is that not the case?

**Arik Gihon:**

So the statement is not, accurate, completely. So SMT is a good feature for scaling, multi thread. So if you’re running 2 threads on the same core, then you could get additional nT performance by not increasing the power so much, and therefore, you are increasing the performance by a similar mode. It used to be more than it is now, like, 30ish percent of additional performance, so they’re now in the order of 20ish percent.

But, since we have added the SMT, a while back, things had changed. And we have, added, high level architecture in which we are scaling multi thread, via E-cores. And it’s a much more efficient way to scale multi threading. And therefore today, if we want to have single thread running efficiently on the core, one of the way to do that was to remove SMT and build a much more efficient core that can deliver the IPC in a lower power.

**George Cozma:**

Speaking of those E-cores on Lunar Lake, you’ve moved all the e cores off of the ring because previously in Meteor Lake you had E-cores on the CPU tile and then your low power E-cores on the SOC tile. You’ve moved that all just to the low power island. What was the reasoning behind that?

**Arik Gihon:**

Correct. Actually, it’s happened already in the previous generation in which, there was a change of, putting 2 LP E-cores outside the ring [and] outside the compute die. We have optimized it further, and indeed, we have put 4 E-cores outside the ring in Lunar Lake configuration and this was, in order to improve efficiency. You know, you have the Ring plus the last level cache in which it gives you benefits on certain cases while it is, costly on other cases.

And when we want to take Lunar Lake into a low power envelope, it we actually benefited quite a lot by doing so, in latency, memory, and as well as power overhead versus the additional IPC that the last level cache gives you.

**George Cozma:**

And on caching [structure], with the new P-cores, you now have a new intermediate L1 [cache]. Now that you have essentially 4 data side caches and the SLC cache, how do you think that will impact programs that are more latency sensitive?

**Arik Gihon:**

It’s a good question. I’m not sure it will affect [latency], it’s actually improving latency. It’s improving, like, several cycles to the original L1 cache.

**George Cozma:**

So it’s effectively in some ways helping latency because it’s moving stuff that might have been moved into the L2 back closer to the core.

**Arik Gihon:**

Correct. And that’s actually, I showed the latency graphs in the presentation and some of the things that you could see there on the lower buffer sizes that you could see the improvements in latency in the big core versus the previous generation of Redwood [Cove].

**George Cozma:**

That memory side cache that’s brand new for Lunar Lake, what are the expected bandwidth and latency characteristics of that memory side cache compared to, say, if it was an L4 on top of the already existing L3 for the CPU?

**Arik Gihon:**

So it comes to me the, at least the memory bandwidth that we have.

**George Cozma:**

So it’s more balanced towards reducing memory operations.

**Arik Gihon:**

Correct.

**George Cozma:**

And what is the expected reduction of memory operations because of that?

**Arik Gihon:**

So it really depends on the workload [and] the footprint [of the application] and depends on how much you can fit into the cache, and it varies. There are workloads that significantly get from that, as we allocate more into the system cache and others that fit less so it really depends.

**George Cozma:**

So speaking of workloads, would that also include the iGPU? Like, is the iGPU a big user of that memory side cache?

**Arik Gihon:**

No it’s not due to the footprint [of applications that use the iGPU].

**George Cozma:**

Interesting. And sort of on the GPU side, what’s interesting is that in Meteor Lake, you guys had sort of a slightly cut down version of the ray tracing cores; but in Lunar Lake, you guys have a essentially the full fat ray tracing core. Why did you move to the full RT core when it seems like iGPUs don’t really have the performance to extract from RT, why would why the added expense of the full fat RT cores, was it to reduce valid validation time?

**Arik Gihon:**

No. Some of the architecture just utilized the hardware better, so it enables using the RT better and therefore in Lunar Lake it is being used.

**George Cozma:**

Again, back to the previous generation, you had a GPU, tile, an SOC tile, and an iGPU tile. On Lunar Lake, that’s now all been reintegrated on to a single die. What was the why move back to a more monolithic design for those parts of the design?

**Arik Gihon:**

Yeah. So it was a trade off, actually. When you start building the project, you start to think which transistor you want to put on which node. And since we have selected the entry, we could fit, more transistors into entry in one monolithic die. And the second is that it was an optimized die just for a specific segment.

You don’t need to stay for the entire family and up to desktops with that. And also, we could just put all of the transistors, all of the compute transistors, on the same die very close to the memory and therefore gain latency and gain performance. So you both gain good process for all of those as well as for the SoC components and the memory components, and closer to the memory.

**George Cozma:**

And so then sort of a follow-up to that, why did you leave the what you’re calling the platform controller die, as its own separate die? Was that because the stuff on that die doesn’t scale as well with newer nodes?

**Arik Gihon:**

It just didn’t need to scale. Those transistors are usually controllers for IOs. They can fit nicely into N6’s process, and the IOs are working there very good. So it was a nice partition.

**George Cozma:**

Okay. And speaking of IO, why PCIe 5? Why move to PCIe 5 for Lunar Lake? Because I know that some folks have said PCIe 4 is more power efficient than PCIe 5. So why the move on a what’s a low power product?

**Arik Gihon:**

If you have the SSDs which are Gen 5 and you want to connect them you can enjoy the additional bandwidth even if those are less efficient.

**George Cozma:**

And I guess sort of a final question is, what’s your favorite type of cheese?

**Arik Gihon:**

Kashkaval.

**George Cozma:**

Nice. Well, that ends our interview with Arik. Thank you for watching. Unfortunately, I do have to shill the hit the like and subscribe button. And if you would like a transcript, there will be a transcript on the site and if you would like to donate, there’s a [Patreon](https://www.patreon.com/ChipsandCheese) and a [PayPal](https://www.paypal.com/donate?hosted_button_id=4EMPH66SBGVSQ). Thank you, Arik, for this interview and have a good one y’all.