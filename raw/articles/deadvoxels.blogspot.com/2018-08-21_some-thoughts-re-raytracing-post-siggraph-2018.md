---
title: Some thoughts re Raytracing post-Siggraph 2018.
url: http://deadvoxels.blogspot.com/2018/08/some-thoughts-re-siggraph-2018.html
author: Jon Greenberg
published: '2018-08-21'
source_blog: Dead Voxels
source_site: http://deadvoxels.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

Okay, so unless you've spent the last week or so living under a rock or simply don't care about graphics, you've probably heard by now about Turing, nVidia's upcoming GPU architecture that handles realtime raytracing. It's not the first push towards this at the hardware level, but it's certainly the first to get this level of a marketting push and by far the most actively promoted to ISVs (ie, gamedevs). It's also well timed in that its actually clear to the game-graphics community, for perhaps the first time, that one can yield some kind of practical win from raytracing despite very limited ray-per-pixel counts.

It's exciting stuff, to be sure. Even if there are lots of open-ended questions/doubts about how one handles various types of content or situations it still adds a rush knowing that yet again the real-time rendering half-life of about 5 years has kicked in and.. half of what you took for granted flies out the window along with scrambling to learn new paradigms.

All that said, it's still not really clear how a lot of this stuff will work in practice. The announced cards are hardly cheap, and it's still unclear where other IHVs like AMD and Intel will fall in the mix. So it's not like we can count of customers having the hardware in large numbers for quite a while.. which means hybridized pluggable pipelines (ie, working your shadowmap shadows to result in a resolved mask that can be swapped for a high quality raytraced result).

Even then, it's not clear what best practices are for gamedevs to consider for all sorts of common scenarios we encounter daily at the moment. A straightforward example of this to consider would be a non-bald human hero character standing in a forest.

- Raytracing relies on rebuilds/refits of BVH structures to describe the dynamic elements in the scene but its certainly not clear how best to manage that, and it seems that currently no one's really sure.

- Do you separate your dynamic elements into a separate BVH from your statics, to reduce the refit burden? But that means needing to double your ray-testing... probably everywhere.

- Presumably the BVH needs to reside in video memory for the raytracing hardware to be effective, but what's the practical memory consumption expected? How much memory do I have for everything else? Is it fair to assume walking an system memory based BVH is something of a disaster? Given the memory reclamation that can happen to an app, I presume one must ensure a BVH can never exceed 50% of total video memory.

- There's some minor allowance for LOD-ish things via ray-test flags, but what are the implications of even using this feature? How much more incoherent do I end up if my individual rays have to decide LOD? Better yet, my ray needs to scan different LODs based on distance from ray origin (or perhaps distance from camera), but those are LODs *in the BVH*, so how do I limit what the ray tests as the ray gets further away? Do I spawn multiple "sub-rays" (line segments along the ray) and given them different non-overlapping range cutoffs, each targetting different LOD masks? Is that reasonable to do, or devastatingly stupid? How does this affect my ray-intersection budget? How does this affect scheduling? Do I fire all LOD's rays for testing at the same time, or so I only fire them as each descending LOD's ray fails to intersect the scene?

- How do we best deal with texture masking? Currently hair and leaves are almost certainly masked, and really fine grain primitives almost certainly have to be. I suspect that while it's supported, manual intersection shaders that need to evaluate the mask are best avoided if at all possible for optimal performance. Should we tessellate out the mask wherever possible? That might sound nice, but could easily turn into a memory consuming disaster (and keep in mind, the BVH isn't memory free, and updating it isn't performance free either). It might be tempting to move hair to a spline definition like the film guys do, but that's likely just not practical as things still have to interop well with rasterization and updating a few hundred thousand splines, or building an implicit surface intersection shader to infer the intersections doesn't sound like fun (well, actually it does, but that's besides the point).

- Even something like a field of grass becomes hugely problematic, as every blade is presumably moving and there are potentially millions of the little bastards in a fairly small space. It's basically just green short hair for the ground. Maybe it ends up procedurally defined as suggested before and resolved in an intersection shader, but again... confusing stuff to deal with.

Or maybe these cases get punted on. That would be disappointing, but certainly simplifies things. We rasterize a gbuffer initially and when we need to spawn rays, we just assume our forest is barren, grass is missing, and our character is bald. We correct for these mistakes via current methods, which are hardly perfect, but better than nothing. This makes things a lot more complicated, though:

