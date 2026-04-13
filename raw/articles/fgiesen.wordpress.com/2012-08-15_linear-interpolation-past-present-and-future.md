---
title: Linear interpolation past, present and future
url: https://fgiesen.wordpress.com/2012/08/15/linear-interpolation-past-present-and-future/
published: '2012-08-15'
source_blog: The ryg blog
source_site: https://fgiesen.wordpress.com
category: graphics
fetched: '2026-04-13'
---

# Linear interpolation past, present and future

Linear interpolation. Lerp. The bread and butter of graphics programming. Well, turns out I have three tricks about lerps to share. One of them is really well known, the other two less so. So let’s get cracking!

Standard linear interpolation is just `lerp(t, a, b) = (1-t)*a + t*b`

. You should already know this. At t=0 we get a, at t=1 we get b, and for inbetween values of t we interpolate linearly between the two. And of course we can also linearly extrapolate by using a t outside [0,1].

### Past

The expression shown above has two multiplies. Now, it used to be the case that multiplies were really slow (and by the way they really aren’t anymore, so please stop doubling the number of adds in an expression to get rid of a multiply, no matter what your CS prof tells you). If multiplies are expensive, there’s a better (equivalent) expression you can get with some algebra: `lerp(t, a, b) = a + t*(b-a)`

. This is the first of the three tricks, and it’s really well known.

But in this setting (int multiplies are slow) you’re also really unlikely to have floating-point hardware, or to be working on floating-point numbers. Especially if we’re talking about pixel processing in computer graphics, it used to be all-integer for a *really* long time. It’s more likely to be all fixed-point, and in the fixed-point setting you typically have something like `fixedpt_lerp(t, a, b) = a + ((t * (b-a)) >> 8)`

. And more importantly, your a’s and b’s are also fixed-point (integer) numbers, typically with a very low range.

So here comes the second trick: for some applications (e.g. cross fades), you’re doing a lot of lerps with the same t (at least one per pixel). Now note that if t is fixed, the `(t * (b - a)) >> 8`

part really only depends on b-a, and that’s a small set of possible values: If a and b are byte values in [0,255], then d=b-a is in [-255,255]. So we really only ever need to do 511 multiplies based on t, to build a table indexed by d. Except that’s not true either, because we compute first t*0 then t*1 then t*2 and so forth, so we’re really just adding t every time, and we can build the whole table without any multiplies at all. So here we get trick two, for doing lots of lerps with constant t on integer values:

U8 lerp_tab[255*2+1]; // U8 is sufficient here // build the lerp table for (int i=0, sum = 0; i < 256; i++, sum += t) { lerp_tab[255-i] = (U8) (-sum >> 8); // negative half of table lerp_tab[255+i] = (U8) ( sum >> 8); // positive half } // cross-fade (grayscale image here for simplicity) for (int i=0; i < npixels; i++) { int a = src1[i]; int b = src2[i]; out[i] = a + lerp_tab[255 + b-a]; }

Look ma, no multiplies!

### Present

But back to the present. Floating-point hardware is readily available on most platforms and purely counting arithmetic ops is a poor estimator for performance on modern architectures. Practically speaking, for almost all code, you’re never going to notice any appreciable difference in speed between the two versions

lerp_1(t, a, b) = (1 - t)*a + t*b lerp_2(t, a, b) = a + t*(b-a)

but you might notice something else: unlike the real numbers (which our mathematical definition of lerp is based on) and the integers (which our fixed-point lerps worked on), floating-point numbers don’t obey the arithmetic identities we’ve been using to derive this. In particular, for two floating point numbers we generally have `a + (b-a) != b`

, so the second lerp expression is generally not correct at t=1! In contrast, with IEEE floating point, the first expression is guaranteed to return the exact value of a (b) at t=0 (t=1). So there’s actually some reason to prefer the first expression in that case, and using the second one tends to produce visible artifacts for some applications (you can also hardcode your lerp to return b exactly at t=1, but that’s just ugly and paying a data-dependent branch to get rid of one FLOP is a bad idea). While for pixel values you’re unlikely to care, it generally pays to be careful for mesh processing and the like; using the wrong expression can produce cracks in your mesh.

So what to do? Use the first form, which has one more arithmetic operation and does two multiplies, or the second form, which has one less operation but unfavorable rounding properties? Luckily, this dilemma is going away.

### Future

