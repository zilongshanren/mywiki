---
title: Model Synthesis and Modifying in Blocks
url: https://www.boristhebrave.com/2021/10/26/model-synthesis-and-modifying-in-blocks/
author: Boris
published: '2021-10-26'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

I’ve written a lot about Wave Function Collapse. Developed in 2016 by Maxim Gumin, it’s an algorithm for generating tilemaps and pixel textures [based on the constraint solving with extra randomization](https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/) . But did you know most of the key ideas come from a paper written a full decade earlier? Today, we’ll be looking into **Model Synthesis**, the [2007 PhD dissertation](https://paulmerrell.org/model-synthesis/) of **Paul Merrell**, and some of the elaborations he’s designed, particularly **Modifying in Blocks**.

## Model Synthesis

Model Synthesis is a very similar idea to WFC, which [I have a whole tutorial on](https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/). But I’ll run through the idea from scratch here.

Model Synthesis starts with a sample tilemap is provided, which is used to learn which tiles can be placed adjacent to each other, building the model. Then an empty grid of cells is initialized for the output. Each cell has a list of “possible” tiles that can fill it.

Initially every tile is possible. The main loop then picks a cell, and selects a given tile for it, marking all the others impossible. It then propagates the consequences of that selection using the AC4 algorithm, which means marking a tile as impossible for a given cell if all its valid adjacencies are already impossible. After propagation, the loops resets and we pick another cell to select a tile for.

Eventually, every cell only has a single possible tile and the map is generated. For more complicated tilesets, it’s possible for contradictions to occur (cells where no tile is possible), which requires a more advanced approach called Modifying in Blocks, described [below](https://www.boristhebrave.com#modifying-in-blocks).

This procedure is very similar to a simple [constraint solver](https://en.wikipedia.org/wiki/Constraint_programming), except for how cells and tiles are chosen. Model Synthesis describes what I consider the fundamental insight of this sort of generation: any constraint based solver can be modified to be a constraint based generator via random choice. It seems to the the first paper taking this approach – earlier approaches to Texture Synthesis were generally more statistical in nature.

![](../../assets/7295fba3a87df36f.jpg)

### Model Synthesis vs Wave Function Collapse

- MS selects cells based off a linear scan. WFC introduces the “minimal entropy” heuristic for selecting tricky tiles.

- MS focusses on chunky tiles and 3d scenes, while WFC has more of a focus on per-pixel generation and texture synthesis (though both are equally capable of both)

![](../../assets/9ec3a2f94ce73e19.jpg)

![](../../assets/cad0ae4c046d990d.png)

- WFC introduces the Overlapped model, where a model is learned about local neighborhoods instead of direct adjacency.

Paul Merrell has [an article on the exact differences](https://paulmerrell.org/wp-content/uploads/2021/07/comparison.pdf) between ModelSynthesis and WFC, and I’m also a a fan of [@expad’s writeup](https://twitter.com/exppad/status/1421058939274371079).

### Why was Model Synthesis ignored?

In my experience, the things WFC adds are nice, but are not deal breakers. You can still get [very nice results with Model Synthesis](https://www.youtube.com/watch?v=-N_TTAsdXgg) and the basic concepts are identical. So why did it languish for 10 years, until Maxim saw the potential and made his repo?

Model Synthesis uses 3d tiles, which are quite difficult to design, and C++, which is difficult to get running. WFC on the other hand, came with a wide variety of examples which were all simple images. The switch to 2d images immediately makes the use and behaviour of the project more understandable, and it lends itself to animations that show the possibility-set of tiles being updated as the animation runs. When I write tutorials, I’m usually careful to introduce ideas in 2d first, and include animations, for this exact reason.

Or it could be a more boring reason. The Model Synthesis website was unavailable for a period of several years, and “Wave Function Collapse” is simply a more catchy title, with it’s alluring promise of quantum physics.

## Modifying in Blocks

Constraint based synthesis, whether Model Synthesis or Wave Function Collapse, suffers from particular difficulty: It’s possible to run into contradictions – situations where the solution is impossible and no forward progress can be made. This sort of thing is endemic to constraint solvers, as the problem space as a whole is [NP-Complete](https://en.wikipedia.org/wiki/NP-completeness).

To illustrate the problem, I used one of Paul Merrell’s samples, “[Escheresque](https://github.com/merrell42/model-synthesis/blob/master/samples/escheresque.txt)” (with permission). Escheresque is deliberately a tricky 3d tileset – many tiles have quite far reaching relationships with each other, and empty space has a low weighting, forcing the scene to be as busy as possible. Thus, contradictions are quite common.

![](../../assets/c458fd64879b7fb2.jpg)

WFC takes an extremely simple approach for dealing with contradictions. If a one occurs, simply **restart **the process from the beginning. As long as contradictions are rare, a solution will be found within a few restarts. Unfortunately, this approach doesn’t scale – as you generate larger and larger outputs, the chances of a contradiction rise, until it’s virtually impossible to get a successful run no matter how many times you restart.

Here’s normal WFC run with the Escheresque sample. As you can see, contradictions are quite common and WFC restarts all the time. The odds of completing the entire 30x30x10 area are tiny.

An alternative approach I use in [Tessera](https://assetstore.unity.com/packages/tools/level-design/tessera-pro-161077), and common to many constraint solvers, is [ backtracking](https://en.wikipedia.org/wiki/Backtracking). Rather than restarting from scratch when a contradiction occurs, backtracking retreats to the last good state, and records additional information so we don’t re-attempt the same thing twice. Backtracking solves the issue of contradictions, but replaces it with the possibility of the algorithm stalling.

Stalling occurs when a partial solution is unsolvable, but the algorithm doesn’t know to backtrack out of it, instead repeatedly exploring variations of the partial solution. For most tilesets, **rabbit holes** such as these are less common than outright contradicitons so you can get more impressive results, but ultimately it still doesn’t scale as a large enough output will encounter one and get stuck.

Enabling backtracking with the Escheresque sample produces better results, but eventually it finds some area that is too tough and gets stuck trying to fix it.

So instead of these, Merrell introduces a different approach, **Modifying In Blocks** (also called modifying in parts). When presented with a large area to generate, instead of approaching it as one large problem, it is broken down into several smaller problems. The output area is partitioned into multiple, overlapping blocks. The blocks are then solved on at a time. If a contradiction is reached, only that block needs restarting, rather than the whole solution. It’s thus a compromise between full restarts and backtracking. The hope is that the restarts will eliminate contradictions, and the blocks are large enough to avoid any rabbit holes, so you can generate extremely large outputs without any growth in overall failure rate.

Run against the Escheresque example, you can see it does successfully generate the entire area, though it did require some careful tuning, and there is quite a lot of error handling not shown in the animaiton.

### Details

Obviously, if you just evaluated each block independently, then you wouldn’t get a coherent output. The whole point of adjacency constraints is that tiles connect to each other. But it turns out there’s a lot of lattitude in exactly how to evaluate the blocks.

The obvious approach would be to partition the entire space into blocks that border on each other, so that every cell belongs to exactly one block. Then you generate the blocks one at a time, starting from one corner, and using the already generated adjacent blocks as input constraints on the shared borders of the current block. That does work fine in a lot of cases.

![](../../assets/fe015fbfc3936918.gif)

But it’s an annoying fact of WFC generation that the constraint solver only considers the tiles inside the generation area as relevant. That means for some tilesets, it can generate outputs that cannot be extended without causing a contradiction. To avoid this, the scheme Paul Merrell uses is slightly different.

When he generates each block, he actually constrains *all* the borders of the block. Some of those constraints come from the blocks previously generated, but for the other sides of the block that are open, he fixes the border at a **known good** set of tiles. The Escheresque sample (above) uses a flat bedrock surface with nothing but air above it, while grass-and-paths tileset uses a solid green background (below).

By fixing all the borders, it ensures that each block is more self contained and easier to extend. The blocks are arranged to overlap each other, so all these fixed borders eventually get overwritten, but it makes success much more likely as we already know there is at least one tile arrangement that works. In fact, in the case that there are too many contradictions / restarts, you can always just give up and fall back to the known good tiles.

![](../../assets/d032165eac3eda49.gif)

## Evaluation

I played around with the Escheresque sample. Like I said, it’s a very fiddly set of tiles to get to generate correctly. I found it was very sensitive to generation order, preferring certain linear scans to min-entropy. Neither WFC with restarts or my own backtracking code stood a chance of scaling to a 30x30x10 output area. Modifying by Blocks, however, was able to go much larger, though it still needed fairly generous block restart settings and error handling.

Performance isn’t too great, as the block overlap means you are doing quite a bit of redundant work. But it does scale slightly better – naive WFC can run into trouble with large outputs as it must repeatedly scan for the minimum entropy cell to generate next, an issue avoided by linear scans.

Overall, I found it’s an interesting tool to add to my toolbox. The large number of tuning parameters, and the need to pre-specify a known good arrangement of tiles, limits how general a technique it is, so I don’t think I’ll add it to Tessera unless there’s specific demand. Nonetheless, I did find some very interesting uses for Modifying in Blocks, which I’ll detail in a later article.

For now, I’d just remind you to credit Dr Merrell with many of the insights needed for constraint based generation, in addition to Maxim Gumin for popularizing it in the form of WFC. I’m especially grateful to him for his help drafting this post and use of his samples.

Hi Boris, thank you for your amazing work. I learn a lot.

I have some questions about those algorithms scope. Does the output generation must be done from the computer or does a user can be involved? Ex: does TownScraper is considered as using WFC?

More details can be found at WFC Explained, or reading my docs on Tessera

Townscaper is using somehting similar to WFC / Model Synthesis yes, see here.

The connection between WFC and constraint solving makes me think of backjumping and clause learning. I guess backjumping wouldn’t be too hard; when you find a conflict, search for the last non-forced choice which lead to that conflict, and make a different decision. I guess clause learning would be trickier, but maybe you could block certain small patterns which always lead to a conflict.

You are quite right Sean. I’ve actually experimented with simple backjumping in https://twitter.com/boris_brave/status/1485006264119799811.

Clause learning is too tricky for me to implement, particularly in an existing library, but I keep my eye out for existing constraint solvers that support it that could be adapted for WFC.