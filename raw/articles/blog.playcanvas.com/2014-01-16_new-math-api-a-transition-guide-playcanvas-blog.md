---
title: 'New Math API: A Transition Guide | PlayCanvas Blog'
url: https://blog.playcanvas.com/new-math-api-a-transition-guide
author: Will Eastcott
published: '2014-01-16'
source_blog: PlayCanvas
source_site: https://blog.playcanvas.com
category: graphics
fetched: '2026-04-13'
---

Yesterday, we announced an imminent update to the PlayCanvas Math API. It's a rare event that we introduce breaking changes and we only do it because we're certain it's going to help you be much more productive. So what have we changed?

Previously, we had a Math API which consisted of static functions that operated on arrays (JavaScript typed arrays, to be specific). It was fast - very fast - but this came at the expense of a developer-friendly interface. Therefore, we have written a brand new Math API that is object-oriented and far crisper to write against. Here's an example of how things were:

`// Generate a vector from a to b rescaled to be 10 units long`

var a = pc.math.vec3.create(1, 2, 3);

var b = pc.math.vec3.create(4, 5, 6);

var result = pc.math.vec3.create();

pc.math.vec3.sub(b, a, result);

pc.math.vec3.normalize(result, result);

pc.math.vec3.scale(result, 10, result);



A bit verbose! Here's how things look now:

`// Generate a vector from a to b rescaled to be 10 units long`

var a = new pc.Vec3(1, 2, 3);

var b = new pc.Vec3(4, 5, 6);

var result = new pc.Vec3();

result.sub2(b, a).normalize().scale(10);



Much better! As you can see, you can now chain math functions together to apply lots of operations in order.

So what if you've already written PlayCanvas script code against the old API? How do you upgrade it? Here's a brief guide.

### Accessing Math Object Elements[](https://blog.playcanvas.com#accessing-math-object-elements)

The old way:

`var x = vector[0];`

var y = vector[1];

var z = vector[2];



The new way:

`var x = vector.x;`

var y = vector.y;

var z = vector.z;



### Creating Math Objects[](https://blog.playcanvas.com#creating-math-objects)

The old way:

`var v2 = pc.math.vec2.create(1, 2);`

var v3 = pc.math.vec3.create(1, 2, 3);

var v4 = pc.math.vec4.create(1, 2, 3, 4);

var m4 = pc.math.mat4.create();

var q1 = pc.math.quat.create(0, 0, 0, 1);



The new way:

`var v2 = new pc.Vec2(1, 2);`

var v3 = new pc.Vec3(1, 2, 3);

var v4 = new pc.Vec4(1, 2, 3, 4);

var m4 = new pc.Mat4();

var q1 = new pc.Quat(0, 0, 0, 1);



### Math Object Constants[](https://blog.playcanvas.com#math-object-constants)

The old way:

`var zeroVec = pc.math.vec3.zero;`



The new way:

`var zeroVec = pc.Vec3.ZERO;`



### API Reference Pages[](https://blog.playcanvas.com#api-reference-pages)

We strongly urge you to check out the API reference pages for the new API. We've worked hard to ensure every function has been lovingly documented (including sample code). If you spot any mistakes, have feedback or need any help whatsoever, [do let us know](https://forum.playcanvas.com)!

Reference pages can be found here:

- A 2-dimensional vector`pc.Vec2`

- A 3-dimensional vector`pc.Vec3`

- A 4-dimensional vector`pc.Vec4`

- A 4x4 matrix`pc.Mat4`

- A quaternion`pc.Quat`


### Unrelated Changes[](https://blog.playcanvas.com#unrelated-changes)

Since we have made such sweeping API changes, we have also taken the opportunity to remove some deprecated functions. The following are no longer in the engine:

`pc.fw.RigidBodyComponent#get/setLinearVelocity`

- useproperty`linearVelocity`

`pc.fw.RigidBodyComponent#get/setAngularVelocity`

- useproperty`angularVelocity`

`pc.fw.RigidBodyComponent#get/setLinearFactor`

- useproperty`linearFactor`

`pc.fw.RigidBodyComponent#get/setAngularFactor`

- useproperty`angularFactor`

`pc.scene.Scene#get/setGlobalAmbient`

- useproperty`ambientLight`


We hope you like the new interface!