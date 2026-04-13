---
title: Network latencies and speed of light
url: https://fgiesen.wordpress.com/2018/01/20/network-latencies-and-speed-of-light/
published: '2018-01-20'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Network latencies and speed of light

In this short post I’m going to attempt to convince you that current network (Internet) latencies are here to stay, because they are already within a fairly small factor of what is possible under known physics, and getting *much* closer to that limit – say, another 2x gain – requires heroics of civil and network engineering as well as massive capital expenditures that are very unlikely to be used for general internet links in the foreseeable future.

This is a conversation I’ve had a few times in my life, usually with surprised conversation partners; last year I happened to write a mail about it that I’m now going to recycle and turn into this blog post so that in the future, I can just link to this if it ever comes up again. :)

When I originally wrote said mail in October 2017, I started by pinging `csail.mit.edu`

, a machine that as far as I know (and Geo-IP services are with me on this one) is actually at MIT, so in Cambridge, MA. I did this sitting at my Windows work machine in Seattle, WA, and got this result:

Pinging csail.mit.edu [128.30.2.121] with 32 bytes of data: Reply from 128.30.2.121: bytes=32 time=71ms TTL=48 Reply from 128.30.2.121: bytes=32 time=71ms TTL=48 Reply from 128.30.2.121: bytes=32 time=70ms TTL=48 Reply from 128.30.2.121: bytes=32 time=71ms TTL=48

Ping times are round-trip times and include the time it takes for the network packet to go from my machine to the MIT server, the time it takes for the server to prepare a reply, and the time for said reply to make it back to my machine and get delivered to the running `ping`

process. The best guess for a single-way trip is to just divide the RTT by 2, giving me an estimate of about 35ms for my ping packet to make it from Seattle to Boston.

