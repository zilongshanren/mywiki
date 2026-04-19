---
title: AMD’s Past and Future CPUs (Formal Retraction)
url: https://chipsandcheese.com/p/amds-past-and-future-cpus
author: George Cozma
published: '2021-02-05'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# AMD’s Past and Future CPUs (Formal Retraction)

**Editor’s Note**: With the release of our Zen 4 article, I issued a formal retraction of this article. When I originally wrote this article I had a very different vision of what Chips and Cheese would be, a much less technical website that would be for all intents and purposes no better than a rumor mill. The criticism from both inside and outside Chips and Cheese due to this article caused me to rethink what I wanted Chips and Cheese to be. I am so glad that I did rethink what Chips and Cheese would become because I can truly say that I am proud of what not just me, but the entire team here at Chips and Cheese have created with our deep diving of microarchitecture.

The original text of this article will remain up, and starts below this note, as a reminder to myself of how sometimes rethinking decisions is the best option.

**Original Text:**

Less than half a decade ago, if you had walked up to someone in the industry and said that in 5 years’ time AMD would have the fastest CPUs, you would have been laughed straight out of the room—but here we are.

At the time of writing, AMD *does* have the fastest CPUs on the market with Zen 3, so let’s see where AMD is heading in the future.

## The Ugly Past

It’s not a controversial statement for me to say that the Bulldozer family of CPUs was a failure. Not just a commercial failure in a period that eventually saw AMD nearing bankruptcy, but also a technical failure. There are however parts of the Bulldozer core that are good such as the FPU and branch predictor unit. Weaknesses in its shared front-end and poor cache/memory systems meant a 4-module Bulldozer CPU lost to a 4-core Sandy Bridge CPU in most workloads, despite the higher clocks. Insult to injury for AMD was the the fact that a 4-module Bulldozer CPU also consumed more power than a 4-core Sandy Bridge CPU while being slower—in short the architecture was almost universally panned.

However, the failure of Bulldozer was not all because of poor CPU design. A lot of Bulldozer’s failures can be traced to its underperforming 32nm node from what was AMD at the time, before its fabs were spun off into Global Foundries. Broadly, the original design goals for Bulldozer were 33% clock speed lift over Phenom on the same 45nm node with no IPC decrease and a release date in 2009. As history shows, this did not happen and so nearly two years later in October 2011, Bulldozer became the product we all know it as: late, hot and slow.

Thankfully for AMD, when the original Zen architecture released in Q1 2017 it finally showed they weren’t out of the CPU game. Zen 1 had an extremely bullish **40% IPC **increase design goal over Excavator and ultimately delivered an **unheard of 52%** **IPC gain**. AMD was back. Following up with Zen 2 and Zen 3, though they were not the same monstrous uplifts as Zen 1, they represented a respectful 15% and 19% IPC gain over their predecessors respectively. But y’all know that already, so let’s talk about the future of AMD’s CPUs.

## A Bright Future

AMD looks poised for even more continued success with Ryzen, assuming of course that the information and sources that both I and the rest of Chips and Cheese’s staff have access to are accurate. Please take all the following information in this section with the usual cautionary dose of salt. While both the Chips and Cheese team and I have full belief that this information is accurate, that does not mean that this is 100% confirmed and you should not take this as unsalable truth. With this disclaimer out of the way, on to the juicy bits: Zen 3+, Zen 4 and even Zen 5.

### AM5 & DDR5 – New IOD and Future Nodes

Zen 3+ looks to be a small IPC gain on base Zen 3, having been told “It’s more than Zen+ was [over Zen 1] but not much” which I interpret to mean around a 4 to 7% IPC gain along with customary clock gains moving to the smaller N6 node from TSMC. N6 is a variant of N7 using 5 layers of EUV and is not a true “new node”, more of a refinement. However, the most interesting thing to me is that Zen 3+ on desktop may be the first AM5 CPU. I was told that the IO die for Zen 3+ desktop is using “Not quite [the same] IOD as Zen 4 but uses Zen 4 IP” which I take to mean that it will be using DDR5 and it will be on the same node as Zen 4’s IOD. That’s all I have on Zen 3+, so now on to Zen 4.

Zen 4 is what a lot of people are waiting for, and, if the info I have is accurate, that wait will prove to be even more worth it. It is important to note that the one common thread in all Zen 4 chatter I have heard is resounding positivity. From IPC gains over 25%, a total performance gain of 40%, and even possibly (finally) 5GHz all-core thanks to the new (full node) N5 fabrication at TSMC! Now, I can’t say what is true and what is an over-exaggeration, however I was told from a trusted source that a **Genoa** engineering sample (Zen 4 server chip) was **29% faster** than a Milan (Zen 3) chip with the same core config at **the** **same clocks**. Factor this in with what I have heard about the possible clock gains that N5 will enable over N7 and Zen 4 sounds like it is going to be a **monster** of a CPU.

Now I said I had Zen 5 info, unfortunately this comes from a different, less-proven source than my Zen 4 info, however they have said that the jump [to Zen 5 from 4] from will be about as much as **Piledriver to Zen 1 design goal, which if you recall to earlier in this article was 40%**. I was told from a 3rd source that Zen 5’s original design goal was 2.5 to 3 times the IPC of Zen 1 which roughly lines up with the perspective of a “Piledriver to Zen 1”-like jump.

## Looking Forward… AMD’s Problem is Success

If this info is all true, then that puts AMD in a very good position from a performance standpoint. However, the biggest problem for AMD of late hasn’t been one of performance but of wafer supply. With Apple moving off of Intel CPUs and onto their own silicon for (gradually) their entire lineup, the supply of N5 wafers from TSMC for AMD will be less than if Apple had stuck with Intel. Being that AMD is always 2nd in line for new nodes at TSMC behind Apple, this may be a cause for concern moving forward.

### Bright Spot: Consoles Out of the Picture with TSMC N5

However, perhaps an even bigger factor for availability on TSMC N5 will be that neither future AMD CPUs nor GPUs will need to compete with console chips as they will remain on N7. Couple this with the rumors that AMD GPUs are also going MCM with RDNA3, and it is possible that Zen 5 and RDNA 3 supply will be better than what we know of the current shortages for Zen 3. This is especially important for the GPU side seeing the current availability issues around RDNA2; the wafer allocation of which has been said to represent low-single digits of TSMC’s N7 supply. This is all of course, wishful thinking. At this point in time, who knows.

One thing is certain however: AMD’s future looks bright.

## Author’s Note (2/8/21)

There was a miscommunication between myself and the editor with regards to the performance claims of Zen 4. The only thing that we are claiming with any level of certainty is the claim of a Genoa ES sample being 29% faster then Milan at the same clocks.

We apologize for any confusion this may have caused.