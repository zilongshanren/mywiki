---
title: Current-gen DOF and MB
url: https://c0de517e.blogspot.com/2012/01/current-gen-dof-and-mb.html
published: '2012-01-04'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

I was thinking to publish this somewhere else, but Crytek at the last Siggraph already disclosed a technique that is close to this one, so at the end I guess it's not worth it and I'm going to spill the beans here instead.

Depth of field and motion blur, from a post-processing standpoint, look similar. They both are scattering filters, they both need to respect depths. So it makes sense to try to combine both effects in the same filter. And if you think about doing it that way, you're almost already done, it's quite obvious that it's possible to combine the DOF kernel with the MB one by skewing the DOF towards the motion-blur direction.

This is what Crytek does, they use a number of taps, their filter is circular and they just transform this circle with a basis that has the motion-blur axis as one vector an a perpendicular one, scaled by the DOF amount, as the second. It's pretty straightforward, the only thing we really have to take care in this process is regions were the motion blur is zero and thus we won't have the required first axis, which might be a bit of a pain.

As you know, doing these effects in post is an approximation, so when I look at these problems I always think in terms of the "correct" solution first and use that as a background in my head to validate any ideas I have.

In this case what we really want to do is to sample some extra dimensions in our rendering integral, temporal in the case of the motion-blur and spatial, on the camera's film plane, in case of the DOF. This leads quite naturally to raytracing, but thinking this way is not particularly useful as we know we can't achieve comparable results to that, we don't have in post the ability of sampling more visibility (and shading) than what we have already in our z-buffer, so we should look instead at a model that gives us "the best" of what we can do with the information that we have (to be fair, there is in literature an method which subdivides the scene in ranges with multiple z-buffers and color buffers, and then ray-marches on these z-buffers to emulate raytracing, which I found pretty cool, but I digress even more). With only a z-buffer and its color buffer, that would be scattering.

You can imagine that as placing a particle at each image point, stretched along the axes we just described, with an opacity that is inversely proportional to its size, and then z-sorting and rendering all these particles (and some PC ports of some games did that, having a lot of GPU power to spare, in general placing some particles is not a bad idea especially if you can avoid having one per pixel but selecting the areas where your DOF highlights would be more visible). This, plus a model to "guess" the missing visibility (remember, we don't have all the information! if an object is moving, for example, it will "show" some of the background behind it, which we don't have, so we need a policy to resolve these cases) is the best we can do in post and should guide us in all the decisions we make in more approximate models.

Ok, going back to the effect we are creating, so far it's clearly a gathering effect. We create a filter kernel at each pixel, and then we gather samples around it. Often, this gathering only respects the depth sorting, we don't gather samples if their depth is farther from the camera than the pixel we're considering. This leads to no missing visibility problems, we assume that the surface on the pixel we're considering fully occludes everything behind it, but it's not really "correct" if we think about the scattering model we explained above.

A better strategy would gather a sample only if the scattering kernel of the surface at that sample point would have crossed our pixel, this strategy is what I call sometimes "scattering as gathering". Now the problem with this is that unless we know that our scattering kernels have a bounded size, and for each pixel we sample everything inside that size to see if there is something that could have scattered towards it, we will miss some scattering, but unfortunately doing so requires a large number of samples.

In particular, as we size our gather kernel using the information at the surface point of the pixel we're considering, we easily miss effects where a large out of focus object scatters on top of some in focus background pixels, for which the gathering kernel would be really small.

Now there are a variety of solutions for that. We could for example fix a minimum size for our gathering kernel, so in the in-focus areas we still "check" around a bit, and we might end up gathering nothing if we found nothing that scatters towards us. This sort-of works but still won't handle large scattering radii. We might think to cheat and get more samples by separating our gathering filter into two passes, each filtering along a line (axis).

This works well for gathering, even when the filter is not really separable (DOF and MB are not, as the kernels, even if we use a gaussian or square one, which are separable, are sized by a function which varies per pixel and is not itself separable) the artifacts are not noticeable, but if we push this with a scattering-as-gathering logic it starts to crumble as the second pass does not have the information of where the first-pass gathering took its samples from, so it can't decide if these samples would have scattered towards a given location and it can't even separate the samples anymore.

