---
title: 'AMD''s Freshly-baked MI350: An Interview with the Chief Architect'
url: https://chipsandcheese.com/p/amds-freshly-baked-mi350-an-interview
author: George Cozma
published: '2025-06-20'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# AMD's Freshly-baked MI350: An Interview with the Chief Architect

Hello you fine Internet folks,

At AMD's Advancing AI 2025, I had the pleasure of interviewing Alan Smith, AMD Senior Fellow and Chief Instinct Architect, about CDNA4 found in the MI350 series of accelerators.

Hope y'all enjoy!

Transcript below has been edited for conciseness and readability.

**George:** Hello you fine internet folks! We're here today at AMD's Advancing AI 2025 event, where the MI350 series has just been announced. And I have the pleasure to introduce, Alan Smith from AMD.

**Alan:** Hello, everyone.

**George:** What do you do at AMD?

**Alan**: So I'm the chief architect of Instinct GPUs.

**George**: Awesome, what does that job entail?

**Alan**: So I'm responsible for the GPU product line definition, working with our data center GPU business partners to define the-, work with them on the definition of the requirements of the GPUs, and then work with the design teams to implement those requirements.

**George:** Awesome. So, moving into MI350: MI350's still GFX9 based, and- for you guys in the audience, GFX9 is also known as Vega, or at least derivative of GFX9. Why is it that MI350 is still on GFX9, whereas clients such as RDNA 3 and 4, GFX11 and 12 respectively?

**Alan:** Sure, yeah, it's a great question. So as you know, the CDNA architecture off of, you know, previous generations of Instinct GPUs, starting with MI100 and before, like you said, in the Vega generations, were all GCN architecture, which was Graphics Core Next. And over several generations, CDNA's been highly optimized for the types of distributed computing algorithms for high-performance computing and AI. And so we felt like starting with that base for MI350 would give us the right pieces that we needed to deliver the performance goals that we had for the MI350 series.

**George:** And with GCN, as you know, there's a separate L1 cache and LDS, or Local Data Store. Why is that still in MI350? And why haven't they been merged?

**Alan:** Yeah, so like you said, you know, it is a legacy piece of the GCN architecture. It's sort of fundamental to the way the compute unit is built. So we felt like in this generation, it wasn't the right opportunity to make a microarchitectural change of that scale. So what we did instead, was we increased the capacity of the LDS. So previously in MI300 series, we had a 64 kilobyte LDS, and we've increased that capacity to 160 kilobytes in MI350 series. And in addition to that, we increased the bandwidth as well. So we doubled the bandwidth of the LDS into the register file, in order to be able to feed the Tensor Core rates that we have in the MI350 series.

**George:** And speaking of Tensor Cores, you've now introduced microscaling formats to MI350x for FP8, FP6, and FP4 data types. Interestingly enough, a major differentiator for MI350 is that FP6 is the same rate as FP4. Can you talk a little bit about how that was accomplished and why that is?

**Alan:** Sure, yep, so one of the things that we felt like on MI350 in this timeframe, that it's going into the market and the current state of AI... we felt like that FP6 is a format that has potential to not only be used for inferencing, but potentially for training. And so we wanted to make sure that the capabilities for FP6 were class-leading relative to... what others maybe would have been implementing, or have implemented. And so, as you know, it's a long lead time to design hardware, so we were thinking about this years ago and wanted to make sure that MI350 had leadership in FP6 performance. So we made a decision to implement the FP6 data path at the same throughput as the FP4 data path. Of course, we had to take on a little bit more hardware in order to do that. FP6 has a few more bits, obviously, that's why it's called FP6. But we were able to do that within the area of constraints that we had in the matrix engine, and do that in a very power- and area-efficient way.

**George:** And speaking of data types, I've noticed that TF32 is not on your ops list for hardware level acceleration. Why remove that feature from... or why was that not a major consideration for MI350?

**Alan:** Yeah, well, it was a consideration, right? Because we did remove it. We felt like that in this timeframe, that brain float 16, or BF16, would be a format that would be leverageable for most models to replace TF32. And we can deliver a much higher throughput on BF16 than TF32, so we felt like it was the right trade off for this implementation.

**George:** And if I was to use TF32, what would the speed be? Would it still be FP32, the speed of FP32?

**Alan:** You have a choice. We offer some emulation, and I don't have all the details on the exact throughputs off the top of my head; but we do offer emulation, software-based emulation using BF16 to emulate TF32, or you can just cast it into FP32 and use it at FP32 rate.

**George:** And moving from the CU up to the XCD, which is the compute die; the new compute die's now on N3P, and yet there's been a reduction from 40 CUs to 36 CUs physically on the die with four per shader engine fused off. Why 32 CUs now, and, why that reduction?

**Alan:** Yeah, so on MI300, we had co-designed for both MI300X and MI300A, one for HPC and one for AI. In the MI300A, we have just six XCDs. And so, we wanted to make sure when we only had six of the accelerator chiplets that we had enough compute units to power the level of HPC or high-performance computing - which is traditional simulation in FP64 - to reach the performance levels that we wanted to hit for the leadership-class supercomputers that we were targeting with that market.

And so we did that and delivered the fastest supercomputer in the world along with Lawrence Livermore, with El Capitan. But so as a consideration there, we wanted to have more compute units for XCD so that we could get 224 total within MI300A. On 350, where it's designed specifically as an accelerator only, a discrete accelerator, we had more flexibility there. And so we decided that having a power of two number of active compute units per die - so 36 physical, like you said, but we enable 32. Four of them, one per shader engine, are used for harvesting and we yield those out in order to give us good high-volume manufacturing through TSMC-N3, which is a leading edge technology. So we have some of the spare ones that allow us to end up with 32 actually enabled.

