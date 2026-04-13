---
title: Frequency responses of half-pel filters
url: https://fgiesen.wordpress.com/2019/07/20/frequency-responses-of-half-pel-filters/
published: '2019-07-20'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Frequency responses of half-pel filters

In the [previous post](https://fgiesen.wordpress.com/2019/04/08/what-happens-when-iterating-filters/), I looked at repeated application of FIR filters on the same signal and laid out why their frequency response is the thing to look at if we’re wondering about their long-term stability under repeated application, because the Discrete-Time Fourier Transform (DTFT) of the filter coefficients corresponds to the eigenvalues of the linear map that convolves a signal with the filter once.

Now, let’s go back to the [original problem](https://caseymuratori.com/blog_0035) that Casey asked about: half-pixel (or half-pel) interpolation filters for motion compensation. We know from Casey’s post which of the filters he tried “blow up” under repeated application, and which ones don’t, and we now know some of the theory. The question is, does it track? Let’s find out!

### A small filter zoo: 6 taps

We’ll be looking at the frequency responses of various filters here. As a reminder, what we’re looking at are the values of the function

where the are our filter coefficients, which are real numbers. It’s easy to prove from this form that the function

is continuous, 2π-periodic, and has

(where the bar denotes complex conjugation, as usual). Therefore the “interesting” part of the frequency response (for our purposes anyway) is contained in the values of

for ω in [0,π]. Furthermore, we only care about the “magnitude response”, the absolute values of the (complex) frequency response, which is conventionally plotted in decibels (i.e. effectively on a logarithmic scale); the angle denotes phase response, which is not relevant to our question (and also happens to be relatively boring in this case, because all filters under consideration are symmetric and thus linear-phase FIR filters). Finally I’ll crop the plots I’m showing to only show frequencies from 0 to 0.8π (up to 80%

[Nyquist frequency](https://en.wikipedia.org/wiki/Nyquist_frequency)) because all filters under consideration sharply decay past that point (if not much earlier), so the portion from 0.8π to π contributes very little information and makes the y axis scaling awkward.

With all that out of the way, let’s start with our first filter: the 2-tap linear interpolation filter [0.5, 0.5] (it’s “bilinear” if you do it in both the X and Y directions, but all filters under consideration are separable and we’re only looking at 1D versions of them, so it’s just straight-up linear interpolation).

![Magnitude response of linear interpolation filter](../../assets/2c8a49a3801e74fc.png)


The dotted line at 0dB is the line we’re not allowed to cross if we want repeated application to be stable. It’s also the line we want to be *exactly on* for an ideal interpolation filter. As we can see from the diagram, linear interpolation is good at the first part, not so good at the second part: it’s unit gain at a frequency of 0 but immediately rolls off, which is what causes it to over-blur. Not great.

The next filter that Casey looks at jumps from 2 taps all the way to 6: it’s the half-pixel interpolation filter from H.264/AVC. Here’s its magnitude response:

![Magnitude response of H.264 filter](../../assets/ff8d4a10718b69cc.png)


This one is quite different. We can immediately see that it has above-unit gain for a significant fraction of its spectrum, peaking around 0.5π. That tells us it should blow up in Casey’s repeated-filtering test, and indeed it does. On the plus side, it has a much wider passband, and is in general much closer to an ideal interpolation filter than basic linear interpolation is.

The image for the 6-tap Lanczos filter is not that different:

![Magnitude response of 6-tap Lancozs filter](../../assets/46c1d2ce3a84953e.png)


In fact, this one’s qualitatively so similar that it seems fair to assume that the H.264 filter was designed as an approximation to Lanczos6 with reduced-precision coefficients. (It would certainly be plausible, but I haven’t checked.)

Next up, let’s look at Casey’s filter with quantized coefficients (numerator of 32):

![Magnitude response of quantized Muratori6](../../assets/85df211d766390b0.png)


Casey’s filter stays at or below unit gain; it has noticeably below-unit gain for much of its passband which is not ideal, but at least its passband is significantly wider than basic linear interpolation, and looks decent out to about 0.5π before it really starts to cut off.

And while we’re at it, here’s Casey’s other 6-tap filter from the second part of his series:

![Magnitude response of Muratori6 filter](../../assets/ca2f29f29b7e5311.png)


This one *very* slightly pokes above unit gain around 0.5π, but evidently little enough not to blow up when the output signal is quantized to 8 bits after every step, as Casey’s test does. Other than that, we have some passband ripple, but are really quite close to unit gain until at least half-Nyquist, after which our performance starts to deteriorate, as it does for all 6-tap filters.

Our final 6-tap filter in this round is a 6-tap Lagrange interpolator. This one’s not in Casey’s series; its coefficients are [ 0.011719, -0.097656, 0.585938, 0.585938, -0.097656, 0.011719 ]. Lagrange interpolators are a classic family of interpolating filters (closely related to Lagrange polynomials) and have extremely flat passbands:

![Magnitude response of 6-tap Lagrange interpolator](../../assets/34ceb1dc50789c8d.png)


On the good side, yes, the passband really is flat. The trade-off is that the filter response visibly starts to dip around 0.4π: the price we pay for that flat passband is losing more of the high frequencies than we would with other filters. On the other hand, this type of filter is not going to explode with repeated application. (Really, this is the second Lagrange-type filter I’ve shown, since the initial linear interpolation filter coincides with a 2-tap Lagrange interpolator.)

### 8-tap filters

I’m putting these in their own category: the two extra taps make a significant difference in the attainable filter quality, so they’re not on even footing with the 6-tap contenders. Let’s start with the filter from H.265/HEVC:

![Magnitude response of HEVC filter](../../assets/13966f4828aa8dc2.png)


Some ripple in the passband and an above-unit peak around 0.6π. Looking at the frequency response, this filter should blow up in Casey’s tests, and indeed it does. However it also manages to pass through frequencies all the way out to nearly 0.7π, not something we’ve seen so far.

Here’s 8-tap Lanczos:

![Magnitude response of Lanczos 8-tap](../../assets/9ba981503adc8a13.png)


Again qualitatively similar to what we see from the HEVC filter, although I overall like the “real” HEVC filter a bit better than this one. Another filter that we would expect to blow up (and Casey’s testing confirms it does).

At the other extreme, 8-tap Lagrange:

![Magnitude response of 8-tap Lagrange filter](../../assets/9bb1f77c00626fc3.png)


Passband straight as a ruler, but not much use past 0.5π. The good news is that, once again, it’s perfectly stable.

Here’s Casey’s contender:

![Magnitude response of Muratori8 filter](../../assets/fe937a2a571527dc.png)


Again some passband ripple and it’s poking slightly above unity around 0.55π, but it manages good results out to about 0.6π before it starts to cut.

### Conclusions

That’s a couple of different filter types, and at this point we’ve seen enough to start drawing some conclusions, namely:

First, adding more taps gives us frequency responses closer to our ideal, which is not exactly surprising. The trade-offs are that filters with more taps are more expensive to evaluate, and that codecs also care about things other than frequency response. Among other things, we generally want reduced-precision fixed-point approximations to the filter coefficients both for efficiency (particularly in hardware decoders) and to ensure different codec implementations agree (which, for various reasons, gets significantly nastier once floating-point is in the mix).

Second, among the filters I showed, there’s a fairly clear spectrum: at one end, we have the Lagrange interpolators with strictly unit-or-below gain. They are completely stable under repeated application but also tend to lose high frequencies fairly quickly. In the other direction, we have filters like the Lanczos-derived ones or those used in H.264 or HEVC that have wider pass bands but also clearly above-unit gain for at least some frequencies, meaning that frequency content in those regions will grow and ultimately explode under repeated application. Finally, Casey’s filters are somewhere in between; they have wider pass bands than pure Lagrange interpolators but keep their maximum gain close enough to 1 to avoid blow-ups when applied to data that is quantized to 8 bit fixed point.

This last part is something I originally intended to do a more in-depth analysis of, which is the reason this post is so delayed. But I just never felt inspired to actually write this part and didn’t make any headway the 3 times I tried to just sit down and write it *without* inspiration either, so, well, sorry. No proper analysis here. I figured it’s better to at least publish the rest of the article without it.

The gist of it is this: if your samples are quantized to say 8-bit fixed point after every step, it seems plausible that you should be able to get away with slightly above unit gain at some frequencies. Essentially, all the inputs (being quantized) are integers, which means they need to change by at least 0.5 steps in either direction to actually round to a different value. If the gain at a given frequency isn’t high enough to accomplish this change, nothing will happen, and even a filter with above-unit gain for some frequencies that should in theory blow up eventually, won’t. Experimentally this seems to be true and I meant to do a proper proof but as said, you’ll have to live without it for the time being. (I might do another post in the future if I do come up with a nice proof.)

Finally: how much does it matter? Casey’s original posts framed not diverging over repeated application as an essential requirement for a motion interpolation filter in a video codec, but it’s really not that simple.

There’s no question that stability under iteration is desirable, the same way that a perfectly flat response over all frequencies is desirable: ideally we’d like interpolation filters to behave like a perfect all-pass filter. But we care about computational cost and memory bandwidth too, so we don’t get to use infinitely wide filters, which means we can’t get a perfect frequency response. This is somewhat hidden by the cropping I did, but all filters shown decay very sharply above around 80% Nyquist. The stability issue is similar: if we care about stability above all else, there is a known answer, which is to use Lagrange interpolators, which give us perfect stability but have subpar response at the high frequencies.

There is another thing to consider here: in a video codec, motion compensation is part of the coding loop. The encoder knows exactly what the decoder will do with a given frame and set of motion vectors, and will use that result to code further updates against. In short, the interpolation filter is not left to its own devices in a feedback loop. The encoder is continuously monitoring what the current state of the frame in a compliant decoder will be. If there is a build-up of high-frequency energy over time, all that really happens is that at some point, the error will become high enough for the encoder to decide to do something about it, which means sending not just a pure motion vector, but instead a motion vector with a residual (a correction applied to the image data after motion compensation). Said residual is also coded in frequency space (essentially), most commonly using a DCT variant. In short, the end result of using a filter that has resonances in the high frequencies is that a few times per second, the encoder will have to send residuals to cancel out these resonances. This costs extra bits, and correcting errors in the high frequencies tends to be more expensive than for the lower frequencies (image and video codecs can generally code lower frequencies more cheaply than high frequencies).

But suppose we didn’t do that, and instead used say a perfectly stable Lagrange interpolator. It doesn’t have any resonances that would cause the image to blow up, but it does act like a bit of a low-pass filter. In short, instead of steadily gaining energy in the high frequencies, we end up steadily losing energy in the high frequencies. And this too ends up with the encoder having to send high-frequency heavy residuals periodically, this time to add in the missing high frequencies (instead of removing excess ones).

Neither of these is obviously preferable to, or cheaper than, the other. Sending high-frequency heavy residuals is relatively expensive, but we end up having to do it periodically regardless of which type we choose.

That’s not to say that it doesn’t matter at all; it’s just to point out that the actual decision of which type of filter to use in any real codec is not made in a vacuum and depends on other factors. For example, H.264/AVC and HEVC at low bit rates rely aggressively on their deblocking filters, which are essentially low-pass filters applied over block edges. In that context, a somewhat sharpening motion interpolation filter can help mitigate some of the damage, whereas a Lagrange interpolator would make things even more one-sided.

In short, there is no such thing as a single “best” interpolation filter. The decision is made in context and depends on what the rest of the codec does.