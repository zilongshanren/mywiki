---
title: Examining the Nintendo Switch (Tegra X1) Video Engine
url: https://chipsandcheese.com/p/examining-the-nintendo-switch-tegra-x1-video-engine
author: Chester Lam
published: '2024-06-28'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

The Tegra X1 SoC featured in Nintendo’s Switch was meant to fill a variety of market segments including Android set top boxes and automotive applications. Hardware video encode and decode are vital to all of those use cases. Tegra X1’s video engine can handle encode and decode for both H264 and HEVC. It’s quite different from desktop Maxwell’s video engine. On one hand, hardware HEVC decode is great to see. Desktop Maxwell supported HEVC encode, but curiously had no HEVC decode support.

A Nintendo Switch with the Tegra X1 chip

Software support is a complicated situation too. ffmpeg can access hardware video offload on mainstream Nvidia cards through “cuvid” or “nvenc” codecs. Tegra X1 uses different L4T codecs that take a different set of parameters. Using those L4T codecs also requires a custom ffmpeg build from Nvidia. This will be a short article comparing Tegra X1’s video engine to Maxwell’s.

Special thanks goes to Titanic for setting up Linux on his Nintendo Switch for testing. Testing was conducted from Linux, not the stock Switch operating system.

Decode Performance

Tegra X1’s video block has enough H264 decode performance to play 4K videos at 60 FPS. It’s not as fast as desktop Maxwell’s video decoder, which has enough throughput to get by in an alternate universe where video content gets created with high refresh rate monitors in mind.

Another use case for faster decode is playing multiple videos at a time. Tegra X1 is probably going to be connected to a single screen, making that an unrealistic scenario. Nvidia likely traded off decode speed for a die area reduction.

H264 VBR Transcode

Unlike with NVENC, Nvidia’s custom ffmpeg build doesn’t have a constant quantization option. Therefore, variable bitrate is the best mode available for recording gameplay. The Switch can encode video with decent bitrate efficiency, but ends up trailing desktop Maxwell’s NVENC. It also trails Intel’s QuickSync video engine from the Core i5-6600K. In variable bitrate mode, desktop Maxwell’s video engine tended to undershoot the requested bitrate, while Tegra X1 was right on target. With a 15 mbps target, the GTX 980 Ti averaged 11.85 mbps. The Tegra X1 averaged 14.87 mbps.

Actual bitrate plotted on the X axis

Gaps between the different hardware encoders close up past 20 mbps, so users encoding video at high quality shouldn’t see a noticeable difference between the encoders tested here. As we get to very high bitrates like 40 mbps, they even close the gap with software encoding. Of course, libx264 with the veryslow preset isn’t fast enough for realtime recording. Results from libx264 are presented here just to provide perspective, as software encoders are the gold standard in terms of compression quality.

With the highest quality preset, none of the encoders can encode 4K video at 60 FPS. However, all three have enough throughput to deal with 30 FPS. For the Switch, it’s more than enough performance because Switch games will never get anywhere near 4K. The Switch itself has a 720P screen driven by a rather weak iGPU.

Interestingly, the Tegra X1’s transcoding speed doesn’t vary with requested bitrate. Intel’s QuickSync and Maxwell’s NVENC encoders see a slight decrease in framerate as bitrate increases. Intel’s QuickSync encoder is technically the fastest. Desktop Maxwell and Tegra X1’s encoders have similar performance at low bitrate targets, but Maxwell starts falling behind at higher bitrates.

HEVC VBR Transcode

Tegra X1’s video engine also supports HEVC encoding. HEVC offers better compression efficiency than H264, but can be more troublesome to use due to patent and royalty issues. Again, desktop Maxwell’s video engine undershot bitrate targets while the Tegra X1’s got closer. For example, the GTX 980 Ti averaged 12.13 mbps with a 15 mbps target, while the Tegra X1 averaged 14.16 mbps. Intel’s QuickSync on Skylake CPUs can also do HEVC encoding, and massively undershot bitrates. With the same requested 15 mbps, QuickSync averaged just 10.2 mbps.