- You can drop leaves from the trees for shadow casting, but then you're going to still need leaf shadows from some processes - presumably shadowmapping. How do you make the two match up (since presumably raytracing devastates the SM quality comparison)?

- Maybe for AO you trace a near field and far field, and for near field you ignore the leaves and for far field you use an opaque coarse leaf proxy? Maybe this can work for shadows as well in certain cases if you apply the non-overlapping range-ray idea mentioned earlier, assuming they're going to get softened anyway?

- Maybe for AO you trace a near field and far field, and for near field you ignore the leaves and for far field you use an opaque coarse leaf proxy? Maybe this can work for shadows as well in certain cases if you apply the non-overlapping range-ray idea mentioned earlier, assuming they're going to get softened anyway?

There are all sorts of other problems too, related to BVH generation...

- Say I've got a humanoid, and build the BVH against a T-pose initially. How does the refit handle triangles massively changing orientation? How well does it handle self-intersection (which sadly, happens more than we might like)? What happens when my character is attempting to dodge and rolls into a ball to jump out of the way? Do these degenerate cases cause spikes, as the BVH degrades and more triangles end up getting tested? Does my performance wildly fluctuate as my character animates due to these issues?

- Say I've got a humanoid, and build the BVH against a T-pose initially. How does the refit handle triangles massively changing orientation? How well does it handle self-intersection (which sadly, happens more than we might like)? What happens when my character is attempting to dodge and rolls into a ball to jump out of the way? Do these degenerate cases cause spikes, as the BVH degrades and more triangles end up getting tested? Does my performance wildly fluctuate as my character animates due to these issues?

- If I have an open world game, how do I stream in the world geometry? At some point in the future, when the BVH format is locked down and thus directly authored to, maybe this becomes straightforward, but for now... yikes. Does one have to rethink their entire streaming logic? Maybe a BVH per sector (assuming that's even how you divide the world), although that causes all sorts of redundant ray-fires. Maybe you manually nest BVHs by cheating - use the custom intersection from a top level BVH to choose from amongst which of lower BVHs to intersect, so that you can have disparate BVHs but don't have to rayfire from the top-most level? Who knows?

Partial support is certainly better than zero support, but is raytracing as sexy of a solution when it fails to consider your hero character and/or other dynamics? There's an obvious desire for everything's appearance to be unified, but it wasn't soooo long ago that having entirely different appearance solutions for the world and for characters was the norm, and that the focus was primarily on a more believable looking world of mostly static elements (say, all the original radiosity-lightmapped games). Even now there tends to be a push to compromise on the indirect lighting quality of dynamics on the assumption they're a minority of the scene. Perhaps a temporary step backwards is acceptable for an interlude, or maybe that horse has already left the barn?

This post might all sound really negative, but its really not meant to be that way - raytracing for practical realtime scenarios is still in its infancy and its just not realistic for every problem to be solved (or at least, not solved well) on day-1. To make matters worse, in many cases while working with gamedevs is clearly a good call, it's certainly a big responsibility of nVidia and other IHVs to not prematurely lock down the raytracing pipeline to one way of working simply because they talked to one specific dev-house who have a particular way of thinking and/or dealing with things.

These problems are currently open ones, but a lot of smart people will do their best to come to reasonable solutions over the next few years. Raytracing remains a needed backbone for a ton of techniques, so a desire to see it working isn't going away anytime soon. Personally I'm pretty excited to explore these problems, and really looking forward to the visual jump we'll be able to see in games in the not-so-distant future.

Very interesting comments. I am excited about real-time ray tracing but also concerned to have a new black box where we cannot change or experiments nothing.

ReplyDeleteThe current thinking by a lot of the community is that eventually some flavor of BVH will be opened up to us. Hopefully that comes to pass eventually. Given how unclear best practices going forward are, it's probably for the best (at least in the near future) that IHVs have the opportunity to explore different approaches to deal with the data sets that games will soon be throwing at them.

ReplyDeleteNote on texture masking: coming from nvidia optix background, the intersection shader is always custom, but yes, it hurts perf a lot when you're trying to extend it beyond tri-ray test. What I did in the end was sorting tris based on if they're opaque or transparent so at least you can quickly skip the mask check based on triID<x, then read a pre-thresholded bitmask texture, check the bit and decide if the ray should continue. There might be a better way.

ReplyDeleteHair and grass with real-time raytracing - https://youtu.be/Q8e3rFkLZUg?t=1885

ReplyDelete