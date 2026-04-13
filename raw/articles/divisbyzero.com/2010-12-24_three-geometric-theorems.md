---
title: Three geometric theorems
url: https://divisbyzero.com/2010/12/24/three-geometric-theorems/
author: Dave Richeson
published: '2010-12-24'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Just for fun I thought I’d share a few interesting geometric theorems that I came across recently.

**Morley’s miracle**

In 1899 Frank Morley, a professor at Haverford, discovered the following remarkable theorem.

*The three points of intersection of the adjacent trisectors of the angles of any triangle form an equilateral triangle.*

I’ve made a ![Screen shot 2010-12-23 at 10.04.43 PM](../../assets/1d457a22dcaaf71e.png)


[Geogebra applet](http://users.dickinson.edu/~richesod/morley/)illustrating this theorem. You can find

[several proofs of Morley’s miracle at this website](http://www.cut-the-knot.org/triangle/Morley/index.shtml).

**The Pascal line**

When he was sixteen years old Blaise Pascal discovered [the following theorem](http://en.wikipedia.org/wiki/Pascal's_theorem).

*If any hexagon (convex or not) is inscribed in a conic section and opposite sides are extended until they meet, then the three points of intersection will be collinear.*

The line is now called the Pascal line.

I’ve made a [Geogebra applet](http://users.dickinson.edu/~richesod/pascalline/) illustrating the Pascal line in the case where the conic section is a circle. When you try the applet, do not forget to try the nonconvex configurations!

In fact, given a hexagon, we could keep the vertices fixed and permute their order to obtain other hexagons. A little combinatorics shows that there are [60 different hexagons](http://mathworld.wolfram.com/PascalLines.html) for each collection of six points. Each configuration has its own Pascal line. There is a lot known about these Pascal lines and their intersections.

**Steiner-Lehmus theorem**

This last theorem is remarkable, not for what it says, but because of the difficulty of the proof. In 1840 C. L. Lehmus asked for a purely geometric proof of [the following elementary-looking theorem](http://en.wikipedia.org/wiki/Steiner–Lehmus_theorem).

*Any triangle with two angle bisectors of equal lengths is isosceles.*

For example, suppose we have the triangle shown below with angle bisectors

and

of the same length. Prove that

and

are the same length.


Steiner gave the first purely geometric proof. Now there are many geometric (and trigonometric) proofs, but they are all tricky and are all proofs by contradiction. In 1852 Sylvester asked whether there exists a direct proof of this theorem. It appears that this is still an open problem. (From what I understand, there have been direct proofs, which were followed by arguments why the proofs really weren’t direct proofs. Moreover, there are some convincing arguments why a direct proof cannot exist.)![Screen shot 2010-12-23 at 10.27.05 PM](../../assets/dc766420c3e431b5.png)


**Bonus: Archimedean spiral in Adobe Illustrator**

This isn’t a geometric theorem. But I thought I’d share it with you because it is cool. Earlier this week I needed to draw an Archimedean spiral () using Adobe Illustrator. Unfortunately Illustrator does not have that capability. However, after a little searching I found this

[ingenious hack](http://forums.adobe.com/message/1250295#1250295) on the Adobe forum by jpro2007. Basically, draw concentric circles separated by a constant radial distance . Then create a brush which is a sloped line of any length, but rises a distance of

. Apply the brush to the circles to get the desired spiral. Amazingly clever! (I tweaked this a little by giving the circles radii

and a vertically-aligned brush so that the spiral would begin at the origin and start in the first quadrant.)


Here’s my JavaScript version of Morley’s trisector theorem: http://www.jasondavies.com/morley-triangle/

Thanks, Jason! I meant to add a link to your applet, but forgot.

Dave, Morley is one of my favorites, partly because he came from a small town in England near where I used to live (and where we used to have a DOD school)… and partly because he was a better educator than mathematician (my opinion)

but it wasn’t a theorem for years after Morley made his observation (conjecture?)

Speaking of threes, his three sons were ALL Rhodes Scholars…

http://pballew.blogspot.com/2011/03/trisecting-angle.html