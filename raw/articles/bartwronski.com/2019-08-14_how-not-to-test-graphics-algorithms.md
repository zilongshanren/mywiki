---
title: How (not) to test graphics algorithms
url: https://bartwronski.com/2019/08/14/how-not-to-test-graphics-algorithms/
published: '2019-08-14'
source_blog: Bart Wronski
source_site: https://bartwronski.com
category: game programming
fetched: '2026-04-13'
---

## Intro

Siggraph 2019 is sadly over, but as always I came back super inspired and grateful for meeting many friends.

Conferences are mostly not about seeing the presentations – but about all the interesting and inspiring discussions, and one of such casual lunch-time chats lead to me writing this blog post.

We chatted quite a lot about how to test automatically graphics features and while I am happy that the games industry starts to introduce various forms of testing, I believe that (in the games industry) **many (if not most) people testing graphics features do it wrong**.

This is a bold opinion, so I am going to elaborate on it, but first I will share my personal experience.

## Personal backstory – frustrated by tests

My story with using tests is not glorious.

Over my career switching workplaces, I went from teams using zero tests at all (not even trivial build tests! my first game gig binary builds were initially checked in to VCS by a programmer “from time to time”), through simple pre- and post-submit build tests, to full testing culture, but for most of my career and at most of those places, the code itself – the functionality – was not tested.

I encountered some form of “functional” tests quite late in my career – don’t want to mention here the company / team name, as it is not relevant, and I am sure a lot has changed since then. The important thing is – the amount of tests was orders of magnitude more than I have seen before.

