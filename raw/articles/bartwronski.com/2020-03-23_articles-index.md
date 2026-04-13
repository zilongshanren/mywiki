---
title: Articles index
url: https://bartwronski.com/articles-blog-posts-index/
published: '2020-03-23'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Categories

Note: In each category, post are sorted in reverse chronological order. I have marked posts that I think are particularly interesting and stood the test of time (by looking at high view counts, or using my subjective judgement) with **bold **and a star ⭐ .

## Image processing

[Gradient-descent optimized recursive filters for deconvolution / deblurring](https://bartwronski.com/2022/09/05/gradient-descent-optimized-recursive-filters-for-deconvolution-deblurring/) **September 2022** – Explanation of infinite impulse response (recurrent) filters, their desirable properties, as well as practical implementation obstacles. In the second part of the post, I propose a novel, data-driven optimization-based method of designing symmetric recurrent filters.

** Removing blur from images – deconvolution and using optimized simple filters ⭐ May 2022** – Mathematical and signal processing background on how can we “unblur” an image, practical problems, and a way to do it real-time efficiently through a linear combination of “simple” filters.

[Fast, GPU friendly, antialiasing downsampling filter](https://bartwronski.com/2022/03/07/fast-gpu-friendly-antialiasing-downsampling-filter/) **March 2022** – A very fast, very high quality 2X downsampling filter that I propose to use everywhere as a drop-in replacement to bilinear / box downsampling. Designed with anti-aliasing, sharpness, and performance in mind.

[Practical Gaussian filtering: Binomial filter and small sigma Gaussians](https://bartwronski.com/2021/10/31/practical-gaussian-filter-binomial-filter-and-small-sigma-gaussians/) **October 2021** – Two “tricks” related to Gaussian filter / blur in a practical setting: a binomial filter, a great approximation to Gaussian filters that is particularly well suited for CPUs, DSPs and a fixed point implementations. Second trick is observation how point sampling a Gaussian PDF undersamples and leads to wrong results for small sigma (<0.7) Gaussians and how to fix it.

[Processing aware image filtering: compensating for the upsampling](https://bartwronski.com/2021/07/20/processing-aware-image-filtering-compensating-for-the-upsampling/) **July 2021** – given a fixed upsampling filter of poor quality (like super-fast, hardware accelerated bilinear filter), can we design a downsampling filter that would improve on some of its shortcomings and produce images closer to the input? Yes! I present a few alternatives and observe how it relates to mip map filtering.

** Bilinear down/upsampling, aligning pixel grids, and that infamous GPU half pixel offset ⭐ February 2021** – what is bilinear downsampling/upsampling? where are pixels located in a pixel grid? Where are borders of the image? How this relates to

*infamous*“half texel offset”? Should your down/upsampling filters be odd or even? I dig deep into one of the most basic, most important – yet most misunderstood! – topics in image processing and computer graphics.

** Bilinear texture filtering – artifacts, alternatives, and frequency domain analysis ⭐ April 2020** – bilinear filtering is “bread and butter” of all real-time computed graphics and one of the most commonly used filtering techniques ever – to large extent because of native GPU hardware acceleration. In this post I analyze star-shaped “bilinear artifacts”, shortcomings of the filter, some commonly used alternatives, and spectral (Fourier) properties of all of those.

**Using JAX, numpy, and optimization techniques to improve separable image filters **⭐**March 2020** – using “optimization” techniques and gradient descent in numpy and JAX to improve low-rank separable image filters (see below) and remove some of their visual artifacts (ringing, negative values, unpleasant corners).

[Separate your filters! Separability, SVD and low-rank approximation of 2D image processing filters](https://bartwronski.com/2020/02/03/separate-your-filters-svd-and-low-rank-approximation-of-image-filters/) **February 2020** – how to tell if an image processing 2D filter is separable, and finding separable approximations (up to a rank k – k multiple passes of separable filter) of some common filters commonly used in graphics, e.g. circular or hexagonal *bokeh*.

**Local linear models and guided filtering – an alternative to bilateral filter** ⭐**September 2019** – how fitting linear models locally (through least-squares in a small window around a pixel) can be a great cheap alternative to bilateral filter – both for filtering a single image, but also for joint / guided bilateral, and bilateral upsampling. I show the technique using SSAO filtering example.

[Checkerboard rendering, rotated anti-aliasing and grid frequencies](https://bartwronski.com/2018/05/14/checkerboard-rendering-rotated-anti-aliasing-and-grid-frequencies/) **May 2018** – description of what is “checkerboard rendering”, Fourier domain analysis of aliasing, reconstruction and why it often makes sense to rotate your sampling grid.

[Separable disk-like depth of field](https://bartwronski.com/2017/08/06/separable-bokeh/) **August 2017** – a very short post where I came back from Siggraph and seeing [“Circularly symmetric convolution and lens blur”](http://yehar.com/blog/?p=1495) by Olli Niemitalo presented as [“Circular Separable Convolution Depth of Field”](http://dl.acm.org/citation.cfm?id=3085022) by Kleber Garcia blew my mind so much that I had to implement it myself in Shadertoy for demonstration. 🙂

## Machine Learning, Data Science and Analysis

[Procedural Kernel (Neural) Networks](https://bartwronski.com/2022/01/03/procedural-kernel-neural-networks/) **January 2022** – quick note on a technical report / paper I wrote on using very small neural networks to produce parameters for traditional algorithms and generate functional kernels like bilateral/non-local means, anisotropic Gaussian, polynomial reblurring. Those networks train in less than 10min on a single GPU machine, have less than 20k parameters, and allow for significantly improving the results of traditional algorithms, reduce costly tuning process, interpretability, as well as some novel applications of old techniques.

[Comparing images in frequency domain. “Spectral loss” – does it make sense?](https://bartwronski.com/2021/07/06/comparing-images-in-frequency-domain-spectral-loss-does-it-make-sense/) **July 2021** – I look into how recent ML papers use (differently defined) “spectral loss” and try to compare images in Fourier domain – and how most of them are unfortunately wrong – either proposed loss is equivalent to L2/pointless, or introduces a singularity.

[Neural material (de)compression – data-driven nonlinear dimensionality reduction](https://bartwronski.com/2021/05/30/neural-material-decompression-data-driven-nonlinear-dimensionality-reduction/) **May 2020** – more experiments with compressing whole PBR materials / texture sets together – this time we use tiny Neural Networks (Multi Layer Perceptor) and explore power of data driven nonlinearity.

[Compressing PBR material texture sets with sparsity and k-SVD dictionary learning](https://bartwronski.com/2020/08/30/compressing-pbr-texture-sets-with-sparsity-and-dictionary-learning/) **August 2020** – I look further into compressing whole PBR materials / texture sets (as opposed to single textures) and provide a gentle intro to dictionary learning, sparsity, and k-SVD.

[Dimensionality reduction for image and texture set compression](https://bartwronski.com/2020/05/21/dimensionality-reduction-for-image-and-texture-set-compression/) **May 2020** – how you can use SVD and PCA dimensionality reduction and the correlation between channels for aggressively compressing whole sets of PBR textures/materials.

[Analyze your own activity data using Google Takeout – music listening stats example](https://bartwronski.com/2020/01/06/analyze-your-own-activity-data-using-google-takeout/) **January 2020** – how one can “take out” personal data from big internet service providers and then analyze it offline and create cool visual charts. Example on creating personal annual music listening stats for Google Play Music.

## Photography concepts in real-time graphics

**Image dynamic range** ⭐**September 2016** – what is the dynamic range? What is gamma curve/compression, how does it relate to EOTF – Electro Optical Transfer Function? How do viewing conditions impact the dynamic range and why sRGB is different from Rec709? Clearing up many misconceptions and confusions around those topics.

**Localized tonemapping – is global exposure and global tonemapping operator enough for video games?** ⭐**August 2016** – a blog post on why “global tonemapping” is not enough and games need either lighting “hacks”, or some sort of localized tonemapping. Combines some photography experiments, screenshots from **God of War **and introduction to general tonemapping theory.

[White balance and physically based rendering pipelines. Part 1 – introduction.](https://bartwronski.com/2015/10/14/white-balance-and-physically-based-rendering-pipelines-part-1-introduction/) **October 2015** – what is “white balance” as used in photography, and why it matters in real-time graphics. Effects of white balance on perceptual effects (gold/blue dress!), WB adaptation, and in some of the famous works of art. [Part 2](http://White balance and physically based rendering pipelines. Part 2 – practical problems.) discusses some problems that white balance can cause, some of the still unsolved! (e.g. partial / localized white balance).

[Anamorphic lens flares and visual effects](https://bartwronski.com/2015/03/09/anamorphic-lens-flares-and-visual-effects/) **March 2015** – short post on where the (in)famous “JJ Abrams” anamorphic lens flares come from, how they are used in real time graphics, and how one can achieve such an effect.

**Bokeh depth of field – going insane! part 1** ⭐**April 2014** – A blog post where I describe what is “bokeh”, why we care about it in graphics / computational photography, and an “insane” (as in computationally expensive and unreasonable for those times) approach I used in **The Witcher 2**.

## General graphics techniques

[Progressive image stippling and greedy blue noise importance sampling](https://bartwronski.com/2022/08/31/progressive-image-stippling-and-greedy-blue-noise-importance-sampling/) **August 2022** – An exploration of a fun, artistic visual concept – progressive blue-noise stippling and dithering of images. I explain this concept and propose a method based on the modified void-and-cluster algorithm. Beyond interesting visual animations, the method can be used for blue-noise importance sampling of images like environment maps.

** Exposure Fusion – local tonemapping for real-time rendering ⭐ March 2022** – After 6 years (!) I close the loop on the topic of local tonemapping for rendering, proposing to use exposure fusion – older algorithm that works very well in real-time rendering context.

[Light transport matrices, SVD, spectral analysis, and matrix completion](https://bartwronski.com/2022/02/15/light-transport-matrices-svd-spectral-analysis-and-matrix-completion/) **February 2022** – how straight linear algebra can help rendering and computing the light transport. From introductory concepts to more advanced (and semi-novel) analysis and applications – spectral analysis and matrix completion.

[Superfast void-and-cluster Blue Noise in Python (Numpy/Jax)](https://bartwronski.com/2021/04/21/superfast-void-and-cluster-blue-noise-in-python-numpy-jax/) **April 2021** – Explanation and implementation of my simplified, very fast numpy/Jax Python implementation of the void-and-cluster algorithm.

** Why are video games graphics (still) a challenge? Productionizing rendering algorithms ⭐ December 2020** – why graphics research rarely ends in production? Why gamedevs of a game ‘x’ don’t use this amazingly brilliant technique ‘y’? Why we still render mainly with old-school polygonal meshes? Thoughts on how challenging it is to manage a large rendering pipeline and produce content for large scale AAA video games and other real time rendering scenarios.

[“Optimizing” blue noise dithering – backpropagation through Fourier transform and sorting](https://bartwronski.com/2020/04/26/optimizing-blue-noise-dithering-backpropagation-through-fourier-transform-and-sorting/) **April 2020** – Using optimization / backpropagation and numpy/JAX/colab to generate “blue noise” dithering patterns and matrices directly – highly customizable approach in which we design a loss function and run gradient descent on it.

**Cull that cone! Improved cone/spotlight visibility tests for tiled and clustered lighting** ⭐**April 2017** – a very simple, pretty efficient “hybrid” method of testing geometric cone (used for e.g. spotlights, but also potentially AI) intersection suitable for optimizing real-time tiled lighting. Includes some pretty sweet visualizations and is linked quite a bit.

**Dithering in games – mini series** ⭐**October 2016 **– three post series on how dithering can and should be used in video games – why it matters, how it can improve the visual results, what is Golden ratio based low discrepancy sequence, what is blue noise – includes numerical, visual and Fourier-domain comparisons. Quite popular introductory material.

[Fixing screen-space deferred decals](https://bartwronski.com/2015/03/12/fixing-screen-space-deferred-decals/) **Mach 2015** – problem caused by the texture derivatives (used to compute mip-map levels) in the case of analytical/procedural effects that convert from screen to texture/world space, like screen-space deferred decals, and how one can solve them.

[Designing a next-generation post-effects pipeline](https://bartwronski.com/2014/12/09/designing-a-next-generation-post-effects-pipeline/) **December 2014** – a blog post on the post-processing (camera effects, tonemapping, bloom, blurs, but also particle rendering) pipeline that I designed for **Far Cry 4** (and later used almost exactly same one on **God of War**) with the goal of unifying/generalizing all those effects together for fast, half resolution processing.

[Hair rendering trick(s)](https://bartwronski.com/2014/07/20/hair-rendering-tricks/) **July 2014** – a few multi-pass tricks to render character hair (dense, includes transparent parts, as well as complicated BRDFs) on older hardware. A technique we played with for **The Witcher 2/3** games.

[Temporal supersampling pt. 2 – SSAO demonstration](https://bartwronski.com/2014/04/27/temporal-supersampling-pt-2-ssao-demonstration/) **April 2014** – where I extend the [blog post about temporal anti-aliasing](https://bartwronski.com/2014/03/15/temporal-supersampling-and-antialiasing/) to the actual super-sampling part, with some examples from **Assassin’s Creed 4**. Little did I know at that time, that soon everyone will be using temporal super-sampling for everything, and that many years later [I will lead a project at Google that does multi-frame super-resolution for camera zoom](https://arxiv.org/abs/1905.03277).

[GDC follow-up: Screenspace reflections filtering and up-sampling](https://bartwronski.com/2014/03/23/gdc-follow-up-screenspace-reflections-filtering-and-up-sampling/) **March 2014** – quite (out)dated post now on how one can filter and upsample screen-space reflections. See instead my [guided filtering post](https://bartwronski.com/2019/09/22/local-linear-models-guided-filter/)!

[Temporal supersampling and antialiasing](https://bartwronski.com/2014/03/15/temporal-supersampling-and-antialiasing/) **March 2014** – most popular blog post of mine! Introduction to temporal techniques, timed “perfectly” – around when it switched from being an experimental technique, to contemporary ubiquitous state of the art. It’s not very relevant anymore, as state of the art is much better than that, but shows a fun piece of the graphics history. 🙂

[The future of screenspace reflections](https://bartwronski.com/2014/01/25/the-future-of-screenspace-reflections/) **January 2014** – a blog post about screen-space reflections I implemented for **Assassin’s Creed 4: Black Flag**, in hindsight probably quite lame (describing one of the earliest approaches to solving the problem), but conversely in hindsight also quite “visionary” post, as it directly precedented the emergence of a huge SSR hype – to the point that people were joking that one of the main differentiators of PS4/XboxOne games were screen-space reflections and shiny surfaces. 🙂

## Low level / hardware / math / numerical analysis

[Transforming “noise” and random variables through non-linearities](https://bartwronski.com/2022/03/16/transforming-noise-and-random-variables-through-non-linearities/) **March 2022** – what happens to mean and variance of a random variable when it is transformed by non-linear functions (squaring, gamma, piecewise linear), why sRGB OETF has a linear segment, and how transforming a noisy image can cause it to get brighter/darker.

**Small float formats – R11G11B10F precision** ⭐**April 2017 **– description of some “small float” formats (IEEE floating point with less than 32 bits per single channel) – with main focus on 3 channel, R11G11B10F GPU hardware-accelerated float format – analysis of numerical precision, problems how to avoid color banding, comparison to 8 and 10bit sRGB curves. Highly recommended, as I dispel some myths that are still alive – e.g. that pre-exposure can improve color precision (with floats, it won’t!).

**GPUs and GCN – two ways of latency hiding and wave occupancy** ⭐**March 2014** – description of how modern GPUs hide latency – essentially the main difference between their, and CPU memory model. I recommend it to anyone who ever considers writing GPU code, and I include some assembly analysis based on AMDs popular GCN GPU architecture.

## Technical leadership, process, team management, tools

[Praising hacking and low-tech solutions. ChatGPT wrote me a personal Javascript browser “plugin.”](https://bartwronski.com/2023/09/17/praising-hacking-and-low-tech-solutions-chatgpt-wrote-me-a-personal-javascript-browser-plugin/) **September 2023** – sometimes all you need is just “quickly” hacking stuff and not spending many hours tinkering. With Large Language Models, it’s becoming easier than ever. How ChatGPT wrote me a plugin to generate Obsidian Markdown and summarize arXiv papers.

[ Insider guide to tech interviews](https://bartwronski.com/2022/01/04/insider-guide-to-tech-interviews/) ⭐

**January 2022**– how does a technical interview look like in a large or a small company? How to prepare for problem solving, knowledge, and behavioral interviews? How to talk with a recruiter? How to negotiate salary? What questions to ask your future team to make sure for a good fit? And much more!

**How (not) to test graphics algorithms** ⭐**August 2019** – how to test graphics techniques? Why “golden testing” and end to end testing is – in my personal opinion – often a terrible idea? How to incorporate graphics testing in your programming and team workflows.

[Tech and scientific writing – graphics, diagram and graph creation tools](https://bartwronski.com/2017/10/22/tech-and-scientific-writing-graphics-diagram-and-graph-creation-tools/) **October 2017** – a survey of what other graphics programmers use for creating diagrams, graphs and visualizations (spoiler: everyone uses something different! 🙂 but I still give some recommendations).

**Short names are short** ⭐**September 2016** – Opinionated post on programming variable and function naming and why I think that short names are not great for code readability / understandability, and there is no place for them in the XXI century.

**Technical debt… or technical weight?** ⭐**June 2016** – a blog post on *“technical weight”* or *“technical burden”*, which is **not **the same as *“technical debt”*. Sometimes great, clean solutions can slow you and your progress down, and it can be better to do things in more crude, simple, or even hacked way if it allows for faster long term progress.

[On pursuit of (good) free mathematics toolbox](https://bartwronski.com/2014/01/19/mathematics-toolbox/) and [Python as scientific toolbox – 8 months later](https://bartwronski.com/2014/09/16/python-as-scientific-toolbox/) **September 2014** – old posts on how I was trying to find a good free / open-source replacement for Mathematica. Still kind-of-relevant, as my recommendation of using numpy and Jupyter notebooks still stands, but this time the choice is much simpler – use [Google Colab](https://colab.research.google.com/)!

[Runtime editor-console connection in The Witcher 2](https://bartwronski.com/2014/05/13/runtime-editor-console-connection-in-the-witcher-2/) **May 2014** – An idea / tooling we used on Witcher 2 for real-time connection between game editor, and the console, allowing for real-time editing and preview on the target platform (Xbox 360 at that time). I believe now it is quite “standard” in all engines, but was novel to me at that time.

[Compare it!](https://bartwronski.com/2014/02/05/compare-it/) **February 2014** – Importance of having reference implementation and comparing against it. Might seem “obvious” now, but it wasn’t so obvious to most of my colleagues back then and I believe still isn’t a common practice among most games graphics programmers!

[Why big game studios (usually) use single main 3d software environment?](https://bartwronski.com/2014/02/25/why-big-game-studios-usually-use-single-main-3d-software-environment/) **February 2014** – I got asked why most game studios force a single main editing program (like Maya and 3D Studio Max) and I provide probably all the possible answers – there are many reasons!

## Audio, DSP, and audio programming

[Study of smoothing filters – Savitzky-Golay filters](https://bartwronski.com/2021/11/03/study-of-smoothing-filters-savitzky-golay-filters/) **November 2021** – A quick study and a DSP analysis of Savitzky-Golay filters (low degree polynomial fits to sample points) and a proposal how to improve them through windowing to improve their behavior around Nyquist.

[Modding Korg MS-20 Mini – PWM, Sync, Osc2 FM](https://bartwronski.com/2021/10/14/modding-korg-ms-20-mini-pwm-sync-fm/) **October 2021** – some basic electronics and DIY to add extra capabilities to a Korg MS-20 analog synthesizer.

[Converting wavetables to Ableton Operator AMS waves](https://bartwronski.com/2021/01/05/converting-wavetables-to-ableton-operator-ams-waves/) **January 2021** – using wavetables (from wavetable synthesis) in Ableton Operator additive/FM synthesis soft synth and information about additive synthesis, FFT on wavetables, and role/importance of the phase in tonal synthesis.

## Photography

[Processing scanned/DSLR photos of film negatives in Lightroom](https://bartwronski.com/2015/02/19/processing-scanneddslr-photos-of-film-negatives-in-lightroom/) **February 2015** – How to process scanned film negatives (and turn them to positives), without leaving convenient Adobe Lightroom.

[Voigtlander Nokton Classic 40mm f1.4 M on Sony A7 Review](https://bartwronski.com/2014/08/08/voigtlander-nokton-classic-40mm-f1-4-m-on-sony-a7-review/) **August 2014** – Review of a classic-like, manual focus beautiful lens perfect for a mirrorless digital camera. Interestingly, a post that seems “random” to my blog, but is also the most popular I ever wrote! 🙂

[Coming back to film photography](https://bartwronski.com/2014/06/08/coming-back-to-film-photography/) **June 2014** – how I tried to get back to film photography (I have a long, personal relationship with it), some photos, and thoughts about it. In hindsight, my attempt to get back to it didn’t succeed heh.

[Sony A7 review](https://bartwronski.com/2014/07/31/sony-a7-review/) **July 2014** – a quick review of my first mirrorless camera.

## Personal / projects / updates / misc / random

[I left Silicon Valley for NYC 2.5y ago – a retrospective](https://bartwronski.com/2023/09/04/i-left-silicon-valley-for-nyc-2-5y-ago-a-retrospective/) **September 2023** – Follow-up to the “Leaving California” post. Did NYC fulfill my hopes, dreams, and expectations? Did such a move “destroy my (tech) career”?

[On leaving California and the Silicon Valley](https://bartwronski.com/2021/06/28/on-leaving-california-and-the-silicon-valley/) **June 2021** – A very personal post; some of my thoughts on California, San Francisco Bay Area, suburbs and why it wasn’t a life choice and lifestyle for me.

[New debugging options in CSharpRenderer framework](https://bartwronski.com/2014/09/14/new-debugging-options-in-csharprenderer-framework/) and [CSharpRenderer Framework update](https://bartwronski.com/2014/10/18/csharprenderer-framework-update/) **October 2014** – Some updates to my CSharpRenderer, in hindsight has a few cool, usable ideas for debugging, as well as “bilateral vectors” – optimization for precomputing optimal UVs for depth-guided bilateral upsampling ahead of time.

[Review: “Multithreading for Visual Effects”, CRC Press 2014](https://bartwronski.com/2014/09/21/review-multithreading-for-visual-effects/) **September 2014** – a review of a book about multi-threading use in the VFX industry.

[C#/.NET graphics framework on GitHub + updates](https://bartwronski.com/2014/06/08/c-net-graphics-framework-on-github-updates/) **June 2014** – update post, but includes IMO a cool and somewhat novel idea -> “scriptable” constant / uniform buffers with procedural, scripted rules describing how they are derived. Allows for coupling together all shader logic in a single file, while still allowing for CPU pre-computation and optimization.

[C#/.NET graphics framework](https://bartwronski.com/2014/04/10/c-net-graphics-framework/) **April 2014** – Description of my own, [open-source DX11 graphics prototyping framework](https://github.com/bartwronski/CSharpRenderer), motivations, some implementations details and ideas that can be incorporated in graphics engines.

[My first visit to Cuba](https://bartwronski.com/2014/01/05/my-first-visit-to-cuba/) **January 2014** – my first blog post ever! About my personal travel to Cuba.