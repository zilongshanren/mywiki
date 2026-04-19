---
title: GPU Hardware Video Encoders – How Good Are They?
url: https://chipsandcheese.com/p/gpu-hardware-video-encoders-how-good-are-they
author: Chester Lam
published: '2022-03-30'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

Figuring out the best way to encode a video is very computationally expensive, and it might not a good idea to throw a ton of CPU cycles at encoding video when you’re running a game. That’s why modern GPUs usually include hardware video encoders.

Here, we’ll take a brief look at how some implementations compare. We’ll be using Netflix’s Video Multimethod Assessment Fusion (VMAF) metric to evaluate quality. Compared to traditional video quality metrics like PSNR and SSIM, VMAF generally does a better job of predicting how a human would subjectively rate a video. That’s because VMAF uses several quality metrics, and a machine learning model to determine how much weight each sub-metric should be given. The model is trained using ratings from human viewers, who rank videos as “excellent”, “good”, “fair”, “poor”, or “bad”. These are linearly mapped to VMAF scores from 0-100, with 100 representing an “excellent” rating, and 20 corresponding to poor. Along the way, 80 would indicate “good”, 60 “fair”, and 40 “poor”. I personally like to see a VMAF rating above 90. That would be between “excellent” and “good”, and generally means a clean looking video with very few noticeable artifacts.

For 4K clips, we used the vmaf_4k_v0.6.1 model, which was trained to predict quality on a 4K TV, at a distance of 1.5x the height of the screen. And for 1080P clips, we used vmaf_v0.6.1, which targets viewing on a 1080p HDTV in a living room.

Unlike other evaluations that used movie clips, we’re using gameplay footage. Specifically, we’re going to use a saved Overwatch Play of the Game video, and a 20 second clip from an Elder Scrolls Online raid. The Overwatch clip features a lot of camera motion with relatively simple objects. The ESO raid clip is the opposite. There’s not much camera movement for most of the clip, but there’s more detail, more players on screen, and more effects.

Most of our commentary will focus on AMD and Nvidia’s latest encoders, in RDNA 2 (VCN, Video Core Next) and Turing (NVENC) respectively. I don’t have an Ampere card unfortunately. We’ll be using the H.264 codec too, because it’s very well supported.

Streaming

Streaming is a very demanding scenario for any video encoder. The output stream can’t spike above a set bitrate, because that could overwhelm upload bandwidth and cause stuttering. That means the encoder has low flexibility if it needs to use more bits to represent complex movements or fine detail. At the same time, it has to encode fast enough to enable real-time streaming. That limits how much it can analyze video frames to come up with an optimal encoding.

To evaluate this, we’re going to use each encoder in constant bitrate mode, at settings from 10 mbps to 4 mbps. Since streaming at 4K is impractical, the original videos were downsized to 1080P. For software encoding, we’re using libx264’s faster preset, because that can sustain over 60 FPS on a single 3950X CCX, with boost off. That should leave enough CPU power free to handle game logic, at least on modern CPUs with more than four cores. All of the hardware encoders were able to exceed 100 FPS with their highest quality presets, making speed a non-issue.

In the Overwatch video, Nvidia’s Turing NVENC does very well. It’s able to match or beat libx264 software encoding all bitrates. At the low end of the bitrate range, which could be important for streaming with low upload speeds, Turing’s quality is unmatched. Nvidia’s previous generation encoder, found in Pascal based cards, is slightly worse. But it’s still a very solid performer that stays neck and neck with software encoding. AMD’s VCN (Video Core Next) encoder isn’t as impressive. Its quality is significantly worse than Nvidia’s throughout the bitrate range. It also can’t compete with software encoding, assuming you have enough CPU power to spare.

6900XT first, RTX 2060 second. Both @ 10Mbps

Subjectively, VCN has a harder time handling fast camera movements. All of the encoders struggle when there’s a lot of motion, but VCN suffers a bit more from blocking. It’s also more prone to artifacts around text and UI elements. NVENC recovers much faster from fast movements

Software encoding turns the tables with the ESO clip. NVENC’s low bitrate quality advantage evaporates, and libx264 takes a slight lead throughout the bitrate range. Hardware encoders seem to struggle with more complex frames. Relative to NVENC, AMD’s VCN continues to fall behind.

Subjectively, none of the encoders here do a particularly good job. Even at 10 mbps, a lot of fine detail is removed, and there are visible artifacts around UI text. Still, I slightly prefer Turing’s output, because it makes low contrast player names slightly easier to read.

6900 XT first, RTX 2060 second. Both at 10 mbps

libx264 faster preset in first image, RTX 2060 p7 preset in second image. Both at 10 mbps

Interestingly, Nvidia’s encoder tends to overshoot the bitrate target, which means it could use more upload bandwidth than expected. This overshoot gets worse in the ESO clip, suggesting that Nvidia is using more bits to handle extra detail, even if doing so would use more bandwidth than what a user’s asking for. AMD’s VCN and libx264 also overshoot a bit, but only at the low end of the bitrate range. Towards the upper end (10 mbps), they tend to undershoot.

Recording

