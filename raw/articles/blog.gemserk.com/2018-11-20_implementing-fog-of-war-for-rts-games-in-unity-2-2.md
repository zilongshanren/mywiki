---
title: Implementing Fog of War for RTS games in Unity 2/2
url: https://blog.gemserk.com/2018/11/20/implementing-fog-of-war-for-rts-games-in-unity-2-2/
published: '2018-11-20'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

As I said in the previous [blog post](https://blog.gemserk.com/2018/08/27/implementing-fog-of-war-for-rts-games-in-unity-1-2/), some time ago I started working on a new Fog of War / Vision System solution aiming the following features:

- Being able to render the fog of war of each player at any time, for replays and debug.
- Being able to combine multiple players’ visions for alliances, spectator mode or watching replays.
- Blocking vision by different terrain heights or other elements like bushes.
- Optimized to support 50+ units at the same time in mobile devices at 60FPS.
- It should look similar to modern games like Starcraft 2 and League of Legends (in fact, SC2 is already eight years old, not sure if that is consider a modern game or not :P).

This is an example of what I want:

*Example: fog of war in Starcraft 2*

To simplify a bit writing this article, when I write unit I mean not only units but also structures or anything that could affect the fog of war in the game.

# Logic

First, there is a concept named UnitVision used to represent anything that reveals fog. Here is the data structure:

```
struct UnitVision
{
// A bit mask representing a group of players inside
// the vision system.
int players;
// The range of the vision (in world coordinates)
float range;
// the position (in world coordinates)
vector2 position;
// used for blocking vision
short terrainHeight;
}
```


Normally, a game will have one for each unit but there could be cases where a unit could have more (for example a large unit) or even none.

A bit mask is used to specify a group of players, so for example, if player 0 is 0001 and player1 is 0010, then 0011 means the group formed by player0 and player1. Since it is an int, it supports up to `sizeof(int)`

players.

Most of the time the group would contain only one player but there might be some situations, like a general effect or cinematic, etc, that needs to be seen by all players and one possible solution is to use a unitVision with more than one player.

The `terrainHeight`

field stores the current height of the unit and it is used for blocking vision or not. It normally will be the world terrain’s height on that position if it is a ground unit but there are cases like flying units or special abilities that could change the unit height that should be consider when calculating blocked vision. It is the game’s responsibility to update that field accordingly.

There is another concept named VisionGrid that represents the vision for all the players. Here is the data structure:

```
struct VisionGrid
{
// the width and height of the grid (needed to access the arrays)
int width, height;
// array of size width * height, each entry has an int with the
// bits representing which players have this entry in vision.
int[] values;
// similar to the values but it just stores if a player visited
// that entry at some point in time.
int[] visited;
void SetVisible(i, j, players) {
values[i + j * width] |= players;
visited[i + j * width] |= players;
}
void Clear() {
values.clear(0);
}
bool IsVisible(i, j, players) {
return (values[i + j * width] & players) > 0;
}
bool WasVisible(i, j, players) {
return (visited[i + j * width] & players) > 0;
}
}
```


Note: arrays have a size of width * height.

The bigger the grid is, the slower it gets to calculate vision but it also has more information which could be useful for units’ behaviors or to get better fog rendering.The smaller the grid is, the opposite. A good balance must be defined from the beginning in order to build the game over that decision.

Here is an example of a grid over the game world:

![](../../assets/679a3e97ae9a4e27.png)


Given a grid entry for a world position, the structure stores an int in the *values* array with the data of which players have that position inside vision. For example, if the entry has 0001 stored, it means only the player0 sees that point. If it has 0011, then both the player0 and player1.

This structure also stores when a player revealed fog in the past in the *visited* array which is used mainly for rendering purposes (gray fog) but could also be used by the game logic (to check if a player knows some information for example).

The method `IsVisible(i, j, players)`

will return true if any of the players in the bit mask has the position visible. The method `WasVisible(i, j, players)`

is similar but will check the `visited`

array.

So, for example, if player1 and player2 (0010 and 0100 in bits) are in an alliance, then when player2 wants to know if an enemy is visible to perform an attack, it can call isVisible method with the bitmask for both players 0110.

## Calculating vision

Each time the vision grid is updated, the `values`

array is cleared and recalculated.

Here is a pseudo code of the algorithm:

```
void CalculateVision()
{
visionGrid.Clear()
for each unitVision in world {
for each gridEntry inside unitVision.range {
if (not IsBlocked(gridEntry)) {
// where set visible updates both the values and the
// visited arrays.
grid.SetVisible(gridEntry.i, gridEntry.j,
unitVision.players)
}
}
}
}
```


To iterate over grid entries inside range, it first calculates vision’s position and range in grid coordinates, named gridPosition and gridRange, and then it [draws a filled circle](https://stackoverflow.com/questions/1201200/fast-algorithm-for-drawing-filled-circles) of gridRange radius around gridPosition.

![](../../assets/c056076954d54c9c.png)


## Blocked vision

In order to detect blocked vision, there is another grid of the same size with terrain’s height information. Here is its data structure:

```
struct Terrain {
// the width and height of the grid (needed to access the arrays)
int width, height;
// array of size width * height, has the terrain level of the
// grid entry.
short[] height;
int GetHeight(i, j) {
return height[i + j * width];
}
}
```


Here is an example of how the grid looks over the game:

![](../../assets/88c9ccf868d2310e.png)


Note: that image is handmade as an example, there might be some mistakes.

While iterating through the vision’s grid entries around unitVision’s range, to detect if the entry is visible or not, the system checks if there are no obstacles to the vision’s center. To do that, it [draws a line](http://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#C.23) from the entry’s position to the center’s position.

If all the grid entries in the line are in the same height or below, then the entry is visible. Here is an example where the blue dot represents the entry being calculated and white dots the line to the center.

![](../../assets/9ec57346aa1e8dae.png)


If there is at least one entry in the line that is in a greater height, then the line of sight is blocked. Here is an example where the blue dot represents the entry we want to know if it is visible or not, white dots represents entries in the line in the same height and red dots represents entries in a higher ground.

![](../../assets/17053d9c9897afa5.png)


Once it detects one entry above the vision it doesn’t need to continue drawing the line to the vision center.

Here is a pseudo algorithm:

```
bool IsBlocked()
{
for each entry in line to unitVision.position {
height = terrain.GetHeight(entry.position)
if (height > unitVision.height) {
return true;
}
}
return false;
}
```


## Optimizations

- If an entry was already marked as visible while iterating over all unit visions then there is no need to recalculate it.
- Reduce the size of the grid.
- Update the fog less frequently (In Starcraft there is a delay of about 1 second, I recently noticed while playing, it is an old game).

# Rendering

To render the Fog of War, first I have a small texture of the same size of the grid, named FogTexture, where I write a Color array of the same size using the Texture2D.SetPixels() method.

Each frame, I iterate on each VisionGrid entry and set the corresponding Color to the array using the `values`

and `visited`

arrays. Here is a pseudo algorithm:

```
void Update()
{
for i, j in grid {
colors[i + j * width] = black
if (visionGrid.IsVisible(i, j, activePlayers))
colors[pixel] = white
else if (visionGrid.WasVisible(i, j, activePlayers))
colors[pixel] = grey // this is for previous vision
}
texture.SetPixels(colors)
}
```


The field `activePlayers`

contains a bit mask of players and it is used to render the current fog of those players. It will normally contain just the main player during game but in situations like replay mode, for example, it can change at any time to render different player’s vision.

In the case that two players are in an alliance, a bitmask for both players can be used to render their shared vision.

After filling the FogTexture, it is rendered in a RenderTexture using a Camera with a Post Processing filter used to apply some blur to make it look better. This RenderTexture is four times bigger in order to get a better result when applying the Post Processing effects.

![](../../assets/8d49faec07609bc0.png)


Once I have the RenderTexture, I render it over the game with a custom shader that treats the image as an alpha mask (white is transparent and black is opaque, or red in this case since I don’t need other color channels) similar to how we did with Iron Marines.

Here is how it looks like:

![](../../assets/08837b6bb77ee371.png)


And here is how it looks in the Unity’s Scene View:

![](../../assets/0fa5d9bcfbd18e66.png)


The render process is something like this:

![](../../assets/1fc17bb5641f0830.png)


## Easing

There are some cases when the fog texture changed dramatically from one frame to the other, for example when a new unit appears or when a unit moves to a higher ground.

For those cases, I added easing on the colors array, so each entry in the array transitions in time from the previous state to the new one in order to minimize the change. It was really simple, it added a bit of performance cost when processing the texture pixels but in the end it was so much better than I preferred to pay that extra cost (it can be disabled at any time).

At first I wasn’t sure about writing pixels directly to a texture since I thought it would be slow but, after testing on mobile devices, it is quite fast so it shouldn’t be an issue.

# Unit visibility

To know if a unit is visible or not, the system checks for all the entries where the unit is contained (big units could occupy multiple entries) and if at least one of them is visible then the unit is visible. This check is useful to know if a unit can be attacked for example.

Here is a pseudo code:

```
bool IsVisible(players, unit)
{
// it is a unit from one of the players
if ((unit.players & players) > 0)
return true;
// returns all the entries where the unit is contained
entries = visionGrid.GetEntries(unit.position, unit.size)
for (entry in entries) {
if (visionGrid.IsVisible(entry, players))
return true;
}
return false;
}
```


Which units are visible is related with the fog being rendered so we use the same `activePlayers`

field to check whether to show or hide a unit.

To avoid rendering units I followed a similar approach to what we did for Iron Marines using the GameObject’s layer, so if the unit is visible, the default layer is set to its GameObject and if the unit is not visible, a layer that is culled from the game camera is set.

```
void UpdateVisibles() {
for (unit in units) {
unit.gameObject.layer = IsVisible(activePlayers, unit) : default ? hidden;
}
}
```


# Finally

This is how everything looks working together:

# Conclusion

When simplifying the world in a grid and started thinking in terms of textures, it was easier to apply different kind of image algorithms like drawing a filled circle or a line which were really useful when optimizing. There are even more image operations that could be used for the game logic and rendering.

SC2 has a lot of information in terms of textures, not only the player’s vision, and they provide an [API to access it and it is being used for machine learning experiments.](https://www.youtube.com/watch?time_continue=1&v=-fKUyT14G-8)

I am still working on more features and I plan to try some optimization experiments like using c# job system. I am really excited about that one but I first have to transform my code to make it work. I would love to write about that experiment.

Using a blur effect for the fog texture has some drawbacks like revealing a bit of higher ground when it shouldn’t. I want to research a bit of some other image effect to apply where black color is not modified when blurring but not sure if that is possible or if it is the proper solution. One thing that I want to try though is an upscale technique like the one [used in League of Legends](https://engineering.riotgames.com/news/story-fog-and-war) when creating the fog texture and then reduce the applied blur effect, all of this to try to minimize the issue.

After writing this blog post and having to create some images to explain concepts I believe it could be great to add more debug features like showing the vision or terrain grid itself at any time or showing a line from one point to another to show where the vision is blocked and why, among other stuff. That could be useful at some point.

This blog post was really hard to write since, even though I am familiarized with the logic, it was hard to define the proper concepts to be clear when explaining it. In the end, I feel like I forgot to explain some stuff but I can’t realize exactly what.

As always, I really hope you enjoyed it and it would be great to hear your feedback to improve writing this kind of blog posts.

Thanks for reading!