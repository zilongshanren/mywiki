---
title: '153: Shader Programming with The Book of Shaders and Godot'
url: https://alfredbaudisch.com/experiments/gamedev/153-shader-programming-with-the-book-of-shaders/
published: '2022-01-07'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

**Shader programming is one of the things I have never touched in my life. And I always saw whoever makes shaders as some mythical programmer.**

Since Monday I've been studying Shaders from scratch using [The Book of Shaders](https://thebookofshaders.com/) and the [Godot Engine documentation](https://docs.godotengine.org/en/stable/tutorials/shading/index.html).

Shader programming is:

- It's hard.
- It requires a lot of low level Math knowledge.
- It's fulfilling as soon you figure things out.

## My First Shader Ever

The result is a pulsating gradient.

```
shader_type canvas_item;
void fragment() {
COLOR = vec4(UV.x, UV.y, abs(sin(TIME)), 1.0);
}
```


## Fence Problem

I spent the past 3 days cracking my head trying to understand chapter 5 – Shaping Functions, specifically the "fence problem".

I finally understood it today and I can now even create variations of it. GLSL `ste`

p and `smoothstep`

really made me think and research a lot.

## Variations of the Fence Problem with Godot

### Diagonals

`smoothstep(0.0, 0.01, abs(0.5-x + 0.5-y));`


With this, we get exactly where they cut in the middle: 0.5-x + 0.5-y

Now wherever there was green, there's black, because 1.0 (ok, green) has been changed to 0 (black):

![](../../assets/d5cfaff0ba4c7cf7.png)


`return 1.0-smoothstep(0.0, 0.01, abs(0.5-x + 0.5-y));`


Diagonal with `step`

:

`return 1.0 - step(0.01, abs(1.0-st.y - st.x));`


#### Alternative easier to understand

`return smoothstep(0.01, 0.0, abs(1.0-st.y - st.x));`

- y is being subtracted by 1 due to godot's inverse Y, outside Godot:
`return smoothstep(0.01, 0.0, abs(st.y - st.x));`


**Notice that edge2 is 0.0, which means exactly where y & x meet, i.e**:

- y == x, y – x = 0, when x >= edge2, return 1.0

### Verticals

`return smoothstep(0.0, 0.01, abs(0.5-x));`


`return 1.0-smoothstep(0.0, 0.01, abs(0.5-x));`


### Horizontals

`return 1.0-smoothstep(0.0, 0.01, abs(0.5-y));`


### Crosshair

![](../../assets/ec95b7cf4b4e168b.png)


`return 1.0-smoothstep(0.0, 0.01, abs(0.5-y)) + 1.0-smoothstep(0.0, 0.01, abs(0.5-x));`