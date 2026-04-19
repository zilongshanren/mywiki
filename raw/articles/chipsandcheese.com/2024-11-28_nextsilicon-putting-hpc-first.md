---
title: 'NextSilicon: Putting HPC First'
url: https://chipsandcheese.com/p/nextsilicon-putting-hpc-first
author: George Cozma
published: '2024-11-28'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# NextSilicon: Putting HPC First

### Not an FPGA, not a GPU, but something different!

Hello you fine Internet folks!

At SC24, I got the chance to interview Elad Raz, CEO of NextSilicon which is a startup that is focusing on the HPC market which is unique considering that most of the hardware startups are focusing on AI and Machine Learning.

And the targeting of the HPC market isn't the only thing unique about NextSilicon, they are also taking a different approach with their hardware.

Hope y'all enjoy!

This transcript has been edited for readability and conciseness.

**George Cozma:** Hello, you fine internet folks. We are here at Supercomputing 2024 at the NextSilicon booth and to introduce you guys to NextSilicon, since they have some upcoming announcements, we have--.

**Elad Raz:** I'm Elad Raz. I'm the founder and CEO of NextSilicon and I'm a software engineer and I'm really excited about the Maverick 2 product that's our new chip, 5 nanometer, 108 billion transistors and we are aiming for the Supercomputing conference. We are now live from Atlanta, from SC24, the biggest supercomputering show ever.

**George Cozma:** Oh, yeah. Oh, yeah. Huge this year. Over 17,000 attendees. It's massive. So talk a little bit about NextSilicon and sort of why did you pick HPC, since AI is all the rage today.

**Elad Raz:** So we are next generation compute, starting with accelerated compute portion. And we have a unique architecture in the fact that it can run anything which is massively parallel. We decided to target the supercomputing industry because it's a huge market and under-served market. So Supercomputing is a $50 billion market out of which you have storage, interconnect, all the infrastructure. And when you just count the number of computing chip being sold, the CPUs, the GPUs, other accelerators, it's $20 billion a year. So it's a huge market that you can list up and you have hundreds of AI-specific accelerator and GPUs so I believe as someone who needs to raise hundreds of millions of dollars, it's better to show revenues first and I think that the HPC is a big one. So we decided to start with the HPC industry.

**George Cozma:** Awesome. So talking about your new chip, the Maverick 2, sort of starting out and moving in, [it has] two 100 gig ethernet ports. We've been seeing headlines about 400 and soon 800 gig; 100 gig seems modest. Why is that?

**Elad Raz:** So you need to understand how Supercomputing works unrelated to a machine learning hardware chip. Because in AI chip, you have limited amount of fast memory in the HBM that are in the edges of the chip here. And the HBM has limited capacity. You can put like 2 terabytes of superfast memory on a single chip. Right now the Maverick 2 has 192 gigabyte. There are some flavor that can reach up to 288 gigabyte, which is big. But for 350 billion parameters, for example, assuming FP16, you need a 700 gigabyte. So you can put the entire weight on a single chip. You need a couple of them. And then they need all to communicate with each other in the reduction. So interconnect is superfast.

My previous company got acquired by Mellanox. So I spent a big chunk of my life doing interconnect. For Supercomputing, Infiniband, Ethernet, RDMA over Infiniband, RoCE, RDMA over converged Ethernet. And it's super hard. So the way that you need to think about the product is not that, hey, you're coming with a chip and an interconnect solution. And everyone is going to use your interconnect, which is ethernet-based, and start doing RDMA on that. It's not going to happen. But what it's going to serve is financial sectors. So in financial sector, you have high frequency trading, risk management, that the optimization point is latency rather than throughput. We don't need the 800 gig. What we need is to get a packet going to the processor core really fast and getting it out. So everything I said so far is how you can build a company in incremental steps. Go to the HPC company, generate revenues, then move on to other verticals. And this is how we think about also with the interconnect.

**George Cozma:** And so speaking of interconnecting feeding the chip, and I promise you I'm going somewhere with this, how much bandwidth do you see over the PCIe bus for this chip?

**Elad Raz:** Right. PCIe is limited. PCIe Gen 5 [with] 16 lanes is 64 gigabyte per second. It's not nearly enough to feed data in and out. PCIe Gen 6 is going to be twice as that. And with 112 Gbps lanes, that's not the speed gigabit per second. Yes, you can reach to 256 gigabyte per second with some overhead. Again, your Apple M1 has 500 gigabyte. The M1 has 400 gigabyte. And now with the M4, it's bumped to 500 and something gigabyte per second. 550 per second. So your laptop has more memory bandwidth than the PCIe. So the goal of accelerated compute is dividing the workload that some computation will happen on the host, localized with the host memory, and the majority of the time you want to stay on device, on chip. OK. So it's obviously you want to put the latest and greatest assuming support from the CPU side, CXL, PCIe. But our architecture is not bound by the PCE because we have this smart algorithm that try to figure out what's important and place it on the chip. Now once it's localized on the chip, you stay on the chip.

**George Cozma:** So speaking of the chip, you have up to 6.4 terabytes per second of bandwidth from the HBM's into the chip. How exactly are you using all that bandwidth? So what exactly is that bandwidth accomplishing?