Google Maps tells me the great circle distance from my office to Cambridge MA is about 4000km (2500 miles, if a kilometer means nothing to you). Any network packets I’m sending these days over normal network infrastructure are likely to use either optical fiber (especially for long-distance links) or copper cable as a transmission medium. The rule of thumb I learned in university that effective signal transmission speed over both is about 2/3rds of the speed of light in vacuum. This is called the [velocity factor](https://en.wikipedia.org/wiki/Velocity_factor); that article has some actual numbers, which work out to 0.65c for Cat-6A twisted pair cable (used for 10Gbit Ethernet), 0.64c for Cat-5e (1Gbit Ethernet), and 0.67c for optical fiber, all of which are close enough to each other and to the aforementioned 2/3c rule of thumb that I won’t bother differentiating between different types of cables in the rest of this post.

Divide our distance of 2500mi by 2/3c, we get about 4×106m / (2×108 m/s) = 2 × 10-2 s = 20ms. That is the transmission delay we would have for a hypothetical optical fiber strung along the great circle between Seattle and Cambridge, the shortest distance between two points on a sphere; I’m neglecting height differences and Earth being not quite spherical here, but I’m only doing a back-of-the-envelope estimate. Note that the actual measured one-way latency I quoted above is already well below twice that. Hence my earlier comment about even a factor-of-2 improvement being unlikely.

Now, if your goal is actually building a network (and not just a single point-to-point link), you don’t want to have long stretches of cable in the middle of nowhere. Again as per Google Maps, the distance from Seattle to Cambridge actually driving along major roads is about 4800km (3000mi). So in this case, we get about 20% extra “overhead” distance from building a network that follows the lay of the land, goes through major population centers, and doesn’t try to tunnel below the Great Lakes or similar. That’s a decent trade-off when your plan is to have an actual Internet and not just one very fast link. So this extra 20% overhead puts our corrected estimate of transmission delay along a more realistic network layout at about 24ms.

That means that of our approximately 35ms one-way trip, 24ms is just from physics (speed of light, index of refraction of optical fiber) and logistics (not having a full mesh of minimum-distance point-to-point links between any two points in the network). The remaining 11ms of the transit time are, presumably, spent with the packets briefly enqueued in some routers, in signal boosters and network stacks. These are the parts that could be improved with advances in network technology. But even reducing that part of the cost to zero still wouldn’t give us even a full 1.5× speed-up. And that’s why I think mainstream network tech isn’t going to get that much faster anytime soon.

What if we *are* willing to pay up and lay a private dedicated fiber link for that distance (or use some dark fiber going the right direction that’s already there)? That’s still using mainstream tech, just spending money to reduce the fraction of time spent on sub-optimal routing (physical route that is) and in the network, and it seems likely that you could get the RTT to somewhere between 45ms and 50ms using regular fiber if you were willing to spend the money to set it up (and maintain it).

But that’s still assuming using something as pedestrian as fiber (or copper cable), and actually sticking to the surface of the Earth. Going even further along the “money is no object” scale, and edging a teensy bit into Bond Villain territory, we can upgrade our signal velocity to full light speed and also get rid of pesky detours like the curvature of the Earth by digging a perfectly straight tunnel between the two points, keeping a vacuum inside (not strictly necessary, but might as well while we’re at it) and then establishing a *really* high-powered microwave link; it would have to be to make it along a distance of a few thousand kilometers, given beam divergence. Keeping in theme, such a link would then also be attractive because the transceivers at either end because a sufficiently high-powered microwave transmitter should make for a serviceable death ray, in a pinch. More seriously, high-powered point-to-point microwave links are a thing, and are used in very latency-sensitive applications such as high-frequency trading. However, as far as I know (which might be wrong – feel free to correct me!), individual segments typically span distances of a few miles, not tens of miles, and definitely not hundreds. Longer links are then built by chaining multiple segments together (effectively a sequence of repeaters), adding a small delay on every split, so the effective transmission speed is definitely lower than full speed of light, though I don’t know by how much. And of course, such systems require uninterrupted lines of sight, which (under non-Bond-villain conditions) means they tend to not work, or only work in a diminished capacity, under bad weather conditions with poor visibility.

Anyway, for that level of investment, you should be able to get one-way trip times down to about 12ms or so, and round-trips of around 24ms. That is about 3× faster than current mainstream network tech, and gets us fairly close to the limits of known physics, but it’s also quite expensive to set up and operate, not as reliable, and has various other problems.

So, summarizing:

- If you have a good consumer/business-level Internet connection, ping someone who does likewise, and there are no major issues on the network in between, the RTTs you will get right now are within about a factor of 3 of the best they can possibly be as per currently known physics: unless we figure out a way around Special Relativity, it’s not getting better than straight-line line-of-sight light-speed communication.
- If you’re willing to spend a bunch of money to buy existing dark fiber

capacity that goes in the right direction and lay down some of your own

where there isn’t any, and you build it as a dedicated link, you should be able to get within 2× of the speed of light limit using fairly mainstream tech. (So about a 1.5× improvement over just using existing networks.) - Getting substantially better than that with current tech requires

major civil engineering as well as a death ray. Upside: a death ray is its own reward.

Microwave communications is a seriously old tech (developed in the 30s, ubiquitous since the 50s), not the “New Kid On The Block” some people want to make it appear as.

In telecom older, lower band width links tend to be longer (like a few dozen km), the new ones use higher frequencies and don’t get as far (I’m told 10 km is already stretching it). Transmitter power is tiny, about the same as a cell phone. The antenna makes all the difference.

The blogger “Sniper In Mahwah” has published a lot of details about microwave HFT networks. It seems the HFT guys are able to cross the English Channel with a reach of something like 80 km perhaps.

Here’s a related write-up with some interesting details: https://tabbforum.com/opinions/high-speed-trading-lines-radios-and-cables-oh-my?print_preview=true&single=true

This was both informativ and hilarious (death ray, lol).

“What if we are willing to pay up and lay a private dedicated fiber link” actually happened, it is the first chapter of a book called “Flash Boys”. Someone was willing to do exactly what you describe, building a slightly shorter fiber line between Chicago and New York, shaving a few ms in latency over existing telecom routes. And then charging everyone 10x more, which Wall Street gladly paid.

Amazon has the chapter available for reading: https://www.amazon.com/Flash-Boys-Wall-Street-Revolt-ebook/dp/B00HVJB4VM

I know that’s a thing, same as dedicated Microwave links are a thing, but neither of those are common for regular Internet backbones, and for cost reasons are unlikely to become so in the foreseeable future.

The UK used to have a national microwave network for phones and TV – in the 1980s my family lived close to the Charwelton relay station. The typical link length in the network was about 50 miles – see https://en.wikipedia.org/wiki/British_Telecom_microwave_network for details and a sketchy map.

You’re exactly right, as far as your analysis goes. Without huge expenditure of money, your latency can’t get much better than ~70 msec round trip between the two coasts,

But most people are suffering with latencies of hundreds of msec when there’s traffic on their line. Here’s how to see if you’re afflicted.

– Start your ping test, as you have done

– Start a speed test at your favorite site (DSLReports.com is mine)

– If your latency/ping times change significantly, you have Bufferbloat

Learn more at bufferbloat.net, especially how to fix it

Great post except that your assumptions regard the internet as a single network. This is not the case. The internet is a network of networks. The “distance” between two points on the internet can vary greatly based on who your internet provider is and who the provider of the other end point is.

For example, driving distance from Richmond, VA to Kansas City, MO is about 1100 miles. However, the network path from Richmond to Kansas City may route from Richmond to Atlanta to Chicago to Dallas to Kansas City (exactly the case for one of our remote offices with only two internet providers in the loop: Windstream and Hurricane Electric). The distance of the actual drive times between those cities is 2750 miles. You can verify this with traceroute (or tracert for Win folk).

The rest of what you say is right because, well, it’s science.

I was talking about lower bounds. The actual topology of the Internet is irrelevant here because all it can do is cause extra increases over that lower bound.