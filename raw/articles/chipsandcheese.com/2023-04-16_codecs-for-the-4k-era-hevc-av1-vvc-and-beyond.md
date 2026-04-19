---
title: 'Codecs for the 4K Era: HEVC, AV1, VVC and Beyond'
url: https://chipsandcheese.com/p/codecs-for-the-4k-era-hevc-av1-vvc-and-beyond
author: Dingo Networks
published: '2023-04-16'
source_blog: Chips and Cheese | Substack
source_site: https://chipsandcheese.com/
category: graphics
fetched: '2026-04-19'
---

This article was written in March 2023. At the time of writing, the encoders we used were still in active development. As codec standards and encoders evolve, some of the information may become outdated.

A Turning Point for Codecs

For the longest time, MPEG LA’s Advanced Video Coding (AVC), or H.264, has been everyone’s go-to video codec. Thanks to Cisco’s OpenH264, software projects no longer have to worry about patents as Cisco foots the bill for royalties. However, AVC is showing its age after 20 years, as it struggles to handle resolutions beyond 1080p, while maintaining low bitrates.

AVC’s official successor – High Efficiency Video Coding (HEVC), or H.265 – is not enjoying the same level of popularity. Video platforms like YouTube refuse to adopt HEVC due to licensing fees. On the other hand, open-source software projects, such as Mozilla Firefox, deliberately choose not to implement HEVC to avoid potential legal trouble. Although HEVC was published almost a decade ago, AVC still dominates the codec market to this day.

In 2015, an industry consortium led by Google – the Alliance for Open Media (AOMedia) – decided to develop their own open, royalty-free alternative to HEVC – AOMedia Video 1 (AV1). AV1 was initially planned to release in 2017, but the world of codecs moves slowly, and mainstream mobile platforms still lack hardware decoding capabilities as we speak.

With its adoption within grasp, the hype for AV1 has never been higher. Some expect AV1 to follow AVC’s path, but its fate may not be as clear-cut. Back in 2015, HEVC was AV1’s competitor, but HEVC’s successor – Versatile Video Coding (VVC), or H.266 – was released in 2020. Meanwhile, MPEG LA is developing two other codecs in parallel: Essential Video Coding (EVC) and Low Complexity Enhancement Video Coding (LCEVC). A subset of EVC – Type 1 – only uses patents within the public domain and thus is royalty-free. LCEVC, on the other hand, is not a standalone codec but an innovative enhancement layer. LCEVC enhances a base codec by compressing lost details and compensating for compression artifacts. LCEVC has the potential to re-vitalize older codecs, such as AVC, and bring their relevance back into the 4K arena.

We’re at a turning point for codecs, and it begs the question: born in between MPEG LA’s two generations of codecs, how does AV1 perform? This is a huge topic, so let’s narrow it down a bit. There are already many good writings on how codecs work, and I’m not really qualified to comment on the legal side without an LL.B. Therefore, we’re exclusively taking a look at the technical performance of HEVC, AV1 and VVC, namely compression efficiency and computational complexity. Both EVC and LCEVC are currently in heavy development, and real-world applications are difficult to find. So we’ll exclude them in today’s discussion. I hope you are not already lost from too many acronyms (TMA), and I promise you it’s not getting much better from here on.

An Opinionated Methodology

Codec testing is a minefield. Each codec has many encoders, and each encoder has dozens of parameters with dialectical relationships with both speed and quality. It is certainly ideal to cover the common configurations, but testing combinations of too many variables quickly becomes convoluted.

On the other hand, visual quality is perceptual and even up to individual taste. For example, some may consider movies without film grain clearer and thus higher quality, while others argue staying true to film – one hallmark of visual quality – means retaining the grain. Therefore, the best way to assess visual quality is to conduct in-person subjective assessments where real human judges by their perception. However, we can’t afford such a massive project, and algorithmic metrics come with its own set of pitfalls.

Therefore, the testing methodology is (highly) opinionated, as we have made a number of decisions based on what we think is best. Every time I read an article on codec testing, I almost always get frustrated by questionable choices left and right, and leave with dozens of questions left unanswered. Let me save you from the same frustration by walking through the decisions we’ve made. You may not agree with our methodology (especially if you hang out on Doom9), and you may have good reasons for doing so, but at least you will have an explanation of why we’ve done what we’ve done.

Software Selection

For HEVC, we use the most popular open-source implementation x265 3.5+95. For AV1, we have picked SVT-AV1 1.4.1 as our encoder as it strikes a balance between quality and encoding speed, but VideoLAN’s dav1d 1.1.0 is the decoder of our choice as it’s a faster implementation. For VVC, we use Fraunhofer’s Versatile Video Encoder VVenC 1.7.0, an extensive optimized encoder based on the reference design VTM, and its sibling decoder VVdeC 1.6.1.

We also use FFmpeg to assist with our testing. VVC is not implemented by FFmpeg at the moment, so we use the VVC v6 patch to provide such support. Both encoding and decoding are ran on an 8-core, 16-thread KVM on the second CCD of an AMD Ryzen 7950X.

Software encoding can be painstakingly slow, and we have only tested this one clip as it already took weeks to process. To make the problem worse, no comparison can represent all use cases. Please note the limitation that if your source material is drastically different from a typical film such as Sintel, you might produce different results from ours.

Codec Usage

We have decided to test the aforementioned codecs for archival purposes. As no mainstream system can software encode any of the three codecs on the fly, it is difficult to test them for streaming purposes. Perhaps we can come up with a follow-up article to dive into common GPU hardware encoder implementations. Let us know if you’re interested.

Video archiving leads to two major assumptions: one, archival generally aims for the “best” subjective quality at the smallest file size; two, encoding time doesn’t matter. These two assumptions will later help us decide our encoding parameters.

Encoder Tuning

Rate Control

For x265 and SVT-AV1, we use Constant Rate Factor (CRF) for rate control. In short, CRF is optimal for archival as it ensures consistent quality for a given file. We start our testing at the default CRF while controlling the average VMAF score between 91 and 96.

VVenC is still in heavy development and doesn’t currently support CRF. Therefore, we use the next best option – two-pass variable bitrate (VBR) – for VVC. In this case, we start encoding at 1000 kbps, and increase the bitrates by 500 kbps until we reach an average VMAF of 96. During the first pass, the encoder dynamically allocates bitrates based on scene complexity. Then the encoder uses the collected information to encode the video for the second pass.

Presets

Each encoder has dozens of parameters, and different source materials can benefit from different tunings to achieve optimal compression efficiency and quality. However, since we’re comparing codecs rather than encoder settings, we assume the encoder presets are sane and have decided to use the presets. Since encoding time doesn’t matter, we use the slowest preset for each encoder to achieve best compression efficiency.

For SVT-AV1, the slowest preset is 0; for VVenC, the slowest is “slower.” The slowest preset for x265 is “placebo,” but we use “veryslow” instead. As the name suggests, the improvements from “veryslow” to “placebo” is negligible, but the encoding time is a lot longer as “placebo” has reached past the point of diminishing returns.

Beyond presets, we choose 10-bit colour outputs as it generally improves compression efficiency and reduces artifacts at the expense of encoding time. x265 disables AVX-512 support by default due to clock speed regressions on Intel Skylake-X systems. Since we’re using an AMD system, we manually enable AVX-512 to speed up encoding.

We use Netflix’s Emmy-winning Video Multimethod Assessment Fusion (VMAF) to assess visual quality, as it’s the best available tool at the moment. VMAF uses machine learning to predict subjective video quality, and we use the vmaf_4k_v0.6.1 model specifically trained for 4K. As discussed, visual quality is subjective. But for the sake of quantitive analysis, we target at an average VMAF score of 95 for our final encode as the “best” quality.

However, VMAF is not perfect, and solely relying on algorithms is problematic, as machines ultimately perceive visuals differently from humans. Therefore, we will also take a closer look at the final encodes, and compare our findings with VMAF scores.

Result

Compression Efficiency

Figure 1. Compression efficiency of HEVC, AV1 and VVC at various visual quality according to VMAF at 4K resolution.

The VMAF scores show a clear advantage for VVC, delivering the highest quality at any given bitrate. HEVC and AV1 traded blows, with AV1 performing better at lower quality between VMAF 91 to 94, and HEVC performing better at higher quality between VMAF 94 to 96. But at the target VMAF 95, HEVC’s delivered an extra 5.6% bitrate savings than AV1.

Computational Complexity

Figure 2. Computational complexity of HEVC, AV1 and VVC according to encoding and decoding speed at VMAF 95. Test ran on an 8-core, 16-thread KVM on the second CCD of an AMD Ryzen 7950X. *VVenC scales poorly beyond 8 threads.

Here, we expectedly see a geometric increase in computational complexity in newer codecs. Although we say encoding time doesn’t matter, AV1 is 7.5x slower than HEVC, and VVC took literal days to encode a 14-minute clip using the slowest preset. The large discrepancy will ultimately affect decisions on codec selection and encoder tunings in real-life applications.

We put an asterisk behind VVC’s encoding time because we have found VVenC struggles to scale beyond 8 threads despite running on an 16-thread machine. I’m confident that future optimizations can drastically improve encoding time on high core-count machines.

The decoding speed is reasonable for all 3 codecs, but the tests were ran on an 8-core desktop system. In the age of mobile device proliferation, hardware-accelerated decoding is critically necessary for a codec’s adoption. Hardware acceleration will not only help mobile devices conserve battery life, but also ensure good playback performance on TVs and set-up boxes using similar SOCs.

Visual Quality at VMAF 95

Figure 3. Visual quality of each frame encoded in HEVC according to VMAF at average VMAF 95.

Figure 4. Visual quality of each frame encoded in AV1 according to VMAF at average VMAF 95.

Figure 5. Visual quality of each frame encoded in VVC according to VMAF at average VMAF 95.

According to VMAF, newer codecs produce less consistent quality across frames. The most consistent quality came from x265 with the lowest 1% score of 84.67. Meanwhile, the 1% low for AV1 is 81.28, and 79.26 for VVC.

Wait, what?

A Closer Look: Adaptive Quantization

VMAF is suggesting newer codecs have better compression efficiency, but visual quality is less consistent across frames. However, we were using CRF and 2-pass VBR for rate control, which should give us consistent quality throughout a video. What’s happening here?

If you dig through the manuals, you’ll see all three encoders have “benchmark modes,” which disable psycho-visual optimizations in exchange of higher algorithmic metrics scores, including VMAF. We deliberately choose not to use benchmark modes because we’ve decided to aim for the “best” subjective quality, rather than replicating exact copies of every frame. This also gives all three encoders an equal starting point as we’re not interested in which encoder is best optimized for benchmarking.

But what are the psycho-visual optimizations? Why do encoders and VMAF interpret visual quality so differently? Let us take a closer look at a specific frame then. According to VMAF, frame 11506 is VVC’s worst frame, which also happens to be HEVC’s 9th worst frame. How does it look?

We see drastic differences between three codecs in frame 11506. HEVC retained most details, and VVC is outright blurry in some areas. The screenshots do corroborate VMAF’s frame-by-frame analysis, but it raises another question. Videos are motion pictures. This frame comes from a fast, panning transition scene, and it’s only shown for 1/24 of a second. How does the scene look like when it’s playing?

With the fast camera movement, the difference in visual quality is arguably negligible across all codecs despite the degradations in individual frames. I want to point out that we – including you, my dear readers – are staring at and scrutinizing the tree, but the average viewer likely isn’t.

Earlier, we mentioned that it is problematic to solely rely on VMAF, which penalizes psycho-visual optimizations. One of these optimizations is Adaptive Quantization (AQ). When watching motion pictures, the human eye is more sensitive to certain regions of a frame. For example, we’re more drawn to flat and low-texture regions – usually foreground – than the background high-texture regions. We’re also more drawn to high-motion areas than low-motion areas. In Sintel‘s frame 11506, the tree is not only the high-texture background, but also moves quickly to give way to the protagonist in the foreground. AQ redistributes more bits to where the human eye is drawn to, and therefore allows encoders to vary compression within a frame to improve subject visual quality at the expense of background details.

This is why VMAF shows less consistent quality in newer codecs. Although VMAF is a state-of-the-art machine learning algorithm, it ultimately looks at motion pictures differently from humans. We watch videos, but VMAF watches frames.

Result 2: Electric Boogaloo

Earlier, we compared VMAF results between HEVC, AV1 and VVC. Although VMAF is a useful metric, we now know it doesn’t accurately represent perceptual visual quality. If we were to correct for VMAF’s biases, at the same average score, newer codecs would produce higher perceptual quality overall due to improvements in Adaptive Quantization. Therefore, AV1 would be generally on par with, and sometimes surpass HEVC in terms of compression efficiency. VVC would still be the best codec among the three.

There are also some real-life implications from our results. If you want to retain as much detail as possible, then you might want to use an older codec, such as AVC, and turn off psycho-visual optimizations. For home labs, HEVC is probably the best codec of the time since royalties are rarely relevant for personal use. Although the compression efficiency isn’t the best, HEVC enjoys significantly faster encoding speed and widespread hardware decoding support. VVC theoretically has the best compression efficiency, but at the time of the writing, we could not find any video player that supports it out of the box, let alone any hardware acceleration. VVC is still in heavy development, but it looks good for the future.

Born in between MPEG LA’s two generations of codecs, AV1’s biggest advantage is that it’s royalty-free, which makes it attractive for commercial usage, but everything is almost always more complicated than it seems. Sisvel, a patent licensing outfit, has already started a patent pool for AV1. Although AOMedia published a statement to establish a legal defence program against patent claims, no one can predict what the future holds.

As previously mentioned, I don’t feel qualified to make legal commentary as I don’t have a law degree, but I’m allowed to complain. Although HEVC is on par with AV1 in terms of compression efficiency, AV1 is so much more computationally complex, and thus energy inefficient, because AOMedia actively avoids patents that they don’t possess. VVC faces the same patent problem as HEVC, and even AV1’s royalty-free status needs an asterisks at the end.

It’s truly a shame. In the field of multimedia, almost all important techniques and formats are covered by broad and trivial patents. If HEVC isn’t encumbered by patents and royalties, we’d have been in the HEVC-era by now with significant bandwidth and storage savings. Valuable engineering resources can be put into improving existing codecs for everyone, instead of painstakingly creating new ones that might ultimately also be embroiled in patent disputes. As a fan of free, libre software, I feel strongly that patents shouldn’t be exploited to impede progress and innovation in the pursuit of profit. The future looks bright when we look at the technology itself, but the future is also dishearteningly complicated.

If you like our articles and journalism, and you want to support us in our endeavors, then consider heading over to our Patreon or our PayPal if you want to toss a few bucks our way. If you would like to talk with the Chips and Cheese staff and the people behind the scenes, then consider joining our Discord.