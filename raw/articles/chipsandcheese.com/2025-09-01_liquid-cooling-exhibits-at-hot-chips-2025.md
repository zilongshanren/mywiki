---
title: Liquid Cooling Exhibits at Hot Chips 2025
url: https://chipsandcheese.com/p/liquid-cooling-exhibits-at-hot-chips
author: Chester Lam
published: '2025-09-01'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

# Liquid Cooling Exhibits at Hot Chips 2025

Hot Chips doesn’t just consist of presentations on hardware architecture, although those are the core of what Hot Chips is about. The conference also features stands where various companies show off their developments, and that’s not restricted to chips. Some of those showed off interesting liquid cooling components, particularly in cold plate design.

# Water Jets

Many of the waterblocks on display use microjets, rather than microfin arrays. Water flows through a manifold at the top of the block, and reaches the cold plate surface through small channels. These channels can be distributed across the cold plate, ensuring cold water supply across the chip.

Alloy Enterprises showed a cutaway of an early prototype of a MI350X waterblock. The manifold in the top layer (bottom in the photo) would take incoming cold water. Holes in an intermediate layer allow water to pass through, forming microjets. A bottom layer, not shown, would interface with the chip. Finally, hot water from the bottom layer would be drawn out through tubing and eventually make its way to a heat exchanger.

Another advantage is that the jets can be positioned with chip hotspots in mind, rather than uniformly across the chip. Jetcool showed off such a design, with holes for water jets positioned at anticipated chip hotspots. Their “SmartLid” waterblock has non-uniform water jet distribution, seen in the hole placement below. Larger holes on the side let water exit.

“SmartLid” goes further too, sending water directly to the die without using a cold plate and thermal interface material. Removing layers improves heat transfer efficiency, a concept that enthusiasts are familiar with delidding. Hitting the die directly with water jets is a natural next step, though one that I find at least slightly scary. I hope that rubber gasket is a really good one. I also hope the chip being cooled doesn’t have any water-sensitive surface mount components too close to the die.

It’s also worth noting how small the water jets are. They’re difficult to see with the naked eye, so Jetcool mounted LEDs inside to show the water jet hole placement.

Needless to say, a solution like this won’t be broadly applicable to PC hardware. Coolers for PC enthusiasts must cater to a wide range of chips across different platforms. Specializing by positioning water jets over anticipated hot spots would require different designs for each chip.

But large scale server deployments, such as those meant for AI, won’t have a diverse collection of hardware. For logistics reasons, companies will want to standardize on one server configuration with memory, CPUs, and accelerators set in stone, and deploy that across a wide fleet. With increased thermal requirements from AI, designing waterblocks tightly optimized for certain chips may be worthwhile.

# More Waterblock Designs

Alloy had a range of waterblocks on display, including the one above. Some used copper, much like consumer PC cooling solutions, but aluminum was present as well. Copper allows for excellent heat transfer efficiency, which is why it’s so popular, but its weight can be a huge disadvantage. Sometimes servers need to be transported by aircraft, where weight restrictions can be a concern. Aluminum is much better when weight matters. However, corrosion can reduce lifespan. As with everything, there’s a tradeoff.

For example, here’s the back of an aluminum waterblock for the MI300 series. While not obvious from a photograph, this design is noticeably lighter than copper waterblocks. Interestingly, the cold plate features cutouts for temperature sensors.

Jetcool’s stand also featured a copper waterblock for the MI300 series. It’s copper, and features contact pads for various components located around the GPU die.

The top of the waterblock has some beautiful metal machining patterns.

Jetcool also showed off system level stuff. This is a setup meant for cooling Nvidia’s GB200 setup, which features two B200 GPUs and a Grace CPU.

The three chips are connected in series. It looks like coolant would flow across one GPU, then to the other GPU, and finally to the CPU. It’s a setup that makes a lot of sense because the GPUs will do heavy lifting in AI workloads, and generate more heat too.

The cold plates for the GB200 setup are copper and flat, and remind me of PC cooling waterblocks.

Finally, Jetcool has a server set up with a self-contained water cooling setup. It’s a reminder that not all datacenters are set up to do water cooling at the building level. A solution that uses radiators, pumps, and waterblocks all contained within the same system can seamlessly slot into existing datacenters. This setup puts two CPUs in series.

# Nvidia’s GB300 Server

While not specifically set up to showcase liquid cooling, Nvidia had a GB300 server and NVLink switch on display. The GB300 server has external connections for liquid cooling. Liquid goes through flexible rubber pipes, and then moves to hard copper pipes as it gets closer to the copper waterblocks. Heated water goes back to rubber pipes and exits the system.

A closer look at the waterblocks shows a layer over them that almost looks like the pattern on a resistive touch sensor. I wonder if it’s there to detect leaks. Perhaps water will close a circuit and trip a sensor.

The NVLink switch is also water cooled with a similar setup. Again, there’s hard copper pipes, copper waterblocks, and funny patterns hooked up to what could be a sensor.

Water cooling only extends to the hottest components like the GPUs or NVSwitch chips. Other components make do with passive air cooling, provided by fans near the front of the case. What looks like a Samsung SSD on the side doesn’t even need a passive heatsink.

# Final Words

The current AI boom makes cooling a hot topic. Chips built to accelerate machine learning are rapidly trending towards higher power draw, which translates to higher waste heat output. For example, Meta’s Catalina uses racks of 18 compute trays, which each host two B200 GPUs and two Grace CPUs.

A single rack can draw 93.5 kW. For perspective, the [average US household](https://www.eia.gov/energyexplained/use-of-energy/electricity-use-in-homes.php) draws less than 2 kW, averaged out over a year (16000 kWh / 8760 hours per year). An AMD MI350 rack goes for even higher compute density, packing 128 MI355X liquid cooled GPUs into a rack. The MI350 OAM liquid cooled module is designed for 1.4 kW, so the 128 GPUs could draw nearly 180 kW. For a larger scale example, a Google “superpod” of 9216 networked Ironwood TPU chips draws about 10 MW. All of that waste heat has to go somewhere, and datacenter cooling technologies are being pushed to their limits. The current trend sees power draw, and thus waste heat, increase generation over generation as chipmakers build higher throughput hardware to handle AI demands.

All of that waste heat has to go somewhere, which drives innovation in liquid cooling technologies. While liquid cooling hardware displayed at Hot Chips 2025 was very focused on the enterprise side and cooling AI-related chips, I hope some techniques will trickle down to consumer hardware in the years to come. Hotspotting is definitely an issue that spans consumer and enterprise segments. And zooming up, I would love a solution that lets me pre-heat water with my computer, and use less energy at the water heater.

If you like the content then consider heading over to the [Patreon](https://www.patreon.com/ChipsandCheese) or [PayPal](https://www.paypal.com/donate/?hosted_button_id=4EMPH66SBGVSQ) if you want to toss a few bucks to Chips and Cheese. Also consider joining the [Discord](https://discord.gg/TwVnRhxgY2).

IMHO, Harvesting of all this excessive energy is a Hot Topic as well. 99.9x % of all the MW scale energy just gets transformed into Thermal Energy.

Were there any new developments to be seen in order to gain efficiency through harvesting as well? Aside from the environmental aspect this might help reduce TCO a lot.