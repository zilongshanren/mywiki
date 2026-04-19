---
title: '16BPP.net: Blog / The Performance Impact of C++''s `final` Keyword'
url: https://16bpp.net/blog/post/the-performance-impact-of-cpp-final-keyword/
published: '2024-04-22'
source_blog: '16BPP.net: Blog / Page 1'
source_site: https://16bpp.net/
category: graphics
fetched: '2026-04-19'
---

If you're writing C++, there's a good reason (maybe...) as to why you are. And probably, that reason is performance. So often when reading about the language you'll find all sorts of "*performance tips and tricks*" or "*do this instead because it's more efficient*". Sometimes you get a good explanation as to why you should. But more often than not, **you won't find any hard numbers to back up that claim**.

I recently found a peculiar one, the `final`

keyword. I'm a little ashamed I haven't learned about this one earlier. [Multiple blog posts](https://devblogs.microsoft.com/cppblog/the-performance-benefits-of-final-classes/) [claim that it can](https://blog.feabhas.com/2022/11/using-final-in-c-to-improve-performance/) [improve performance](https://levelup.gitconnected.com/c-performance-improvement-through-final-devirtualization-258e7ae1d2b5)(sorry for linking a Medium article). It almost seems like it's almost free, and for a very measly change. After reading you'll notice something interesting: no one posted any metrics. Zero. Nada. Zilch. It essentially is *"just trust me bro."* Claims of performance improvements aren't worth salt unless you have the numbers to back it up. You also need to be able to reproduce the results. I've been guilty of this in the past ([see a PR for Godot I made](https://github.com/godotengine/godot/pull/33101)).

Being a good little engineer with a high performance C++ pet project, I really wanted to validate this claim.

Update May 3rd, 2024: When posting on /r/cpp, someone else did mention they did some perf testing of final before and had some numbers. Theirs was from about a decade ago. I did not find this in my initial searches. [The comment thread and their article can be found here](https://www.reddit.com/r/cpp/comments/1caarda/the_performance_impact_of_cs_final_keyword/l0r1n2r/).

I keep on finding myself unable to get away from my pandemic era distraction, [PSRayTracing](https://github.com/define-private-public/PSRayTracing). But I think this is actually a VERY good candidate for testing `final`

. It has many derived classes (implementing interfaces) and they are called millions of times in normal execution.

For the (many) of you who haven't been following this project, the quick and skinny on PSRayTracing: it's a ray tracer implemented in C++, derived from [Peter Shirley's ray tracing minibooks](https://raytracing.github.io/). It serves mainly an academic purpose, but is modeled after my professional experiences writing C++. The goal is to show readers how you can (re)write C++ to be more performant, clean, and well structured. It has additions and improvements from Dr. Shirley's original code. One of the big features I have in it is the ability to toggle on and off changes from the book (via CMake), as well as being able to supply other options like random seeds, multi-core rendering. It is somewhere 4-5x faster than the original book code (single threaded).


### How This Was Done

Leveraging the build system, I added an extra option to the `CMakeLists.txt`

:

Then in C++ we can use (ab)use the pre processor to make a `FINAL`

macro:

And easily it can slapped onto any classes of interest:

Now, we can turn on & off the usage of `final`

in our code base. Yes, it is very hacky and I am disgusted by this myself. **I would never do this in an actual product**, but it provides us a really nice way to apply the `final`

keyword to the code and turn it on and off as we need it for the experiment.

`final`

was placed on just about [every interface](https://github.com/define-private-public/PSRayTracing/tree/b213aa1338744931977263e61cc6fd4cee6a7f32/render_library/Interfaces). In the architecture we have things such as [ IHittable](https://github.com/define-private-public/PSRayTracing/tree/b213aa1338744931977263e61cc6fd4cee6a7f32/render_library/Objects),

[,](https://github.com/define-private-public/PSRayTracing/tree/b213aa1338744931977263e61cc6fd4cee6a7f32/render_library/Materials)

`IMaterial`

[, etc. Take a look at the final scene from book two, we've got quite a few 10K+ virtual objects in this scenario:](https://github.com/define-private-public/PSRayTracing/tree/b213aa1338744931977263e61cc6fd4cee6a7f32/render_library/Textures)

`ITexture`


And alternatively, there are some scenes that don't have many (maybe 10):


### Initial Concerns:

For PSRT, when testing something that can boost the performance, I first reach for the default scene `book2::final`

. After applying `final`

enabled the console reported:

$ ./PSRayTracing -n 100 -j 2 Scene: book2::final_scene ... Render took 58.587 seconds


But then reverting the change:

$ ./PSRayTracing -n 100 -j 2 Scene: book2::final_scene ... Render took 57.53 seconds


I was a tad bit perplexed? *Final was slower?!* After a few more runs, I saw a very minimal performance hit. Those blog posts must have lied to me...

Before just tossing this away, I thought it would be best to pull out the verification test script. In a previous revision this was made to essentially fuzz test PSRayTracing ([see previous post here](https://16bpp.net/blog/post/automated-testing-of-a-ray-tracer/)). The repo already contains a small set of well known test cases. That suite initially ran for about 20 minutes. But this is where it got a little interesting. The script reported using `final`

slightly faster; wtih `final`

it took 11m 29s. Without `final`

it was 11m 44s. That's +2%. Actually significant.

Something seemed up; more investigation was required.


### Big Beefy Testing

Unsatisfied with the above, I created a "large test suite" to be more intensive. On my dev machine it needed to run for 8 hours. This was done by bumping up some of the test parameters. Here are the details on what's been tweaked:

- Number of Times to Test a Scene:
`10`

→`30`

- Image Size:
`[320x240, 400x400, 852x480]`

→`[720x1280, 720x720, 1280x720]`

- Ray Depth:
`[10, 25, 50]`

→`[20, 35, 50]`

- Samples Per Pixel:
`[5, 10, 25]`

→`[25, 50, 75]`


Some test cases now would render in 10 seconds, others would take up to 10 minutes to complete. I thought this was much more comprehensive. The smaller suite did around 350+ test cases in 20+ minutes. This now would do 1150+ over the course of 8+ hours.

The performance of a C++ program is also very compiler (and system) dependent as well. So to be more thorough, this was tested across three machines, three operating systems, and with three different compilers; once with `final`

, and once without it enabled. After doing the math, the machines were chugging along for a cumulative 125+ hours. 🫠

Please look at the tables below for specifics, but the configurations were:

- AMD Ryzen 9:
- Linux: GCC & Clang
- Windows: GCC & MSVC

- Apple M1 Mac: GCC & Clang
- Intel i7: Linux GCC

For example, one configuration is "AMD Ryzen 9 with Ubuntu Linux using GCC" and another would be "Apple M1 Mac with macOS using Clang". Not all versions of the compilers were all the same; some were harder to get than others. And I do need to note at the time of writing this (and after gathering the data) a new version of Clang was released. Here, is the general summary of the test results:


This gives off some interesting findings, but tells us one thing right now: **across the board, final isn't always faster; it's in fact slower in some situations**. Sometimes there is a nice speedup (>1%), other times it is detrimental.

While it may be fun to compare compiler vs. compiler for this application (e.g. "Monday Night Compiler Smackdown"), I do not believe it is a fair thing to do with this data; it's only fair to compare "with `final`

" and "without `final`

" To compare compilers (and on different systems) a more comprehensive testing system is required. But there are some interesting observations:

- Clang on x86_64 is slow.
- Windows is less performant; Microsoft's own compiler is even lagging.
- Apple's silicon chips are absolute powerhouses.

But each scene is different, and contains a different amount of objects that are marked with `final`

. It would be interesting to see percentage wise, how many test cases ran faster or slower with `final`

. Tabling that data, we get this:


That 1% perf boost for some C++ applications is very desirable (e.g. HFT). And if we're hitting it for 50%+ of our test cases it seems like using `final`

is something that we should consider. But on the flip side, we also need to see how the inverse looks. How much slower was it? And for how many test cases?


Clang on x86_64 Linux right there is an absolute "*yikes*". More than 90% of test cases ran at least 5% slower with `final`

turned on!! Remember how I said a 1% increase is good for some applications? A 1% hit is also bad. Windows with MSVC isn't faring too well either.

As stated way above, this is very scene dependent. Some have only a handful of virtual objects. Others have warehouses full of them. Taking a look (on average) how much faster/slower a scene is with `final`

turned on:

I don't know Pandas that well. I was having some issues creating a Multi-Index table (from arrays) and having the table be both styled and formatted nicely. So instead each column has a configuration number appended to the end of its name. Here is what each number means:

- 0 - GCC 13.2.0 AMD Ryzen 9 6900HX Ubuntu 23.10
- 1 - Clang 17.0.2 AMD Ryzen 9 6900HX Ubuntu 23.10
- 2 - MSVC 17 AMD Ryzen 9 6900HX Windows 11 Home (22631.3085)
- 3 - GCC 13.2.0 (w64devkit) AMD Ryzen 9 6900HX Windows 11 Home (22631.3085)
- 4 - Clang 15 M1 macOS 14.3 (23D56)
- 5 - GCC 13.2.0 (homebrew) M1 macOS 14.3 (23D56)
- 6 - GCC 12.3.0 i7-10750H Ubuntu 22.04.3


So this is where things are really eye popping. On some configurations and specific scenes might have a 10% perf boost. For example `book1::final_scene`

with GCC on AMD & Linux. But other scenes (on the same configuration) have a minimal 0.5% increase such as `fun::three_spheres`

.

But just switching the compiler over to Clang (still running on that AMD & Linux) **there's a major perf hit of -5% and -17% (respectively) on those same two scenes**!! MSVC (on AMD) looks to be a bit of a mixed bag where some scenes are more performant with final and others ones take a significant hit.

Apple's M1 is somewhat interesting where the gains and hits are very minimal, but GCC has a significant benefit for two scenes.

Whether there were many (or few) virtual objects had next to no correlation if `final`

was a performance boon or hit.


### Clang Concerns Me

PSRayTracing also runs on Android and iOS. Most likely a small fraction of apps available for these platforms are written in C++, but there are some programs that make use of language for performance reasons on the two systems. **Clang is the compiler that is used for these two platforms.**

I unfortunately don't have a framework in place to test performance on Android and iOS like I do with desktop systems But I can do a simple "*render-scene-with-same-parameters-one-with-final-and-one-without*" test as the app reports how long the process took.

Going from the data above, my hypothesis was that both platforms would be less performant with `final`

turned on. By how much, I don't know. Here are the results:

- iPhone 12: I saw no difference; With and without
`final`

it took about 2 minutes and 36 seconds to perform the same render. - Pixel 6 Pro:
`final`

was slower. It was 49 vs 46 seconds. A difference of three seconds might not seem like much, but that is a 6% slowdown; that is fairly significant. (clang 14 was used here BTW).

If you think I'm being a little silly with these tiny percentages, please take a look at [Nicholas Ormrod's 2016 CppCon talks about optimizing std::string for Facebook](https://www.youtube.com/watch?v=kPR8h4-qZdk). I've referenced it before and will continue to do it.

I have no idea if this is a Clang issue or an LLVM one. If it is the latter, this may have implications for other LLVM languages such as Rust and Swift.


### For The Future (And What I Wish I Did Instead):

All in all this was a very fascinating detour; but I think I'm satisfied with what's been discovered. If I could redo some things (or be given money to work on this project):

- Have each scene be able to report some metadata. E.g. number of objects, materials, etc. It is easily doable but didn't seem worth it for this study of
`final`

. - Have better knowledge of Jupyter+Pandas. I'm a C++ dev, not a data scientist. I'd like to be able to understand how to better transform the measured results and make it look prettier.
- A way to run the automated tests on Android and iOS. These two platforms can't easily be tested right now and I feel like this is a notable blindspot
`run_verfication_tests.py`

is turning more into an application (as opposed to a small script).- Features are being bolted on. Better architecture is needed soon.
- Saving and loading testing state was added, but this should have been something from the start and feels like more of a hack to me
- I wish the output of the results were in a JSON format first instead of CSV. I had to fuddle with PyExcel more than desired.

- PNGs are starting to get kinda chunky. One time I ran out of disk space. Lossless WebP might be better as a render output.
- Comparing more Intel chips, and with more compilers. The i7 was something I had lying around.


### Conclusions

In case you skimmed to the end, here's the summary:

- Benefit seems to be available for GCC.
- Doesn't affect Apple's chips much at all.
- Do not use
`final`

with Clang, and maybe MSVC as well. - It all depends on your configuration/platform;
**test & measure to see if it's worth it.**

__Personally, I'm not turning it on. And would in fact, avoid using it. It doesn't seem consistent.__

For those who want to look at the raw data and the Jupyter notebook I used to process & present these findings, [it's over here](https://gitlab.com/define-private-public/PSRayTracing/-/tree/b275e22c5adaa0d576f788cbdfbe7f15f08c6196/final_keyword_experiment).

If you want to take a look at the project, [it's up on GitHub ](https://github.com/define-private-public/PSRayTracing)(but the active development is done [over on GitLab](https://gitlab.com/define-private-public/PSRayTracing/)). Looking forward to the next time in one year when I pick up this project again. 😉

Update May 3rd, 2024: This article has generated quite a bit more buzz than I anticipated. I will be doing a follow up soon enough. I think there is a lot of insightful discussion on [/r/cpp](https://www.reddit.com/r/cpp/comments/1caarda/the_performance_impact_of_cs_final_keyword/) and [Hacker News](https://news.ycombinator.com/item?id=40116644) about this. Please take a look.