---
title: Gotta Go Fast
url: https://16bpp.net/blog/post/even-faster-asin-was-staring-right-at-me
published: '2026-03-16'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

I don't normally do follow-ups and never this quick. After posting [that last article,](https://16bpp.net/blog/post/faster-asin-was-hiding-in-plain-sight/) it was fun to read the comments on [Reddit](https://www.reddit.com/r/cpp/comments/1rqtw8q/faster_asin_was_hiding_in_plain_sight/) and [Hacker News](https://news.ycombinator.com/item?id=47336111) as they rolled in. I even found [other discussions](https://lobste.rs/s/bunmdv/faster_asin_was_hiding_plain_sight). I couldn't help wonder, *"Could I have made it even more performant?"*. After heading home I decided to take another look.

There was.


## Gotta Go Fast

Look at the implementation of the Cg `asin()`

approximation;

double asin_cg(const double x) { // Original Minimax coefficients constexpr double a0 = 1.5707288; constexpr double a1 = -0.2121144; constexpr double a2 = 0.0742610; constexpr double a3 = -0.0187293; // Strip sign const double abs_x = abs(x); // Evaluate polynomial using Horner's method double p = a3 * abs_x + a2; p = p * abs_x + a1; p = p * abs_x + a0; // Apply sqrt term and pi/2 offset const auto x_diff = sqrt(1.0 - abs_x); const double result = (Pi / 2.0) - (x_diff * p); // Restore sign natively return copysign(result, x); }


Does something about how `p`

is computed look a little curious? It can be rewritten to be fully `const`

. While it's not a requirement, it's generally something you should strive for. This was missed in the first pass.

const double p = ((a3 * abs_x + a2) * abs_x + a1) * abs_x + a0;


From here we can do a polynomial expansion and factoring. This is where the magic happens. Showing the work step by step:

p = ((a3 * abs_x + a2) * abs_x + a1) * abs_x + a0 p = (a3 * abs_x * abs_x + a2 * abs_x + a1) * abs_x + a0 p = (a3 * abs_x^2 + a2 * abs_x + a1) * abs_x + a0 p = a3 * abs_x^3 + a2 * abs_x^2 + a1 * abs_x + a0 p = (a3 * abs_x^3 + a2 * abs_x^2) + (a1 * abs_x + a0) p = (a3 * abs_x + a2) * abs_x^2 + (a1 * abs_x + a0)


Taking that last term for `p`

, we have this in code:

const double x2 = abs_x * abs_x; const double p = (a3 * abs_x + a2) * x2 + (a1 * abs_x + a0);


`p`

is now evaluated a little bit differently but arrives at the same numerical value. We are now leveraging a technique known as [Estrin's Scheme](https://en.wikipedia.org/wiki/Estrin%27s_scheme) to rewrite this equation. With the above, the compiler (and CPU) can evaluate `a3 * abs_x + a2`

and `a1 * abs_x + a0`

independently of each other. This reduces the dependency chain length from three to two, allowing modern out-of-order CPUs to execute these operations in parallel. For those unaware, this is [Instruction-level parallelism](https://en.wikipedia.org/wiki/Instruction-level_parallelism).


## Benchmark Measurements

The full benchmarking code [is available here](https://github.com/define-private-public/PSRayTracing/blob/22ad708cd16b8034d4eb2a8c30b54cbc8a34be3a/experiments/asin_cg_approx/benchmark.cpp). This gets into microbenchmarking (a little bit), which is fairly tricky. A full "run" of the benchmark has 10,000,000 calls to the respective arcsine function, and each chip/OS/compiler combo does 250 runs in total. Testing environments were:

- Intel i7-10750H
- Ubuntu 24.04 LTS: GCC & clang
- Windows 11: GCC & MSVC

- AMD Ryzen 9 6900HX
- Ubuntu 24.04 LTS: GCC & clang
- Windows 11: GCC & MSVC

- Apple M4
- macOS Tahoe: GCC & clang



I'd love to measure this on some mobile chips and a newer Intel, but this is what I own. [Gifts are always welcome](https://16bpp.net/page/contact/). The data is as follows ([and details are here if you're interested](https://github.com/define-private-public/PSRayTracing/tree/9ffba62428212610b95789237cc88967f69f3546/experiments/asin_cg_approx/benchmark_results_part_two_electric_boogaloo)). A lower `ms`

count is the most desirable and `std::asin()`

is the baseline.

Intel Core i7 Linux GCC 14.2 (-O3) std::asin() : 74385 ms asin_cg() : 48374 ms -- 1.54x asin_cg_estrin() : 41388 ms -- 1.80x Clang 20.1 (-O3) std::asin() : 73504 ms asin_cg() : 47211 ms -- 1.56x asin_cg_estrin() : 41350 ms -- 1.78x Windows GCC 14.2 (-O3) std::asin() : 113396 ms asin_cg() : 91925 ms -- 1.23x asin_cg_estrin() : 90925 ms -- 1.25x MSVC VS 2022 (/O2) std::asin() : 84733 ms asin_cg() : 53592 ms -- 1.58x asin_cg_estrin() : 45014 ms -- 1.88x AMD Ryzen 9 Linux GCC 14.2 (-O3) std::asin() : 74986 ms asin_cg() : 53129 ms -- 1.41x asin_cg_estrin() : 52166 ms -- 1.44x Clang 20.1 (-O3) std::asin() : 75188 ms asin_cg() : 52837 ms -- 1.42x asin_cg_estrin() : 51856 ms -- 1.45x Windows GCC 14.2 (-O3) std::asin() : 136393 ms asin_cg() : 122071 ms -- 1.12x asin_cg_estrin() : 120953 ms -- 1.13x MSVC VS 2022 (/O2) std::asin() : 121639 ms asin_cg() : 92612 ms -- 1.31x asin_cg_estrin() : 92290 ms -- 1.32x Apple M4 macOS GCC 15.1.0 (-O3) std::asin() : 26176 ms asin_cg() : 25764 ms -- 1.02x asin_cg_estrin() : 25668 ms -- 1.02x Apple Clang 17.0.0 (-O3) std::asin() : 33626 ms asin_cg() : 32755 ms -- 1.03x asin_cg_estrin() : 30245 ms -- 1.11x


Summarizing the above:

- AMD has barely any speedup. So it does not help, but it doesn't hurt either
- The (older) Intel chip gets a massive boost using the Estrin method of the Cg version (Windows/GCC excluded)
- The speedup on Apple's Chip is only present when compiling with clang
- But GCC's code is faster



## Ray Tracer Measurements

I'll use the same test [as the last article](https://16bpp.net/blog/post/faster-asin-was-hiding-in-plain-sight/). Taking a few renders, this is what a median run looked like. On Intel i7, using the older `asin_cg()`

method:

ben@linux:~/Projects/PSRayTracing/build_gcc_14$ ./PSRayTracing -n 250 -j 4 -s 1920x1080 Scene: book2::final_scene Render size: 1920x1080 Samples per pixel: 250 Max number of ray bounces: 50 Number of render threads: 4 Copy per thread: on Saving to: render.png Seed: `ASDF` Rendering: [==================================================] 100% 212s Render took 212.311 seconds


Turning on this new Estrin optimization:

ben@linux:~/Projects/PSRayTracing/build_gcc_14$ ./PSRayTracing -n 250 -j 4 -s 1920x1080 ... Rendering: [==================================================] 100% 206s Render took 205.99 seconds


A nice +3% speedup over the `asin_cg()`

method from last time. We're not going to see a massive jump like the benchmark above since calling arcsine is such a small part of this program (compared to everything else). On the Apple M4 Mac Mini (Tahoe), with the old `asin_cg()`

:

ben@Mac build_clang_17 % ./PSRayTracing -j 4 -n 250 -s 1920x1080 ... Render took 101.747 seconds


Plugging in our new one:

ben@Mac build_clang_17_asin_cg_estrin % ./PSRayTracing -n 250 -s 1920x1080 -j 4 Render took 101.817 seconds


While on the surface this might look like an absolutely atomic performance degradation, it's actually nothing. Rendering each time can vary give or take two seconds, despite the ray tracer being fully deterministic. I usually chalk this up to "gremlins in the computer" and by that, I mean things like the OS doing context switching and CPUs having dynamic clocks. The best thing to do would be to take 250 runs of this. I don't think it's worth it. From a heuristic standpoint 0.1 seconds is not a lot of time out of 102. Also clang on the M4 doesn't have that much of a speedup when doing `asin_cg_estrin()`

vs the plain `asin_cg()`

.


## Last Words (and Opinions)

When I started work on [PSRayTracing](https://github.com/define-private-public/PSRayTracing), I wanted to show off how you can rewrite your code for the compiler to make better optimizations; this is another one of them. In this series I hope I've really hammered down the importance of benchmarking (i.e. taking measurements) as well. **This is something I do not see others doing**.

I took [a brief look at using a LUT](https://github.com/define-private-public/PSRayTracing/blob/9ffba62428212610b95789237cc88967f69f3546/experiments/asin_cg_approx/benchmark_with_lut.cpp#L101), while that might have been faster in the past (and on paper), it wasn't the case for me. It also had a lot more error. Email me for charts. Stick with a math formula. It's simpler. Using SIMD to speed up the computation isn't an option either due to the architecture of [the original code PSRayTracing was based on](https://raytracing.github.io/). It's something I'd *like* to do, as sometimes a performance bottleneck can be architectural, but there are many other ways I'd like to spend my days in this life.

Lastly, keep in mind this is an approximation of arcsine, not the actual method. Most of the time (especially for computer graphics) you can get away with one, but there are cases where you cannot.

Always step back from the problem, collaborate, and then reevaluate. You'll find something better.


Edit 3/17/2025: Discussion threads: