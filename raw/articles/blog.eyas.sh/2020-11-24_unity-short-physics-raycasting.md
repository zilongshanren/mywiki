---
title: 'Unity Short: Physics Raycasting'
url: https://blog.eyas.sh/2020/11/unity-for-engineers-pt10-2-raycasting/
author: Eyas Sharaiha
published: '2020-11-24'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Continuing the “shorts” week in the
[Unity for Software Engineers](https://blog.eyas.sh/tag/unity-for-software-engineers) series (now
updated and [available as a book](https://leanpub.com/unity-for-engineers)),
today we’ll be discussing Unity’s **Physics Raycasting**. As a reminder, this
week is packaged as a series of short-form overviews, introducing readers to the
*breadth* of the Unity toolkit.

Raycasting is Unity’s way of checking collisions between objects in the scene
and an invisible [ray](https://en.wikipedia.org/wiki/Line_%28geometry%29#Ray)
with a given geometry. Raycasting is used in a myriad of ways. Some examples:

-
Implementing gunshots or laser guns as rays with instantaneous damage, rather than modeling them as a projectile with a finite speed.

Raycasting can check if a given shot hits an enemy or target.

-
Manual kinematic controllers. While realistic physics is sometimes fun, many platformers and first-person games manually define and fine-tune a character’s motion and collision behavior.

Raycasting can, for example, check if the player is grounded (by casting a ray from the bottom of the player downwards) and can move, or if the player is colliding with walls, etc.

-
Translating Screen-Space pointer placement to World-Space positions.

In many games, your pointing device can place items in the world or give commands to units. Translating your pointer’s position (2D, in screen space) to a world position happens by casting a ray from the camera plane forwards.

-
Enemy AI.

For example, an enemy might cast a ray from its eye level to the player to determine if the player is currently visible to the enemy.


## How to Raycast

Let’s start with the basics. Raycasting is done in C# through the static
`Physics.Raycast()`

method in the `UnityEngine`

namespace. `Raycast`

has plenty
of overloads, but the inputs of the method can be summarized as:

- A
**Ray**. Provided either as a`UnityEngine.Ray`

object, or two parameters:`Vector3 position`

and`Vector3 direction`

.[1](https://blog.eyas.sh#user-content-fn-1) - Optionally, a
**maxDistance**value, limiting the distance along the ray that collisions will be checked. When absent, this is inferred as infinity. - Optionally, a
**layerMask**integer, restricting*which*objects to be included in the raycast.Layer Masks were briefly described in ”[2](https://blog.eyas.sh#user-content-fn-2)[Understanding Unity Engine Objects](https://blog.eyas.sh/2020/10/unity-for-engineers-pt5-object-component#gameobject)”. - Optionally, a
enum, determining whether`QueryTriggerInteraction`

should be included in a raycast. By default, this takes the value of*trigger*colliders`Physics.queriesHitTriggers`

.

A call for `Physics.Raycast`

returns:

- A boolean, whether the ray collided with anything.
- Usually, a
struct determining where a collision happened, its normal, distance, corresponding collider, and other details.`RaycastHit`


In addition, `Physics.RaycastAll()`

allows users to find *all* collisions along
a Ray and a distance. Simple versions of this method return a `RaycastHit[]`

array with information about each hit. These overloads will therefore allocate
an array on the heap each time the method is called. If you are calling this
method frequently (e.g., in `Update()`

or `FixedUpdate()`

), consider using
`RaycastNonAlloc`

, which takes in a pre-allocated `RaycastHit[]`

array (that you
can reuse between frames) and returns the number of hits it populated in the
array.

Raycasting is the most common of physics collision simulation functions, but
note that the `Physics`

static class also provides `BoxCast`

, `CapsuleCast`

, and
`SphereCast`

variations similar to `Raycast`

.

## Pointer Raycasting

If you have a reference to a `Camera`

, you can translate a mouse position on the
screen to a `Ray`

using `Camera.ScreenPointToRay(Vector3)`

. Note that while this
function takes in a `Vector3`

, the `z`

value is ignored. A `Vector2`

is
implicitly converted to a `Vector3`

by copying the `x`

and `y`

values and
setting `z`

to 0.

Given
[this week’s example NavMeshMover](https://blog.eyas.sh/2020/11/unity-for-engineers-pt10-1-pathfinding),
we can create a rudimentary player controller as follows:

```
using UnityEngine;
using UnityEngine.InputSystem;
[RequireComponent(typeof(NavMeshMover))]
public class RaycastMover : MonoBehaviour
{
private NavMeshMover _mover;
private Camera _camera;
private void Awake()
{
_mover = GetComponent<NavMeshMover>();
_camera = Camera.main;
}
private void Update()
{
var mouse = Mouse.current;
if (mouse == null) return;
if (mouse.leftButton.isPressed) // alternatively: wasPressedThisFrame
{
Vector2 screenPosition = mouse.position.ReadValue();
Ray ray = _camera.ScreenPointToRay(screenPosition);
if (Physics.Raycast(ray, out RaycastHit hit))
{
_mover.NavigateTo(hit.point);
}
}
}
}
```


[As described in the InputSystem article](https://blog.eyas.sh/2020/10/unity-for-engineers-pt3-input-system/),
a cleaner input-handling implementation involves defining an Input Action and a
public callback `public void OnMove(InputAction.CallbackContext input)`

via a
Player Input Controller.

## Simple Enemy AI Example

Here’s a simplified function in an Enemy AI that determines if it sees a suspicious target:

```
private Vector3? DetermineSuspectedPosition_Vision()
{
Vector3 lookStart = EyeLevelPosition();
Vector3 lookForward = EyeLevelForward();
Transform target = FindClosestTarget();
float distance = Vector3.Distance(lookStart, target.position);
if (distance > _maxChaseRange) return null;
float angle = Vector3.Angle(target.position - lookStart, lookForward);
if (Mathf.Abs(angle * 2) > _maxFieldOfView) return null;
if (!Physics.Raycast(
lookStart,
target.position - lookStart,
out var hit,
_maxChaseRange,
~SeeThrough)) return null;
if (hit.transform != target) return null;
return target.position;
}
```


## Collider Raycasting

Every `Collider`

component implements a raycasting method:

```
public bool Raycast(Ray ray, out RaycastHit hitInfo, float maxDistance);
```


This allows you to cast an *entire collider* along a ray. This is helpful when
checking for collisions where a ray, box, sphere, or capsule aren’t enough or
when simulating the collisions of a specific mesh.

## Closing Thoughts

I tried to demonstrate the breadth of raycasting use cases in Unity. It is a
generally cheap 3 method of allowing objects to reason about their spatial
relationship to the rest of the scene.

## Footnotes

-
The

`direction`

`Vector3`

is a*direction vector*. You can think of the ray it represents as starting in`position`

and extending through`position + direction`

.[↩](https://blog.eyas.sh#user-content-fnref-1) -
For example, a “UI” layer might be excluded from a raycast to determine gun collisions. Similarly, see-through objects such as glass windows can be grouped into a “See-through” layer and excluded from raycasts by enemy AI when determining its vision.

[↩](https://blog.eyas.sh#user-content-fnref-2) -
As long as you’re not using variants of

`RaycastAll`

that allocate on every call.[↩](https://blog.eyas.sh#user-content-fnref-3)