---
title: Fold-and-Cut Hat and Spectre Tiles
url: https://divisbyzero.com/2024/08/14/fold-and-cut-hat-and-spectre-tiles/
author: Dave Richeson
published: '2024-08-14'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

In the late 1990s, Erik Demaine, Martin Demaine, and Anna Lubiw proved that any pattern made from straight line segments in the plane—connected or not—can be cut out of a piece of paper by first making some strategic folds and then making a single cut. This is the now-famous [Fold-and-Cut Theorem](https://en.wikipedia.org/wiki/Fold-and-cut_theorem). (See [Erik Demaine’s website](https://erikdemaine.org/foldcut/), which has a lot of links and a video lecture of him discussing the problem.)

Early fold-and-cut examples include Betsy Ross cutting out the five-pointed stars in the American flag (supposedly), Harry Houdini entertaining audiences before his escape-artist career, and Martin Gardner writing about the problem in *Scientific American*.

My son saw [this video by Vsauce](https://www.youtube.com/watch?v=K4vTGnVgYXU) on the Fold-and-Cut Theorem the other day and said, “You should figure this out for the [hat](https://cs.uwaterloo.ca/~csk/hat/) and [spectre](https://cs.uwaterloo.ca/~csk/spectre/) tiles!” He knows me well. So, this was the perfect [nerd snipe](https://xkcd.com/356/)!

I wanted to figure out the process of solving the fold-and-cut problems anyway, so,… why not?!?!

I used the algorithm proposed by Demaine and his co-authors. The two essential ingredients are (1) folding along angle bisectors so that two adjacent cut lines coincide and (2) folding in a direction perpendicular to a cut line so the cut line folds onto itself. Carrying out the algorithm and then figuring out the mountain and valley folds was a little tricky, but I was successful!

Below are photos and videos of the hat and spectre tiles. At the end of the post, you can download PDFs to try this yourself. In the templates, the dot-dash lines should be mountain folds, and the dotted lines should be valley folds. The blue lines should not be folded; they should line up and be the single cut line. Be aware that the folding is a little tricky. But, as you can see, it is possible!

Update: I have also found a folding pattern for the turtle tile. [You can find it here.](https://divisbyzero.com/2024/08/20/fold-and-cut-turtle-tile/)

Update: After posting this on social media, Brian Trease reached out to say that he found a fold-and-cut pattern for the hat tile as well, and he submitted [this PDF to the Einstein Mad Hat Contest](https://drive.google.com/file/d/1I3AlKoT6hmHN1ojgdW4sf4Hbs-rF8t0b/view). His method is different from mine. He also makes different assumptions about the fold-and-cut requirements—his pattern uses the edge of the paper to form some boundaries, and some of his folds line up with the cut line.

![](../../assets/ff2249fed57588ed.jpeg)


![](../../assets/ff2249fed57588ed.jpeg)

![](../../assets/2b15517fbbb6e335.jpeg)


![](../../assets/2b15517fbbb6e335.jpeg)

![](../../assets/6f7de3b3c96cdf2c.png)


![](../../assets/6f7de3b3c96cdf2c.png)

![](../../assets/f86241413170d010.png)


![](../../assets/f86241413170d010.png)

## One Comment

Comments are closed.