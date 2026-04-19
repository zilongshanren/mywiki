---
title: Quicker Trig
url: https://16bpp.net/blog/post/faster-asin-was-hiding-in-plain-sight
published: '2026-03-11'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

This one is going to be a quick one as there wasn't anything new discovered. In fact, I feel quite dumb. This is really a tale of "*Do your research before acting and know what your goal is,*" as you'll end up saving yourself a lot of time. Nobody likes throwing away work they've done either, and there could be something here that is valuable for someone else.

I still can't escape [PSRayTracing](https://16bpp.net/blog/post/psraytracing-a-revisit-of-the-peter-shirley-minibooks-4-years-later/). No matter how hard I try to shelve that project, every once in a while I hear about something "new" and then wonder "*can I shove this into the ray tracer and wring a few more seconds of speed out of it?"* This time around it was [Padé Approximants](https://en.wikipedia.org/wiki/Pad%C3%A9_approximant). The target is to provide me with faster (and better) trig approximations.

Short answer: **"no"**. It did not help.

But... I found something that ended up making the ray tracer significantly faster!!


## Quicker Trig

In any graphics application trigonometric functions are frequently used. But that can be a little expensive in terms of computational time. While it's nice to be accurate, we usually care more about ** fast** if anything. So if we can find an approximation that's "good enough" and is speedier than the real thing, it's generally okay to use it instead.