Some of the tests were very reasonable – for example [smoke tests](https://en.wikipedia.org/wiki/Smoke_testing_(software)) on code and content build and some of the actual game levels. They were catching lots of real issues, both in the code, as well as in the checked-in data.

On the other hand, as a graphics engineer, I quickly discovered that I have to deal with numerous *“visual tests”* for graphics features and they were source of some frustrations and tensions.

The testing framework itself and infrastructure were pretty good, but the team practices and processes around testing graphics features were far from useful – at least to me and in my experience.

They were essentially [golden tests](https://softwareengineering.stackexchange.com/questions/358786/what-is-golden-files) for each feature, all testing for exact output image rendered by the game engine. I will describe the basic workflow to test some new features in a new section, naming it **Approach A**.

It was quite an extreme process, but talking with colleagues from other companies, I learned that many developers use at least partially similar testing strategies!

That past experience caused the immature me to literally hate all kinds of tests (allergic [Pavlovian reaction](https://en.wikipedia.org/wiki/Classical_conditioning)), but after some time and working with teams somewhat more experienced in terms of engineering practices and “[code health ](https://www.mediawiki.org/wiki/Code_Health)culture”, I think **I got to love well designed tests **and I think I can dissect one by one how **Approach A** could have been improved.

In the next sections, I am going to compare the **Approach A** with an **Approach B** – an example of a how a graphics feature could be tested, and then by comparing both approaches analyze what distinguishes a *“good”* and a *“bad”* test process for graphics and imaging programmers.

## How testing shouldn’t be done – Approach A

- Tech artist or a programmer creates a new “level”, placing meshes and materials (that use the new feature) with the main game editing tool.
- Virtual camera is placed in the world and a script is set up to take a screenshot after some time. Optionally, the script would toggle some rendering features on / off.
- The test is submitted in the data repository (not the code repository!) since it has some data dependencies.
- Screenshot (golden file) is stored in some database.
- During the testing itself, the screenshot is compared (hash, exact equality) with the output – any single difference = test failure.
- Some time later, someone changes something and suddenly, test output changes a few of the pixel values = failure. You can see both the hash difference, as well as gold and test + diff images.
- Any test failure after submission = submits are blocked for the whole team, until the tests are “fixed” or “blessed” (golden file updated).

Basically every single point on that list was either ineffective, or simply frustrating.

At least once a week I had to go through +/- thousand of screenshots and “bless” them under peer pressure (I have just blocked other colleagues from submitting) – overall very stressful experience, magnified by other artifacts of the submit/integration process like waiting in line for integration to happen, getting kicked out of the queue on broken tests etc.

At the same time, those tests were not catching many serious, real problems – like some important part of lighting being not normalized, NaNs appearing in BRDF at gloss values of 1, etc.

## How it could be done – Approach B

Let’s say you have written a new awesome feature – [subsurface skin scattering](https://en.wikipedia.org/wiki/Subsurface_scattering) shader, requested so much by character artists. Both them and you are happy with the prototype results on a test model and you could click submit… But instead you decide to improve the code a bit, modularize it, and write some tests.

You think about steps of your algorithm, and decide to test some following properties:

- Does the skin shader work – does it actually diffuse the incoming light?
- Does the skin shader preserve energy conservation (no matter what is the scatter profile, there should never be energy added)?
- Does the skin shader respect specified diffusion profile?
- Does the skin shader produce “reasonable” values – never negative, NaNs, inf.
- Is the diffusion rotation invariant / isotropic?
- Are the artist-authored material properties properly packed?
- Does the diffusion stop at significant depth discontinuities?
- How much performance cost does it add?

Ok, knowing +/- what you want to test (this is all just an example), you finally decide to write some tests!

- You create a simple C++ (or the language of your choice) file along your code and add it to your build system with some “decoration” that it should be compiled as a part of an existing or a new test suite.
- In this file, you add simple macro decorated functors / classes that test behaviors one at a time.
- For every behavior, you create synthetic, procedural input from your code.
- For every behavior, you verify the output procedurally from your code. Apart from checking the actual behavior, you call some helper function e.g. ValidateOutput that checks for NaNs, inf, negative values.
- On test failures, you add code printing as much information as possible – expected vs actual, histogram of differences if checking multiple values, maybe additionally produced image disk dump.
- You write a (micro)benchmark that times the newly added pass depending on different sizes of inputs, different proportion of pixels with the feature enabled / disabled etc.

The **points 3 and 4** are absolutely crucial and very different from the **Approach A,** and not very commonly used among colleagues I talked with.

I will make this example more concrete now – let’s say that you wanted to check for energy conservation of the diffusion process.

You would create a **synthetic **lighting **buffer **(and potentially a synthetic GBuffer if necessary) by filling it on CPU with zeros and a single pixel in the middle that would be “1” (or any reference value). You call your normal skin code pass, and then fetch the results to the CPU. **On the CPU, you analyze the output programmatically** – e.g. numerically integrate the pixel values. Such a test could have a few sub cases – testing unit response (no actual diffusion), perfectly flat box-filter like diffusion, and a Gaussian-like profile. Again, the most important part of this workflow is having very deterministic, extremely simple, and procedural inputs/outputs that you can reason about.

**Important note**: analyzing outputs numerically doesn’t mean that you can’t save the intermediate / final outputs for debugging and **inspect them visually as well**. On the contrary, I highly encourage having such option! Cases with all zeros or all infinity might be easy to see in a debug printout, but often visual inspection can provide insights on more non-obvious problem patterns (hey, why is this checkerboard pattern there? did I skip some samples?). Furthermore, visual verification of the test inputs / outputs when writing them can verify it they “make sense” and are representative of the expected outcome.

## What is the difference between both approaches?

Let’s now dissect differences between the two approaches.

### Tests (not) verifying correctness

What is the purpose of a test? There are many, but the most straightforward one is verifying correctness. If your input is some data, and it *“looks kind of ok”*, is this verifying the correctness?

If you want to test a skin shader, it might seem like a good idea to test it on a mesh of a head, but in such a setting you cannot verify any of the systems design or implementation assumptions – just whether it “*looks right”*. This might be important for the user to verify whether the feature is what they asked for, but is useless for other engineers who will be looking at changed results of such tests in the future.

Are you sure that your Gaussian blur is not brightening the image? That its sigma is correct? Will the lighting shader work well with parameters at the end of the input range? Is your subsurface scattering shader really applying the requested diffusion profile? Is data after GBuffer packing/unpacking within the theoretical quantization precision across the range? None of those questions can be answered by eyeballing the output.

### Easiness/difficulty adding new tests

In this category, the problem with the **Approach A** was obvious – adding a new test involved multiple steps and workflows that were not typical programmer workflow. Launching the editing tool, setting up some geometry, setting up scripts, adding new golden data… Quite a lot and very discouraging if you want to provide. My personal no1 rule of creating a healthy team culture is to make sure that valued and desired behaviors are “easy” to do (in a perfect world would be easier than the undesired ones). Having to jumping through many hoops to create a simple test doesn’t encourage testing culture.

Adding a new test that would be executed automatically should be just a few lines of code – and it is possible if you have testing process set up like in **Approach B**.

### Tests close to / separated from the code tested

If tests “live far away” from the code tested like in the **Approach A**, it is hard to correlate one with another. If you are refactoring some feature and need to verify if tests that changed were actually supposed to change or not, it destroys your confidence that should come from using tests…

Furthermore, I believe that tests can serve as a supplemental “documentation” (just like well named functions and variables, well commented code etc) – and I often rely on them to see how a piece of code might be used, what are the assumptions etc. With the **Approach B** you can open the tests file and learn about the potential use-cases and assumptions that the code author has made.

If tests are completely separated and just test functionality, this advantage is also completely gone… I might even find and open test scene, but not necessarily know what was set up there and how!

### Testing on synthetic vs authored (and binary) data

Tests should be as simple, “atomic” and as isolated as possible (unless you want to do specifically [integration tests](https://en.wikipedia.org/wiki/Integration_testing)). Relying on some arbitrary, authored and ad hoc data makes it very difficult to analyze / debug the test and the desired results – see “verifying correctness” above.

A second problem is that now all your testing relies on your data processing pipelines. If you change your data pipelines even slightly (let’s say introduce subtle compression, quantization or anything), all your tests are going to change! This leads us into the next section…

### Unit testing / testing end-to-end

Relying on e.g. data processing pipelines in all of your tests makes reasoning about safety of changes (one of the points of testing) impossible – you will see hundreds of tests changed their value, but among this noise might miss some real problem.

Notice how in the **Approach B **any changes in your content pipeline will not cause unexpected visual changes.

Testing end-to-end like in the **Approach A **relies on tens of different systems… Content build system (previous point), material system, lighting system, camera system, mesh rendering, post processing, even gamma correction! Once after changing from [regular z buffer to inverse z](https://developer.nvidia.com/content/depth-precision-visualized), I had to “bless” all the tests – not only unnecessary, but dangerous (I could have missed some legit regression). This is lots of moving pieces, and makes it impossible to correlate simple inputs to the output value. If it changes (suddenly test becomes broken by an “innocent” change) – good luck debugging where it comes from!

### (Not) Understanding the breakages

Ok, your input got broken… Why is that? Even ignoring the above (“testing end-to-end”), are those single pixel differences caused by “quantization noise”, or an inf/nan? Oh, the energy conservation broke – do we now have too much, not enough, or simply wrongly distributed outputs?

Having numerical analysis, histograms of differences, or simply asserts in tests (“assert that the output is always below 1”) like in the **Approach B** would immediately answer at least some of those questions.

### (Lack of) tests documentation

Tests themselves should be documented and commented if possible. I find it much easier to do it through code comments and meaningful function naming (trivial example – e.g. VerifyNoNaNs called from within a test) than through some metadata attached to the test itself and the scene.

### Test updates separated from changes / code CLs

Ok, let’s say that you have refactored some system and expect decreased/increased precision of some stages. In the case of **Approach A** you would submit your CL, and then update the goldens values. In the case of **Approach B**, you can put it in the same CL (again, change and test relative “locality”), and specifically reason about the changes “ok, I have lowered the precision of quantization by 2 bits, so I expect to change my test epsilons by no more than 4x”.

### Relying on GPUs and floating point operations for exact comparisons

This one is a tough one and I don’t have a great answer for.

Doing graphics and work on GPUs, we want to test floating point operations, as well as catch some e.g. driver regressions.

On the other hand, float point operations are flaky, can depend on the target platform (e.g. presence of SSE vs AVX), some runtime environment flags that change floating point behavior, or a driver version.

I personally think that having a hybrid tests that do all the input creation, packing, output fetching and analysis on the CPU, but execute the actual graphics production code on the GPU is a good middle ground, but as I said – it’s quite tough point, and every approach I have tried had its pros and cons.

If you suffer from lots of noise from driver / testing device changes, (and are sure that your tests are designed in a good way) then consider using a [WARP device](https://docs.microsoft.com/en-us/windows/win32/direct3darticles/directx-warp) for DirectX, or excellent [SwiftShader](https://github.com/google/swiftshader) for OpenGL.

### Test speed

This point might be too much of an implementation detail, so I will keep it short – but in the **Approach B** tests have almost no dependencies, are extremely minimal and execute in literally milliseconds. Fast tests encourage adding more tests, and testing often during the coding process itself.

## When and how to test graphics?

Having described general ideas regarding how features can be tested, one might ask – when it is worth doing it?

First use case – that I +/- already described here – is testing features when their interface and functionality are more or less defined, and most of the code is written. I want to emphasize that you are not limited to just the simplest single pass and image inputs / outputs.

Nothing prevents you from creating procedurally a simple scene with some e.g. decals, and verify if they get rendered correctly, and all the stencil buffer logic works (every game engine that I worked on and that used stencil buffer – it got broken on some platform for some feature during an unrelated refactor / optimization).

The second use of tests is to guide you and help you when writing the code.

While I think the whole concept of [TDD](https://en.wikipedia.org/wiki/Test-driven_development) is a classic over-complicated snake oil, it is often worth writing a test for the functionality you are about to add / in the process of adding. For example, writing GBuffer bit packing having a test that verifies that 0 maps to 0, 1 maps to 1 and 0.5 maps to 0.5 can help save you a lot of time. I cannot count instances of bugs when an engine had 127/128 or 255/256 instead of 1.0 because of wrong packing logic. 🙂

Similarly you can write tests during feature development for any functionality from high level – like material blending, through mid level (what is the [z buffer precision](https://developer.nvidia.com/content/depth-precision-visualized)? Count all the discrete z values in the range 100m-101m and you have an immediate metric estimating [z-fighting](https://en.wikipedia.org/wiki/Z-fighting) in that range!), to low level – I cannot imagine writing [fixed-point math](https://en.wikipedia.org/wiki/Fixed-point_arithmetic) code without some hard check tests for under/overflows and verification of rounding.

Third use case that I highly encourage that is testing for performance – (micro)benchmarking. If you set up inputs procedurally, you can track the exact performance / timing of a given feature in isolation. Setting up the inputs/outputs procedurally allows you to control it very precisely and avoid inherent noisiness (and data dependence) of testing of the real scenes. Such benchmark can be used in the optimization process itself (especially with shader/code hot-reloading), but more importantly to track any performance changes and regressions. You want to track, locate, (and stop) any functionality regressions – why would you not want to do the same for performance? 🙂 Tracking it over time and having logs for many months can also help to analyze trends like immediately not obvious regression creep (death by a thousand paper cuts). Or conversely, you might immediately see a performance improvement from a new driver / compiler update – as a technical owner of a feature / system / technology, you should be aware of all of the changes, including the positive ones.

## Offtopic – sanitizers and fuzzing

When talking about testing, I couldn’t resist myself from dedicating a tiny section and not mention here two techniques that are simply amazing when it comes to ROI – [sanitizers](https://github.com/google/sanitizers/wiki), and [fuzz testing](https://en.wikipedia.org/wiki/Fuzzing).

They are especially effective when used together (given that sanitizers can slow down code to the point when manual testing is not possible/pleasant…), and will catch lots of real problems almost immediately.

I promise that [TSan ](https://github.com/google/sanitizers/wiki/ThreadSanitizerCppManual)will trigger almost any time you introduce some new parallel code, and that it won’t be a false positive. 🙂

## Summary / caveats

**Testing **is not “scary” and **should never be a burden and a struggle**. After all, it is a tool for you – engineer, your future self, and your colleagues.

If testing is a burden, revisit your workflows and processes and figure out which parts can be improved!

I have compared two approaches of testing specific graphics features – **Approach A**, which is a real workflow that I used to work with, and **Approach B**, which is how I personally suggest approaching it.

I see not many virtues of the end-to-end / screenshot based approach in the case of testing features, however for the completeness and to be entirely fair, I see some good use cases for golden testing.

One is to have a simple smoke test and watch out for random breakages “somewhere in the pipeline”, when not anticipated and from unexpected sources. The second one is that it does provide a form of integration testing, testing the interaction of multiple systems. The third one is a bit paradoxical – the inherent flakiness and sensitivity of such tests makes then a good candidate to catch some unexpected compiler / toolchain / driver changes.

To combine those use-cases and some real advantages of golden tests, and not get into the problems / frustrations, I would suggest to have – a few (no more than 10-15!) golden “smoke tests”, with lots of features stuck into one scene, and testing the pipeline end-to-end. Expect that they might get changed pretty often, but be very thorough when investigating the differences (easier when four images change, than a thousand…). Finally, use programmatic tools like simple histograms, printouts and design the process of debugging the changes as well.

Finally – and the reason why I wrote this blog post – I hope that your adventures with finding the right testing strategy for you, and the potential productivity boost that comes from good tests will be easier to get for you than they were for me. 🙂

Hi Bart –

I saw your presentation PDF for SIGGRAPH2019 and I see on the last page (73) that there is a “Computational Cost” slide. What does the “fixed cost” refer to? Is there a fixed cost in addition to the per-frame cost? Or the per-frame cost includes the fixed-cost as a minimum? Thank you.

Hi Andy! By the fixed cost we mean cost that is additive and independent of the frame count; it stays the same no matter if we merge a single frame, or 100. In practice it involves some “bookkeeping”, creating buffers, compiling shaders, synchronizing CPU and GPU (part of it at beginning, part of it at the end of processing). While not an inherent part of our algorithm, but an implementation detail, we still included it for transparency.

Pingback: Why are video games graphics (still) a challenge? Productionizing rendering algorithms | Bart Wronski

Hi Bart,

This is a great post. I know which test system you’re talking about when mentioning Approach A. However, I believe there are some things with the process that didn’t work back then which caused all the frustrations you mention (I had the same when working with that system), even though I do think there is a lot of value in Approach A. One of the things I had to implement was the multi-threaded command list generation, and having Approach A was a life savior because I was changing a lot of code, which caused a lot of breakage regardless of the actual algorithms. Being able to validate each change was really good, and provided a much more robust code when checked-in.

Your approach B is a great approach too, but I feel its much more for the person who is writing the actual feature and wants to validate each corner case rather than making sure the feature doesn’t break. I would also say that with approach A you can also implement approach B, and in fact would argue you want both.

On the floating point errors, those are an interesting problem. At Pixar, they use perceptual differences to validate their algorithms instead of perfect image equality. We could implement that as well, but I wonder how you can measure the proper “error” where the new results, while different, are still validated as correct.

But to conclude, I think we can both agree that writing good graphics/rendering tests is hard, and there aren’t perfect answers.

Eric