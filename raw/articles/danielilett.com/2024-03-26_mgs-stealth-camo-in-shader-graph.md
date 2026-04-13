---
title: MGS Stealth Camo in Shader Graph
url: https://danielilett.com/2024-03-26-tut7-9-mgs-stealth-camo/
author: Daniel Ilett
published: '2024-03-26'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

In most main-series Metal Gear Solid games, you can obtain a special item called the *Stealth Camo* by being bad at mashing the circle button, holding up enemies and getting them to shake their booty, or shooting adorable toy frogs. Standard hero stuff. The stealth camo makes Snake or Raiden totally invisible to enemies, and in this tutorial, we’re going to recreate its look in Shader Graph.

![Solid Snake using the stealth camo. Solid Snake using the stealth camo.](../../assets/e69481fd7bcdb529.png)


# Setup

To our eyes, Snake appears like a translucent ghost, although the specific appearance changes slightly from game to game. Usually, it’s vaguely green, transparent, and it refracts light from occluded objects a little, as you can see from the straight lines that turn wobbly when seen through Snake. At least, that’s how it appears in MGS2, which I’ll primarily use as my reference.

That gives us a couple of clues about how we might want to make our own version of the shader. Evidently, it’ll need to be transparent. To do the light refraction, we’ll sample the frame buffer - well, not quite, we’ll get the screen contents through the camera texture, which is an image of the game screen captured partway through the rendering loop, which can then be accessed later on during rendering.

![The (simplified) rendering pipeline. The (simplified) rendering pipeline.](../../assets/6889eabbd8fead5b.png)


To use the camera texture, that means step 1 will be heading over to your `URP Asset`

and ticking the *Opaque Texture* option near the top in the Inspector. In a default URP project there are three of these assets for different quality settings inside *Assets/Settings*, so make sure you enable the texture on all three. Now we can sample the camera texture inside our shaders. Here’s the effect we’ll get by the end of this tutorial:

![A character with the completed stealth camo shader attached. A character with the completed stealth camo shader attached.](../../assets/819ae99b508d92a5.png)


# Creating the Shader

Let’s create a new Unlit shader via *Create -> Shader Graph -> URP -> Unlit Shader Graph*, and I’ll name it `StealthCamo`

. You can make it Lit if you want, but I’ll keep it simple.

When we open the graph, we’ll be met with the output stack and the Graph Inspector. Over in the Graph Settings tab of the latter, I will change the *Surface Type* to *Transparent*. This is important because Unity captures the camera texture between rendering all the opaques and all the transparents, so this graph will not work if we use *Opaque* rendering here.

![Enabling transparent rendering in the Graph Settings. Enabling transparent rendering in the Graph Settings.](../../assets/e3e5d1eb16aa13e6.png)


Next, I’m gonna add some graph properties. I’ll actually add all three of them up front. The first will be a `Color`

named `Base Color`

- this lets us choose which flavor of jelly to turn Snake into. The alpha channel of this color will control the ratio of the final pixel color between the `Base Color`

*RGB* values and the camera texture values. Basically, without implementing any distortion, this shader would act like a bog-standard transparency shader with extra steps.

Next up are two `Float`

properties called `Noise Size`

and `Noise Strength`

. If we just wanted this camo shader to look transparent, we would only need a color property. But what I’m going to do is wobble the camera texture around a bit to simulate light refracting through Snake, which I’ll do using noise. These two properties simply control the size of the noise clouds and how strongly they disrupt the original texture - I used default values of 20 for the size and 0.5 for the strength.

![The Base Color, Noise Size, and Noise Scale properties. The Base Color, Noise Size, and Noise Scale properties.](../../assets/41e5a8ef51cb5f93.png)


Let’s now construct the graph - it’s relatively small! I’ll work from the outputs backwards. First, make sure the *Alpha* output is set to a constant 1. Counterintuitively, we don’t want Unity to handle any of the transparency by itself, because we’re manually going to control the appearance of every pixel of the output.

For the `Base Color`

output, I’m going to use a `Lerp`

node to pick between a `Scene Color`

node in the *A* slot - this is the node that gets the camera texture - and the `Base Color`

property in the *B* slot. As I mentioned, the `Base Color`

alpha channel controls the ratio between these two colors, so use a `Split`

node to get only the alpha (A) component of `Base Color`

and connect it to the *T* slot on the `Lerp`

node.

![Linking the Base Color and the Scene Color nodes. Linking the Base Color and the Scene Color nodes.](../../assets/2f235c8d1f1ccf40.png)


Already if we save and observe the shader in the Scene View, by changing the `Base Color`

alpha we can slide between seeing the color and seeing the wall behind Snake. Now let’s add some wobble.

We’re going to do that by changing the UVs used for the `Scene Color`

node. Start with a `Simple Noise`

node and use the `Noise Size`

property for its *Size* parameter. This outputs noise clouds with values between 0 and 1. The next step is a small tweak, but basically, I want the noise to move the camera texture pixels in *all* directions rather than just towards the bottom-left (with a [0, 1] range, that’s what will happen currently), so I’ll remap that [0, 1] range to a [-1, 1] range instead using a `Remap`

node.

![Simple noise with its output range remapped. Simple noise with its output range remapped.](../../assets/fe9598395d5a0a09.png)


Then, I’ll `Multiply`

by `Noise Strength`

to get an offset value. But what will it offset? By default, the `Scene Color`

node takes a set of screen-space UVs which are identical to the `Screen Position`

node, so all we need to do is add our offset to `Screen Position`

, and input it to the `Scene Color`

node. And that’s the graph complete!

![Changing the UVs used for the Scene Color node. Changing the UVs used for the Scene Color node.](../../assets/0ff826c0fbbad42b.png)


Back in the Scene View, we can bump the `Noise Strength`

to anything above 0 and see some distortion of the wall behind Snake. Here, the `Base Color`

alpha is at about 30% so we get a good look at the wall while still retaining the green jelly baby look. Now fake Snake can slip past the enemy without being seen and complete his goal of meeting up with his jelly brethren.

![A character with the completed stealth camo shader attached. A character with the completed stealth camo shader attached.](../../assets/819ae99b508d92a5.png)