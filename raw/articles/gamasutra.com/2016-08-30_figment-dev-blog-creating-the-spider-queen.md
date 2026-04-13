---
title: Figment dev blog - Creating the Spider Queen
url: https://www.gamedeveloper.com/art/figment-dev-blog---creating-the-spider-queen
author: Emilie Mavel
published: '2016-08-30'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Figment dev blog - Creating the Spider Queen

A step-by-step presentation of Bedtime Digital Games' art process using one of the main character from our current project, "Figment", as an example.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

This blog post was originally published on [Bedtime Digital Games' dev blog](http://www.bedtime.io/blog).

Hej!

I'm Emilie, your humble host today. Following the [introduction you got to our art team two weeks ago](http://www.bedtime.io/single-post/2016/08/15/Making-a-Figment---Art), we wanted to go in depth and present a practical case. I was thus tasked to collect information from Jonas Byrresen (our lead game designer and director who has [already written](http://www.bedtime.io/single-post/2016/04/11/Figment-Dev-Blog-%E2%80%93-A-world-inside-the-mind) [some articles](http://www.bedtime.io/single-post/2016/05/18/Figment-Dev-Blog-%E2%80%93-Meeting-the-characters)), Stefan Lindgren (our art director) and Lasse Westmark (our technical artist), whom you’ve seen in the last “Making a Figment” video, to make you discover an interesting element of Figment. So, are you ready to learn more about The Spider Queen, one of the game’s Nightmares?


As I just said, the Spider Queen is one of the Nightmares currently thriving in the mind Dusty and Piper are protecting - but what are Nightmares exactly? Well, it’s pretty simple actually: they are the entities clogging the mind with fear and doubt, refraining the character from living his life to its fullest. To be worthy of that name, a Nightmare has to represent a human fear and be as universal as possible. They can be, for example: the fear of loss, the fear of loneliness, the fear of the unknown…

First thing first: we needed to know who was the Nightmare who was going to numb Clockwork Town, the logical part of the mind. The Spider Queen’s meaning came early in development: she came from the fear of the other, of things different from us. The game designers then sat down with the artists to define her look and personality. For the Queen, it went smoothly: the fear of difference made them quickly think of insects. Often frowned upon, considered scary because of their alien appearances, they were the perfect start for this character. The team explored different designs, with various kind of insects, then settled on spiders, which are regarded as one of the most frightening insects worldwide.

![The Spider Queen's concept art The Spider Queen's concept art](../../assets/3b6239178d96800c.png)



The Spider Queen's concept art

The spiders had several interesting aspects which could be easily applied to this character. They can embody the gothic lifestyle, which focuses on feels and passions and questioning (or even breaking!) systems. Their dark and gloomy imagery was a good starting point for the Nightmare which was supposed to block Clockwork Town.

One of their natural skills also fitted Clockwork Town’s “perfect Nightmare” - their web. It was really easy to imagine them clogging gears and paralyzing heavy machinery with their silk. We felt they represented accurately the mind-numbness we sometimes feel when facing, or being filled with, fears.

This convinced us to keep the spider approach and make a terrifying Queen, twisting her features to make a scarier, out-of-place spider Nightmare.

After the concept art got Jonas’ seal of approval, it was time for Lasse to transform those 2D concepts into a usable 3D asset. [In the video](http://www.bedtime.io/single-post/2016/08/15/Making-a-Figment---Art), you can see that the average 3D asset is made to work from the angle of the camera only, but as the Spider Queen is dynamic and moves around a lot, she needed to work from all angles. That’s why Lasse got, in complement of the 2D concepts, a “turn-around” of the Queen. That way, he knew how she was supposed to look from any angle.

![Here’s a turn-around example with Dusty, one of our main characters. Here’s a turn-around example with Dusty, one of our main characters.](../../assets/a1e1146a4a6f1d2a.png)


Here’s a turn-around example with Dusty, one of our main characters.

Another important thing Lasse needed to know was the size of the Queen; more importantly her size compared to the other characters. Was she twice as big as Dusty? Or as small as Piper? An itsy-bitsy spider could make her way anywhere, but wouldn’t be very frightening, whereas an enormous one could be easily spotted but be more scary. The other important thing which depends on her size is her level of details : if she’s hardly discernible, there’s no use in making her over-detailed.

Here is an old size-chart to give you an idea of her height:

![An old size charts. Some characters on it don’t exist anymore. An old size charts. Some characters on it don’t exist anymore.](../../assets/e4bac5b418630e54.png)



An old size charts. Some characters on it don’t exist anymore.

With this information in hand, it was time to model her. The process was pretty simple, since the Queen has a simple geometry. Troubles arose when Lasse began animating her. He had several things to be careful of when modeling her eight long legs:

He had to be sure they had the right amount of mesh to support the animation;

They needed enough space between them so they had room for motion ;

The legs’ rigs had to be made so as not to disturb the animation system.


Of course, while working on all those points, Lasse also had to keep in mind the Queen’s 3D model needed to stay as close to the original concept arts as possible. After some rework, Lasse found the right amount of space and meshes and it finally looked good ingame.

![A WIP animation of the Queen. A WIP animation of the Queen.](../../assets/3ab70ef6eb1f202b.gif)


![A WIP animation of the Queen. A WIP animation of the Queen.](../../assets/346a88ddba83cf4e.gif)



A WIP animation of the Queen.

In the meantime, while Lasse worked on the animation, Stefan was working on the textures.

![Not very Queen-ie without her textures... Not very Queen-ie without her textures...](../../assets/4cdd9364528e4532.png)


Not very Queen-ie without her textures...

The beginning was pretty simple, thanks to the concept art. The first step was to reproduce what was decided earlier in the process. Using the UV unwrap Lasse gave him, Stefan started with Photoshop to give the Queen her basic color: a deep black, fitting the spider she is. Now that the base was done, Stefan could switch to 3D Coat to work on the seams and make them invisible. Not the most enthralling task, but an important one nonetheless.

![The Spider Queen’s look with the basic colors The Spider Queen’s look with the basic colors](../../assets/168acf03769a91f3.png)


The Spider Queen’s look with the basic colors.

After that, it was time for some polishing using ArtRage. For those of you who don’t know this software, it focuses on mimicking traditional media, such as oil-painting or watercolours. Stefan used it to give the Queen the usual “brushstroke”-texture you can see throughout the game - it really helped give her a “living painting” feel. It is a necessary step for all assets in the game; without that, they wouldn’t follow our art direction and would really stand out from the rest of the game (in a bad way).

After this step, the first version of the Queen was finished.

![An ingame picture with the first version of the Spider Queen. An ingame picture with the first version of the Spider Queen.](../../assets/460d23c3e8dbc43a.png)


An ingame picture with the first version of the Spider Queen.

However Stefan felt she was a bit too “dull” - even if she was supposed to be a creepy Nightmare, she still needed to give the feeling she was born from our colorful universe.

Luckily for him, some changes in the game design lead to changes in her appearance. In the game, the Spider Queen is not the only antagonist in Clockwork Town - she has an entourage of small spiders with her, tasked with putting up webs everywhere they can. While iterating on them, a few changes were made and in the end, the player could smack the spiders in the butt and send them flying away to beat them. I assure you, it’s as fun as it sounds.

With these changes, the spiders and their Queen needed a makeover. The first idea was to put a sort of target on the spiders, to push the player to hit them in the back. The problem with that approach was, from a technical standpoint, you could hit the spider anywhere, not only on a precise point. Stefan then went through some iterations to make a mark that wouldn’t be too “target-y”, and ended up with colorful tattoos all over the Queen and her breed. Player confusion = gone. Spider’s dullness = gone too.

![The flat texture of the Queen. The flat texture of the Queen.](../../assets/9fdf9498a367c8ca.png)


The flat texture of the Queen.

![Here’s the current Queen. You’ll have to play Figment to see more of her smack-able butt! Here’s the current Queen. You’ll have to play Figment to see more of her smack-able butt!](../../assets/a113be740e47d6e9.png)


Here’s the current Queen. You’ll have to play Figment to see more of her smack-able butt!

The Queen is now close to her final state. There’s still work to be done, mainly animations, but she is in a good-enough-shape that we could show you her creation process. Be assured you’ll see more of her in the following months!

We hoped you liked this quick peak behind the curtains! As usual, you can [subscribe to our mailing list](http://www.bedtime.io/) (at the bottom of the page) or [follow us on twitter](http://twitter.com/BedtimeDG) if you want to be sure to get all our latest news.

Cheers!