When it comes to texturing objects in PSRayTracing (which is based off of the [Ray Tracing in One Weekend books](https://raytracing.github.io/), circa the 2020 edition), the [ std::asin()](https://en.cppreference.com/w/cpp/numeric/math/asin.html) function is used. When profiling some of the scenes, I noticed that a significant amount of calls were made to that function, so I thought it was worth trying to find an approximation.

In the end I ended up writing [my own Taylor series based approximation](https://github.com/define-private-public/PSRayTracing/tree/fc9ae1f58f87f5d0338a0056b40b9d049a61a8b7?tab=readme-ov-file#trigonometric-approximations). It is faster but also has a flaw, whenever the input `x`

was less than `-0.8`

or greater than `0.8`

it would deviate heavily. So to look correct, it had to fall back to `std::asin()`

past these bounds.

![Taylor series approximation with fallback The Taylor series arcsin approximation with a fallback for edges](../../assets/dbebef600356a34b.png)



The C++ is as follows:

double _asin_approx_private(const double x) { // This uses a Taylor series approximation. // See: http://mathforum.org/library/drmath/view/54137.html // // In the case where x=[-1, -0.8) or (0.8, 1.0] there is unfortunately a lot of // error compared to actual arcsin, so for this case we actually use the real function if ((x < -0.8) || (x > 0.8)) { return std::asin(x); } // The taylor series approximation constexpr double a = 0.5; constexpr double b = a * 0.75; constexpr double c = b * (5.0 / 6.0); constexpr double d = c * (7.0 / 8.0); const double aa = (x * x * x) / 3.0; const double bb = (x * x * x * x * x) / 5.0; const double cc = (x * x * x * x * x * x * x) / 7.0; const double dd = (x * x * x * x * x * x * x * x * x) / 9.0; return x + (a * aa) + (b * bb) + (c * cc) + (d * dd); }


After a bit of trial and error, I found that a fourth-order Taylor series was the most performant on my hardware. It was measurably faster (by +5%), so I kept it and moved onto the next optimization.

![Original Taylor series approximation error The raw Taylor series arcsin approximation showing significant error at the edges](../../assets/105321312230a8ec.png)



## Padé Approximants

I can't remember where I heard about this one.... I'm drawing a complete blank. If you want a more in depth read, [check the Wikipedia article](https://en.wikipedia.org/wiki/Pad%C3%A9_approximant). But in a quick nutshell, they are a mathematical tool they can help provide an approximation of an existing function. To compute one, you do need to start out with a Taylor (or Maclaurin) series. While PSRayTracing is mainly a C++ project, Python is going to be used for simplicity's sake; we'll go back to our favorite compiled language when it matters though.

For the arcsine approximation above, using the four-term Taylor, we have this in Python:

def taylor_fourth_order(x: float) -> float: return x + (x**3)/6 + (3*x**5)/40 + (5*x**7)/112


Computing that into a Padé Approximant, we get what's known as a [3/4] Padé Approximant:

def asin_pade_3_4(x): a1 = -367.0 / 714.0 b1 = -81.0 / 119.0 b2 = 183.0 / 4760.0 n = 1.0 + (a1 * x**2) d = 1.0 + (b1 * x**2) + (b2 * x**4) return x * (n / d)


I'm also going to provide the one from a 5th order Taylor Series as well, a [5/4] Padé Approximant:

def asin_pade_5_4(x): a1 = -1709.0 / 2196.0 a2 = 69049.0 / 922320.0 b1 = -2075.0 / 2196.0 b2 = 1075.0 / 6832.0 n = 1.0 + (a1 * x**2) + (a2 * x**4) d = 1.0 + (b1 * x**2) + (b2 * x**4) return x * (n / d)


Now when charting all three, we get this:

![Pade approximants comparison Comparison of Taylor series and Pade approximants for arcsin](../../assets/5c486f91955e52d8.png)



Wow, that already looks much better. Less error! It's a bit hard to see that, so let's zoom in on right side of the functions:

![Edge zoom of Pade errors Zoomed view of Pade approximant errors at the range edges](../../assets/15da33ef6d14b54e.png)



The error hasn't fully gone away, but it's much less than before. Instead of defaulting back to the built-in `asin()`

method, there's a better trick up our sleeves: leveraging [Inverse Trig Functions](https://en.wikipedia.org/wiki/Inverse_trigonometric_functions)/Half Angle Transforms. Look at this:

![Half angle transform formula The arcsin half angle transformation formula](../../assets/6c1273d9a4508a93.png)


This does seem a tad confusing, yet it lets us do [a pro gamer move](https://youtu.be/ewAHYVzMobw?t=785). When `|x|`

is past a value we can "teleport" from the edge of the function more towards the center of arcsin(), perform the computation, and then go back and use the result there. In Python, this is our new asin(x) approximation:

def asin_pade_3_4_half_angle_correction(x: float) -> float: abs_x = abs(x) # If past the range, then we can use the half angle transformation to account for error if abs_x > 0.85: small_x = math.sqrt(0.5 * (1.0 - abs_x)) r = (math.pi / 2) - (2.0 * asin_pade_3_4(small_x)) return -r if x < 0 else r # Within the border we can just use the 3/4 approximation like normal return asin_pade_3_4(x)


Now with the correction in place, the edges look more like this:

![Pade error with HAT correction Pade approximant errors with half angle transform correction applied](../../assets/523a22293d5aad90.png)



It might be a little hard to see, but the dashed lines are the ones with this half angle transform correction method and they are hugging the `y=0`

line. There is a tiny bit of error if you zoom in.

There's even a further optimization that could be had: use (and adapt) a [1/2] Padé on the inside of the `if`

body. This is because `small_x`

will always be less than the square root of `0.075`

(which is `~0.27`

). The [1/2] Padé approximant for `asin()`

can compute much faster, but only for smaller values of `x`

. It can even be inlined into our function for further optimization. See below:

def asin_pade_1_2(x): b1 = -1.0 / 6.0 d = 1.0 + (b1 * x**2) return (x / d) # ... def asin_pade_3_4_half_angle_correction(x: float) -> float: abs_x = abs(x) # If past the range, then we can use the half angle transformation to account for error along with a "smaller" Pade if abs_x > 0.85: z = (1.0 - abs_x) / 2 b1 = -1.0 / 6.0 d = 1.0 + (b1 * z) small_pade = math.sqrt(z) / d r = (math.pi / 2) - (2.0 * small_pade) return -r if x < 0 else r # Within the border we can just use the 3/4 approximation like normal return asin_pade_3_4(x)


It still looks the same as the above chart, so I don't think it's necessary to include another one. Written as C++, we have this:

constexpr double HalfPi = 1.5707963267948966; inline double asin_pade_3_4(const double x) { constexpr double a1 = -367.0 / 714.0; constexpr double b1 = -81.0 / 119.0; constexpr double b2 = 183.0 / 4760.0; const double x2 = x * x; const double n = 1.0 + (a1 * x2); const double d = 1.0 + (b1 * x2) + (b2 * x2 * x2); return x * (n / d); } double asin_pade_3_4_half_angle_correction(const double x) { const double abs_x = std::abs(x); if (abs_x <= 0.85) { return asin_pade_3_4(x); } else { // Edges of Pade curve const double z = 0.5 * (1.0 - abs_x); constexpr double b1 = -1.0 / 6.0; const double d = 1.0 + (b1 * z); const double pade_result = std::sqrt(z) / d; const double r = HalfPi - (2.0 * pade_result); return std::copysign(r, x); } }


Compared to the original approximation method, this is more complicated, but it has benefits:

- For a larger range [-0.85, 0.85] it will default to a simpler computation
- For the edge cases it will use a quicker computation than
`std::asin()`

- There is less error

I'm very much a "put up or shut up" type of person. So let's actually plug it back into PSRayTracing and see if there is a speed improvement. We'll use the default scene (which is the final render from book 2):

![Book 2 final scene render Final render of the Ray Tracing in One Weekend Book 2 scene](../../assets/c666f4dd37e42304.png)



## Measuring

That globe is the user of `asin()`

. All images generally look the same (minus a little fuzz). For the test case we will render a 1080p image, with 250 samples per pixel, and take up a few cores. The testing was done on an M4 Mac Mini (running a version of macOS Tahoe, using GCC15 compiled with -O3). Doing a few runs each, taking a median:

With `std::asin()`

it took about 111 seconds to render the scene:

ben@Benjamins-Mac-mini build_gcc15 % ./PSRayTracing -j 4 -n 250 -s 1920x1080 -o render_std_asin.png Scene: book2::final_scene Render size: 1920x1080 Samples per pixel: 250 Max number of ray bounces: 50 Number of render threads: 4 Copy per thread: on Saving to: render_std_asin.png Seed: `ASDF` Rendering: [==================================================] 100% 111s Render took 110.891 seconds


The older `asin()`

approximation took roughly 105 seconds (~5% speedup):

ben@Benjamins-Mac-mini build_gcc15 % ./PSRayTracing -j 4 -n 250 -s 1920x1080 - o render_asin_taylor.png ... Render took 104.674 seconds


And this new Padé Approximant approach took... The same amount of time:

ben@Benjamins-Mac-mini build_gcc_15 % ./PSRayTracing -j 4 -n 250 -s 1920x1080 -o render_asin_pade.png ... Render took 104.87 seconds


This new `asin()`

method is better (in terms of correctness), but not much of a contest when it comes to performance. It's a small victory.


## An LLM Prompt

There's no denying the AI tooling of the past 3+ years is going to go away. At CppCon 2023 Andrei Alexandrescu gave an excellent talk entitled "[Robots Are After Your Job: Exploring Generative AI for C++](https://youtu.be/J48YTbdJNNc)"; it's worth your time to listen. After all of the above work and that talk in mind, I decided to ask an LLM (Gemini in this case): "*What's a fast approximation for asin(x) I can use in C++?"*. It gave me this:

constexpr double HalfPi = 3.1415926535897932385 / 2.0; double fast_asin_cg(const double x) { // Original Minimax coefficients constexpr double a0 = 1.5707288; constexpr double a1 = -0.2121144; constexpr double a2 = 0.0742610; constexpr double a3 = -0.0187293; // Strip sign const double abs_x = fabs(x); // Evaluate polynomial using Horner's method double p = a3 * abs_x + a2; p = p * abs_x + a1; p = p * abs_x + a0; // Apply sqrt term and pi/2 offset const double x_diff = sqrt(1.0 - abs_x); const double result = HalfPi - (x_diff * p); // Restore sign return copysign(result, x); }


This looked too simple for me to believe. The source it cited was [the documentation for asin in Nvidia's Cg Toolkit](https://developer.download.nvidia.com/cg/asin.html); a product that hasn't been updated since 2012. The reference implementation contained a rewritten form of the above. Porting it over to Python/Jupyter to verify it is trivial:

def asin_cg(x: float) -> float: ''' Fast branchless asin(x) approximation. Based on Abramowitz and Stegun formula 4.4.45 ''' # https://developer.download.nvidia.com/cg/asin.html # https://personal.math.ubc.ca/~cbm/aands/page_81.htm # Original Minimax coefficients from Abramowitz and Stegun a0 = 1.5707288 a1 = -0.2121144 a2 = 0.0742610 a3 = -0.0187293 abs_x = abs(x) # Evaluate polynomial using Horner's method p = a3 * abs_x + a2 p = p * abs_x + a1 p = p * abs_x + a0 result = (math.pi / 2) - math.sqrt(1.0 - abs_x) * p # Restore sign natively return math.copysign(result, x)


I was in disbelief that it was so clean and elegant. The implementation, error, and output. Look for yourself

![Nvidia Cg asin approximation profile Performance and error profile of the Nvidia Cg asin approximation](../../assets/6b832af9ae9cbe50.png)



That curve; it overlaps the `arcsin()`

function without any visible difference. And the error is practically nothing. Though the real test would be in the ray tracer itself:

ben@Benjamins-Mac-mini build_gcc_15_new_asin_cg % ./PSRayTracing -j 4 -n 250 -s 1920x1080 ... Render took 101.462 seconds


Wow, This is considerably faster than any other methods. After verifying the render vs `std::asin()`

's output, it's indistinguishable. **A better asin() implementation was found**.


## Measuring Further

This led me down a small rabbit hole of [benchmarking](https://github.com/define-private-public/PSRayTracing/blob/8dea5113f6b00e1ef6bb5c0c117562e971280271/experiments/asin_cg_approx/benchmark.cpp) this implementation on a few select chips and operating systems.

Intel i7-10750H, Ubuntu 24.04 ( w/ GCC 14 and clang 19):

./test_gcc_O3 "ASDF" "100" "10000000" std::asin() time: 29197.9 ms asin_cg() time: 19839.8 ms Verification sums: std::asin(): -34549.5 asin_cg(): -34551.1 Difference: 1.60886 Error: -0.00465669 % Speedup: 1.47169x faster ./test_clang_O3 "ASDF" "100" "10000000" std::asin() time: 29520.7 ms asin_cg() time: 19044.3 ms ... Speedup: 1.55011x faster


Intel i7-10750H, Windows 11 (w/ MSVC 2022):

C:\Users\Benjamin\Projects\PSRayTracing\experiments\asin_cg_approx>test_msvc_O2.exe ASDF 100 10000000 std::asin() time: 12458.1 ms asin_cg() time: 6562.1 ms ... Speedup: 1.8985x faster


Apple M4, macOS Tahoe (w/ GCC 15 via Homebrew and clang 17):

./test_gcc_O3 "ASDF" "100" "10000000" std::asin() time: 10469 ms asin_cg() time: 10251 ms ... Speedup: 1.02126x faster ./test_clang_O3 "ASDF" "100" "10000000" std::asin() time: 12650 ms asin_cg() time: 12073.2 ms ... Speedup: 1.04777x faster


All of them have this CG `asin()`

approximation well in the lead. On the Intel chip it's faster by a very significant margin. I'm curious to test this on an AMD based x86_64 system, but I'll leave that up to any readers. My guess is that it's just as good. The Apple M4 chip didn't have much as a boost, but it's still measurable (and reproducible). Anything greater than a 2% change is notable. I refer to [Nicholas Ormrod's old talk](https://www.youtube.com/watch?v=kPR8h4-qZdk) on this matter.


## Lessons

I think I originally went down the Taylor series based rabbit hole because I started trying that out with `sin()`

and `cos()`

, then naturally assumed I could apply it to other trig functions. I never thought to just first see if someone had solved my problem: a faster arcsine for computer graphics.

And here's the worst part: this all existed before LLMs were even available. I can't seem to recreate it, but there was a combination of the words "fast c++ asin approximation cg" that I queried into a search engine. The first result was a link to the Nvidia Cg Toolkit doc page. I only found this a few days ago.

I am surprised that no one else mentioned anything to me either. I even highlighted my faster `asin()`

in the README as an achievement **and no one bothered to correct me**... I know this project (and these articles) have made the rounds in both C++ and computer graphics circles. People way more experienced and senior than me never said a thing.

This amazing snippet of code was languishing in the docs of dead software, which in turn the original formula was scrawled away in a math textbook from the 60s. It is annoying too when I tried to perform a search that **no benchmarks were provided**. Hopefully the word is out now.

I think my main problem is that I never bothered to slow down, double check what my goal was, and see if someone else already figured it out. That's what I gained from this experience.

And some fancy charts.


Edit 3/15:26: Discussion threads about this are here: