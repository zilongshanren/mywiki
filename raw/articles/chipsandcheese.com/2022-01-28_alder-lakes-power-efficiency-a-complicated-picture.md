---
title: Alder Lake’s Power Efficiency – A Complicated Picture
url: https://chipsandcheese.com/p/alder-lakes-power-efficiency-a-complicated-picture
author: Chester Lam
published: '2022-01-28'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Alder Lake’s Power Efficiency – A Complicated Picture

Reviews across the internet show Alder Lake getting very competitive performance with very high power consumption. For example, Anandtech measured 272 W of package power during a POV-Ray run. Our own testing showed eight Golden Cove cores alone could pull over 168W. But that’s at stock settings. And stock settings don’t do Alder Lake any favors when efficiency is in the spotlight.

Here, we’ll take a look at how Alder Lake scales at different power levels, and evaluate efficiency by seeing how much total power its cores use to complete a task. We’re running benchmarks with four cores because it’s hard to match core counts if more are used. A single threaded workload might give a more sanitized view, but it’s also a bit unrealistic because many modern applications are multithreaded. There’s also some funkiness with Intel’s core power counters, which seem to include shared components like the ring stop and L2 cache. A single Gracemont core’s power consumption gets drowned out by power draw from these shared components. By using an entire Gracemont cluster, we can make sure the majority of our measured power is core power.

To test power scaling on Alder Lake, we used the intel_pstate driver in Linux, and set max_perf_pct to various values. We read the core power plane (PP0) counter before and after the test run, and take the difference to get energy used during the test.

### Validating Intel’s Data – Performance vs Power

This looks bad for the Gracemont based E-Cores. According to Intel, they can’t beat the P-Cores at any power level, meaning the E-Cores are only efficient in terms of area. Anyway, let’s run our own tests.

With a vectorized workload, Gracemont only beats Golden Cove when running at ultrabook-throttlefest speeds and drawing under 6W. Remember that Gracemont isn’t optimized for 256-bit vectors. That’s over 17% of instructions in libx264, so Gracemont is not having a good time. It looks much better with a pure integer workload:

Below 15 watts, Gracemont achieves higher performance while consuming less power than Golden Cove. Add around 6 watts for uncore power, and we’re roughly within the power targets of thin and light laptops.

Looking through the entire power range, Gracemont struggles to scale well past 3-4 watts per core. That’s completely expected from a microarchitecture targeting low power. Unfortunately, the i7-12700K’s stock settings push Gracemont way past its sweet spot. Golden Cove cores also run into diminishing returns, but show much better scaling with power. On the 12700K, they boost to 5 GHz for 107% and 54% lead over Gracemont in libx264 and 7-Zip, respectively. That’s understandable behavior, considering the P-Cores’s focus on peak performance.

### Energy Efficiency

Average power draw is only part of the picture. Gracemont cores are called E-Cores for efficiency, not LP-Cores for low power. So let’s examine how much total power Alder Lake’s two microarchitectures consume to complete a task at various clock speeds.

At stock speeds, Gracemont cores are more efficient. Although slower, they draw so little power that they end up consuming less energy to finish the job. Golden Cove can be efficient too – just not at stock. Between 3 and 4 GHz, these P-Cores can give the E-Cores a run for their money. In an integer workload, Golden Cove consumes about the same amount of total energy while completing the task faster. With a vectorized load, Golden Cove finishes the task so much faster that it ends up using less total energy than Gracemont, even though Gracemont draws less power. That means running Gracemont above 3.2 GHz is pointless if energy efficiency is your primary concern. Running the E-Cores at 3.8 GHz basically makes them worse P-Cores. But that’s exactly what Alder Lake does by default.

Below 3 GHz, Gracemont shines. It’s able to maintain better performance at very low power targets (as we saw in the previous section) while consuming less energy. With an integer workload, it’s especially efficient. But nothing scales down forever. Going under 1 GHz decreases efficiency for both cores. At those speeds, they take so long to finish that static power consumption erases any potential efficiency gain from lower power draw.

### Is Intel Making Progress?

Half a decade ago, Intel’s Core line was well known for their power efficiency. Ivy Bridge, Haswell, and Skylake covered everything from desktops to servers to thin and light devices. Let’s see how far Alder Lake has come.

In libx264, Skylake remains very competitive against Gracemont. Above 20 watts of core power draw, or about 5 watts per core, the two architectures are neck and neck even though one of them is more than half a decade old and uses an older node. Skylake also keeps scaling when given more power, while Gracemont stops. These E-Cores aren’t designed to excel in vector loads. At lower power levels, they pull a decent advantage against Skylake, but I would expect more from an efficiency oriented design with a process node advantage.

Again, Gracemont turns things around in the compression job. Skylake can’t touch Gracemont’s performance at any power point.

Golden Cove probably makes concessions in low power scalability to target high performance at high power, because Skylake keeps up very well below 5 W (or just above 1 W per core). Skylake falls behind as power levels increase. At roughly matched power levels, Intel’s latest big core has a staggering 42% and 52% lead over Skylake in our video encoding and compression tests, respectively.

Intel’s new architectures are more efficient at almost all clock speeds. With a new node and more than half a decade of progress, that’s expected. It’s not all sunshine and rainbows for Alder Lake though. At stock speeds, Skylake is more efficient because Golden Cove draws too much power to reach the upper 4 GHz range. Compared to Gracemont, Skylake is able to achieve similar efficiency in vector workloads by running at lower clocks. For example, Skylake at 3 GHz encoded the video at 5.71 FPS using 6368 joules of core energy. Gracemont at 3.7 GHz hit 5.72 FPS, but used 6711 joules.

