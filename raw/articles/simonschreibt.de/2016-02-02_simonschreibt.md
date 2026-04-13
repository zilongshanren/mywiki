---
title: Simonschreibt.
url: https://simonschreibt.de/gat/fishtanks-in-games/
author: Simon
published: '2016-02-02'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

![](../../assets/4acf05ca1c449e91.png)


![](../../assets/4acf05ca1c449e91.png)

I didn’t embed the video directly to avoid any tracking from Google and complications with the DSGVO.

Do you need a fish tank for your game? No problem! This brochure contains three different fish tank solutions and at the end you’ll find two extra fish tricks!

Fish tanks are nice to look at because you can add a lot animated detail and if something doesn’t look perfect you can hide it by adding some water-distortion. For example these fishes are flat (seen from the side) because they’re just moving textures on a cylinder:

But as you see in the first video this disadvantage is covered by placing some algae. Really interesting: The abrupt bending of the fish when it hits a “corner” of the cylinder-polygons fits well to the “spontaneous” movement of real fish.

Looking closer you’ll notive that they **aren’t** flat! The manufacturer [Rocksteady](http://rocksteadyltd.com) made them out of tasty polygons:

You might ask yourself how these particles disappear at the end of their lifetime. We guess it’s to avoid sorting-problems that developers **don’t** like to to use materials which can **fade out smoothly**:

They just shrink – but don’t worry! The aquarium setting works to our favor again. Do you know when big round aquariums distort the view a bit?

If you look at the first video again it almost looks like the bent surface acts like a magnifying glass and shows the growing & shrinking fishes in the middle bigger as the ones on the border. That’s why we think that the behavior of these fishes will not confuse observers too much.

[Rocksteady](http://rocksteadyltd.com)uses to bring fishes a nice home. The example below might look very similar but there’s a lot more free, random and happy fish-movement:

Even if the fishes try to hide a secret by **not** showing their flank to the observer when turning around (as you can see above) we must confess that in reality these fishes **are flat** like their brothers in the very first example:

(We blame the distortion for that some fishes have a small offset to their particle and overhang a bit.)

But the frosted glass hides that perfectly and the only question left is: How do these guys look at the end of their lifetime? Well, see for yourself:

The particles get scaled in **one** axis which almost looks like that at a last action in his life the fish shows his flat secret to the observer. An very interesting alternative to “just” fade the particles out smoothly.

You **don’t** need to get a fish with a complex rig doing crazy animations do show its back above the water:

It’s enough to get a simpler roll-fish with animated tail as long as nobody can look below the sea level and see what’s going on:

Fishes with big eyes can be very interesting if they can **dynamically** look around:

At first this doesn’t sound like a complicated issue. Just put the fish and its pupils on different layers:

But when the fish can **close his eyes** you would expect that the eye lid would hide the pupil … which doesn’t work because they’re on the topmost layer!

It’s solved by removing the pupil layer for **some animation states** and render the pupils **into** the fish texture:

Here you see all possible animation states of the face texture and you’ll notice that some of them have pupils rendered into the texture and some don’t – the latter are the states where a extra pupil-layer is added to make the fish able to look around dynamically.

The code makes the fish look around but from where does the code know where the eyes “end” and avoids that the pupils move **out** of the eyeball? A very simple and clever trick: The pupils **don’t move** but only get rotated – with a slightly offset pivot point:

Thanks to our good friends at [Claybox Games](https://simonschreibt.de/clayboxgames.com) for supporting us with in-depth material!

I hope you found that stuff as interesting as I do and if you have questions or other feedback feel free to get in contact with me! :)

![](../../assets/ba0680151067ebbc.png)

[The-Adjudicator](https://www.reddit.com/user/The-Adjudicator)mentioned in

[my reddit thread](https://www.reddit.com/r/gamedev/comments/43wddy/i_made_an_article_video_about_3_ways_of_doing/)a really creative way of making an aquarium in

[Ultima Online](https://en.wikipedia.org/wiki/Ultima_Online):

“Basically it was made out of dyed “cloth”, stacked up into piles, then random dead fish are simply dropped where it overlays the cloth stacks. […] Ultima allowed you to stack items, so by stacking these square shaped pieces of cloth and coloring them in various colors people could create all kinds of items. [Like this piano from cloths and a chess board.](http://uo.stratics.com/homes/betterhomes/images/piano_IIII.jpg)”

![](../../assets/ba0680151067ebbc.png)

[Jedi: Fallen Order](https://store.steampowered.com/app/1172380/STAR_WARS_Jedi_Fallen_Order/)and fell in love with these little fishes. Look how cute they wiggle their tails:

And I found the flipbook for these fishes as well. Yes, they don’t look extremely realistic, but to be honest, they are usually seen under blurry circumstances and in the background anyway, so that’s totally good enough:

Last tips are really cool especially the one with the eye ball which is really awesome, thanks Simon !

Yeah I liked that game in general. It’s made by a friend and I think they did a great job with the graphics and how cute it is :)

lol, very interesting insight on something that often goes by without any major afterthought. WC3 saw-fish is my absolute fav.

Good to hear that you like the Wacraft-Fish too! I really like it too – so simple, so effective :)

Too bad the aquarium didn’t save X rebirth!

Hehe but at least it was a lot of work put into the game after the release and many patches improved the game in many areas.