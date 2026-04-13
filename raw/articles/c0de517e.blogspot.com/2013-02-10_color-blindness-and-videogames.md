---
title: Color blindness and videogames
url: http://c0de517e.blogspot.com/2013/02/color-blindness.html
published: '2013-02-10'
source_blog: C0DE517E
source_site: http://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

After PC Gamers published

[this article on color blindness](http://www.pcgamer.com/2013/02/01/why-games-need-color-blind-modes-see-simcity-with-simulated-color-blindness/)and games, I was curious to see what could be done and how, to target better the 5% (8% among males) of gamers affected with this deficiency. The original article didn't link any research or implementation hint but came with a note saying that it should be trivial to do... As most games nowadays do some form of color correction, often via volume color textures, you would think it's not hard to bake a global color transform that maps better the RGB space into what can be seen by colorblind persons.
Well, indeed, it is. Most papers seem to reference as a starting point a project report by Fidaner, Lin and Ozguven, "

[Analysis of Color Blindness](http://scien.stanford.edu/pages/labsite/2005/psych221/projects/05/ofidaner/project_report.pdf)" which derives a simple linear transform by going from RGB to[LMS color space](http://en.wikipedia.org/wiki/LMS_color_space), simulating color blindness by losing one of the receptors in the LMS space, computing the difference between the two images and feeding back this difference by adding colors that can be perceived instead.
The algorithm is so simple it's easier to read the paper than my summary of it. Past this simple mapping, all the research I've found improve on the mapping by adjusting for the characteristic of the image you need to convey, which is not only more expensive but also could be not ideal in our case, as the image contents are changing frame to frame. I wonder if a nonlinear transform could improve the situation, but I haven't found much about static, global color transforms other than the aforementioned work.

Further notes:

**The website daltonize.org has**[implementations](http://www.daltonize.org/search/label/Developers)of the linear transform in many languages.- Some papers seem to do the RGB->LMS (and viceversa) conversion in gamma space (including the Analysis of Color Blindness one), while some other don't. The confusion I guess comes from the fact that there are many RGB spaces, and not only sRGB with its gamma 2.2ish transfer function. From what Wikipedia says, CIEXYZ to LMS is a linear transform, and keeping in mind that
[sRGB to CIEXYZ](http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html)is not, we have to gamma/degamma. I've also found[this paper](http://nn.cs.utexas.edu/?depaula:utcstr06-49)(comes with sourcecode) which makes conversion between sRGB to LMS an even less trivial matter. - There are some variants of the original daltonization algorithm. In particular,
[this paper](http://biecoll.ub.uni-bielefeld.de/volltexte/2007/52/pdf/ICVS2007-6.pdf), proposes (among other things which are less relevant) the use of a modified error matrix (formula n.5). - If you wanted to spare some GPU cycles, it's possible to feedback the error term computed by the daltonization in other post-effects, to locally enhance contrast of areas between two similar colors.
[This paper](http://www.sciencedirect.com/science/article/pii/S0016003212000804)illustrates the concept.- You could feedback into an existing, suitable effect (i.e. bloom)
- You could trade off a post/processing step for this, for example, remove DOF or motion blur and add an "unsharp mask" filter guided by the error. A way of doing this is to compute an unsharp mask, in a single pass, for both the regular and color-blind simulated colors, and then feedback the error (contrast loss) in the image.
- A color-blind simulation mode could at the very least, help UI designers with their job.

## 5 comments:

Seems like the best place to do this would be in the monitor hardware. Press a button on the monitor, and presto, *everything* is fixed with no software mods.


Being red-weak person I love to choose my color in RTS games - which is not always possible.






I have changed runway lights colors in some fly sim - in order to see them better (even better than in real life)

I don't want to change all color space. I see world as I SEE and "press a button" would change ALL colors to different than in real life for me.

In order to balance "real" and "foolproof" color scheme I like to cherry-pick exactly those game-play elements (such as warring red LED:P ) which are hard to distinguish for me.

If I would change all red shades - I would have ugly sunsets :)

The more colors will be changed the more unreal they be (even for color blind persons)

Yes, ideally the game visuals should be designed and not just patched, for color blind users. Note thought that knowing how to simulate these defects, and the fact that it seems quite easy to do, could encourage game makers to implement such methods and allot some testing time to make sure the game is playable in these modes as well.

Interesting stuff.






I'm color blind and when I was a kid and found out I thought it a death sentence. I couldn't be a pilot or a cop(here in Sweden). When I did my army tryouts I changed my mind. After the color blindness test the recruiters send me to a different place than the other and I got to do tests for a scout. The reason was I can see some things a lot better because _of_ my color blindness. When I was a kid I wondered why anyone would use camo-netting, it just made the thing they where trying to hide stand out. Reason was my color blindness. And camo-netting was just the tip of the iceberg.

The term color blindness makes it sound like handicap but it's got a few perks. Better night vision, overall better luma perception, increased pattern recognition etc.

The last one of these is the only one I've even felt as a handicap in gaming. My mind recognizes to many patterns and some games designed for the color seeing, or "luma blind", are to "patterned". For a color seeing person the colors will blend off the patterns but for me it becomes a mess.

Not seeing red buttons and things like that are rare for me, I make them out using other clues. An example relevant to you profession is anti-aliasing. For me some anti aliasing techniques don't work, lines and edges are still jagged and in some cases even becoming worse.

So the premise, fixing color vision for the color blind, is not necessarily the only problem. It's of course different with different types of color blindness.

That's very interesting ideed. I agree, with you, fixing "color vision" is just the tip of the iceberg.

On the other hand, pragmatically, the amount of effort spent by developers to go in depth on this is proportional (or ideally should be) to the market of color blind gamers which find these issues to be problematic.

So I think it would be great if we could identify easy, low-cost solutions for such problems, creating a color-blind filter is really really easy, so this article was aimed at least at making aware that such things are inexpensive for gamedevs.

It would be interesting to understand, and publish, other similar low impact solutions, if there are any.

Post a Comment