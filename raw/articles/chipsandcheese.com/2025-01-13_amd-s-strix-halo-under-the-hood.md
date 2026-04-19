---
title: AMD's Strix Halo - Under the Hood
url: https://chipsandcheese.com/p/amds-strix-halo-under-the-hood
author: George Cozma
published: '2025-01-13'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# AMD's Strix Halo - Under the Hood

Hello you fine Internet folks,

At CES 2025 I got the chance to sit down with Mahesh Subramony, AMD Senior Fellow, to talk about AMD's upcoming Strix Halo SoC which is a brand new type of product for AMD and is the big iGPU SoC that many of us have been waiting for from AMD for a long while.

The transcript below has been lightly edited for readability and conciseness.

**George Cozma:** Hello, you fine internet folks.

We're here at CES 2025 with AMD, and the big AMD announcement was this [points to an ASUS ROG Flow Z13]. Strix Halo is being productized as AMD Ryzen AI Max, and we happen to have a system with one in it! So, but not just that, I happen to have...

**Mahesh Subramony:** I'm Mahesh Subramony, Senior Fellow at AMD.

**George Cozma:** And what do you do at AMD?

**Mahesh Subramony:** I'm a technology advisor for the client business unit. But for the better part of the last decade, I was an SOC architect for chips within AMD.

**George Cozma:** So, let's start with Strix Halo. Let's start with the CPU side, what's different about the Zen 5 here compared to say, I don't know, desktop Zen 5?

**Mahesh Subramony:** Yeah, I mean, first off, I think putting that chip together has been a life's dream over the time. I think ever since we did the merger a long time ago with ATi to bring graphics inhouse, we've always talked about building a big APU of sorts where we could match the CPU performance and the GPU performance on a single package and deliver that in the form factor that you see today.

It took quite a few iterations to kind of get it to where it is right now to get that right value that we could bring to the end user. So it took four iterations to get here, and so we're glad we're here. It had to check a lot of boxes because at the end of the day, it had to meet the needs of the consumer. And so we're very aware of that; the CPUs here, they have the same DNA. It's still Zen5, it's still the same architecture, but we needed to pay more attention to power.

So the CCDs that are featured, to a first order, in the desktop part they have an actual PHY that connects the two dies. And so there’s actually a distance that it needs to travel. It's a [SERDES ](https://en.wikipedia.org/wiki/SerDes)and you're able to go some distance between the two. That's how we've always connected the two. And that's a low cost interface, if you will. It is a high bandwidth interface. But that had low-power states that could only take it so far. And you had retraining and latency implications every time the chip went down and came back up and so on. So for an always-on kind of a desktop kind of machine, that seemed like the best interconnect to connect that as we try to build this into an APU. The first thing we had to do was to change the interconnect between the two dies. And so the CCD that you see here, the core die that you see here, has a different item. That's the first change.