Clearly, creating an efficient, low power core is very difficult. Sacrifices like half-width AVX execution are sensible because wide vector execution units can draw a lot of power. But a core with bigger vector units running at lower clock speeds can take advantage of lower voltages. Power draw drops a lot with lower voltage, making a big core as efficient as a little one, even on an older process.

### Is AMD Scary?

Alder Lake doesn’t exist in a vacuum. AMD CPUs have been pretty efficient ever since Zen 2 launched. How does Intel compare?

Please take power measurements in this section with a grain of salt. Research suggests that AMD doesn’t have power measurement hardware, which limits the accuracy of their RAPL counters:

The results indicate that the energy data is modeled, not measured….this does not necessarily imply that RAPL readouts are wrong. But it shows that they cannot be used to accurately estimate and therefore optimize for total system power, as opposed to Intel systems since Haswell.


We don’t have hardware to directly measure CPU power consumption ourselves. So we’re presenting this data as-is. To get core energy consumption, we’re reading MSR 0xC001029A (Core Energy Status) on the first thread of every physical core before the workload is run and after it finishes.

At the high end of its power range, Zen 2 looks like a better version of Gracemont. It scales further, and does much better with vector workloads. But Golden Cove is a vector monster, and Zen 2 can’t beat it with the same core power draw except in a narrow range between 10 and 15 watts. There, Zen 2 is running in the low to mid 3 GHz range and seems to be in its efficiency sweet spot. On 7-Zip, Zen 2 has excellent power characteristics. It beats both Golden Cove and Gracemont throughout its power range. Zen 2’s only flaw there is its inability to hit very low power levels. Desktop Zen 2 can’t keep scaling down because it hits a voltage floor much earlier than Golden Cove and Gracemont.

But what about Zen 2 in mobile form?

This complicates comparisons. Mobile and desktop Zen 2 have very different power characteristics. It’s almost like Golden Cove and Gracemont. In Renoir form, Zen 2 scales down very well to low power levels. It beats both of Alder Lake’s microarchitectures below 15 watts of core power, and beats Gracemont at all core power levels. But Renoir can’t scale well to high power levels. Desktop Zen 2 already can’t scale up in power as well as Golden Cove can, and Renoir is worse.

Overall, Zen 2 is more power efficient at mid to low power levels. At higher power, Golden Cove is more efficient in vector workloads because Zen 2 doesn’t scale well as power increases. Compared to Gracemont, Zen 2 cores are better at all power levels, except when desktop Zen 2 cores hit an early voltage floor.

In terms of energy efficiency at similar clocks, Zen 2 cores are excellent. Golden Cove has to drop below 2 GHz to finish the encode job with the same energy budget as desktop Zen 2. Gracemont can do better, but also has to clock below 2 GHz. Again, we see desktop Zen 2 cores failing to gain efficiency at lower clock speeds. Their energy efficiency peaks when boost is turned off, and going lower actually makes the cores pull more total power. Renoir is much better at scaling down to low power. At least in the near future, AMD can probably get by without maintaining separate E-Core and P-Core architectures. They’re already covering both bases by changing L3 size and optimizing the same architecture for different power and performance targets.

## Conclusion

In summary:

Out of the box, the 12700K prioritizes absolute performance over power efficiency. “Race to sleep” is complete bullshit, at least until you get down to very low power levels.

Golden Cove is very efficient below 4 GHz, especially with a vectorized workload

Even though it’s paired with E-Cores, Golden Cove still scales well to very low power levels.

Gracemont is very efficient with integer workloads in the low 3 GHz range.

256-bit instructions give Gracemont a hard time. With libx264, it needs to go below 3 GHz before it really shines in terms of energy efficiency

When run at sane clocks, both Alder Lake architectures show significant efficiency gains compared to Skylake


Alder Lake looks bad if we evaluate efficiency at stock. Four Golden Cove cores take more energy to complete the same task compared to Zen 2, and even Skylake. So Alder Lake plenty of criticism over power draw.

When we compare it to AMD however, with that 142 W PPT limit that AMD has, Intel is often trailing at a 20-70 W deficit when we’re looking at full load efficiency.


[The Intel 12th Gen Core i9-12900K Review: Hybrid Performance Brings Hybrid Complexity], from Anandtech

Gracemont too is pushed past its sweet spot. To be blunt, Alder Lake’s E-Cores have no business going above 3.5 GHz. But Intel has decided to make them do exactly that, so they don’t go beyond being a performance per area play. Unsurprisingly, this doesn’t look good when reviewers expect E-Cores to boost energy efficiency:

The one thing that this architecture shows is that it’s less energy efficient compared to a 5950X at 7nm. So for me, the E cores are not really a selling point?


[Core i9 12900K processor review], from Guru3D

But that’s not the complete picture. Both Golden Cove and Gracemont scale down in power very well. With Golden Cove below 4 GHz and Gracemont below 3 GHz, both architectures show significant gains compared to Skylake. Intel’s latest process and CPU architectures are capable of excellent performance at reasonable power. Unfortunately, none of that comes out at default settings, which is how most customers will run their CPUs.

If you like our articles and journalism and you want to support us in our endeavors then consider heading over to our [Patreon](https://www.patreon.com/ChipsandCheese) or our [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks our way or if you would like to talk with the Chips and Cheese staff and the people behind the scenes then consider joining our [Discord](https://discord.gg/TwVnRhxgY2).

This is a great write-up and I hope you do same tests with recent Intel SKUs.

IMO these tests are very important for consumers caring not just about parallel processing.

Would be interesting to know how AVX512 mixes in when Intel finally manages to add it to E-cores or make the limitation of instruction set more transparent to the OS.