---
title: Generating Shapes Using UV in Godot Shaders | Tutorial
url: http://bun3d.com/tutorials/uv/godot_generating_shapes/
author: Binbun
published: '2026-03-07'
source_blog: Binbun3D
source_site: https://bun3d.com/
category: graphics
fetched: '2026-04-19'
---

In the [first part](http://bun3d.com/godot_uv_basics/#shapes) I briefly covered using `UV`

to get a gradient, but this tutorial will focus on generating more stuff!
We’ll start with the humble circle.

## Circle[#](http://bun3d.com#circle)

For ages humans have obsessed over drawing a * perfect circle*. We don’t have to, because it’s pretty simple!
We start out with a radial gradient.

```
void fragment() {
vec2 uv = UV;
uv = uv * 2.0 - 1.0;
float gradient = length(uv);
COLOR.rgb = vec3(gradient);
}
```


![radial_gradient](../../assets/c356e6205d3aa9e9.png)

`uv = uv * 2.0 - 1.0;`

pretty much centers our`uv`

not too unlike in the[scaling tutorial](http://bun3d.com/godot_manipulating_uvs/#scaling-around-a-point).- In other words we map
`x`

and`y`

of`uv`

to a range from**-1 to 1**when normally they range from**0 to 1**

- In other words we map
`float gradient = length(uv)`

we get the length our`uv`

- In other words the distance to
`(0.0, 0.0)`


- In other words the distance to

So our `gradient`

value here represents the distance to the center. Near the center it’s darker, because the distance is shorter.
Next we can use `step()`

to get a hard edge.

```
void fragment() {
vec2 uv = UV;
uv = uv * 2.0 - 1.0;
float gradient = length(uv);
gradient = step(gradient, 0.8)
COLOR.rgb = vec3(gradient);
}
```


![radial_gradient_stepped](../../assets/4313369f75b003cf.png)

I ain’t a mathematician so I can’t explain what the step function does behind the scenes. For us it’s just a shorter version of doing this:

```
void fragment() {
vec2 uv = UV;
uv = uv * 2.0 - 1.0;
float gradient = length(uv);
if(gradient > 0.8){
gradient = 0.0;
} else {
gradient = 1.0;
}
COLOR.rgb = vec3(gradient);
}
```


## Square[#](http://bun3d.com#square)

The ColorRect is already a square we don’t need to do anything

No I’m just kidding. Similarly to circles, we can get a square gradient which can be used for different things.

```
void fragment() {
vec2 uv = UV;
uv = uv * 2.0 - 1.0;
float gradient = max(abs(uv.x), abs(uv.y));
COLOR.rgb = vec3(gradient);
}
```


![square_gradient](../../assets/2e92a159e382bfd0.png)

`abs()`

gets the absolute value of the given value.- “Absolute value” here means its distance from 0.0. So it just turns negative values into positives.
- Because we map our
`uv`

value to a range from**-1 to 1**, using`abs()`

makes our gradient value go from**1 to 0 to 1** `max()`

compares two values and returns the one that’s greater.


![square_gradient_abs](../../assets/77462b0ceff16f7b.png)

`min()`

which returns the lesser value.If you’ve used any graphics/drawing programs you might’ve come across **Lighten** and **Darken** blend modes. They’re actually just `max()`

and `min()`

.

## Conclusion[#](http://bun3d.com#conclusion)

Yeah we can make some shapes for sure. By this time I’ve been writing for hours on end. I might update this part later with more shapes. On the next post we’ll cover some interesting stuff with different coordinate spaces, so if you’re interested drop me a follow on my socials to stay updated