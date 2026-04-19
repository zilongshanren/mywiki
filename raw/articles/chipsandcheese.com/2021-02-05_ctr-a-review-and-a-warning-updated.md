---
title: 'CTR: A Review and a Warning (updated)'
url: https://chipsandcheese.com/p/ctr-a-review-and-a-warning
author: George Cozma
published: '2021-02-05'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Update 5/2/21 1340 GMT: 1usmus himself has replied to our findings; we have included his reply and some points after the conclusion at the end of the article. Article has been edited for clarity.

What is CTR?

Clock Tuner for Ryzen (CTR) is a tool created by Yuri Bubliy, a.k.a. 1usmus, that is designed to auto overclock your Zen 2/3 CPU for you. It is designed to be as simple as clicking the big tune button then applying the profile to your CPU. It claims to do a better job than PBO can, so the staff at Chips and Cheese decided to take it for a spin.

Testing on our 5950X

Our initial testing for this article was with a 5950X, Gigabyte X570 Aorus Master, 64GB of RAM and an Arctic Liquid Freezer II 420. Here is the result of my diagnostic test that you are meant to run first:

Alas, our 5950X only managed a Bronze Rating. The Rating feature is a central component to CTR.

So, with this information in hand I plugged in the values it gave me for P2 into the advanced tuning options. I forgot to take a screenshot for this step, however it gave me the clocks of 4675 MHz for CCD0 and 4475 MHz for CCD1 at a set voltage of 1.25 with High LCC. With these settings the system settled in to about 1.2 volts under a CB23-like load and resulted with a score of 30683:

CTR P2 settings on our 5950X netted 30683.

For comparison, I wanted to try running the same testing using only PBO-applied tuning. Below is the same CB23 run with with PBO. Limits for PBO ran at 280W PPT, 230A TDC, 230A EDC and Curve Optimizer set to -12 All Core in the BIOS. These settings got a score of 29758 at a clock of 4400 MHz across all cores and a voltage of around 1.181V:

Quick PBO auto-OC using Curve Optimizer couldn’t match our initial CTR run.

So from this initial testing, CTR sounds great! More performance at similar voltages and similar power usage… At least in theory it would be.

Real-World Testing and OTP

After applying the P2 tune and the initial P1 profile from the first photo in this article, I decided to run a LinX 10GB run. For me, this is a much better representation of a real-world workload, as it is a very similar workload to the astrophysical simulations I work on. Right away it triggered the CPU’s Over-Temperature Protection (OTP) almost instantly. The highest temperature I saw before the system shutdown was 103.6C as measured by Ryzen Master.

103.6C? What about cooling?

Now, once again the system this was run on was a 5950X on a Gigabyte X570 Aorus Master with 64GB of RAM and an Arctic Liquid Freezer II 420mm. Most importantly the system was effectively an open-air test bench—a Fractal Design Meshify S2 on its side with no side, front, or top panels and the radiator elevated above the system using a plastic bin. As most readers are no doubt aware, open-air systems typically represent the least airflow restriction. The Aorus Master X570 is also regarded as one of the best built AM4 platforms as well, so this was not a case of inadequate cooling or inadequate power delivery from the motherboard.

Now, if was the only thing that CTR had done that wouldn’t warrant the next part of this review…

A Warning

Triggering OTP is not a good thing for a piece of software which is designed to be easily accessible to inexperience overclockers, who don’t necessarily know how to manually overclock their CPU but want more performance than PBO can give.

4650G, We Hardly Knew Ye

However, this piece of software has damaged at least one CPU that I know of by shoving 1.55V into another Chips and Cheesestaff member’s 4650G.

CTR setting 1.55 volts on our 4650G Renoir sample

Previously to this run with CTR, our member’s Renoir sample was able to run 4300 MHz, 100% daily stable at 1.325V. Since the 1.55V incident, this 4650G is no longer able to hold this clock at the same daily-safe voltages and most telling of all, CTR has downgraded the rating on this Renoir from a Silver Sample to a Bronze Sample:

Prior to CTR applying 1.55V to the 4650G, our Renoir was rated as a Silver sample.

After CTR applied 1.55V to the 4650G, CTR now claimed it was a Bronze sample—evidence of degradation that we would later verify with manual OCing.

The number of 1.55 volts also happens to be the max voltage allowed by the VID tables for Renoir, which means that the software maxed out the VID tables—implying there are no safeties that have been built into prevent overvolting the CPU.

