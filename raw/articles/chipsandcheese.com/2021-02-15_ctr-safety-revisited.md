---
title: CTR Safety, Revisited
url: https://chipsandcheese.com/p/ctr-safety-revisited
author: Chips; Cheese
published: '2021-02-15'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

There are times when being a journalist is exciting. Your team writes something important, people engage with it and it generates a large response. Unfortunately, those are often the exact situations where emotions run high. If you write glowingly about how great a product is, the competition cries foul and suddenly you’re biased. If you write critically about a product’s flaws, then creators are upset and you’re biased again (or incompetent).

It’s all very normal, but good journalism is trying to keep things objective in pursuit of the truth, to the benefit of our readers.

Today in this follow-up article, we will share some of the developments in the situation and do our best to address some of the passionate questions and hot topics that arose in the debate following our original CTR article. You can look forward to some responses from the author of CTR, (Yuri Bubliy a.k.a. “1usmus”), more testing results, responses from respected overclocking experts, and an official statement from AMD. Last and certainly not least of all, our continuing balanced assessment of CTR for you, the reader.

CTR 2.0’s Built-in Testing

Revisiting the topic of CTR’s safety, our first point of investigation is CTR 2.0’s built-in stability testing.

CTR 2.0, the version we originally tested in our first article, is lacking the ability to select different levels of AVX workload intensity that it can use during it’s built-in tests. Instead of defaulting to a safer and more rigorous Heavy AVX option, it instead defaults to—and indeed only allows—the aptly named Light AVX mode. The issue with this default/limitation is that it allows for potentially impossible clock speeds and settings that aren’t stable at heavier loads, meaning under CPU stress you face an almost guaranteed possibility of overheating.

This is especially important for higher core count CPUs on setups with good enough cooling to mask the issue while testing at these low loads. When higher loads kick in, these ‘test stable’ settings then overwhelm the CPU and cooling system with excessive clock speed and voltage resulting in high temperatures. This imperfect ‘light test only’ is made more complicated by the lack of AVX heavy mode, workaround for which is to: “increase the voltage … by 75-100mV and then manually test stability for these cases.” The issue is compounded here, as the light testing does not stress the CPU enough to warn CTR awayfrom higher voltages, so adding more voltage will just compound the high-load temperature situation more:

If I could find fault with anything, it would only be the persistent lack of an “AVX Heavy” test mode. Even though only a very small part of the user base might have a use for this, such edge cases can often become critical. If you start a heavy AVX workload like Prime95 small-ffts with AVX or LinpackXtreme, the system always crashes with an “AVX Light” tested profile. The only workaround is to increase the voltage for the P1 and P2 profiles by 75-100 mV and then manually test for stability for these cases. For the vast majority of games and applications you wouldn’t need it, of course, but if you did need it, you’d wish you’d known about it beforehand.

As per Igor’s Lab review of CTR 2.0, ~100mV may be needed for AVX Heavy stability.

What’s possibly coolable at 1.250V may be impossible for the cooling solution to handle at 1.350V. This is where another advantage of AMD’s Precision Boost methods come in: it dynamically adjusts both clock speed and voltage based on temperature and power draw, something a static all-core overclock cannot do. This is the reason that a Ryzen CPU using PBO idling at 1.45v isn’t a degradation risk: because even a minor multi-core load sees the voltage drop; under heavy loads you can see it drop to 1.100V or less. Contrast that to a static overclock like CTR applies, which sets a single clock and voltage per profile—they don’t change. We would also like to add that rather common workloads like video compression are also AVX heavy, especially with more modern codecs, which would mean seemingly unrealistic scenarios attained by Prime95 Small FFT or Linpack Extreme can be very good indicators of realistic voltage and stability requirements.

‘A year at 1.55V’ – Not Dangerous, or a Disaster? It’s Complicated

Our original CTR article centered on risks around the way the program tests, tunes and sets voltages. Chiefly we suffered degradation on our Renoir 4650G sample after being given 1.55V by CTR. After posting the article, we were happy to get a response from CTR’s creator, Yuri, himself. Unfortunately, he did not agree with our conclusions that even a short exposure to this voltage could be the source of OC variance we verified after the incident:

Yuri Bubliy’s (1usmus) response re: 1.55V applied by CTR damaging our Ryzen 4650G, which is made on TSMC’s 7 nanometer process. Comment made on our original CTR article.

While we don’t care much if people call us or our sources names, we do have a passion and a responsibility for telling you objectively good information. We think there are some corrections needing to be addressed here.

Degradation and Process Explored

The degradation process is a very long process, if you run the processor for a year at 1.55 [volts], the maximum degradation will be about 100 MHz.

Yuri Bubliy on 1.55V’s effects on a TSMC N7 Renoir 4650G.

