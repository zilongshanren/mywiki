---
title: Cardioid Drawbridges
url: https://divisbyzero.com/2024/05/24/cardioid-drawbridges/
author: Dave Richeson
published: '2024-05-24'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

Suppose you want to design a drawbridge as shown in the figure below. A cable runs from the end of the drawbridge to the top of a tower and then down to a heavy counterweight that rolls along a curved track. The counterweight makes it easier to raise and lower the bridge.

![](../../assets/06def2d443ab2041.png)


![](../../assets/06def2d443ab2041.png)

A natural question is: can we choose the weight and the shape of the curved track so the bridge and the weight are always in equilibrium? That is, when the bridge is in any position, it is neither pulled up by the counterweight nor down by gravity. Surprisingly, the answer is yes, and it involves one of my favorite curves: the cardioid.

First, let’s introduce some notation. As shown in the figure, we will assume the length of the bridge and the height of the tower are both units. At any moment, the angle between the tower and the bridge is

and the angle between the bridge and the cable attached to the counterweight is

Let

be the length of the cable from the top of the tower to the counterweight. The masses of the bridge and the counterweight are

and

respectively.


Let’s first discuss the masses. When the bridge is down and the counterweight is at the top of the tower, the system should be in equilibrium. The drawbridge is a lever with a fulcrum at the tower’s base. The bridge produces a downward force of that is applied

units from the fulcrum. The force along the cable is

and because it makes a

angle with the bridge, the upward component is

applied

units from the fulcrum. Because the forces are in equilibrium,


Hence, the counterweight’s mass must be

![](../../assets/384cff5e0ce65377.png)


![](../../assets/384cff5e0ce65377.png)

When the drawbridge is down, the length of the cable is So, obviously, this is the cable’s length at any intermediate stage. In such an intermediate configuration, the bridge, the tower, and the cable joining them make an isosceles triangle with vertex angle

So, the length of that portion of the cable is

Thus,


Finally, saying that the system is always in equilibrium is the same as saying the potential energy is the same in every configuration. When the bridge is down, the counterweight holds all the potential energy, What if the bridge is partially raised? To compute the potential energy of the bridge, we assume that the entire mass

is located at the bridge’s midpoint. Its height is

so its potential energy is

The height of the counterweight is

so its potential energy is

Setting these equal, we obtain


which simplifies to

A trigonometric identity gives us

When we combine the equations for cable length and potential energy by eliminating the terms, we obtain


which is the polar equation for a cardioid! As we see in the figure below, the track is only a small portion of the cardioid curve (from to

to be precise).


![](../../assets/e1e24084de5827a5.png)


![](../../assets/e1e24084de5827a5.png)

This design has been used around the world at various times. The bridge below is the Jackknife Bridge in Buffalo, New York. It was constructed in 1897, and this photo dates to 1900–1910. (Image source: [Library of Congress](https://www.loc.gov/item/2016809926))

![](../../assets/3c5efeaba78618e9.jpg)


![](../../assets/3c5efeaba78618e9.jpg)

The Glimmer Glass Bridge, located in Monmouth, New Jersey, is another such example. It was built in 1898 and was placed on the National Register of Historic Places in 2008. (Image source: [Wikimedia](https://commons.wikimedia.org/wiki/File:Brielle_Road_Bridge_over_the_Glimmer_Glass_%287%29.JPG))

![](../../assets/b6e0514c610f0107.jpg)


![](../../assets/b6e0514c610f0107.jpg)

This topic appeared in a pair of articles in the *Mathematical Gazette* in the 1990s. In 1990, H. Martyn Cundy wrote “[The bascule bridge: An unexpected cardioid](https://www.jstor.org/stable/3619354)” (74 (468): 124–127). In 1995, Michael Deakin followed up with the much simpler argument I have expanded in this blog post (“[More on bascule bridges](https://www.jstor.org/stable/3620009).” 79 (484): 107–108).