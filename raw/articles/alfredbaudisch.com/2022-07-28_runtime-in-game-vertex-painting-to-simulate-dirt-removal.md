---
title: Runtime In-Game Vertex Painting to Simulate Dirt Removal
url: https://alfredbaudisch.com/experiments/gamedev/runtime-in-game-vertex-painting-to-simulate-dirt-removal/
published: '2022-07-28'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

The easiest way to accomplish runtime painting of splat maps, in order to dynamically change the blending of textures in-game, is to use vertex colors and then in a shader, get the interpolation alpha amount from the vertex color channel.

Not only it's easy to implement, it's also very cheap, performance wise.

But there's a big downside, it's dependent on the mesh density, which may produce triangulation artifacts.

Notice that this is not the same as a splat map, there's actually no splat map involved, it just simulates splat maps.

## Usages

My intention in order to make this, is because I wanted to simulate dirt being added to a car, and then the dirt can progressively fade out or even be remove by the player, by "washing" the car.

## Implementation

Check this experiment's logs below to see the implementation and examples with both the [Godot Engine](https://alfredbaudisch.com/experiment-logs/in-game-vertex-painting-with-godot-engine-wash-car-effect/) and [Unreal Engine](https://alfredbaudisch.com/experiment-logs/in-game-vertex-painting-with-unreal-engine-wash-car-effect/).