**Elad Raz:** Sure. There were experiments on taking CPUs and adding, instead of DDR, putting an HBM. And users quickly realized that they cannot saturate HBM bandwidth because if you think about it, assuming that CPU can every clock, every clock, issuing a load or restore command to the memory, and you've vectorized everything and it gets 512 bits, OK, maybe you can saturate the HBM, OK? And typically, the CPUs are doing compute and you lose misses. So it's like every one to 16 clocks at 64, 96 cores working in parallel on the HBM. You can't feed them with the latest HBM, OK? We have a different architecture. It's not a processor core. It's hardware accelerator that can issue those wide chunk of memory and feed HBM.

**George Cozma:** So speaking of your architecture, moving in [from the memory system], sort of a yes or no question, is your SRAM distributed between all the different cores?

**Elad Raz:** Yes.

**George Cozma:** Because that's what it looks like here [points to a die shot on the wall].

**Elad Raz: **Yeah, those are the SRAM.

**George Cozma: **So if you have this SRAM and it's moving all this data around, because it's a spatial architecture, what is the NOC, so the network on chip, how much bandwidth does that have to do to move all this data around, say if this core [pointing to a processor unit in the top left quadrant of the chip] needs to access that memory channel [points to a HBM PHY in the bottom right corner of the chip]?

**Elad Raz:** So we call it-- and excuse me for the language like the shit factor, because you don't want that one side of the core will communicate to the other side. You want to keep everything localized. And if you see here, those NOC barriers, those are actually barriers in between. And you get a penalty causing those tiles with each other. OK. So there is a penalty.

And the penalty is measured in latency rather than in throughput. We designed a NOC that you can have a full throughput. But even that, you don't want to walk around and roam around. Yeah, of course I'll achieve. Now most of specialized architecture run a domain-specific language, right? Like you need to write ROCm for AMD or CUDA for Nvidia. And the AI startup, each one has its own language, which is great. And one of the things that you can see in those accelerator is the way that memory works. The reason why you cannot use a C++ or a full-time architecture is because it's not cache coherent. OK? So inside the language, there is a notion of shared memory that's the name in CUDA. In LLVM, it's address space, address space number three, which saying, here is a localized memory. The processor code, talk to that. If you want to go and access another one, you need to do a DMA and move data around. So obviously we have that feature because we can run CUDA and ROCm and other. But what happens if you run a C++ code?

And the last thing about intelligent computer architecture is that you can optimize those features at runtime and localize the data so that each one of those data flow graph will communicate with each other, and the data will stay localized. And yes, if you have an address command once in a while that go to the other chip, you get the latency penalty. But it doesn't matter overall.

**George Cozma:** So now, as you were talking about programs and data, sort of a known quantity with spatial architecture just trying to fit programs onto a chip, historically has been very difficult because you never have enough SRAM to fit an entire program. How are you trying to get around not being able to fit an entire-- so because program is data and you can't fit all of it and you work on data, how are you getting around this?

**Elad Raz:** Yeah. So we have the notion of likely flow and unlikely flows. Likely flows are the computational kernels that happen most of the time. Those are loops. Loops aren't stored inside memory. They are not stored inside SRAM or the HBM. Those are not processor code. I don't have here instructions, fetch usage, and sophisticated branch prediction. They're like, there is no branch predictor whatsoever. There is a data flow. And I have limited-- we don't want to go inside the inner of the architecture. So for now, we just keep it-- I mean, imagine an FPGA, but like FPGA for software, something like that. And the way that it's working is-- the reconfiguration is changing the different ALUs beside each one of those computational graph. And then you etch inside the chip like the function graph. And then you fetch data in as data processing. And every clock, new data coming in, new data coming out. So there is a notion in compiler code, same program, multiple data (SPMD).

So you have exactly some function for example, there is no notion of vectorized instruction shared. There is no very long instruction state because you can have many types on the data flow. I mean, it's just different. And it's like a mindfuck because you need to think about it in a different way. And it's rotating the computing architecture on the side and say, that is the right way to execute massively parallel application. And we were able to crack it down.

**George Cozma:** Awesome. And so our final question, or my final question, is what's your favorite type of cheese?

**Elad Raz:** Well, I will start with the one that I hate the most, which is ricotta. My wife love it. And one time she just put it inside my mouth, and I didn't like it. But I like most of stinky cheese, blue. Danish blue, for example, is my favorite one.

**George Cozma:** We just had another interview where Danish blue came up as their favorite. So thank you so much. Thank you for having me [Elad]. Thank you for watching. Like and subscribe. I know I hate having to show all that, but it does help. And hope you have a good one, folks.

**Elad Raz:** Thank you very much.

To the author thanks a lot for sharing this and for taking the time for the interview.

On the person interviewed... I must say I was very underwhelmed... It sounds like you're hearing politic speeches "yes we have this, that is great, and you will and to use and it's so much better than the others you can't even compare. It's very difficult to understand but we did it"...

I was surprised to see this out of such a high profile individual.

I would have loved to hear a bit more about the actual technical innovations and practical accomplishments.

I would love to see it running actual code. I kind of understood how they adapt the topology to the instruction and data flows, but I suspect software will be the biggest challenge here. In order to have high utilization, it'll need to fine tune not only the topology on the fly, but also the data flowing into the code.