That's a sea of wires. We use fan out, we're for level fan out in order to connect the two dies. So you get the lower latency, the lower power, it's stateless. So we're able to just connect the data fabric through that connect interface into the CCD. So the first big change between a [Granite [Ridge]](https://www.amd.com/en/products/processors/desktops/ryzen/9000-series/amd-ryzen-7-9800x3d.html) or a 9950X3D and this Strix Halo is the die-to-die interconnect. Low-power, same high bandwidth, 32 bytes per cycle in both directions, lower latency. So everything - and almost instant on-and-off stateless - because it's just a sea of wires going across. So it's a little [bit of a tradeoff] of course, the fabrication technology is more expensive than the one over there [points to a 9950X3D], but it meets the needs of the customer and the fact that it has to be a low power that can actually connect.

**George Cozma:** And are the FPUs in the Strix Halo cores the full 512 bit FPU or is it like Strix Point where it's similar to Zen 4 where it's 256 bit?

**Mahesh Subramony:** This machine is intended to be a workhorse. It is a workstation. I almost joke about it saying it's a Threadripper to put in the palm of your hands. So we didn't pull any punches. These have the 512 bit data path. It is a full desktop architecture. We have binned the parts for efficiency. So it might not hit the peak frequency that you would see on the desktop. That's one of the second differences in the cores you would find over here and the cores over there. They're colder, so you get the efficiency that you would like on these parts when you run multithreaded workloads, you're able to get a higher effective frequency on these. But what you give up is some peak frequency, which I think in a thin form factor that you have today, you don't have the thick cooling solutions that you would see on a desktop part anyway. So the demand of the form factor says that you need cores that are cooler, if you will, lower in that FP curve where you can extract efficiency. So these are binned, the same architecture, the same set of pipes, the data parts are the same. The differences are in how we bin the part and how we connect the two parts.

**George Cozma:** Now moving from the CPU over to the big huge SOC tile over here that holds your iGPU, I know that this wasn't mentioned in the slide deck, but there's 32 megabytes of what's known as MALL or infinity cache. How does that react with the CPU cores? Can the CPU cores access that 32 megs of cache?

**Mahesh Subramony:** It cannot. So let me make sure I make that statement very clear. The MALL exists to amplify graphics bandwidth. I think that's the intent of it. So the only compute engine right now… I mean, it's a flexible allocation policy. We should start with that. But the intended way it is configured right now is… writes from source from the GPU installs into the MALL. CPU writes do not install into the MALL. Can we change that with a flip of a bit? But we don't see an application right now where we need to amplify the CPU’s bandwidth.

So we reserve and there were times when we have worked on carve-outs for say, display or video encode/decode to kind of say, hey, look, can I have two slices of the MALL kind of be a place where the VCN or the video encode decoder, the display can kind of play or even the inference engine to store some weights. So we have played around with what can and cannot allocate into that structure. And the way it is defined right now is where only the GPU installs into the MALL. Now… as we explore more and more applications, you know, it's a software release where we can release a firmware that says, hey, look, we have changed the configuration of how the MALL is going to be set up; so much will be reserved for the GPU, and we carve this out for another computer engine and NPU, the video encode-decoder display.

And now you're going to get X amount of speed up X amount of battery life, you know, so on. So any agent can install into it. I want to make sure the flexibility in the architecture exists. But the way it is defined right now… we've run a few use cases, we feel the best use of that MALL is for graphics to use it as a bandwidth amplifier. So graphics is the only compute engine with a flag set where all rights installed into the MALL. Now, the MALL is coherent. So when a CPU access comes in, it does check the MALL to say, is the [cache] line existing over there because it's a right that is waiting to be committed. And it either says no longer because somebody else asked the line. So let's just forward that that data over to whoever asked for it. So it stays coherent. It is part of the coherent fabric.

Every write to memory, there is a lookup into the MALL as well. It's a cache that we need to look up as well. But from a from a point of view as who gets the most benefit from that MALL, it is the GPU; it writes into the MALL, and depending on the traffic pattern, if there are more hits onto the MALL, you get that read bandwidth amplification, which in certain scenarios, we've seen that to be double digit. So we are going from a GDDR memory that exists in a discrete solution to LPDRR. So we understand we are undersized, but the MALL acts as an amplifier. So, for a large GPU we have over here, 40 compute units you know, the perfect use of that MALL is to get that amplification.

**George Cozma:** Speaking of that coherency, is MALL acting as your last layer of coherency for all your compute units?

**Mahesh Subramony:** No, that is still a block in our data fabric that sits right before the memory controller, that acts as the point of coherence. All memory accesses. So memory is divided up based on its interleaving. Here are the different controllers that if you want to access this line, you have to go to this controller, and the data fabric IP that sits right before- it says, any access to whatever is behind me, comes to me. I'm the point of coherence for all lines below. OK. Now, I am going to check the profile structure to see if the CPU has the line. I'm going to check the MALL to see if that has been installed in here by some… all points of coherence run through those data fabric IPs that interface with the memory controllers. So, that stays as the point of coherency.

**George Cozma:** Speaking to again to the data fabric, are you seeing any clock speed benefit from the fact that it's just a sea of wires connecting the CPU to the SOC tile?

**Mahesh Subramony:** We are able to get power benefits. Because, prior to that, we had a GMI PHY that lived in there and that consumed a whole lot of power in order to be able to send this over high frequencies over short distances. Here we are clocking it at… way less than the 20GHz that the GMI was being clocked at. This is anywhere between, you know, one to two gigahertz. You know, really, clockrate matched to the data fabric itself. So there is no asynchronous interface here where you have to pay a whole lot. It's just mapped to-, directly the fabric. So at a lower voltage, you are able to because we used a sea of wires, you are able to get that-, that high bandwidth to match it. We spend the area in terms of the wires that need to come through but we're able to clock it at a meaningfully lower speed so you get the power benefit.

Can we clock this even faster? Well, there would be no need for it if we don't we are not able to clock memory faster as well. Remember, there is no DDR here like on desktop where you have OC and you're able to push this higher and higher. So moving the fabric clock gets you some benefits; this is LPDDR. It's a little tense, tends to be less conducive to overclocking. So being rate matched to memory, in a more power efficient way… that was the target, rather than trying to push the clock. But yeah, we have more flexibility here if you wanted to.

**George Cozma:** And so, sort of to end this conversation back where we started at the CPU with that fabric- how much memory bandwidth can the single CCD access? Since it is 32 bytes per cycle reads.

**Mahesh Subramony:** It really comes down to… We can have a single CCD saturate them. You don't need both. You can have a single CCD saturate data bandwidth. You can have four cores, even two cores if you write the right stream benchmark and saturate data bandwidth, because the CPU can issue a request every cycle. The CCD CPU can request an issue every cycle. So you're going to see that eventually you're going to get picked back by how quickly a response can come back. And a response can come back once every depending on where it goes and how the response comes back. You're eventually going to get clogged by how quickly the memory requests are draining on the on the on the UMC side of the memory controller side. So we have one to two CPUs being able to get close to saturating DRAM bandwidth, with the right stream bandwidth going to open pages and so on and so forth.

But again, with the right mix of the right mix of traffic between reads and writes, like I said, a couple of CPU threads can saturate bandwidth. So it's not… but again, when it comes to bandwidth, we believe that NPU and the GPU are the ones that benefit more than from a CPU standpoint. I think latency, and latency under load - 15 to 20 percent load - but still not have that hockey stick in terms of latency just jumping up. So we're not faking it, that only the first request gets the lowest latency, and everybody else does not take the bypass paths, and pairs base heavy penalty, making sure you have steady low latency for the CPU and high bandwidth for GPU.

**George Cozma:** And to finish off, the most important question, what's your favorite type of cheese?

**Mahesh Subramony:** Gorgonzola. Is that… is that an answer? It's a good answer. The Gorgonzola ravioli [as a] shout out to… to do a restaurant back in my hometown.

**George Cozma:** Thank you so much for this interview. Mahesh.

**Mahesh Subramony:** Always a pleasure. George.

**George Cozma:** Absolutely.

If you like the content then consider heading over to the [Patreon](https://www.patreon.com/ChipsandCheese) or [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks to Chips and Cheese. Also consider joining the [Discord](https://discord.gg/TwVnRhxgY2) and subscribing to the [Chips and Cheese Youtube channel](https://www.youtube.com/@chipsandcheesecc).

AMD really needs a formal Whitepaper with diagrams and such that goes into detail about this IP! There has to be more Whitepaper content published by AMD going forward or it's not going to be easy to see the advantage on the work that AMD is doing!

So he said that single CCD can pull 256 GB/s bandwidth instead 64 GB/s "normal zen5" can pull, and has lower latency than desktop zen5, can you please verify this when you do your Strix Halo tests,

also I hope we get RDNA4 and 5090 tests ( compared to RDNA3 and 4090) soon, most other sites do tests from gaming standpoint, you are only one doing serious GPU compute tests a la AnandTech R.I.P.