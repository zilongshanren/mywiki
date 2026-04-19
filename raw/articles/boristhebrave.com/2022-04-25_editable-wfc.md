---
title: Editable WFC
url: https://www.boristhebrave.com/2022/04/25/editable-wfc/
author: Boris
published: '2022-04-25'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

When I spoke about [autotiling](https://www.boristhebrave.com/2021/09/12/beyond-basic-autotiling/), I briefly touched on how it’s possible to use [Wave Function Collapse](https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/) (or other [constraint based generators](https://www.boristhebrave.com/2021/10/31/constraint-based-tile-generators/)) as a form of autotiling, i.e. user-directed editing of tilemaps.

I’ve usually referred to this technique as “**editable WFC**“. It’s a combination of autotiling and WFC, and contains the best of both:

- Being an autotiler, it allows users to easily and interactively make changes to an existing level.
- Being constraint based, it automatically ensures that those changes are consistent with the predefined rules of the constraints, potentially making further changes to the level to make it fit

This is different from most other autotilers, which either require manual configuration of patterns used to enforce good behaviour, hidden layers, or come with more stringent requirements on what tiles are available.

The major example of Editable WFC is [Townscaper](https://store.steampowered.com/app/1291340/Townscaper/). In this toy, you can click to add a block to the world, not dissimilar from a variety of [marching cube](https://www.boristhebrave.com/2018/04/15/marching-cubes-tutorial/) based tools ([like Brick Block](https://oskarstalberg.com/game/house/index.html)). I think [Spirit and Stone](https://store.steampowered.com/app/1932290/Spirit__Stone/) [works similarly](https://twitter.com/GardenGateSeth/status/1516476493697716225), though I’ve not got many details.

But a single click doesn’t always lead to a simple change. Sometimes, the rules of Townscaper mean that a small change can have far reaching effects.

Despite some explanation from Oskar, I still don’t precisely understand how Townscaper does this. Instead, I invented my own technique which is **more complex, but more general**. It’s available as an enhancement to [DeBroglie](https://boristhebrave.github.io/DeBroglie/), my open source C# library for constraint based generation.

It’s a cool technique, but I think it is rather complex – I urge you to review other autotiling methods and marching cubes first to make sure they do not fit your need.

Table of Contents

Here’s a few gifs of it working. I’m afraid I don’t have the time to make an interactive example.

Note how in several of these clicks, multiple tiles are changed. That’s because the algorithm has determined that the that tile is not consistent with the desired change.

The basic operation for WFC and other constraint based generators like Model Synthesis is the following:

Initialize a per-cell list of possible tiles.

Then in a loop:

**Pick**a currently unresolved cell**Select**a particular tile for that cell, based on the list of possible tiles**Propagate**any consequences of that tile choice, potentially removing tiles as possibilities for nearby cells.

(see [WFC Explained](https://www.boristhebrave.com/2020/04/13/wave-function-collapse-explained/) for a full description of propagation)

You can get a lot of different affects with different pick/select algorithms. WFC, for example, uses min-entropy as the pick heuristic, while Model Synthesis uses a linear scan.

We’re going to use some special pick/select heuristics to achieve what we want.

The way my implementation of editable WFC works is that we do a full generation of the level from scratch, with the previous level used as guidance for the new generation. So there’s a few key changes from normal generation.:

- There is one extra constraint, corresponding to the users input of which tile to paint.
- We pick cells filtered to a
*dirty list*, instead of the whole grid. - We guide the new generation to match the previous level as much as possible
*(optional)*We stop the generation early, when we can be sure that all the remaining cells can just be copied from the previous level verbatim.

As I covered in [WFC Tips and Tricks](https://www.boristhebrave.com/2020/02/08/wave-function-collapse-tips-and-tricks/), it’s extremely easy to add support for constraints in the form of forcing a particular cell to contain a particular tile. You just need to remove all other tiles from that’s cells list of possible tiles, before starting the main WFC loop.

We do this for the users input. I.e. if they, say, click to place a wall, we remove all non-wall tiles from that cells possible list. You can also support more complicated edit instructions by doing a different set of constraints.

Instead of the usual min-entropy heuristic for picking which cell to evaluate next, we use a **dirty cell heuristic**. A cell is considered dirty if has not been resolved, and the corresponding tile in the previous level is not in the possible list. The dirty cell heuristic simply picks a dirty cell with minimal entropy.

As we placed an extra constraint at the start corresponding to the desired edit, we start with at least one dirty cell. When we resolve a cell, we do propagation, which affects the possible tile lists for nearby cells, potentially making them dirty.

If there are no dirty cells, then we can terminate generation early. All remaining cells can be resolved by copying the corresponding tile from the previous level. This is because the lack of dirty cells indicates that the tiles chosen so far are fully consistent with that choice.

In normal WFC, after picking a cell, we’d populate that cell with a tile picked at random. That’s no good in this case. If we did that, the new generation would have nothing in common with the previous level.

Instead, we want a heuristic that guides the new generation to resemble the previous level as much as possible. That will drive the the dirty cell count lower and lower, until there are none left. Unfortunately, I don’t think this is a one size fits all heuristic.

In Townscaper, the select heuristic is simply a predefined priority list of tiles – it always chooses the first tile it finds that is appropriate for a given location. As this is fully deterministic, it naturally causes the new level to have the same tiles as the previous level. But full determinism isn’t appropriate for all games.

In my demos, I instead use a **similarity heuristic**. We consider all possible tiles, and pick the one that is most similar to the corresponding tile in the previous level. That’s usually the tile itself, but if not that one, it finds as close a substitute as possible based on the tile adjacency information. If there’s a tie, a random choice is made.

This isn’t a perfect heuristic – if the tileset is sufficiently complicated, then there may indeed be no similarity at all between the possible tiles and the previous one.

[Tiled](https://www.mapeditor.org/) has something similar, but goes a step further. It rates tiles based on how easy it is to transition from one to another, which helps with more complicated tile sets.

As mentioned, once there are no dirty tiles, we can stop, just copying all remaining data from the previous level. If your solver invovles exotic constraints, this may not be a safe operation.

Because we’re aiming to change only a small set of tiles in a much larger map, it’s important to bear in mind performance. Stopping early helps, but if there are heavy fix costs associated with starting the generator, then it can still be expensive. But we need the whole map to be available, as it’s often impossible to know ahead of time which cells are going to change.

Fortunately, most of the datastructures in WFC can be constructed lazily. That means they start empty (or with a sentinel value), and are initiailzed the first time they are actually used. That means you don’t pay much cost for cells that are never touched.

I also found this trick useful for the similarity metric – computing the similarity of all tiles vs each other is a lot of operations that are probably unneeded.

So how do you use it in [DeBroglie](https://boristhebrave.github.io/DeBroglie/)? You’ll need the version from the master branch, then set appropriate properties on `TilePropagatorOptions`

when constructing your `TilePropagator`

.

Setting up the pick heuristic is fairly straightforward. In `TilePropagatorOptions`

, you set `IndexPickerType`

to `Dirty`

, and supply the previous level as an array in the `CleanTiles`

field.

Setting the select heuristic is more complcated. DeBroglie doesn’t come with a similarity metric as tiles are opaque to the library. You need to specify it yourself, and in quite a weird format expected by `TilePickerType.ArrayPriority`

.

A WeightSet stores a per-tile weight information. It can also include “priority” information. When doing a random weighted sample, only tiles of the highest priority are considered. Equivalently, you can imagine the true weight of a tile to be equal to *priority × N + weight*, where N is an incredibly large number.

Given a similarity metric, we can create a weight set that represents “prefer tiles similar to tile X” by filling the priority of tile Y as the similarity between X and Y. The weight can be set as usual as it serves a randomized tiebreaker.

Once we have constructed weightsets for “similarity to X” for each tile X, we need to tell DeBroglie to use different weight sets for different cells. That means supply a list of weight sets, each numbered, and then an array that stores per-cell which weight set to use. These are the `WeightSets`

and `WeightSetByIndex `

fields respectively.

You can step/run the TilePropagator as usual and it should enter state `Decided`

, but due to the early stopping, you may still find some individual cells are `Undecided`

. When using the output, these cells should be copied from the previous level.

If you’ve played Townscaper, you probably noticed that it behaves quite differently to how I’ve described.

Some of those differences you notice are actually unrelated to differences in how we handle editing, and are more to do with how the game is configured:

- Deterministic Tiles – Townscaper uses deterministic tile choices, which simplifies a lot of details, particularly the need for a tile similarity metric.
- Dual tiles – Edits in townscaper actually occur on the corners of tiles, not the tiles itself. Thus one click must edit at least the 8 tiles that share that vertex. This is more complicated, but isn’t really a fundamental change algorithmically.

But the biggest difference is Townscaper uses what I’ve been calling ** driven WFC**. When a user clicks, they are not

*directly*affecting the tiles drawn at all. Instead, they are affecting some hidden layers that store solidity and color. Those arrays then become constraints when the WFC is run itself.

Thus the actual data edited is never touched by a generator, instead, the game just needs to recompute the processed result of that data. By contrast, the editing technique I described works more like an actual paint program – the source data is the set of tiles making up the level, and we mutate it directly with the generator. This complicates things, but works in a wider variety of cases.

I’d strongly consider the Townscaper approach if your game supports it. Oskar has many tweets giving some details on how it works.

Well, I’ve descibed my implementation, but I still feel a bit unsatisfied. It’s a complicated process, partly as I had to retrofit it into an existing library, and the quality and performance leave something to be desired.

But I sitll there are still uses for it. The more complicated a tileset, the harder it will be to write a more convential autotiling system that can keep up with it. But this should scale fairly well.

I hope to return to this later and see if I can simplify either the approach or explanation into something reasonable.