Degradation isn’t always slow. We could talk about this one for many pages (really!) and there are large groups of very smart people working on this exact issue at every electronics or chip manufacturing company. It’s complicated. It’s varied. It’s even hard to exactly predict for a single device but we do know unequivocally that the speed of degradation is increased as voltage goes up and transistor/device size shrinks. You can certainly degrade a CPU or GPU in a single session, even without killing it completely. Degradation is a death race of time and voltage that we overclockers play with. We just try to stay out of the fastest lanes unless we have a spare CPU or are running for that one-shot world record.

For those interested in some of the hairy details (serious math time warning), you can see that degradation is positively correlated to both current density and temperature. The below image, copied from Wikipedia, shows Black’s Equation: a mathematical model for the MTTF (Mean Time To Failure) of a semiconductor circuit due to electromigration. Black’s Equation demonstrates that MTTF decreases (life span shortens) with an increase in current density and device temperature:

Black’s Equation for electromigration’s effect on MTTF.

So, higher density in current voltage is a primary factor in elecromigration for semiconductors. It must be understood that not all processor architectures, and most importantly, all fabrication process nodes, handle voltage the same. All Ryzen processor cores present in Zen 2 and Zen 3 designs are fabricated on TSMC’s seven nanometer ‘N7’ node. It is a cutting edge process, currently among the smallest and densest in production. This means that a dense node like N7 is already ‘stacking the deck’ in regards to risk for electromigration. The other half in this equation then, is voltage.

Is 1.55V Safe or not?

Yuri’s comment that 1.55V would only cause degradation slowly over the period of about a year, seems to be in direct contradiction to the manual for CTR, written by Yuri:

As for the safe voltage and AVX Light load, it’s simple. I don’t recommend going over the 1.35V mark if you are using a fairly aggressive LLC mode. If it is a loyal mode (Auto) – maximum safe voltage will be about 1.412 – 1.425V. Anyway, CTR will tell you what to do.

Yuri’s words in his CTR guide.

Our hope is that Yuri’s inconsistency between these two statements comes down to some simple late night typos. In addition, CTR will warn you if you key in greater than 1.35V. However, it will auto-tune above that 1.35V without warning you. This hypocritical behavior of the software’s auto-tune (which is typically favored by users with less experience, and therefore more at risk to not understand the danger) is concerning.

The maximum danger is from the highest voltage. What is the highest voltage in the Renoir VID table? Yes, it’s 1.55V, which is what CTR pushed into the 4650G during its automated tuning. It may have been fine for some workloads because it wouldn’t generate too much heat and/or it wasn’t sent through certain chip sections at all or for as long. Remember that wafer-level components are worn out faster with higher temperature, higher density and longer exposure. So, a CPU is stressed the most when running AVX Heavy or other instruction streams designed to continuously exercise as many wafer-level components as possible.

Ryzen Community Weighs In

We reached out to some overclocking experts for comment on 1.55V in the context of AMD Ryzen. These are people well known in the community. That is not to say that any of these users is 100% omniscient. However, when they all say the same thing, it makes us sit up and take notice. And in case you’re wondering, no. Not one person we asked said 1.55V was safe.

Overclockers’ Stance: 1.55V for Sub-Ambient

Included below are excerpts from our chats with ‘keeph8n‘ and ‘Brutus‘. Keep is a well known user on the hwbot ranks, and Brutus is an admin of Reddit’s r/AMD community as well as several overclocking chat groups.

‘Buildzoid‘, a Youtuber well-known for his highly technical and detailed motherboard and graphics card teardowns, has his own take on safe Ryzen CPU voltages. In this video on his channel, you can see the voltages he uses between 21:20 to 23:46. For the time challenged, we captured 1.35/1.36V idle; 1.44V for Prime95 1 thread, drooping down to 1.29V for Prime95 16 threads. That’s for a water cooled system using a 280mm radiator.

Static 1.55V Unsafe; Multiple Users Experiencing high voltages with CTR

In summary: there’s a lot of work setting up the voltage curves for a CPU that won’t glitch or destroy itself. AMD sets these tables up to keep our CPUs safe for all normal operating conditions.

Finally the day after our first post about CTR, Yuri made a comment to a user on Twitter, @MrPrayer, saying that CTR 2.0 removed the issue of the program setting 1.55 volts Vcore and that he was the only one who encountered this issue; these two statements are both false.

Yuri denies other users have suffered 1.55V from CTR.

One of our commenters experienced 1.5V from running CTR on his 3970X, and did not take too lightly to Yuri’s cavalier response to our first article.

As per our experience detailed in our original article, there is no safety features within CTR to prevent the SMU from shoving 1.55V in to the CPU. However, this would be a good safety feature to add to CTR in the future.

CTR Tuning – Worth It?

To test further, we had a user run a test for us on his Ryzen 7 5800X, a ‘Silver Sample’ according to CTR. He ran the tool and compared his scores before and after running the automatic tune. Unfortunately, no performance increase was seen. It did however, significantly reduce the power consumption: dropping from 137.2W to 112.8W. As you will see from the score though, it is almost the exact same, which you could get by simply running the test multiple times—no performance increase.