And that's a nice power of two, and it's easy to tile tensors if you have a power of two. So most of the tensors that you're working with, or many of them, would be matrices that are based on a power of two. And so it allows you to tile them into the number of compute units easily, and reduces the total tail effect that you may have. Because if you have a non-power of two number of compute units, then some amount of the tensor may not map directly nicely, and so you may have some amount of work that you have to do at the end on just a subset of the compute unit. So we find that there's some optimization there by having a power of two.

**George:** While the new compute unit is on N3P, the I/O die is on N6; why stick with N6?

**Alan:** Yeah, great question. What we see in our chiplet technology, first of all, we have the choice, right? So being on chiplets gives you the flexibility to choose different technologies if appropriate. And the things that we have in the I/O die tend not to scale as well with advanced technologies. So things like the HBM PHYs, the high-speed SERDES, the caches that we have with the Infinity Cache, the SRAMs, those things don't scale as well. And so sticking with an older technology with a mature yield on a big die allows us to deliver a product cost and a TCO (Total Cost of Ownership) value proposition for our clients. And then we're able to leverage the most advanced technologies like N3P for the compute where we get a significant benefit in the power- and area-scaling to implement the compute units.

**George:** And speaking of, other than the LDS, what's interesting to me is that there have not been any cache hierarchy changes. Why is that?

**Alan:** Yeah, great question. So if you remember what I just said about MI300 being built to deliver the highest performance in HPC. And in order to do that, we needed to deliver significant global bandwidth into the compute units for double precision floating point. So we had already designed the Infinity Fabric and the fabric within the XCC or the Accelerated Compute Core to deliver sufficient bandwidth to feed the really high double precision matrix operations in MI300 and all the cache hierarchy associated with that. So we were able to leverage that amount of interconnecting capabilities that we had already built into MI300 and therefore didn't need to make any modifications to those.

**George:** And with MI350, you've now moved from four base dies to two base dies. What has that enabled in terms of the layout of your top dies?

Alan: Yeah, so what we did, as you mentioned, so in MI350, the I/O dies, there's only two of them. And then each of them host four of the accelerator chiplets versus in MI300, we had four of the I/O dies, with each of them hosting two of the accelerator chiplets. So that's what you're talking about.

So what we did was, we wanted to increase the bandwidth from global, from HBM, which, MI300 was designed for HBM3 and MI350 was specially designed for HBM3E. So we wanted to go from 5.2 or 5.6 gigabit per second up to a full 8 gigabit per second. But we also wanted to do that at the lowest possible power, because delivering the bytes from HBM into the compute cores at the lowest energy per bit gives us more power at a fixed GPU power level, gives us more power into the compute at that same time. So on bandwidth-bound kernels that have a compute element, by reducing the amount of power that we spend in data transport, we can put more power into the compute and deliver a higher performance for those kernels.

So what we did by combining those two chips together into one was we were able to widen up the buses within those chips; so we deliver more bytes per clock, and therefore we can run them at a lower frequency and also a lower voltage, which gives us the V-squared scaling of voltage for the amount of power that it takes to deliver those bits. So that's why we did that.

**George:** And speaking of power, MI350x is 1000 watts, and MI355x is 1400 watts. What are the different thermal considerations when considering that 40% uptick in power, not just in terms of cooling the system, but also keeping the individual chiplets within tolerances?

**Alan:** Great question, and obviously we have some things to consider for our 3D architectures as well.

So when we do our total power and thermal architecture of these chips, we consider from the motherboard all the way up to the daughterboards, which are the UBB (Universal Baseboard), the OAM (OCP Accelerator Module) modules in this case, and then up through the stack of CoWoS (Chip on Wafer on Substrate), the I/O dies, which are in this intermediate layer, and then the compute that's above those. So we look at the total thermal density of that whole stack, and the amount of thermal transport or thermal resistance that we have within that stack, and the thermal interface materials that we need in order to build on top of that for heat removal, right?

And so we offer two different classes of thermal solutions for MI350 series. One of them air-cooled, like you mentioned. The other one is a direct-attach liquid cool. So the cold plate would then, in the liquid cool plate, liquid-cooled case would directly attach to the thermal interface material on top of the chips. So we do thermal modeling of that entire stack, and work directly with all of our technology partners to make sure that the power densities that we build into the chips can be handled by that entire thermal stack up.

**George:** Awesome, and since we're running short on time, the most important question of this interview is, what's your favorite type of cheese?

**Alan:** Oh, cheddar.

**George:** Massively agree with you. What's your favorite brand of cheddar?

**Alan:** I like the Vermont one. What is that, oh... Calbert's? I can't think of it. [Editor's note: It's Cabot Cheddar that is Alan's favorite]

**George:** I know my personal favorite's probably Tillamook, which is, yeah, from Oregon. But anyway, thank you so much, Alan, for this interview.

If you would like to support the channel, hit like, hit subscribe. And if you like interviews like this, tell us in the comments below. Also, there will be a transcript on the Chips and Cheese website. If you want to directly monetarily support Chips and Cheese, there's Patreon, as well as Stripe through Substack, and PayPal. So, thank you so much for that interview, Alan.

**Alan:** Thank you, my pleasure.

**George:** Have a good one, folks!

No MI350A (or MI350C) makes me sad... Oh well...

Thanks for the interview. And another year of death, taxes and GFX9 😂

Truly the most eternal of gpu architectures