Recording is a bit different from streaming. The encoder still needs to be fast enough to keep up in real time, but the output doesn’t have to fit within tight upload bandwidth restrictions. That makes it possible to record gameplay in 4K at very high quality. Of course, we still want to use storage as efficiently as possible.

In this test, we’re going to set various quality levels using the quantization parameter (for hardware encoders) or constant rate factor (for libx264). Each encoder gets to use the best quality preset that can do more than 60 FPS. For libx264, we’re again going to restrict it to one 3950X CCD with boost off, which means it needs the ultrafast preset.

Now, hardware encoders show their strength. 4K encoding demands too much from the CPU. A single Zen 2 CCX at 3.5 GHz has to use the fastest preset to stay above 60 FPS. That prevents it from exploiting the CPU’s flexibility, and libx264 ends up at the bottom of the pack. With fast, fixed function hardware, GPUs can do better analysis while keeping up enough speed for real time recording.

Nvidia’s Turing takes the top spot again, with Pascal not far behind. AMD’s VCN can’t quite match Nvidia, but beats software encoding. All of the options deliver very good quality past 40 mbps.

In the ESO clip, software encoding struggles even more. Now, it can’t match hardware encoders throughout the bitrate range. Among the hardware encoders, Turing dominates even more. Pascal and AMD’s VCN are both a step behind, though Pascal gives marginally better quality.

6900 XT at 22.1 mbps in the first image, RTX 2060 Mobile at 20.09 mbps in the second image, for VMAF scores of 75.6 and 82.1 respectively. 4K frames scaled down to 1080P

Transcoding

In this scenario, we’re trying to compress a high quality, recorded clip to get smaller file sizes, preferably while losing as little quality as possible. Speed doesn’t matter as much. Like the recording scenario, we’re using constant quantization or constant rate factor. But unlike with recording, every encoder will be set to the slowest, highest quality preset. The only exception is libx264, where the “veryslow” preset is used instead of “placebo”. The latter is just slower while barely providing better quality.

Turing’s NVENC is still a very strong performer, but software encoding provides a clear quality advantage above 10 mbps. Pascal’s NVENC closely trails Turing’s, while AMD’s VCE falls behind.

All of the video encoders can provide excellent quality with more than 30 mbps. Above that, the VMAF score continues to converge and differences become indistinguishable. Below 10 mbps, all of the encoders tested deliver awful output. Netflix says a score of 70 is a vote between “good” and “fair“, but there’s nothing good or fair about noisy color blocks all over the place:

Turing got a VMAF score of 73.09 at 7.18 mbps. I guess “fair” fits if I’m being really, really generous?

With the ESO clip, software encoding pulls farther ahead. Nvidia’s NVENC runs into a wall of sorts, with Turing and Pascal practically tied. AMD’s VCN is still dead last, but catches Nvidia above 50 mbps.

Speed didn’t matter in the other two scenarios as long as the encoder was fast enough to handle real time encoding. For transcoding though, faster is better.

NVENC and libx264 slow down as the quantization parameter or constant rate factor goes up, while AMD’s VCN holds a constant speed regardless of quality. Higher scene complexity slows down all of the encoders, but AMD’s VCN is barely affected (44 FPS vs 45 FPS).

At the highest quality preset, Pascal’s NVENC is the fastest. Turing trades some speed for quality, which is a good tradeoff for transcoding. VCN’s speed is in the same ballpark as Nvidia’s, but loses in terms of quality. Software encoding with libx264 is a lot slower, but provides quality and bitrate efficiency that hardware encoders can’t match.

Final Words

Nvidia has steadily improved their NVENC implementation over the years. With Turing, they’ve built an excellent hardware encoder that can go head to head with libx264’s faster preset. Technically, the best streaming setup would use a powerful CPU and a higher quality software encoding preset. But Turing’s NVENC is a very good alternative, especially on weaker CPUs. On the other hand, AMD has some catching up to do. Their latest VCN encoder is fast, but can’t even match Nvidia’s last generation NVENC, found in Turing.

In AMD’s favor, VCN covers 4K recording very well, mostly because you can record at higher bitrates where there’s practically no quality difference between the encoders. VCN thus ends up being good enough. It gives AMD users a better option than software encoding, and shows the strength of hardware encoders for this use case even if it’s not best in class. Still, Nvidia is better if you want to record at lower bitrates.

For transcoding, software encoding is king. Hardware encoders simply can’t reach the same level of bitrate efficiency. They probably have simple, fixed function circuits that are very fast, but aren’t flexible enough to do the complex analysis software is capable of. Still, hardware encoders can work in a pinch. If you know your video is dominated by simple scenes, aren’t very picky about video quality, and just want the encode done quickly, Turing’s p7 preset can do a reasonable job.

In future articles, we plan to look at other encoders like Intel’s Quick Sync or AMD’s older VCE. If time permits, we’ll take a look at newer video encoding formats too, like HEVC and AV1.

If you like our articles and journalism and you want to support us in our endeavors then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way or if you would like to talk with the Chips and Cheese staff and the people behind the scenes then consider joining our Discord.

Additional Notes

3-31-2022: Version 164 of the libx264 encoder was used for testing in this article