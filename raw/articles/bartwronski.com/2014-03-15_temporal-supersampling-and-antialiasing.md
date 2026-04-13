---
title: Temporal supersampling and antialiasing
url: https://bartwronski.com/2014/03/15/temporal-supersampling-and-antialiasing/
published: '2014-03-15'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Aliasing problem

Before I address temporal supersampling, just a quick reminder on what aliasing is.

Aliasing is a problem that is very well defined in signal theory. According to the general sampling theorem we need to have our signal spectrum containing only frequencies lower than Nyquist frequency. If we don’t (and when rasterizing triangles we always will as triangle edge is infinite frequency spectrum, step-like response) we will have some frequencies appearing in the final signal (reconstructed from samples) that were not in the original signal. Visual aliasing can have different appearance, it can appear as regular patterns (so-called moire), noise or flickering.

## Classic supersampling

Classic supersampling is a technique that is extremely widely used by the CGI industry. Per every target image fragment we perform sampling multiple times at much higher frequencies (for example by tracing multiple rays per simply pixel or shading fragments multiple times at various positions that cover the same on-screen pixel) and then performing the signal downsampling/filtering – for example by averaging. There are various approaches to even easiest supersampling (I talked about this in [one of my previous blog posts](https://bartwronski.com/2014/02/05/compare-it/)), but the main problem with it is the associated cost – N times supersampling means usually N times the basic shading cost (at least for some pipeline stages) and sometimes additionally N times the basic memory cost. Even simple, hardware-accelerated techniques like MSAA that do estimate only some parts of the pipeline (pixel coverage) in higher frequency and don’t provide as good results, have quite big cost on consoles.

But even if supersampling is often unpractical technique, it’s temporal variation can be applied with almost** zero** cost.

## Temporal supersampling theory

So what is the *temporal* *supersampling*? Temporal supersampling techniques base on a simple observation – from frame to frame most of the on-screen screen content do not change. Even with complex animations we see that multiple fragments just change their position, but apart from this they usually correspond to at least some other fragments in previous and future frames.

Based on this observation, if we know the precise texel position in previous frame (and we often do! Using motion vectors that are used for per-object motion blur for instance), we can distribute the multiple fragment evaluation component of supersampling between multiple frames.

What is even more exciting is that this technique can be applied to any pass – to your final image, to AO, screen-space reflections and others – to either filter the signal or increase the number of samples taken. I will first describe how it can be used to supersample final image and achieve much better AA and then example of using it to double or triple number of samples and quality of effects like SSAO.

## Temporal antialiasing

I have no idea which game was the first to use the temporal supersampling AA, but Tiago Sousa from Crytek had [a great presentation on Siggraph 2011](http://iryoku.com/aacourse/) on that topic and its usage in Crysis 2 [1]. Crytek proposed using a sub pixel jitter to the final MVP transformation matrix that alternates every frame – and combine two frames in post-effect style pass. This way they were able to increase the sampling resolution twice at almost no cost!

Too good to be true?

Yes, the result of such simple implementation looks *perfect* on still screenshots (and you can implement it in just couple hours!***), but breaks in motion. Previous frame pixels that correspond to current frame were in different positions. This one can be easily fixed by using motion vectors, but sometimes the information you are looking for was occluded or had. To address that, you cannot rely on depth (as the whole point of this technique is having extra coverage and edge information from the samples missing in current frame!), so Crytek proposed relying on comparison of motion vector magnitudes to reject mismatching pixels.

***yeah, I really mean maximum one working day if you have a 3D developer friendly engine. Multiply your MVP matrix with a simple translation matrix that jitters in (-0.5 / w, -0.5 / h) and (0.5 / w, 0.5 / h) every other frame plus write a separate pass that combines frame(n) and frame(n-1) together and outputs the result.

## Usage in Assassin’s Creed 4 – motivation

For a long time we relied on FXAA (aided by depth-based edge detection) as a simple AA technique during our game development. This simple technique usually works “ok” with static image and improves its quality, but breaks in motion – as edge estimations and blurring factors change from frame to frame. While our motion blur (simple and efficient implementation that used actual motion vectors for every skinned and moving objects) helped to smooth edge look for objects moving quite fast (small motion vector dilation helped even more), it didn’t do anything with calm animations and subpixel detail. And our game was full of them – just look at all the ropes tied to sails, nicely tessellated wooden planks and dense foliage in jungles! 🙂 Unfortunately motion blur did nothing to help the antialiasing of such slowly moving objects and FXAA added some nasty noise during movement, especially on grass. We didn’t really have time to try so-called “wire AA” and MSAA was out of our budgets so we decided to try using temporal antialiasing techniques.

I would like to thank here especially Benjamin Goldstein, our Technical Lead with whom I had a great pleasure to work on trying and prototyping various temporal AA techniques very late in the production.

## Assassin’s Creed 4 XboxOne / Playstation 4 AA

As a first iteration, we started with single-frame variation of morphological [SMAA by Jimenez et al](http://www.iryoku.com/smaa/). [2] In its even most basic settings it showed definitely better-quality alternative to FXAA (at a bit higher cost, but thanks to much bigger computing power of next-gen consoles it stayed in almost same budget compared to FXAA on current-gen consoles). There was less noise and artifacts and much better morphological edge reconstruction , but obviously it wasn’t able do anything to reconstruct all this subpixel detail.

So the next step was to try to plug in temporal AA component. Couple hours of work and voila – we had **much** better AA. Just look at the following pictures.

Pretty amazing, huh? 🙂

Sure, but this was at first the result only for static image – and this is where your AA problems start (not end!).

## Getting motion vectors right

Ok, so we had some subtle and we thought “precise” motion blur, so getting motion vectors to allow proper reprojection for moving objects should be easy?

Well, it wasn’t. We were doing it right for **most** of the objects and motion blur was ok – you can’t really notice lack of motion blur or slightly wrong motion blur on some specific objects. However for temporal AA you need to have them proper and pixel-perfect for all of your objects!

Other way you will get huge ghosting. If you try to mask out this objects and not apply temporal AA on them at all, you will get visible jittering and shaking from sub-pixel camera position changes.

Let me list all the problems with motion vectors we have faced and some comments of whether we solved them or not:

- Cloth and soft-body physical objects. From our physics simulation for cloth and soft bodies that was very fast and widely used in the game (characters, sails) we got full vertex information in world space. Object matrices were set to just identity. Therefore, such objects had zero motion vector (and only motion from camera was applied to them). We needed to extract such information from the engine and physics – fortunately it was relatively easy as it was used already for bounding box calculations. We fixed ghosting from moving soft body and cloth objects, but didn’t have motion vectors from the movement itself – we didn’t want to completely change the pipeline to GPU indirections and subtracting positions from two vertex buffers. It was ok-ish as they wouldn’t move very abruptly and we didn’t see artifacts from it.
- Some “custom” object types that had custom matrices and the fact we interpreted data incorrectly. Same situation as with cloth existed also for other dynamic objects. We got some custom motion vector debugging rendering mode working and fixing all those bugs was just matter of couple days in total.
- Ocean. It was not writing to the G-buffer. Instead of seeing motion vectors of ocean surface, we had proper information, but for ocean floor or “sky” behind it (when with very deep ocean there was no bottom surface at all). The fix there was to overwrite some G-buffer information like depth and motion-vectors. However, still we didn’t store previous frame simulation results and didn’t try to use them, so in theory you could see some ghosting on big and fast waves during storm. It wasn’t very big problem for us and no testers ever reported it.
- Procedurally moving vegetation. We had some vertex noise based artist-authored vegetation movement and again, difference between two frame vertex position values wasn’t calculated to produce proper motion vectors. This is single biggest visible artifact in game from temporal AA technique and we simply didn’t have the time to modify our material shader compiler / generator and couldn’t apply any significant data changes in patch (we improved AA in our first patch). Proper solution here would be to automatically replicate all the artist created shader code that calculates output local vertex position if it relies on any input data that changes between frames like “time” or closest character entity position (this one was used to simulate collision with vegetation), pass it through interpolators (perspective correction!), subtract it and have proper motion vectors. Artifacts like over blurred leaves are sometimes visible in the final game and I’m not very proud of it – although maybe it is usual programmer obsession. 🙂
- Objects being teleported on skinning. We had some checks for entities and meshes being teleported, but in some single and custom cases objects were teleported using skinning – it would be impractical to analyze whole skeleton looking for temporal discontinuities. We asked gameplay and animations programmers to mark them on such a frame and quickly fixed all the remaining bugs.

## Problems with motion vector based rejection algorithm

Ok, we spend 1-2 weeks on fixing our motion vectors (and motion blur also got much better! 🙂 ), but in the meanwhile realized that the approach proposed by Crytek and used in SMAA for motion rejection is definitely far from perfect. I would divide problems into two categories.

### Edge cases

It was something we didn’t really expect, but temporal AA can break if menu pops up quickly, you pause the game, you exit to console dashboard (but game remains visible), camera teleports or some post-effect immediately kicks in. You will see some weird transition frame. We had to address each case separately – by disabling the jitter and frame combination on such frame. Add another week or two to your original plan of enabling temporal AA to find, test and fix all such issues…

### Wrong rejection technique

This is my actual biggest problem with naive SMAA-like way of rejecting blending by comparing movement of objects.

First of all, we a had very hard time to adjust the “magic value” for the rejection threshold and 8-bit motion vectors didn’t help it. Objects were either ghosting or shaking.

Secondly, there were huge problems on for example ground and shadows – the shadow itself was ghosting – well, there is no motion vector for shadow or any other animated texture, right? 🙂 It was the same with explosions, particles, slowly falling leaves (that we simulated as particle systems).

For both of those issues, we came up with simple workaround – we were not only comparing similarity of motion of objects, but on top of it added a threshold value – if object moved faster than around ~2 pixels per frame in current or previous frame, do not blend them at all! We found such value much easier to tweak and to work with. It solved the issue of shadows and visible ghosting.

We also increased motion blur to reduce any potential visible shaking.

Unfortunately, it didn’t do anything for transparent or animated texture changes over time, they were blended and over-blurred – but as a cool side effect we got free rain drops and rain ripples antialiasing and our art director preferred such soft, “dreamy” result. 🙂

Recently Tiago Souse in his Siggraph 2013 talk proposed to [address this issue by changing metric to color-based](http://advances.realtimerendering.com/s2013/index.html) and we will investigate it in the near future [3].

## Temporal supersampling of different effects – SSAO

I wanted to mention another use of temporal supersampling that got into final game on the next-gen consoles and that I really liked. I got inspired by [Matt Swoboda’s presentation](http://directtovideo.wordpress.com/2012/03/15/get-my-slides-from-gdc2012/) [4] and mention of distributing AO calculation sampling patterns between multiple frames. For our SSAO we were having 3 different sampling patterns (spiral-based) that changed (rotated) every frame and we combined them just before blurring the SSAO results. This way we effectively increased number of samples 3 times, needed less blur and got much much better AO quality and performance for cost of storing just two additional history textures. 🙂 Unfortunately I do not have screenshots to prove that and you have to take my word for it, but I will try to update my post later.

For rejection technique I was relying on a simple depth comparison – we do not really care about SSAO on geometric foreground object edges and depth discontinuities as by AO definition, there should be almost none. Only visible problem was when SSAO caster moved very fast along static SSAO receiver – there was visible trail lagging in time – but this situation was more artificial problem I have investigated, not a serious in-game problem/situation. Unlike the temporal antialiasing, putting this in game (after having proper motion vectors) and testing took under a day, there were no real problems, so I really recommend using such techniques – for SSAO, screen-space reflections and many more. 🙂

## Summary

Temporal supersampling is a great technique that will increase final look and feel of your game a lot, but don’t expect that you can do it in just couple days. Don’t wait till the end of the project, “because it is only a post-effect, should be simple to add” – it is not! Take weeks or even months to put it in, have testers report all the problematic cases and then properly and iteratively fix all the issues. Have proper and optimal motion vectors, think how to write them for artist-authored materials, how to batch your objects in passes to avoid using extra MRT if you don’t need to write them (static objects and camera-only motion vector). Look at differences in quality between 16bit and 8bit motion vectors (or maybe R11G11B10 format and some other G-Buffer property in B channel?), test all the cases and simply take your time to do it all properly and early in production, while for example changing a bit skeleton calculation or caching vertex skinning information (having “vertex history”) is still an acceptable option. 🙂

### References

[1] [http://iryoku.com/aacourse/ ](http://iryoku.com/aacourse/)

AC4 AA on PS4 is indeed outstanding! Please use if for all Ubisoft games on next gen. No more blurry FXAA please!

Pingback: VR And Multi-GPU – Nathan Reed's coding blog

Pingback: Temporal supersampling pt. 2 – SSAO demonstration | Bart Wronski

Hi! I enjoyed your post very much and is implementing the same temporal AA in my 4K demo. However, there is one confusion I had about the jittering matrix. You said “Multiply your MVP matrix with a simple translation matrix that jitters in (-0.5 / w, -0.5 / h) and (0.5 / w, 0.5 / h)”. I assume w and h mean screen width and height and 0.5 = 0.25*2 which indicates you are working in NDC. But NDC is only obtained after perspective division, which is performed by GPU after vertex shader and you can’t have that in vertex shader. By multiplying the MVP matrix directly with the jitter translation matrix, you are basically doing the jittering in clip space, in which case you should jitter different amount for vertices at different depth, not uniformly like you does in NDC. Sorry about my unclear explanation…please correct me if I am missing something. Thanks a lot!

Hi Nemo!

You are right that one cannot add to (x,y,z,w) clip space (tx,ty,0,0). But this is not how translation matrices work. 🙂 They worked based on assumption of uniform coordinate system, typically 1 in w (this w gets multiplied by proper translation matrix column/row) – but after perspective projection w doesn’t contain 1. So if you multiply such matrices, you end up with (x + tx*w, y + ty*w, z, w), which after division by w produce correct results. Cheers!

Ahhh! After doing some hand calculation, I found that multiplying MVP by the jitter translation matrix and dividing the result by w yields the same result as doing perspective division first and applying the jitter translation matrix to the NDC coordinates. Thank you very much!!!!

Hello Sir!

I really liked this post and your other work in graphics. I am implementing TAA in my demo

and I did exactly like you said, Adding jitter in perspective matrix and then subtracted it from texCoords to remove the jitter(with right range). Jitter is almost gone but not completely gone. Is it a precision issue after perspective divide or I am missing something? I am using float32 matrix.(This is for static scene so there is no velocity yet).Thank a lot!

Hi Ninad, I am not sure if I understand 100% correctly the issue you are describing, but some camera shaking will stay – it depends on the used robustness etc. But if the TAA doesn’t average two frames 100%, we are expected to see some jittering and shaking.

Thank you for the reply.

If we add jitter in perspective matrix like you said :

PerspectiveMatrix[2][0]=jitter.x;//(-0.5/w to 0.5/w)

PerspectiveMatrix[2][1]=jitter.y;//(-0.5/h to 0.5/h)

and then if we output like this on screen quad:

fragColor = texture(currentColorBufferSampler, ((UV*2.0-1.0) – jitter.xy )*0.5 + 0.5);

Here we are supposed to get unjittered stable colors because we are subtracting the jitter from uv.

And like you explained before, the division by w should produce correct values for (x + tx*w, y + ty*w, z, w) and I am getting correct values but losing some precision. So I don’t know where I am losing the precision of jitter because jitter is not completely gone from output frame. Please correct me with what I am missing here. Thank you for your time.

No, this will not make the jitter completely gone – after all, we are introducing it to introduce new information between frames.

We rely on this shaking and difference to produce antialiased edges. If it was enough to just change the UVs, why would we need to change the perspective projection matrix in the first place?

Pingback: Temporal supersampling, flipquads and real time raytracing | The blog at the bottom of the sea

Pingback: FlipQuad & FlipTri Antialiasing | The blog at the bottom of the sea

Hi~I tried to add TemporalAA in our engine, but I have trouble with the blurry of dynamic objects,it seems the dynamic objects, like character, will become blurry because of the linear filter of previous frame target, how do you fix this problem in Assassin’s Creed 4?

Hi, this is the biggest difficulty in temporal techniques – getting good acceptance/rejection logic. You cannot simply “accept” previous frame pixels, because they will contain some dis-occluded information. There are various heuristics for this purpose (none of them perfect!) and depending on the use-case. Common ones are using motion similarity (SMAA 2TX), depth similarity (for SSAO techniques) or color similarity or even history clamping (SMAA 1TX, UE4 AA, Drobot’s HRAA). It is possible to get rid of those artifacts, but it means tons of tweaking and bug-fixing.

Thanks:) I tried to reduce the blending weight of previous frame by analyzing the difference of velocity, and it looks much better.

Pingback: Devblog 118 | Inglorious

Pingback: Dev Blog 118 – RusticNation

Pingback: Rust - Devblog 118 - Traduction Complète ! | france-rust.fr

Pingback: Devblog 118 — RUST4PRO — Официальный сайт проекта

Pingback: Why are video games graphics (still) a challenge? Productionizing rendering algorithms | Bart Wronski

Pingback: Study of smoothing filters – Savitzky-Golay filters | Bart Wronski

Pingback: Gradient-descent optimized recursive filters for deconvolution / deblurring | Bart Wronski