Results from the built-in Cinebench R20 feature in CTR, after tuning on a 5800X.

Also of note is that the R20 score was lower than the default 5800X score by about 11%. Now, this undesirable result may be due to a different cooling system, a less than golden sample CPU, different components, different BIOS settings, or any number of variables—this was a blind test. We were hoping for a good result to show our readers. To avoid any seriously bad outcomes, our tester, ‘Redpriest’, was warned to avoid any 1.55V scenarios that could be dangerous.

Is this what you will get? Maybe. Maybe not. Remember that overclocking is like poker, a game of luck tempered with skill. Luck for a single hand but skill for the long game. We’ve seen examples where people get a good chip and a good result from CTR. We’ve also shown some cases where a ‘Silver’ chip gets a bad result (permanent degradation). This is what we call risk vs. reward.

In fairness, is Overclocking even worth it on modern CPUs?

With modern boost algorithms and options like PBO, old-fashioned overclocking is paying less rewards than it used it.

We think that the odds are that you won’t get a significantly faster system. Without the ability to test hundreds of CPUs, it is impossible to predict wtou accuracy how many good samples there are in the wild. So, we can’t put a number on the odds you may degraded your CPU vs. improve your benchmark score. We know damage happens, and that’s enough to make us cautious.

Official statement from AMD

AMD can provide no assistance with overclocking voltage. Any manual increase of core voltage, or static core voltage, necessarily raises what the processor will experience over a 24 hour period when left to its own devices. It is our position that the only truly safe voltage is stock voltage. Voltages beyond what is stock/factory are trial and error and an exercise of community wisdom. As with all other processors, users experiment at their own risk and without warranty support.

AMD has no particular position on 3rd party OC software except to say we’re pleased that users are enjoying the flexibility we offer in our firmware designs.

AMD_Robert

AMD_Robert, an official AMD representative, answers very carefully here. Basically, we are on our own when we overclock in any way. Even if we use AMD’s own PBO, we can cause product damage that will not be under warranty. So, even AMD acknowledges that there is risk with their safer PBO algorithm.

Another word of wisdom comes from the overclocking hive mind: never overclock your daily driver. If you overclock, do it on a system that you can afford to lose. You could lose any component on that system, and you could lose any data on that system. Overclocking is not usually a cheap hobby. There are some people that overclock their daily-use computers. That’s a person comfortable with the risk involved. We will just say that backups are your friend.

CTR 2.0: Still Raw

So, in summary, what do we think of CTR as it stands right now? The short answer is “Yes”, “No”, and “Not Yet”. Simply put, CTR is an ambitious project that isn’t done.

CTR is built on the expertise of this whole community of overclockers, reverse engineers, and other computer enthusiasts. As such, it contains some great techniques to help the non-expert enthusiast play with and get the most out of their AMD CPUs. Unfortunately, we have seen it to contain some algorithms that can damage those expensive CPUs if you are not watching at the right time with a keen eye.

For an expert, you can certainly use this as one more tool to overclock your CPU. You know what you are doing. If you watch for the ways that CTR can damage your CPU and then you stop it, modify it, or control it, CTR can be a “Yes”.

For the normal computer enthusiast, CTR may work and it may do very little that PBO cannot provide. Worst yet it may permanently degrade or kill your expensive investment. Remember, there are documented cases where CTR really does do a better job than PBO. Yet, is it worth the risk? Are you willing to throw away a CPU because CTR made a mistake? If not, CTR is a big “No”.

Our Recommendation

As the Chips and Cheese staff discussed the varied responses to our article, we were of mixed emotions. On the whole, we can’t give a good recommendation for CTR. Could you recommend a car that only kills some passengers, not all of them?

We see that Yuri wants his product to be judged as an overclocking tool with the benefit of a disclaimer. Basically, any bad outcome is your responsibility. We understand that. All overclocking is a journey into risk. However, CTR is marketed as an easy overclocking tool for the non-expert. You can’t have both. We agree with and applaud the goal of making overclocking more accessible. The real question becomes then, isn’t AMD themselves doing that with PBO? In the end we are all united in hoping that CTR and other tools reach their potential. We are rooting for all tool creators and authors because it benefits the whole community when they succeed: us, you, our readers, everyone.

This gives us our final and overall recommendation of “Not Yet”. It has great potential. It can do some good stuff right now, but beware. The risk simply isn’t worth it… Yet. At least not until it gets these high voltage issues ironed out. And we will be here to review it again when it does.

Like making a fine cheese; with good ingredients, hard work, and some time, the end result will be worth it.

Clock Tuner for Ryzen 2.0 is awardedChips and Cheese’s

NOT READY Award

You can drink it, but it might give you indigestion.