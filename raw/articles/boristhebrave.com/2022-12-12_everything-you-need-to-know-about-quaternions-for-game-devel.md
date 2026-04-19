---
title: Everything you need to know about Quaternions for Game Development
url: https://www.boristhebrave.com/2022/12/12/everything-you-need-to-know-about-quaternions-for-game-development/
author: Boris
published: '2022-12-12'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

They represent 3d rotations.

That’s it, that’s the article.

…ok, obviously there is a bit more to say. But it’s basically true. [Quaternions](https://en.wikipedia.org/wiki/Quaternion) are fairly advanced mathematical objects, with all sorts of deep theory behind them. And absolutely none of it is relevant to game development.

You don’t need to know the theory, because what you actually need is how to **use** them. And because they represent rotations, how to use them is best explained in terms of rotations. All the maths of how they work is covered by library functions that have nice intuitive meanings (unlike quaternions themselves). I recommend thinking of quaternions the same way as 3×3 rotation matrices, another way of representing 3d rotations. But matrices use 9 numbers, and quaternions just 4 numbers, which makes them more efficient to work with.

## Multiplication

The most common operation with quaternions is called **multiplication **which simply means rotating something by the rotation. So `q * v`

rotates the vector `v`

by the rotation represented by quaternion `q`

. And similarly `q1 * q2`

rotates `q2`

by `q1`

, giving a new quaternion which represents rotating by `q2`

, then `q1`

.

A lot of things you want to do with rotations boil down to quaternion multiplication. For example, if you are used to using [Euler angles](https://en.wikipedia.org/wiki/Euler_angles), you might write code like:

`object.eulerAngles.x += myAngle`


Meaning that you want to rotate the object by myAngle around the x-axis. But you’ll find that code often **behaves weirdly** if the object is already rotated in the other axes. That’s because the x-axis rotation is applied before the y-axis rotation, but *after* the z-axis rotation. Instead, why not try:

`object.rotation = Quaternion.AngleAxis(myAngle, Vector3.right) * object.rotation`


*(here I’m using Unity’s methods for quaternions, but all the methods I’ll mention are widely available and short enough to be ported to new languages easily)*

This makes it clear that we want a rotation that starts with the existing rotation, then applies our new rotation afterwards. So the new rotation will always be around the global x-axis. Or you could do:

`object.rotation = object.rotation * Quaternion.AngleAxis(myAngle, Vector3.right) `


This first rotates about the x-axis, then does the original object rotation. Effectively, this rotates the object around its *local* x-axis.

## Other operations

Beyond multiplication, there’s only a handful of rotation operations you’ll ever need. These all have intuitive geometrical meanings, as long as you don’t try to understand the theory of how they are implemented.

| Function | Plain Language |
|---|---|
| q * v | Rotate vector v by quaternion q |
| q1 * q2 | Combine quaternions q1 and q2 giving a new quaternion. NB: `(q1 * q2) * v == q1 * (q2 * v)` |
| q.
|

i.e.

`q * q.Inverse == Quaternion.identity`

[Angle](https://docs.unity3d.com/ScriptReference/Quaternion.Angle.html)(q1, q2)[Slerp](https://docs.unity3d.com/ScriptReference/Quaternion.Slerp.html)(q1, q2, blendFactor)(typically used for animation)

[identity](https://docs.unity3d.com/ScriptReference/Quaternion-identity.html)[FromToRotation](https://docs.unity3d.com/ScriptReference/Quaternion.FromToRotation.html)(from, to)`from`

to point towards the vector `to`

.[LookRotation](https://docs.unity3d.com/ScriptReference/Quaternion.LookRotation.html)(forward, up)* rotates the vector (0, 0, 1) to point towards

`forward`

* rotates the vector (0, 1, 0) as close as possible to

`up`

[AngleAxis](https://docs.unity3d.com/ScriptReference/Quaternion.AngleAxis.html)(angle, axis)[ToAngleAxis](https://docs.unity3d.com/ScriptReference/Quaternion.ToAngleAxis.html)## Example

Suppose we want to make a camera slowly turn to point towards the player.

We could use LookRotation to figure out the desired rotation, then Slerp to move the current rotation a bit towards it each frame.

```
void Update()
{
var towardsPlayer = player.position - camera.position;
var desiredRotation = Quaternion.LookRotation(towardsPlayer, Vector3.up);
var currentRotation = camera.rotation;
var updatedRotation = Quaternion.Slerp(
currentRotation,
desiredRotation,
rotationSpeed * Time.deltaTime);
camera.rotation = updatedRotation;
}
```


As you can see, this code is perfectly comprehensible and doesn’t involve any maths.

## Further reading

You want to read more? I just said you don’t need to know it! Oh, well I suppose you can try [this video](https://www.youtube.com/watch?v=zjMuIxRvygQ). Or maybe you could learn about [Geometric Algebra](https://www.youtube.com/watch?v=Idlv83CxP-8) and do away with quaternions for good.