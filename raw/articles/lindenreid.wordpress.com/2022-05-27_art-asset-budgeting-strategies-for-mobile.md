---
title: Art Asset Budgeting Strategies for Mobile
url: https://lindenreidblog.com/2022/05/27/optimization-strategies-for-mobile/
author: View all posts by Linden Reid
published: '2022-05-27'
source_blog: Linden Reid
source_site: https://lindenreid.wordpress.com
category: graphics
fetched: '2026-04-13'
---

A perfectly optimized game is not one with 0mb of assets and 0ms spent on the GPU; it’s one whose memory and computing resources are well prioritized and balanced across the entire game’s ecosystem

This post is adapted from a list of notes I keep for myself when working on a game or consulting on a team to help them out with optimization. It’s** **focused on outlining my** high-level strategies for art asset budgeting,** with some specific notes for optimization in **Unity **and **mobile optimization**, but the mindsets, goals, and many of the insights apply for games on any platform.

Simply put, an art asset budget is a **plan that places limits on the size of art assets, **like texture resolution, mesh poly count, and animation bones counts, in order to **optimize your runtime and install size memory**.

Runtime memory usage is critical for overall app performance, especially in terms of how art assets affect rendering performance. In addition, install size is absolutely critical for mobile games, as **players will uninstall large apps on their phone** to make room for texting their friends more GIFs!!! How thoughtless!!

So, asset budgeting is critical for games which have lofty art fidelity or ambitious rendering goals but want to publish on memory-limited platforms, including mobile and VR. This post will teach you strategies to create and maintain art asset budgets to achieve your aesthetic goals!

Note: sorry I never finished this article by adding the images! The text is useful regardless.

