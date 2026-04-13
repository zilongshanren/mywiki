---
title: What goes into graphically updating a decade-old MMORPG like Final Fantasy
  XIV
url: https://www.gamedeveloper.com/art/what-goes-into-graphically-updating-a-decade-old-mmorpg-like-final-fantasy-xiv
author: Alan Wen
published: '2023-11-22'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# What goes into graphically updating a decade-old MMORPG like *Final Fantasy XIV*

Square Enix Technical artist Tatsuya Okahisa and producer/director Naoki Yoshida share insights on the process of the visuals of the long-running MMORPG.

![A photograph of a Final Fantasy XIV Fan Fest panel. A photograph of a Final Fantasy XIV Fan Fest panel.](../../assets/bc61a407a84f2a32.jpg)

As technology advances, it’s common to see games getting visually better, whether in remasters, remakes or a graphical update. But there also has to be consideration taken into whether or not part of the atmosphere or vision of the original is lost in the march of progress. These considerations feel ever more important in a forthcoming graphical update for Square Enix’s [Final Fantasy XIV](https://www.finalfantasyxiv.com/), set to arrive in next year’s 7.0 update and its Dawntrail expansion.

Such an update is a long time coming for the-now 13-year old MMORPG if you factor in the original 2010 release—and you should, as its character models are still mostly based on those from the 1.0 version. But unlike remaking a game that players might not have revisited for many years, MMOs are played long-term with player-created characters, and so there is a greater attachment to how a character looks, even if they might look dated.

Even if the graphical update is intended as an enhancement, there is a risk that it negatively impacts how a player may perceive their created character, a key issue raised by the development team during presentations at last month’s Final Fantasy XIV Fan Festival in London.

In presentations at the event, Square Enix lead technical artist Tatsuya Okahisa and producer/director Naoki Yoshida shone a light on the critically acclaimed MMORPG’s upcoming graphical update—with a surprising amount of detail on the technical and design decisions that went into it.

## Preserving the image of Final Fantasy XIV

“A very important point that we keep in mind is that we don't want to destroy any sort of image that the players have built of Final Fantasy XIV in their minds,” lead technical artist Tatsuya Okahisa said at a development panel that took a deep dive into the graphical update. “That said, this image is very subjective, so it is quite a challenge for us to make sure that these are being maintained and also being updated as well.”

This was similarly addressed by producer and director Naoki Yoshida during the fan festival’s keynote. Following community feedback after the announcement of the graphical update back at the fan festival event in Las Vegas, he shared an update of the Au Ra race, whose updated horns and scales had been initially revealed as looking very reflective but a little too much like enamel.

“This reflectivity looked very high quality so it was good for showing off, but it didn't really match our vision of what we wanted the Au Ra to look like from our original design back in 3.0, so we continued tweaking,” Yoshida admitted before sharing a new headshots of a male and female Au Ra where their horns look less reflective and more natural. “This goes for all of the updates for the other races as well. What we showed in Las Vegas wasn't the final product but a work in progress.”

![A before/after comparison of different graphical renders of an Au Ra player character. A before/after comparison of different graphical renders of an Au Ra player character.](../../assets/9c1076bea7395013.jpg)

Left: an earlier render of an Au Ra player character. Right: An updated version shown at Fan Fest. Image via Square Enix

As Final Fantasy XIV also features a wide variety of races to play as, there’s also different approaches in how to enhance the look of each race. For Hyur or Elezen whose skin closely resembles that of humans, it’s a case of improving the skin textures.

In the graphical update, Okahisa gave an example of a before-and-after of an Elezen male’s face. “You can tell that the texture of the skin as well as the blood flow on the face, what makes it look more lively, is a lot more apparent,” he said of the after image, while highlighting the additional details in bumps, protrusions and other irregularities in real skin that is represented in what the team refers to their ‘normal map data’. “We tried to tweak the different protrusions on the normal map so that the highlights are more finely calculated, so that the skin feels more dewy.”

In addition, the update also implements subsurface scattering, a technique where light doesn’t just bounce off the surface of a polygon but goes beneath the skin so that it scatters around to give a more realistic impression. “One the light scatters beneath the surface of the skin, you see that it is not just a bumpy surface but feels a lot more like real skin,” Okahisa continued.

## Nonhuman species require different graphical considerations

When it comes to other races however, there are other areas to focus on. When showing an example of a Lalafell, known for their cute faces and short stature, he explained, “The person who was handling this aspect of it didn't want to make it too realistic, they wanted to pursue a more doll-like look.” Meanwhile, the Hrothgar race has a different benefit in the graphical update as the feline race will have a dedicated fur shader.

Other character elements are more straightforward cases for enhancing the visuals. Real-time calculations mean a more realistic depiction of catch light reflecting off a character’s iris, whereas previously these were drawn in. Increased resolution means smoother looking hair, while being split into multiple sections for color and hair flow direction allows for more complex hairstyles to be more naturally lit.

Being able to lift the upper restrictions of memory also means gear looks more detailed and varied in different material textures with physics-based rendering.

![A before/after update comparison of a LaLaFell player character. A before/after update comparison of a LaLaFell player character.](../../assets/ce1f50aa67779910.jpg)

Image via Square Enix

Okahisa however added, “With Final Fantasy XIV, we're not trying to pursue a very photorealistic depiction of our graphics. So this physics-based rendering is just a tool that we use in our application, and if there are depictions that we feel are cooler looking, sometimes we might go beyond the boundaries of real-life physics.”

“We want to have that kind of fantasy vibe, there's a certain nuance that we're aiming for, so we don't use the calculation just as they are,” Yoshida agreed. “Sometimes we might drop the precision of the calculations or we might change the calculation so that we can achieve what we have in our vision.”

Some of these changes may feel incredibly minute, with audiences arguably having to really squint to notice the subtle changes of shadow in some of the before and after slides shown at both the keynote and panel. It will however be important to members of the community who regularly show off their screenshots of their characters with the game’s ‘Gpose’ feature, and they will undoubtedly pay attention to those tiniest of changes.

As the work continues with the Final Fantasy XIV’s artists working tirelessly to improve upon 13 years’ worth of graphical assets, Yoshida assured its fans: “We understand that you all love your characters and we don't want to change your characters, but we do want to make them look a lot better.”