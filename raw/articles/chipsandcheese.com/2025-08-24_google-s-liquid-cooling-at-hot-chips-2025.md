---
title: Google's Liquid Cooling at Hot Chips 2025
url: https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips
author: Chester Lam
published: '2025-08-24'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Liquid cooling is a familiar concept to PC enthusiasts, and has a long history in enterprise compute as well. Recently, liquid cooling has taken an increasing role in datacenters, amid increasing power draw and correspondingly high heat output from the latest chips. Machine learning in particular has an insatiable appetite for power and cooling. Google notes that water has a thermal conductivity about 4000 times that of air, making it an attractive solution to deal with the cooling demands associated with the current AI boom. Their talk at Hot Chips 2025 focuses on datacenter-level cooling for their TPUs, which are machine learning accelerators.

Google’s foray into liquid cooled TPUs took form in 2018 after some experimentation and iteration. The company has continued to develop and advance their cooling designs since. Their current liquid cooling solution is designed for datacenter scale, with liquid cooling loops spanning racks rather than being contained within servers. Racks of six CDUs, or Coolant Distribution Units, perform a role analogous to the radiator+pump combo in an enthusiast water cooling loop. The CDUs use flexible hoses and quick disconnect couplings to ease maintenance and reduce tolerance requirements. A CDU rack can provide adequate cooling capacity with five CDUs active, allowing maintenance on one unit without downtime.

CDUs exchange heat between coolant liquid and the facility-level water supply. The two liquid supplies don’t mix, and the CDUs only move heat between the two pools of liquid. Coolant liquid from the CDUs pass through manifolds that distribute the coolant to TPU servers. TPU chips are hooked up in series in the loop, which naturally means some chips will get hotter liquid that has already passed other chips in the loop. Cooling capacity is budgeted based on the requirements of the last chip in each loop.

Google uses a split-flow cold plate, which they found to perform better than a traditional straight-through configuration. To further optimize cooling, Google employs another techniques with parallels in the enthusiast world. TPUv4 switches to a bare-die setup compared to TPUv3’s lidded one. That mirrors delidding in the enthusiast world, where PC builders with especially strong stomachs remove heatspreaders (lids) to gain the higher heat transfer efficiency that bare die cooling can provide. For Google’s part, TPUv4 needs such an approach because it has 1.6x higher power draw compared to TPUv3.

Beyond moving heat off chips, liquid cooling helps reduce cooling-related power requirements. Google found the power consumption of liquid cooling pumps was less than 5% of fan power associated with an air cooling solution. Because Google uses water-to-water heat transfer to get heat off the coolant, the bulk of cooling power comes from pumps. Enthusiast setups don’t realize this potential advantage because they use liquid to move heat from chips to a more optimal location for air cooling. Usually, that’s a radiator with a fan mounted at a case intake. In theory, a PC builder could try exchanging heat to a toilet tank, allowing for highly efficient cooling with each flush. But fan and pump power in a water cooled PC is quite low in absolute terms, especially compared to the high RPM fans typically found in a server. Thus there’s little reason for an enthusiast to tackle cooling-related power.

Finally, maintenance is a concern. PC enthusiasts are familiar with water cooling challenges like microbial growth and leak risk. The same concerns apply to datacenter-scale water cooling solutions. Both worlds share some mitigating measures, like quick disconnect fittings. But datacenters have to address those challenges without taking down a substantial portion of compute capacity. PC builders with an open loop have to power down their machine before draining the loop and replacing components. Google’s extra CDU, mentioned earlier, allows maintenance with zero downtime. But Google takes measures beyond that, because a small problem with one machine can translate to a maintenance nightmare at scale.

Google extensively validates components with leak testing, uses alerting systems to discover problems like leaks, and takes preventative measures like scheduled maintenance and filtration. They also have a clear set of protocols to respond to alerts and issues, allowing a large workforce to respond to problems in a consistent fashion. It’s a far cry from the ad-hoc measures enthusiasts take to maintain their water cooling setups.

All in all, the recent rise in datacenter liquid cooling represents a fascinating crossover with high end enthusiast PCs. Both worlds are driven to liquid cooling by its incredibly efficiency when moving heat. Both must contend with similar problems. But datacenter approahces diverge from there, and driven by scale and reliability requirements. Plenty of water cooling hardware is already visible on the first day of Hot Chips 2025. Nvidia has a GB300 server on display, with external water cooling connections clearly visible. It also uses flexible tubing, and curiously deploys fans as well.

Seen at the Rebellions AI stand, showing people there installing a water block connected to a chiller for their demo

Rebellions AI, a South Korean company demo-ing a new ML accelerator, also has a water cooling setup. Their new “REBEL Quad” chip will eventually use air cooling in a PCIe card. But their demo uses a chiller and a cool looking water block, and it’s quite the sight. Zooming back up, all signs point to water cooling being here to stay as long as datacenter cooling requirements continue to intensify. The AI boom almost guarantees that will be the case.

If you like the content then consider heading over to the Patreon or PayPal if you want to toss a few bucks to Chips and Cheese. Also consider joining the Discord.

Incredibly neat, thanks for the writeup! Curious, is all of this public information that is published somewhere? If so, what benefit does Google get from sharing this with the public? Not complaining, just wondering!

Incredibly neat, thanks for the writeup! Curious, is all of this public information that is published somewhere? If so, what benefit does Google get from sharing this with the public? Not complaining, just wondering!

I have 3 tpuv4 accelerater tray liquid cooled