[Read more: Art Asset Budgeting Strategies for Mobile](https://lindenreidblog.com/2022/05/27/optimization-strategies-for-mobile/)

# Optimization mindsets

Optimization, especially in terms of creating art assets budgets, isn’t just about technical skill; it’s about communication with your whole team. Here’s a review of my high-level strategies for asset budgeting and optimization in general.

- Set goals.
- Before you can start making a budget, you need to set some goals to measure against!
**Minspec:**what are the oldest devices the game needs to run on? This will heavily influence asset budgets, as different devices have different app memory limits.**FPS:**what stable framerate do you want your players to experience?**Battery life**: how many hours should your players be able to play your game before their device’s battery runs out?

**Install size**: what should the initial download size of the app be?- If there’s a difference between initial download size and the size after install (quite common), what are those limits and how are they different?

**Runtime memory usage**: What’s the maximum amount of runtime memory you want your app to use?- You may want to test what the maximum memory usage is on your minspec before the app throttles/ crashes from being out of memory, and aim for being consistently well under this max.

**Gameplay goals**: Communicate with designers to figure out what**performance-impacting gameplay**goals they have. This might include the number of players loaded into a level at once; large swarms of enemies or crowds; view distance for the player… it’s going to vary wildly based on the game.- They may also have goals for the game that affect aesthetic concerns, like monetizing by selling character skins- in that case, for example, you may want to consider prioritizing your art asset budgets on rendering characters by giving them higher poly counts than the environment.


- For mobile games, you want to shoot for rendering the game in around
**22ms**in order to run at**30fps.**(*)- Rendering at 60fps means you only have 16ms total to render the frame; 30 fps means you have 33ms total.
- HOWEVER, these time limits are a maximum, and on mobile,
**you don’t want the app to be consistently using maximum resources in order to render a frame**, as this will cause**battery drain**and**overheating**.- Overheating can throttle performance and make the phone hot (ow).
- Battery drain will literally cut short how long your players have to play your game!
- In my experience, 3D multiplayer games like Fortnite mobile have 1-2 hours of battery life; less aesthetically complicated singeplayer 3D games like like Crash Bandicoot infinite runner mobile game allow 2.5+ hours of battery life.

- Although we won’t talk about shader optimization in this article,
**optimizing your art assets can massively help with achieving your target framerate**, and texture bandwidth can be a huge contributor to device battery drain and heat(*).

**Tackle BIGGEST issues FIRST.**- We usually first identify what the biggest slices of the pie are in terms of overall memory usage, and tackle paring down those issues first.
- There’s plenty of nuance to consider, but we generally move on in order from biggest to smallest issues.

**Prioritize WORST CASE scenarios.***A “worst-case scenario” doesn’t necessarily mean that case is rare.*It just means the app is at its maximum expected resource usage- most expected characters on screen, densest environment, most VFX usage.**Players may still encounter worst-case scenarios quite frequently.**- If we optimize for our worst case scenarios, in many cases, we can either eliminate these scenarios (by fixing bugs or removing or paring down features which are too expensive) or build optimizations that aide both the worst-case AND average-case scenarios.

- You might be asking- how many [polygons/textures/objects] should I budget for on [x platform]? How many is too many??
- I can’t answer that question for you- that’s what this guide is for!
- A game feature, art asset, or rendering feature being “excessive” in this context doesn’t always have a hard number or limit:
**“excessive” is defined by an asset or feature***causing issues for performance*.

- Optimization is about balance and prioritization.
*Something*is going to have to take up time on the GPU.*Something*is going to fill the screen.*Some*art assets have to be made. **A perfectly optimized game is not one with 0mb of assets and 0ms spent on the GPU; it’s one whose memory and computing resources are well prioritized and balanced across the entire game’s ecosystem**, such that the game is meeting**FPS targets***and*aesthetic goals.


<insert a screenshot of a worst-case scenario for a game with an explanation of why this frame was picked>

# Runtime memory usage budgeting

- Utilize a memory profiler to see
**how much memory the app is using**on device in**worst-case scenarios**.- Always profile Release builds, as Debug builds are often bloated in order to allow certain debugging features.
**Always profile on device**! Memory usage in-editor/ on PC and Mac will be super inaccurate, as compression methods are different; you may encounter memory references that the Editor is holding on to which wouldn’t be held in a build; and the Editor may bloat the memory capture with its own resources.

**Profile the worst-case asset runtime memory usage**- Remember you’ll want to do this in a release build and on device!
- Consider making a
**breakdown of everything that was in memory**and grouping it into**categories**, which might look like:- Rendering pipeline memory (render buffers)
- Characters
- VFX
- Environment and other static objects
- UI
- Unexpected items/ potential memory leaks

- Take note of:
- Whether or not you were maintaining your target FPS
- What the total memory usage was
- The total poly count
- The amount of unique textures and their total memory usage
- Whether or not your were maintaining your target memory usage, or encountering out-of-memory crashes
- The memory distribution per each category you noted above


- Once you have your worst-case scenarios profiled, figure out if this is
**sustainable for your gameplay goals**and identify if any optimizations need to be made.- Are textures and meshes being re-used as much as possible?
- Is the mesh density for characters and the environment reasonable, or are they excessively dense for how small they are?
- Are the only assets in memory ones that were needed to render the scene, or is memory leaking from scene to scene?
- If not, consider packaging memory in smarter ways like using Unity’s Asset Bundling system to ensure that assets are smartly loaded in and out of memory.


- In addition to considering runtime memory usage purely in terms of memory, is excessive memory usage slowing down
**rendering time**?- Excessively dense meshes and materials which use a large amount of texture memory can impact draw call performance.
- It might be worth it to run several tests including
**testing poly count limits**and**texture memory usage limits**and to test if significantly decreasing these asset usages improves render times.


<insert an example runtime memory profile screenshot in Unity of example project>

<insert pie chart of memory breakdown of example project of that capture>

## Install size budgeting

- Use the following formula to estimate total game install size at ship time.
**total build size = sum(average cost per object * TOTAL number of objects) +**+**(other game assets)****(game build)**- as in, the total memory usage is the sum of the average size of each object in the build times the number of those objects you expect there to be at ship
- “game build” is stuff like built code that we probably won’t try to change the overall size of
- “other game assets” are other assets that might not make sense to use the cost-per-object formula for- for example you might estimate UI or audio assets differently
- note that this is your
**on-disc install size**, NOT the runtime memory usage


- estimate the
**cost per object**as the**total amount of memory associated with major objects in your game**(characters, environments) and all of the assets related to them- identify art assets associated with each object: meshes, animations, etc
- also include other game data, like enemy tuning, dialogue, or other text-based data, depending on how significant the memory usage is
- for example, we might consider one playable character as an object, and their mesh, textures, and voice lines as their associated objects, and calculate the average total size of each character and all of their assets

- Estimate the
**TOTAL number of objects of each type in the build**at the time you’re shipping the game.- This requires consulting with design on the total number of different environments, characters, etc they plan on having in the final game, and considering the number of unique assets you need for each.

- Once you feel good about this calculation,
**identify if this build size is ship-able or not**. If not, you may need to optimize your asset sizes. This might include:- Setting limits for poly counts for meshes, texture sizes, or animation detail like bone counts

- Increasing the amount of texture compression used- try to balance having the highest compression setting possible while maintaining good texture appearance in-game
- Considering streaming assets- maybe not all of the DLC needs to be installed if the player isn’t expecting to play it all simultaneously


<insert an estimated memory usage calculation>

# Tooling systems to consider

Here’s a list of toolsets and other game systems to consider that can aid in the art optimization process.

**Asset importing rules**- Hook into import stage in your engine to create rules for maximum sizes, compression settings, color settings, etc for assets based on naming conventions/ filetype/ other conventions
- This helps
**enforce optimization-critical asset settings**without expecting artists to remember to change all these settings by hand

**Tiering rendering**and asset quality based on device, which could include:- Turning off non-gameplay-critical rendering features- for example, turning off certain post-processing effects can save on texture memory usage
- Turning down rendering quality settings (MSAA quality, shadow buffer resolution, etc)
- Turning down all image sizes
- Changing asset compression settings
- Reducing particle effect limits
- Rendering the game at a smaller resolution

**Bundle game data**using Addressables in Unity (or equivalent system)- Asset Bundles allow you to package game assets to deliver them at opportune times, both inside the app or by streaming them to the player remotely.
- In-app, bundles allow finer tuning of what’s in memory at runtime.
- We usually separate large chunks of game assets into levels or scenes, but finer-tuned bundles may help us have even more control of what’s in memory for different gameplay situations.
- Get creative! Just remember the time spent loading assets has its own cost, so it’s a balance.


- Features for auto build systems
**Run performance tests on auto-builds**.- Keep a graph of performance over time. Congratulate yourselves for watching the line go down; address spikes as soon as they happen.
- You could graph anything really. Average runtime memory usage. Build size. Your interest in reading this article, word-by-word.

**Enforce asset importing rules on pull requests**.- This literally prevents artists from checking in assets which have the wrong settings or that are too large.
- The only downside is you won’t ever get to laugh at realizing your perf hit was being caused by a long-forgotten high-poly apple in the corner drawing to 3 pixels worth of screen space….



## Fin

I hope this article gave you a helpful overview of how to set up art asset budgets!

Remember that budgets aren’t just about making everything as low as possible; it’s about distributing your limited resources in ways that make sense for your gameplay and aesthetic goals.

Go forth and make more optimized games! And don’t hesitate to reach out if you need a little advice or some professional consulting. 🙂

Good luck,

Linden