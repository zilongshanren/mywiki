---
title: A Geometry Theorem Looking for a Geometric Proof
url: https://divisbyzero.com/2016/03/23/a-geometry-theorem-looking-for-a-geometric-proof/
author: Dave Richeson
published: '2016-03-23'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

[Update: [Dan Lawson has proved the theorem without trigonometry.](https://divisbyzero.com/2016/04/07/a-trig-free-proof-of-crockett-johnsons-theorem/) Thanks, Dan!]

I spent a good chunk of last week reading about David Johnson Leisk (1906–1975), who is better known by his nom-de-plum [Crockett Johnson](https://en.wikipedia.org/wiki/Crockett_Johnson). Johnson is most well known as the author of *Harold and the Purple Crayon, *a children’s book from 1955, and its sequels. Johnson was also the author of the 1940s comic *Barnaby.*![Harold_and_the_Purple_Crayon_(book)](../../assets/14c9f2cd87fcf2ca.jpg)


Later in his life Johnson became interested in mathematics. He was particularly interested in geometry, and most specifically in the problems of antiquity (squaring the circle, trisecting the angle, doubling the cube, and constructing regular polygons). He turned many geometric theorems into works of art. [Eighty of his paintings are now at the Smithsonian](http://americanhistory.si.edu/collections/object-groups/mathematical-paintings-of-crockett-johnson).

Johnson even created new mathematics. I would like to discuss one of his contributions here. (See his article “[A Construction for a Regular Heptagon](http://www.jstor.org/stable/3616804),” *The Mathematical Gazette *Vol. 59, No. 407 (Mar., 1975), pp. 17-21.)

The heptagon is notewothy because it is the regular polygon with the fewest number of sides that cannot be constructed with compass and straightedge alone. In his article, Johnson gives a way to construct the heptagon using a marked straightedge (this is called a *neusis *construction). Johnson did not give the first *neusis *construction of a heptagon—[François Viète](https://en.wikipedia.org/wiki/Fran%C3%A7ois_Vi%C3%A8te) gave [the first such construction in 1593](https://math.berkeley.edu/~robin/Viete/construction.html). (Also, Archimedes gave an unorthodox *neusis-*like construction).

However, Johnson’s proof used trigonometry (including the law of cosines and several trigonometric identities). My question to you is: **Is there a purely geometric proof of his result?** I played around with it for a little while and couldn’t find one, and I couldn’t find a geometric proof in the literature.

## The construction

The key to Johnson’s construction is producing 3:3:1 triangle; that is, a triangle in which the angles are in a 3:3:1 ratio (they would be

and

The three vertices of the triangle are three vertices of a regular heptagon. If we construct the circumcircle, then it is easy to construct the four remaining vertices with a compass and straightedge.


Here’s his construction of a 3:3:1 triangle using a marked straightedge—that is, an otherwise ordinary straightedge, but possessing a mark one unit from the end (or equivalently, two marks one unit apart). We begin by drawing a line segment *AB* of length one (see below, left). Construct a unit line segment *AC* perpendicular to *AB*. Also, construct the perpendicular bisector to *AB*; call it *l*. Then construct a circle with center *B* and radius *BC*. Now we perform the *neusis* construction with the marked straightedge: Construct a line *AD* so that *D* is on *l* and *D* is one unit from the circle. (That is, the end of the straightedge is at *D*, the mark is on the circle, and the edge passes through *A.*) Then is the 3:3:1 triangle.


![heptagonneusis2](../../assets/8dfa0e28b74163e9.png)


## A geometric proof?

Johnson’s proof that is a 3:3:1 triangle used trigonometry (see his article for details). Is there a geometric proof?


Boiled down to its essence, here’s the question: Suppose is isosceles and

*E *is on *AD*. Moreover, suppose

and

, prove that


![triangle](../../assets/1298c764594e1fbe.png)


Here is a fact that may help. Johnson discovered this fact—ironically—when he was sitting in a café in Syracuse on Sicily (the birth place of Archimedes) playing with the wine and food menus and some tooth picks. If we have an isosceles triangle *ABD *with the point *E *on *BD *and *F *on *AD * such that then triangle

*ABD *is a 3:3:1 triangle. (This is easy to prove. Suppose Then, because

is isosceles,

. So the exterior angle of


is

Because

is isosceles,

Lastly, observe that

and

are similar, so

It follows that

)


![zigzag](../../assets/a23b236e6c9bc04b.png)


Thus, a possible route to proving the theorem is to find a point *F *in the original diagram so that

If you find a proof, I’d love to hear about it!

Here are two of the paintings Johnson made from his work with the heptagon.

![NMAH-2008-2545](../../assets/eb193fdebb8954ba.jpg)


![NMAH-2008-2545](../../assets/eb193fdebb8954ba.jpg)

![NMAH-2008-2518](../../assets/c081653f38ea3acd.jpg)


![NMAH-2008-2518](../../assets/c081653f38ea3acd.jpg)

lovely post. Archimedes was also able to trisect an angle! see: http://wp.me/p4LQy6-e0

More Archimedean connections: according to “Triumf der Mathematik” (H. Dörrie), the same argument given here that the wine-menu triangle is 3:3:1 was also used in Archimedes’ own neusis trisection method.

Archimedes’s construction is very unorthodox—and very different from this one. His neusis-like construction is very unusual. He (or supposedly he—some scholars are skeptical that it is his work) performs a construction in which he draws a line through a point so that the two triangles it forms have equal area. Not your typical compass and straightedge move! Once he’s accomplished this, he is able to construct a

angle. So his goal isn’t to explicitly construct the 3:3:1 triangle, but he does get one along the way. Here’s an article that talks about his construction http://www.jstor.org/stable/41133724

That is quite interesting, but I wasn’t remembering a heptagon construction at all; rather I was refering to the same thing gaurish mentioned (though I didn’t notice that he did untill quite later).