VID tables do not go higher than 1.55V.

The triggering of OTP on my 5950X, the overvolting of our staff member’s 4650G and further reports online of CTR causing black screens and BSODs for other users has led us to an inescapable conclusion.

CTR – Much Riskier than PBO

The basic premise of this software, where all you have to do is push a few buttons and automatically your CPU is running better than ever before, is one I think is great.

CTR has some neat features, like showing you the numbers that the CPU uses to determine what cores are best on your CPU, or the undervolting feature that lets you keep most—if not all—of your CPU’s performance while reducing the heat output. However as shown here, there are risks to using this software if you are inexperienced with overclocking.

It must be said in fairness that, in the end, these feats are nothing that PBO can’t do and though PBO also voids your warranty, in my opinion, it is a much safer option. CTR in its current state is an experimental program that can produce good results but can also potentially ruin an 800 US dollar CPU.

So, at this time neither I nor the Chips and Cheese staff can recommend CTR for anyone to use on your primary computer, especially the target audience of CTR, who may want to take a shortcut in tuning their Ryzen CPU. For those who see how long manual tuning is taking and leave the program to do the auto overclocking, you risk coming back to an irreparably damaged CPU or a tune that is not stable in anything heavier than Cinebench.

If you just want to tinker with the program on a secondary computer or a test system with a CPU that you are willing to ruin, that’s the only place where I personally would use CTR; otherwise I would avoid it and just use PBO.

Update: 1usmus’ comment and our Response

Since posting this article we received a direct response from 1usmus in the comments of this article. We have taken the decision to remove parts of these comments, as they contained a direct attack on our staff and a highly derogatory term. We have posted a censored version below instead. I would hope in future that when 1usmus receives criticism, he can meet it with his own constructive criticism instead of immediately resorting to insults.

With regards to the comment, here it is below with the derogatory term censored out:

“Thanks to people like you, ******, who do not read the manual, there will always be problems. The bronze or silver category depends on the operating voltage! The processor can be on the border between categories from the beginning! The category is affected by dozens of factors such as AGESA, garbage in the operating system, unstable RAM, CPU temperature, VRM settings, VRM temperature, BIOS setting, test time and many other factors. A processor is not a streetcar that rides the rails! And it’s written in the manual.

1.55 can only be obtained in two cases:

1)you didn’t read the manual and use manual voltages in the BIOS. 2) you didn’t read the manual and were running another application while CTR was running.

CTR is equipped with a protection system that will not allow damage to the processor. But you also did not read this because it is written in the manual. To my great regret your processor didn’t burn out.

One more thing, Linx is NOT AVX Light.

And most importantly, you did not manage to damage the processor. You demonstrated this fiasco in the screenshots. Fluctuation of the diagnostic results within 4% is normal, as the diagnostic step lasts only 1 minute, not 1 hour. One minute is enough just to estimate an approximate value :)”

1usmus’ response in our comments section.

Whilst it is appreciable that there will be many factors influencing the ratings given by CTR, the fact is the degradation implied by our 4650G dropping from a Silver to Bronze rating has been verified as true with manual overclocking, which means that CTR was able to damage the processor. If CTR features a protection system, it is clear that this did not work effectively to prevent damaging this processor unintentionally.

It must also be noted the owner of the 4650G is not inexperienced in any sense and has overclocked AMD and Intel processors on many occasions over a number of years, and using CTR is the first have they experienced degradation on any of their CPUs. Manual voltages in BIOS were not used during the use of CTR, nor were other applications running outside those needed (such as Ryzen Master). To say that you wished their processor had burnt out shows your contempt for those who criticize you.

Regarding the use of Linx, when testing CTR we were unable to change the testing mode away from AVX Light. This means that we were unable to check what the CTR recommended settings would be for an AVX Heavy workload.

Testing mode box is greyed out; only AVX Light selectable.

Finally, throughout his response, 1usmus makes it clear that it is expected that users will fully read the manual included with CTR to make sure they do not damage their processor and get the best results. This goes directly against the idea that this is a simple “one click” overclocking tool for Ryzen processors. If a user must read through a manual to understand how the application works and to use it safely, then a large part of the reputation that this application has is completely baseless and 1usmus needs to make this clear to the community in future releases.

Response written by Joshua on behalf of George and Zack.