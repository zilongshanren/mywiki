---
title: Diving into Qualcomm's Upcoming Adreno X2 GPU with Eric Demers
url: https://chipsandcheese.com/p/diving-into-qualcomms-upcoming-adreno
author: George Cozma
published: '2026-01-04'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Diving into Qualcomm's Upcoming Adreno X2 GPU with Eric Demers

Hello you fine Internet folks,

Today we are talking about Qualcomm's upcoming X2 GPU architecture with Eric Demers, Qualcomm's GPU Team lead. We talk about the changes from the prior X1 generation of GPUs along with why some of the changes were made.

Hope y'all enjoy!

The transcript below has been edited for readability and conciseness.

George: Hello you fine Internet Folks. We’re here in San Diego at Qualcomm headquarters at their first architecture day and I have with me Eric Demers. What do you do?

Eric: I am an employee here at Qualcomm, I lead our GPU team, that’s most of the hardware and some of the software. It’s all in one and it’s a great team we’ve put together and I have been here for fourteen years.

George: Quick 60 second boildown of what is new in the X2 GPU versus the X1 GPU.

Eric: Well, it’s the next generation for us, meaning that we looked at everything we were building on the X1 and we said “we can do one better”, and fundamentally improved the performance. And I shared with you that it is a noticeable improvement in performance but not necessarily the same amount of increase in power. So it is a very power-efficient core, so that you effectively are getting much more performance at a slightly higher power cost. As opposed to doubling the performance and doubling the power cost, so that’s one big improvement, second we wanted to be a full-featured DirectX 12.2 Ultimate part. So all the features of DirectX 12.2 which most GPUs on Windows already support, so we’re part of that gang.

George: And in terms of API, what will you support for the X2 GPU?

Eric: Obviously we’ll have DirectX 12.2 and all the DirectX versions behind that, so we’ll be fully compatible there. But we also plan to introduce native Vulkan 1.4 support. There’s a version of that which Windows supplies, but we’ll be supplying a native version that is the same codebase as we use for our other products. We’ll also be introducing native OpenCL 3.0 support, also as used by our other products. And then in the first quarter of 2026 we’d like to introduce SYCL support, and SYCL is a higher-end compute-focused API and shading language for a GPU. It’s an open standard, other companies support it, and it helps us attack some of the GPGPU use-cases that exist on Windows for Snapdragon.

George: Awesome, going into the architecture a little bit. With the X2 GPU, you now have what’s called HPM or High-Performance Memory? What exactly is that for and how is it set up in hardware?

Eric: So our GPUs have always had memory attached to them. We were a tiling architecture to start with on mobile which minimises memory bandwidth requirements. And how it does it is by keeping as much on chip as possible before you send it to DRAM. Well, we’ve taken that to the next level and said “let’s make it really big” and instead of tiling the screen just render it normally but render it to an on-chip SRAM that is big enough to actually hold that whole surface or most of that surface. So particularly for the X2 Extreme Edition we can do a QHD+ resolution or 1600p resolution, 2K resolutions, all natively on die and all that rendering, so the color ROPs, all the Z-buffer, all of that is done at full speed on die and doesn’t use any DRAM bandwidth. Frees that up for reading on the GPU, CPU, or NPU. It gives you a performance boost, but saving all that bandwidth gives you a power boost as well. So it’s a performance per Watt improvement for us. It isn’t just for rendering and is a general purpose large memory attached to your GPU, you can use it for compute. You could render to it and then do post-processing with it still in the HPM using your shaders. There’s all types of flexible use-cases that we’ve come up with or that we will come up with over time.

George: Awesome, going into the HPM, there’s 21 megabytes of HPM on an X2-90 GPU. How is that split up? Is it 5.25 MB per slice and that slice can only access that 5.25 MB or is it shared across the whole die?

Eric: So physically it is implemented per slice. So we have 5.25 MB per slice. But no, there’s a full crossbar because if you think about it as a frame buffer there’s abilities to go fetch out of anywhere. You have random access to the whole surface from any of the slices. We have a full crossbar at full bandwidth that allows the HPM to be used by any of the slices, even though it is physically implemented inside the slice.

George: And how is the HPM set up? Is it a cache, or is it a scratchpad?

Eric: So the answer to that is yes, it is under software control. You can allocate parts of it to be a cache. Up to 3 MB of color and Z-cache. Roughly 1/3rd to 2/3rds and that’s typically if you’re rendering to DRAM then you’ll use it as a cache. The cache there is for the granularity fetches so you’ll prefetch data and bring them on chip and decompress the data and pull it into the HPM and use it locally as much as you can then cache it back out when you evict that cache line. The rest of the HPM will then be reserved for software use. It could be used to store nothing, it could be used to store render targets, you could have multiple render targets, it could store just Z-buffers, just color buffers. It could store textures from a previous render that you’re going to use as part of the rendering. It’s really a general scratchpad in that sense that you can use as you see fit, from both an application and a driver standpoint.

