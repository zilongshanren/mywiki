---
title: Elementary Cellular Automaton, Rule 126
url: https://www.4rknova.com/blog/2019/03/18/elementary-cell-auto-rule-126
author: Nikolaos Papadopoulos
published: '2019-03-18'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Theory

Elementary cellular automata are defined in a single dimension of quantized space and control a binary state for each cell. They are usually visualized in 2D by mapping the second axis to time. In this context each quantized unit of time corresponds to an evolution of the previous state of the automaton based on a rule.

A rule defines how each cell evolves based on the current state of its nearest neighbours and itself. For elementary automata, there is a fixed set of 8 transitions. These transitions are encoded in 8 bits. Those 8 bits are what we refer to as the rule.

A rule borrows its unique name by its numerical byte value. Each bit encodes the final state of the transitioning cell depending on a specific input state. That input state is defined by the index of the bit encoded in binary. As the maximum index has a value of 7, we need 3 bits to encode that value. These three bits encode the state of the current cell as well as its left and right neighbours.

```
left self right
\ | /
\ | /
\ | /
bit index 7: 1 1 1 the old state is 1
bit 7 value: 0 the new state is 0
```


Putting all this together, rule 126 is illustrated below:

```
111 110 101 100 011 010 001 000
126 = 0 1 1 1 1 1 1 0 in binary
```


# Implementation

Below is sample code for rule 126, implemented in a GLSL fragment shader.

```
#define D vec2(400,128)
#define S(p,d) (texture(iChannel0, (p + d) / D).r > 0.5)
void mainImage(out vec4 c, in vec2 p)
{
// Grid coordinates
vec2 gc = floor(D * p.xy / iResolution.xy) + 0.5;
// Initialization
if (iFrame == 1 && distance(gc, vec2(D.x*0.5, D.y - 1.)) < 1.) {
c.x = 1.;
return;
}
c.x = S(gc,vec2(0)) ? 1. : 0.; // Restore state
// Every step (in this instance step = frame) calculate
// the next line.
float t = min((D.y - (float(iFrame))), D.y);
// This is a 1D automaton. To visualize it in 2D we
// choose time as our second dimension. Each successive
// line in the grid is the evolution of the previous
// population in the line above.
if (gc.y - .5 == t) {
bool pl = S(gc, vec2(-1,1))
, pc = S(gc, vec2( 0,1))
, pr = S(gc, vec2( 1,1));
// Rule 126. Essentially, a Sierpinski triangle.
c.x = (pl == pc && pc == pr ? 0.0 : 1.0);
}
}
```