Okay, “future” is stretching a bit here, because for some platforms this “future” started in 1990, but I digress. Anyway, in the future we’d like to have a magic lerp instruction in our processors that solves this problem for us (and is also fast). Unfortunately, that seems very unlikely: Even GPUs don’t have one, and [Michael Abrash](http://software.intel.com/file/15542) never could get Intel to give him one either. However, he did get fused multiply-adds, and that’s one thing all GPUs have too, and it’s either already on the processor you’re using or soon coming to it. So if fused multiply-adds can help, then maybe we’re good. And it turns out they can.

A fused multiply-add is just an operation `fma(a, b, c) = a*b + c`

that computes the inner expression using only one exact rounding step. And FMA-based architectures tend to compute regular adds and multiplies using the same circuitry, so all three operations cost roughly the same (in terms of latency anyway, not necessarily in terms of power). And while I say “fma” these chips usually support different versions with sign flips in different places too (implementing this in the HW is almost free); the second most important one is “fused negative multiply-subtract”, which does `fnms(a, b, c) = -(a*b - c) = c - a*b`

. Let’s rewrite our lerp expressions using FMA:

lerp_1(t, a, b) = fma(t, b, (1 - t)*a) lerp_2(t, a, b) = fma(t, b-a, a)

Both of these still have arithmetic operations left that aren’t in FMA form; lerp_1 has two leftover ops and lerp_2 has one. And so far both of them aren’t significantly better than their original counterparts. However, lerp_1 has exactly one multiply and one subtract left; they’re just subtract-multiply (which we don’t have HW for), rather than multiply-subtract. However, that one is easily remedied with some algebra: `(1 - t)*a = 1*a - t*a = a - t*a`

, and that last expression *is* in fma (more accurately, fnms) form. So we get a third variant, and our third trick:

lerp_3(t, a, b) = fma(t, b, fnms(t, a, a))

Two operations, both FMA-class ops, and this is based on lerp_1 so it’s actually exact at the end points. Two dependent ops – as long as we don’t actually get a hardware lerp instruction, that’s the best we can hope for. So this version is both fast *and* accurate, and as you migrate to platforms with guaranteed FMA support, you should consider rewriting your lerps that way – it’s the lerp of the future!

This is a great write up! I’d love to read more on similar topics.

So can this type of optimization be extended to bilinear interpolation? Or is it best to just use lerp_3() three times?

This is not an optimization; it is just as fast (or slow, depending on your perspective) as a sub-then-fma lerp (the a+t*(b-a) form). The point is just that it’s exact at the end points.

Phrased another way, the (1-t)*a+t*b and 2-fma forms given here actually interpolate between a and b; the sub-then-fma form interpolates between a and a+(b-a), which in floating-point arithmetic may be equal to b, or close to b, or not-so-close to b (depending on the exact numerical values).

Building a bilinear interpolation out of three such lerps will match a single linear interpolation on all 4 corners of the square { u=1 or v=1 }, again for approximately the same cost (on typical FMA HW) as building it out of three sub-then-fma stages. I haven’t tried building a direct bilinear along similar lines.

I’ve encountered a bug with (1-t)*a + t*b — when a and b are equal, and t is very small, the result can be not equal to a and b. The other formula works reliably in that case. I’m wondering about the best way to robustify vanilla lerp.

To follow up on robust vanilla lerp, a colleague suggested this (in Javascript for convenience):

function lerp_3(t, a, b) {

var bma = b – a;

if (t < 0.5) {

return a + bma * t;

} else {

return b – bma * (1 – t);

}

}

Which seems to meet all my criteria. A JS console session showing test cases:

function lerp_1(t, a, b) { return (1 – t)*a + t*b; }

function lerp_2(t, a, b) { return a + t * (b – a); }

function lerp_3(t, a, b) { var bma = b – a; if (t 126.99999999999999

lerp_2(5.0586262771736122e-15, 127, 127);

-> 127

lerp_3(5.0586262771736122e-15, 127, 127);

-> 127

// lerp_2 failure case:

lerp_1(1, 1.1805916083717324e+21, 0.000001430511474609375);

-> 0.000001430511474609375

lerp_2(1, 1.1805916083717324e+21, 0.000001430511474609375);

-> 0

lerp_3(1, 1.1805916083717324e+21, 0.000001430511474609375);

-> 0.000001430511474609375

[grrrr, the middle of that post got munged. trying again…]

To follow up on robust vanilla lerp, a colleague suggested this (in Javascript for convenience):

function lerp_3(t, a, b) {

var bma = b – a;

if (t < 0.5) {

return a + bma * t;

} else {

return b – bma * (1 – t);

}

}

Which seems to meet all my criteria. A JS console session showing test cases:

function lerp_1(t, a, b) { return (1 – t)*a + t*b; }

function lerp_2(t, a, b) { return a + t * (b – a); }

function lerp_3(t, a, b) { var bma = b – a; if (t 126.99999999999999

lerp_2(5.0586262771736122e-15, 127, 127);

-> 127

lerp_3(5.0586262771736122e-15, 127, 127);

-> 127

// lerp_2 failure case:

lerp_1(1, 1.1805916083717324e+21, 0.000001430511474609375);

-> 0.000001430511474609375

lerp_2(1, 1.1805916083717324e+21, 0.000001430511474609375);

-> 0

lerp_3(1, 1.1805916083717324e+21, 0.000001430511474609375);

-> 0.000001430511474609375

double grrrr!! WordPress makes a mess of my attempts to paste code. Try this: http://tulrich.com/geekstuff/lerp.html

Where I work we changed the lerp(a, b, t) function from a+t*(b-a) to the other form only to get back a failing unit test which (indirectly) depends on lerp(1.7, 1.7, 0.4) == 1.7 — Floating point math never ceases to surprise :-P

Yep, see also Thatcher’s comment. It boils down to this: you have to pick which properties are most important to you and use the corresponding lerp form.

You maybe mean FNMA instead of FNMS. At least on x86-64 architectures FNMS(a, b, c) = -(a * b) – c, which is not equivalent to c – a*b. Actually FNMA(a, b, c) = -(a * b) + c.

I was talking about

PowerPCfnms, which is specified as negate(fms(a,b,c)) = -fl(a*b-c) = fl(c-a*b), and has been out in that form (and with that name) since the 90s.At the time of writing (Aug 2012), Intel hadn’t even released any x86 CPU with FMA support (that wouldn’t be until Haswell in June 2013). AMD had FMA4 already out but it was never commercially irrelevant (and is now unsupported).