*Digression: In the past I've solved this by doing DOF in two passes, using separable gathering in a first pass while detecting the areas where it fails and masking them using early-z to then do a second pass on them with a large gather-as-scatter filter.*So what we can do? The solution is easy really, we can write our basis vectors to a buffer (which is required anyways if you want to consider MB due to object movement and not only camera movement, the former can't be computed with the information we have from the colour and depth, we need to render the motion of the objects somewhere) and then apply a fixed radius gathering-as-scattering filter there, which as it's only searching to expand the subsequent filtering radii and not sampling colour, can be done with fewer samples without causing too much artifacts, pretty much as "percentage closer soft-shadows" do.

So far, Crytek does something along the very same lines. The twist where the effect I crafted diverges from theirs is that I still employ a separable filter to compute the final blur, instead of using some taps in a circle. The first time I saw this done for MB and DOF was in EA's first Skate game, so it's nothing particularly novel. Skate's implementation though was "driven" by DOF, the motion blur was only added for the camera and it was only present if the DOF was there too (at least, afaik).

Extending this to behave well with the two effects separately requires computing the "right" gathering weights, or as I wrote above, reasoning about the scattering. Also, once you get the ability of doing motion blur without DOF, you will notice that one of the two blur passes will do nothing in areas of pure MB, as the second axes will have zero length (but you are still "paying" to sample N times the same area...). To avoid that waste, I filter along two diagonals, in case of pure MB these coincide but are both non-zero, so we get a bit better filtering for the same price.

I don't think you can do much better than this on current-gen (without proper support for scattering) but I'd love to be proved wrong :) Example code below (it doesn't include many details and it doesn't include the axis scattering pass, but the "important" parts are all there):

float depth = tex2D( DepthSampler, TexCoord );

float2 MB_axis = ( currentViewPos - previousViewPos ) * MB_MULTIPLIER;

float DOF_amount = ComputeDOFAmount(depth);

float MB_amount = length(MB_axis);

float DOF_MB_ratio = DOF_amount / (MB_amount + EPS_FLOAT);

float2 DOF_axis = MB_axis.yx * float2(1,-1) * DOF_MB_ratio;

MB_axis *= max(DOF_MB_ratio, 1.f);

// Compute the 2x2 basis

float4 axis1xy_axis2xy = DOF_axis.xyxy + MB_axis.xyxy * float4(1.0.xx, -1.0.xx);

// Make sure that we are in the positive x hemisphere so the following lerp won't be too bad

//axis1xy_axis2xy.xy *= sign(axis1xy_axis2xy.x);

//axis1xy_axis2xy.zw *= sign(axis1xy_axis2xy.z);

// We have to take care of too small MB which won't be able to correctly generate a basis

float MB_tooSmall = 1.0 - saturate(MB_amount * MB_THRESHOLD - MB_THRESHOLD);

axis1xy_axis2xy = lerp(axis1xy_axis2xy, float4(DOF_amount.xxx, -DOF_amount), MB_tooSmall);

// --- Second and third passes: separable gathering

half2 offset;

if(is_first_separable_blur) offset = GetFirstAxis(TexCoord);

else offset = GetSecondAxis(TexCoord);

half amount = length(offset);

half4 sum = tex2D(ColorSampler, TexCoord) * FILTER_KERNEL_WEIGHTS[0];

half sampleCount = FILTER_KERNEL_WEIGHTS[0];

half4 steps = (offset * TEXEL_SIZE).xyxy;

steps.zw *= -1;

for(int i=1; i < 1+NUM_STEPS; i++)

{

half4 sampleUV = TexCoord.xyxy + steps * i;

// Color samples

half4 sample0 = tex2D(ColorSamplerHR, sampleUV.xy);

half4 sample1 = tex2D(ColorSamplerHR, sampleUV.zw);

// Maximum extent of the blur at these samples

half maxLengthAt0;

half maxLengthAt1;

if(is_first_separable_blur)

{ maxLengthAt0 = length(GetFirstAxis(sampleUV.xy)) * (NUM_STEPS+1);

maxLengthAt1 = length(GetFirstAxis(sampleUV.zw)) * (NUM_STEPS+1); }

else

{ maxLengthAt0 = length(GetSecondAxis(sampleUV.xy)) * (NUM_STEPS+1);

maxLengthAt1 = length(GetSecondAxis(sampleUV.zw)) * (NUM_STEPS+1); }

half currentLength = amount * i;

half weight0 = saturate(maxLengthAt0 - currentLength) * FILTER_KERNEL_WEIGHTS[i];

sum += sample0 * weight0;

sampleCount += weight0;

half weight1 = saturate(maxLengthAt1 - currentLength) * FILTER_KERNEL_WEIGHTS[i];

sum += sample1 * weight1;

sampleCount += weight1;

}

return sum / sampleCount;

## No comments:

Post a Comment