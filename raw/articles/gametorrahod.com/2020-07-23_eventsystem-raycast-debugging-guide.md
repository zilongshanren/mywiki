---
title: EventSystem raycast debugging guide
url: https://gametorrahod.com/eventsystem-raycast-debugging-guide/
author: Sirawat Pitaksarit
published: '2020-07-23'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

Using `EventSystem`

along with `GraphicRaycaster`

, `PhysicsRaycaster`

, or `Physics2DRaycaster`

, and something didn't hit the way you expect it to? Let's dive into the code to debug this.

ps. it's been a long time since the last one! I was away from game development because I got a real, totally unrelated to my passion, boring front end job that actually pays.. lol

## Example problem

![](../../assets/d9b5e5e47f079224.png)

![](../../assets/9d72d8e5f7b7af31.png)

A game about clicking cookie coming into the screen. They are all 2D so I used `Physics2DRaycaster`

. However, when touching any other area that is not the cookie we need to play some effects at that position as well.

Therefore on each cookie `CircleCollider2D`

has been attached along with `IPointerDownHandler`

or `EventHandler`

setup properly. And there is one more `FullScreenTouch`

to handle the miss-touch. This one is a `BoxCollider2D`

.

- I assume you know
`EventTrigger`

only ever trigger one candidate at a time. How that candidate be selected? - There is only one
`EventTrigger`

in the scene. Otherwise you get tons of warning spam. It is a hub to get all kind of raycasters in the scene.

## What is an EventSystem ?

If you are an old timer Unity developer, you may used to "dumbly" place `Input.`

check in some of your `Update`

and if this and that, things happen. Then left click only works in editor, so you add `Input.touches`

check, etc.

Actually `EventSystem`

is not far from that at all. It has `Update`

rapid check that eventually leads to `Input`

like I described. Except that they made it more systematic. I recommend follow into `EventSystem`

code and see its `Update`

for yourself.

- Input initiator is already coded. If left clicking works in editor, then at runtime a touch also initiate the same code.
- What to do is determined by raycasting, which the
`EventSystem`

could collect all casters and gather candidates, and pick the best one. The candidate is further filtered by event type, such as pointer up. - You perform additional checks with a given
`BaseEventData`

or`PointerEventData`

given on your candidates. The input's details are collected in that data. Note that if you aren't satisfied with the input coming it, it is not possible to "let it go" and bubble up to the next candidate. This object had already been picked by the`EventSystem`

. You have to write more custom logic to do that.

## Problem

The plan is to have the cookie take priority.

- However, turns out the cookie didn't get trigger at all, only the
`FullScreenTouch`

one. - More observation, as soon as I disable the full screen box collider the cookie get triggered. This means the cookie collider logic is correct and could trigger, but the bigger box 2d ones always get the priority.
- No, moving the cookies to Z = -0.01 doesn't make them win the selection.

Why?

## Assembling the candidates

It all starts on `RaycastAll`

method in `EventSystem`

when you do something. You can manually invoke it! But if you use your mouse to click, then the invoker is probably `StandardInputModule`

.

```
/// <summary>
/// Raycast into the scene using all configured BaseRaycasters.
/// </summary>
/// <param name="eventData">Current pointer data.</param>
/// <param name="raycastResults">List of 'hits' to populate.</param>
public void RaycastAll(PointerEventData eventData, List<RaycastResult> raycastResults)
{
raycastResults.Clear();
var modules = RaycasterManager.GetRaycasters();
for (int i = 0; i < modules.Count; ++i)
{
var module = modules[i];
if (module == null || !module.IsActive())
continue;
module.Raycast(eventData, raycastResults);
}
raycastResults.Sort(s_RaycastComparer);
}
```


For each module, amount of candidate it could gather depends. In my case, the setting isn't wrong. I have allowed two. So it would get at least the background and one of the cookie provided that cookie can't ever overlap. 2 here is correct. And the raycaster gathered them in.

![](../../assets/56daac99009701b3.png)

But the key is that `raycastResults.Sort`

. **Only the first one of sorted result **will win and get invoked appropriate event handler.

You probably noticed your UI things always win and it didn't let the event go through anything under it. Well, things under it actually are gathered but after the sort the UI ones always win.

## Raycast comparer

This is the destination for your raycast debugging needs. When something doesn't trigger as you expected.