Tegra X1 and desktop Maxwell’s video engines are almost perfectly matched once the discrepancy between target and actual bitrates are accounted for. Intel’s HD 530 generally does worse especially at low quality bitrates. Software encoding comes out ahead except at very low bitrates.

All HEVC encoders offer better compression efficiency, but slow down too. The two Nvidia encoders can no longer break the 4K 30 FPS mark at all bitrate settings. Skylake’s video encoder takes the heaviest hit, going from first to last place while seeing the smallest VMAF score gains.

Curiously, Tegra X1’s video engine now has an encode speed advantage over Maxwell’s while matching it in compression efficiency. It’s not a big enough advantage to matter because neither video engine is fast enough to handle recording 4K gameplay. But it does show that Tegra X1 has a slightly better hardware HEVC support than desktop Maxwell’s. Maxwell’s HEVC support feels incomplete in general, as the GTX 980 Ti lacks HEVC decode support.

VMAF scores provide an objective way to quickly compare output across many quality settings and encoders, but a look at actual video output can be interesting too.

Frame encoded by the Tegra X1. 15 mbps bitrate target requested, average bitrate was 14.16 mbps

At a relatively low 15 mbps bitrate target at 4K, Tegra X1 does a good job at reproducing clear edges around text. However, Tegra’s output suffers from faint halos around high contrast edges, including text. Thankfully, those halos are not too objectionable, and would be difficult to notice when there’s a lot of motion.

Frame encoded by the GTX 980 Ti. 15 mbps bitrate requested, average bitrate was 12.13 mbps

The GTX 980 Ti’s encoder undershot the target bitrate by more, and generally looks worse. High contrast edges around text get color artifacts instead of halos, which I find more distracting. However, desktop Maxwell does produce a better rendering of the billboard to the right. Tegra X1 creates a mess of compression artifacts over the sign’s blue gradient and text. Desktop Maxwell goes for a smoother rendering, which probably drops some fine detail but largely eliminates distracting artifacts. Comparing other smooth areas like rock faces also suggests Tegra X1 tries hard to preserve fine detail, while the GTX 980 Ti discards detail to avoid distracting artifacts.

Frame encoded by the Core i5-6600K’s QuickSync block. 20 mbps requested, average bitrate was 13.52 mbps

Intel’s QSV produces a far worse result. Blocking is evident throughout the frame, and is especially noticeable in the trail left by Wrecking Ball on the road. Red text is noticeably blurred, and the payload’s outline behind the rock formation straight up disappears . Nvidia’s encoders also have artifacts, but they’re far less pronounced. I feel like Intel went for minimal gains with their HEVC implementation, while Nvidia’s encoders really try to take advantage of the more advanced codec.

Final Words

Even though Tegra X1 and the GTX 980 Ti both use the Maxwell GPU architecture, Nvidia has seen fit to give Tegra X1 a completely different video block. Compared to desktop Maxwell, Tegra X1’s video engine cuts back in some areas like decode throughput and H264 encoding. It also drops NVENC features like targeting a constant quantization level, so quality can only be controlled by setting bitrate targets.

In other areas, Tegra X1 takes a step forward. HEVC support is much better, with comparable quality to desktop Maxwell at better speed. Tegra X1 also supports hardware HEVC decode, a notable omission on desktop Maxwell. Because Tegra X1 produces video output with very different artifacts, I doubt Tegra X1 simply got an improved version of the Maxwell video engine.

Hardware accelerated video blocks often see plenty of reuse across a GPU lineup. I’m surprised that Nvidia spent extra engineering resources to make a completely different video engine for Tegra X1, rather than reusing the one in mainstream Maxwell GPUs. Perhaps Maxwell’s video engine was too power hungry to go into a mobile chip targeting 10W of power consumption.

The most amazing thing is Nvidia didn’t have to compromise quality when they divided engineering resources to create two different video blocks. Both video engines are able to provide competitive compression efficiency (especially when using HEVC) against Intel’s HD 530. Nvidia apparently had a ton of engineering resources on hand even as far back as 2015, and it shows.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.