George: What was the consideration to allow only three megabytes of the SRAM to be used as cache and leave the other 2.25 MB as a sort of scratchpad SRAM? Why not allow all of it to be cache?

Eric: Yeah, that’s actually a question that we asked ourselves internally. First of all, making everything cache with the granularity we have has a cost. Your tag memory, which is the memory that tells you what’s going on in your cache grows with the size of your cache. So there’s a cost for that so it’s not like it’s free and we could just throw it in. There’s actually a substantial cost because it also affects your timing because you have to do a tag lookup and the bigger your tag is the more complex the design has to be. So there’s a desired limit at which beyond it’s much more work and more cost to put in. But we looked at it and what we found is that if you hold the whole frame buffer in HPM, you get 100% efficiency. But as soon as you drop below holding all of it, your efficiency flattens out and your cache hit rate doesn’t get much worse unless the cache gets really small and it doesn’t get much better until you get to the full side. So there’s a plateau and what we found is that right at the bottom of that plateau is roughly the size that we planned. So it gets really good cache hit-rates and if we had made it twice as big it wouldn’t have been much better but it would have been costlier so we did the right trade-off on this particular design. It may be something we revisit in the future, particularly if the use-cases for HPM change but for now it’s the right balance for us.

George: And sort of digging even deeper into the slice architecture. Previously, a micro-SP which is part of the slice. There’s two micro-SPs per SP and then there’s two SPs per slice.

Eric: Yeah.

George: The micro-SP would issue wave128 instructions and now you have moved to wave64 but you still have 128 ALUs in a micro-SP. How are you dealing with only issuing 64 instructions per wave to 128 ALUs?

Eric: I am not sure this is very different from others, but we dual-issue. So we will dual-issue two waves at a time to keep all those ALUs busy. So in a way it’s just meaning that we’re able to deal with wave64 but we’re also more efficient because they are wave64. If you do a branch, the smaller the wave the less granularity loss you’ll have, the less of the potential branches you have to take. Wave64 is generally a more efficient use of resources than one large wave and in fact two waves is more efficient than one wave and so for us keeping more waves in flight is simply an efficiency improvement even if it doesn’t affect your peak throughput for example. But it comes with overhead, you have to have more context, more information, more meta information on the side to have two waves in flight. One of the consequences is that the GPRs our general purpose registers where the data for the waves is stored. We had to grow it roughly 30% from 96k to 128k. We grew that in part to have more waves, both to deal with the dual-issue but just having more waves is generally more efficient.

George: So how often are you seeing your GPU being able to dual-issue? How often are you seeing two waves go down at the same time?

Eric: All the time, it almost always operates that way. I guess there could be cases where there are bubbles in the shader execution where they are both waiting and in which case neither will run. You could have one that gets issued and is ready earlier, but generally we have so many waves in flight that there’s always space for two to run.

George: Okay.

Eric: It would really be the case if you had a lot of GPRs used by one wave and that we do not have enough, and normally we have enough for two of those but you might be throttling more often in those cases because you just don’t have enough waves to cover all the latency of the memory fetches. But that’s a fairly corner case of very very complex shaders that is not typical.

George: So the dual-issue mechanism doesn’t have very many restrictions on it?

Eric: No, no restrictions.

George: Cool, thank you so much for this interview. And my final question is, what is your favourite type of cheese?

Eric: That’s a good question. I love Brie, I will always love Brie … and Mozzarella curds. So, I grew up in Canada and poutine was a big thing and I freaking loved Mozzarella curds and it’s hard to find them. The only place I found them is Whole Foods sometimes, but Amazon, surprisingly, I have to go order them so that we can make home-made poutine.

George: What’s funny is Ian, who’s behind the camera. He and I, he’s Potato, I’m Cheese.

Eric: There you go.

George: We run a show called the Tech Poutine, and the guest is the Gravy.

Eric: Ah, there you go, and the gravy is available. Either Swiss chalet, or I forget the other one, but they’re all good. And Five Guys in San Diego makes the fries that are closest to the typical poutine fries. And I actually have Canadian friends that have gone to Costco and gotten the cheese there and then gone to Five Guys, gotten the fries there and made the sauce just to eat that.

George: Thank you so much for this interview.

Eric: You’re welcome.

George: If you like content like this, hit like and subscribe. It does help with the channel. If you would like a transcript of this, that will be on [chipsancheese.com](http://chipsancheese.com) as well as links to the Patreon and PayPal down below in the description. Thank you so much Eric.

Eric: You’re welcome, thank you.

George: And have a good one, folks.

Did Eric comment on Qualcomm's work on drivers for applications and games? I believe that the underwhelming GPU performance of the first generation of the Snapdragon Elites/Extremes really hurt their uptake.

And, while this question runs a bit counter to Eric's job at Qualcomm😄, did he mention anything regarding the use of their new SD Extremes with a dGPU in the system? Is that or will that be supported?