```
private static int RaycastComparer(RaycastResult lhs, RaycastResult rhs)
{
if (lhs.module != rhs.module)
{
var lhsEventCamera = lhs.module.eventCamera;
var rhsEventCamera = rhs.module.eventCamera;
if (lhsEventCamera != null && rhsEventCamera != null && lhsEventCamera.depth != rhsEventCamera.depth)
{
// need to reverse the standard compareTo
if (lhsEventCamera.depth < rhsEventCamera.depth)
return 1;
if (lhsEventCamera.depth == rhsEventCamera.depth)
return 0;
return -1;
}
if (lhs.module.sortOrderPriority != rhs.module.sortOrderPriority)
return rhs.module.sortOrderPriority.CompareTo(lhs.module.sortOrderPriority);
if (lhs.module.renderOrderPriority != rhs.module.renderOrderPriority)
return rhs.module.renderOrderPriority.CompareTo(lhs.module.renderOrderPriority);
}
if (lhs.sortingLayer != rhs.sortingLayer)
{
// Uses the layer value to properly compare the relative order of the layers.
var rid = SortingLayer.GetLayerValueFromID(rhs.sortingLayer);
var lid = SortingLayer.GetLayerValueFromID(lhs.sortingLayer);
return rid.CompareTo(lid);
}
if (lhs.sortingOrder != rhs.sortingOrder)
return rhs.sortingOrder.CompareTo(lhs.sortingOrder);
// comparing depth only makes sense if the two raycast results have the same root canvas (case 912396)
if (lhs.depth != rhs.depth && lhs.module.rootRaycaster == rhs.module.rootRaycaster)
return rhs.depth.CompareTo(lhs.depth);
if (lhs.distance != rhs.distance)
return lhs.distance.CompareTo(rhs.distance);
return lhs.index.CompareTo(rhs.index);
}
```


It is a series of `return`

. That means this is a steps with earlier one having priority over. If we go through each one, surely we could debug anything!

### Event camera

Raycast begins from a camera. Which camera has closer to you depth, then that wins the sort.

### Raycaster kind priority

Then `sortOrderPriority`

and `renderOrderPriority`

which depends on raycaster. This is why `GraphicRaycaster`

for UI always win the sort. But my problem is the battle among `Physics2DRaycaster`

. Let's move to the next one.

### Sorting layer and sorting order

All `GameObject`

has a **layer**.

![](../../assets/3643ad2f80f4b9c2.png)

That could be used on the raycaster so candidates are further reduced. You can combine multiple layers into a mask.

![](../../assets/56daac99009701b3.png)

However "sorting layer" here is not that. It is an event system specific value which is :

```
/// <summary>
/// The SortingLayer of the hit object.
/// </summary>
/// <remarks>
/// For UI.Graphic elements this will be the values from that graphic's Canvas
/// For 3D objects this will always be 0.
/// For 2D objects if a SpriteRenderer is attached to the same object as the hit collider that SpriteRenderer sortingLayerID will be used.
/// </remarks>
```


```
/// <summary>
/// The SortingOrder for the hit object.
/// </summary>
/// <remarks>
/// For Graphic elements this will be the values from that graphics Canvas
/// For 3D objects this will always be 0.
/// For 2D objects if a SpriteRenderer is attached to the same object as the hit collider that SpriteRenderer sortingOrder will be used.
/// </remarks>
```


Now I could see why I am having a problem right now. The wording may not 100% suggest this but I have look at other area in the source code : to qualify for "3D object" you need `SpriteRenderer`

attached. Otherwise your layer/order is 0.

It happen that I thought my invisible full screen box collider didn't need any graphic so I didn't add `SpriteRenderer`

.

My cookies surely are otherwise you can't see them. Let's look at the layer first. (Because the order tied at 0) They are `Important`

.

![](../../assets/5dbcf7b30db7bded.png)

![](../../assets/f5e717fb5aa2b255.png)

My `Important`

happened to be behind Unity's `Default`

which I think defines a 0 in integer value. So that's why the cookie didn't get clicked!

Moving the cookies over `Default`

is no good either since that will affect rendering.

Solution : Add `SpriteRenderer`

to my box 2D collider though I didn't want any graphics, then set layer to maybe `NotImportant`

so it loses in sorting. At least I know how to debug this now.

My problem is solved but there are more to go.

### Depth

This is different from camera depth earlier. It seems to be for equal distance graphics to win over each other. Which means the UGUI system. They are often on the same plane. Look at this comment :

```
/// <summary>
/// Absolute depth of the graphic, used by rendering and events -- lowest to highest.
/// </summary>
/// <example>
/// The depth is relative to the first root canvas.
///
/// Canvas
/// Graphic - 1
/// Graphic - 2
/// Nested Canvas
/// Graphic - 3
/// Graphic - 4
/// Graphic - 5
///
/// This value is used to determine draw and event ordering.
/// </example>
```


This is why dragging around UGUI object in the Hierarchy tree has effect in both draw order sorting and also winning over in raycasting. This won't applied to non-UGUI objects.

### Distance

Finally, is it surprising that distance comes the last? This is why I moving the cookies a bit closer to the camera doesn't work out because there are many other criteria that came before.