---
title: Lindenmayer Systems
url: https://www.4rknova.com/blog/2018/11/14/lindenmayer-systems
author: Nikolaos Papadopoulos
published: '2018-11-14'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Theory

L-systems are named after the Hungarian biologist / botanist Aristid Lindenmayer, who created them in 1968, while studying the growth patterns of various types of bacteria. L-systems were introduced as a formal way to describe the development of simple multicellular organisms, and also illustrate the neighbourhood relationships between plant cells. Later on, this system was extended to describe higher plants and complex branching structures [1].

Due to their nature, l-systems are useful in describing complex, self repeating patterns, such as fractals.

An l-system defines a mathematical model:

\[G = (V, \omega, P)\]where:

| Symbol | Definition | Description |
|---|---|---|
| \(V\) | alphabet | A set of symbols, both constant and variable |
| Constant symbols define an action (eg. move forward) | ||
| \(\omega\) | axiom | The initial state of the system, defined as a string of symbols from V |
| \(P\) | rules | The substitution rules that define how the axiom evolves with each iteration |

# Examples

## OL System

| \(V\) | { F, + , - } |
| F : Move forward 1 unit | |
| + : rotate right 90\(^{\circ}\) | |
| - : rotate left 90\(^{\circ}\) | |
| \(\omega\) | F+F+F+F |
| \(P\) | F = F+F-F-F+F+F- |

You can also view a live version of the code within your browser at this [page](https://turtletoy.net/turtle/f03d8ecf4d).

## Random Weed

| \(V\) | { F, X, + , -, [, ] } |
| F : Move forward 1 unit + random offset | |
| + : rotate right 22.5\(^{\circ}\) + random offset | |
| - : rotate left 22.5\(^{\circ}\) + random offset | |
| [ : push current state to queue | |
| ] : retrieve previous state from queue | |
| \(\omega\) | X |
| \(P\) | X = F-[[XX]+X]+F[+FXX]-X |
| F = FF |

You can also view a live version of the code within your browser at this [page](https://turtletoy.net/turtle/c31e5055d1).

## Sierpinski Arrowhead

| \(V\) | { F, X, Y + , - } |
| F : Move forward 1 unit | |
| + : rotate right 60\(^{\circ}\) | |
| - : rotate left 60\(^{\circ}\) | |
| \(\omega\) | YF |
| \(P\) | X = YF+XF+Y |
| Y = XF-YF-X |

You can also view a live version of the code within your browser at this [page](https://turtletoy.net/turtle/9f884f89fd).

## Von Koch Snowflake

| \(V\) | { F, + , - } |
| F : Move forward 1 unit | |
| + : rotate right 60\(^{\circ}\) | |
| - : rotate left 60\(^{\circ}\) | |
| \(\omega\) | F++F++F |
| \(P\) | F = F-F++F-F |

You can also view a live version of the code within your browser at this [page](https://turtletoy.net/turtle/4934db2221).

## Hilbert curve

| \(V\) | { A, B, F, + , - } |
| F : Move forward 1 unit | |
| + : rotate left 90\(^{\circ}\) | |
| - : rotate right 90\(^{\circ}\) | |
| \(\omega\) | A |
| \(P\) | A = +BF-AFA-FB+ |
| B = -AF+BFB+FA- |

You can also view a live version of the code within your browser at this [page](https://turtletoy.net/turtle/5da041b968).

# Implementation

The following code sample implements example 1 above. The code is using Reindeer’s excellent L-System implementation at [turtletoy](https://turtletoy.net).

```
Canvas.setpenopacity(1);
const turtle = new Turtle(30,-55);
function createLSystem(numIters, axiom) {
let s = axiom;
for (let i=0; i<numIters; i++) {
s = processString(s);
}
return s;
}
function processString(oldStr) {
let newstr = "";
for (let i=0; i<oldStr.length; i++) {
newstr += applyRules(oldStr[i]);
}
return newstr;
}
function applyRules(ch) {
switch (ch) {
case "F": return "F+F-F-F+F+F-";
default : return ch;
}
}
// Create L-System and set number of iterations and axiom
const inst = createLSystem(4, "F+F+F+F");
const distance = 0.9;
const angle = 90;
// The walk function will be called until it returns false.
function walk(i) {
const cmd = inst[i];
switch (cmd) {
case "F": turtle.forward(distance);
break;
case "+": turtle.right(angle);
break;
case "-": turtle.left(angle);
break;
default :
}
return i < inst.length - 1;
}
```