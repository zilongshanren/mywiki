---
title: Featured Blog | From ASCII to Pixel Art and Back
url: https://www.gamedeveloper.com/art/from-ascii-to-pixel-art-and-back
author: Andrei Fomin
published: '2024-05-15'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# From ASCII to Pixel Art and Back

I'm developing a 2.5D pixel art game on my old text-mode engine. A character-based ASCII engine can handle this task, it just needs a couple of upgrades.

![](../../assets/79423fc4bc768814.jpg)

Hello everyone! I'm developing a new game called Coin-Op Vice on my old text-mode engine. However, this is a pseudo-3D (2.5D) pixel art game with perspective. It turns out that a character-based ASCII engine can handle this task, it just needs a couple of upgrades.

## Upgrade number one: custom font

Each character in the font is simply an image. In my case, it's pixel art. If we replace the characters with arbitrary images, we can create cool Pixel Art from this font. However, this method has two limitations:

My font is originally monochromatic. Each letter can only consist of pixels of one color. While there is information about the color of the character, there is no information about the color of each pixel within the character. This is due to the way the font is created in the engine. I've decided not to change this part of the engine.

The character set is limited. If we replace the "/" character in the font with a sprite of a right leg, then all "/" characters on the screen will become right legs. And if this character was used to create an arm (as in the animation below), it will now turn into a leg. At the moment, I'm already using characters from the entire ASCII range to create images.


![](../../assets/1835a72ea672ee8d.gif)

I made this animation as a gift for my future wife.

Due to the monochromatic nature of the characters, the image has a Spectrum-style look. And because of the character set limitation, I can edit and test various configurations right in the code using the keyboard. Essentially, each image in the game corresponds to a key on my keyboard. Lots of benefits!

![](../../assets/2322df2bec0ded53.jpg)

## Upgrade number two: multiple alphanumeric layers with variable grid size

Let's say it's 1978, and you're sitting in front of an alphanumeric display (like a VT100). Let's assume it can display 24 rows by 80 characters. The characters are arranged in a grid with a fixed and uniform size for each cell.

![](../../assets/435ab7cb8e12134f.jpg)

Now we create multiple alphanumeric layers, as if several computers (or video adapters) were sending signals to your display. The signals combine, and you see a composite image - multiple text layers superimposed.

Now let each text layer have its own smooth offset on the screen, as well as its own cell size for characters. That's it. Now you can make a 2.5D Top-Down game with perspective. You just need to calculate the offsets of the alphanumeric layers correctly and set the sizes of their grids.

## Upgrade number three, non-authentic

Couldn't resist adding CGA palette graphics to the game. I really like the colors, and the faces turn out particularly vivid. I hope the retro style vibe isn't compromised by this eclecticism. What's your opinion?

![](../../assets/85ddf6e66d1a39ac.jpg)

## Back to ASCII


One day, during endless testing and debugging of the game, my custom font switched back to the original - character-based one. I really liked the image. It was like being in another world. The Matrix.

![](../../assets/c4afbd1f48d0ce48.gif)

I decided to implement a special mode. If you approach the terminal in the game, you can switch to a "matrix" mode. Since it's better not to use the name "Matrix," I named the mode "Neo-N." It's a reference to the main character of the movie, and the name also emphasizes that everything is illuminated with neon. My wife came up with it.

Being in this mode offers many advantages: monsters don't inflict damage (while I can still harm them), hidden passages become visible, and you can collect special cartridges to build a deck. After 15 seconds, there's an automatic "emergence" from this mode.

During the transition to this expanded text mode, I tried smoothly changing the parallax parameters. The image seemed to, sort of, expand. Isn't that interesting?

![](../../assets/74d76adb88790f83.gif)

Such a comeback in ASCII, even if only at 15-second intervals. I decided to tell you about this unusual game design. I hope you liked the style. Visit the game's page on Steam, where a demo with this feature is already available.

Does such a retro design have the right to exist in our era? What do you think?

Thanks everyone, bye for now!