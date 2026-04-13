---
title: Full Game Aesthetic Walk-Through
url: https://lindenreidblog.com/2018/02/05/__trashed/
author: View all posts by Linden Reid
published: '2018-02-05'
source_blog: Linden Reid
source_site: https://lindenreid.wordpress.com
category: graphics
fetched: '2026-04-13'
---

Hey, y’all! My friends [Kytana Le](https://twitter.com/ivorytea), [Lucien Ye](https://twitter.com/lucestark), and I created a **chill, atmospheric, color-based puzzle game** called during the 2018 Global Game Jam. In the spirit of the Global Game Jam’s encouragement of knowledge-sharing, here’s a tutorial on how we made

[The Endless River](https://sogoodgames.itch.io/the-endless-river)

**all of the visual effects**in the game!

Firstly, here’s the entire [Github repository for the whole Unity project](https://github.com/thelindseyreid/GGJ18). Feel free to download it and use the resources, **as long as you include the same open-source license with your project.**

I’m going to talk about **how we chose the effects** that we used and give a short overview of how to **implement** every effect. One of these effects uses a shader that’s controlled by gameplay code, so this tutorial should be a great example of **how to integrate shaders into the overall aesthetic** and the game mechanics for your games.

In addition, there are a couple of tutorials that cover the details how the shaders were written for some of the effects, as there’s more material than would fit in this tutorial:

Now, on with the tutorial!


## Inspiration

*The Endless River* takes place in the space between life and rebirth. The river and boatman were inspired by the boatman from Greek mythology who guides souls from life to death, and the theme of the game was inspired by Buddhist philosophy surrounding rebirth. Because we had an interesting mix of cultural inspirations, we didn’t want to simply replicate an aesthetic from either culture, but make something our own.

We went with an **ethereal forest** for the backdrop of the river, and since the game is supposed to loop forever, we decided it would be easiest to make it a side-scroller with a looping parallax background. **All of the effects were inspired by this magical, ethereal tone** that we were aiming for. Glowy stuff, fog, soft particle effects, and the pink/purple color palette all contributed to this.

In short, these are all of the visual effects we used:

- A shader with a changeable color, and a script that controls that color, for the faeries, lamp, and soul
- A parallax effect on the forest background
- Bloom
[Custom post-processing](https://lindenreid.wordpress.com/2018/02/05/camera-shaders-unity/)[2D reflective water](https://lindenreid.wordpress.com/2018/01/31/2d-reflective-water-shader-in-unity/)- A particle effect for the small faeries
- A simple faux-fog effect
- Fading text

Now, we’re going to go over how to create each effect in Unity!


## Script-Controlled Color

In the [shader for the faeries, lamp, and soul](https://github.com/thelindseyreid/GGJ18/blob/master/Assets/scripts/shaders/spriteLit.shader), I added an exposed variable for the color of the sprite in the Properties block called **_Color**.

**_Color** ("Color", Color) = (1, 1, 1, 1)

`o.Albedo = sprite.rgb * sprite.a * `**_Color.rgb**;

Then, I added [a C# script](https://github.com/thelindseyreid/GGJ18/blob/master/Assets/scripts/Lamp.cs) to change this value based on what’s going on in the gameplay. To change a shader Color property from a C# script in Unity, you simply need to get a reference to the object’s material, and call material.SetColor(“PROPERTY NAME”, NEW VALUE), like so:

`rend.material.SetColor("`**_Color**", avgColor);

You can call other Set and Get functions on any exposed property in your shader with other functions on [Material](https://docs.unity3d.com/ScriptReference/Material.html), like GetFloat() and SetFloat(), GetInt() and SetInt(), etc.

Note that the string name of the property needs to **match the name of the property exactly**. Note also that I’m getting the object’s material through it’s renderer component, which I made a public field on this class so that I could set it in the inspector.

Here’s what the script now looks like in the inspector. The spriteLit material contains the shader that we created with the exposed **_Color** property.

![spritelit](../../assets/48359f9f2af2866b.png)


## Scrolling Parallax

Firstly, our artist created a unique sprite (or two) for each layer of the parallax. Each sprite was exactly the width of the screen.

Then, I used a script to slowly increase the x-position of the sprite. When the x-position of the sprite passes a certain threshold, the script resets the position of the sprite back to its original position. The script uses two copies of the same sprite in order to fill gaps as the sprite moves across the screen.

You can see the ** full script here**.

You can kind of see how the effect is working with this game view:

![looping](../../assets/a703fde8a5bd5bea.gif)


The downside to this approach is that tuning the start and loop positions for these sprites was pretty tedious. **In retrospect, I would have created a shader that scrolled the texture sample position, which wouldn’t have required any annoying tuning. **Comment below if you’d like to see a tutorial on that! 😉

To **layer multiple levels of sprites**, you’ll want to set their **Sorting Layer and Order in Layer** properties in the inspector. The **lower the layer, the further back** the sprite will appear. You’ll want to customize this layer for almost every sprite you put in the game.

This property is on your SpriteRenderer component:

![spritelit](../../assets/48359f9f2af2866b.png)


## Bloom

Bloom is super easy to set up in Unity. I used the legacy (pre-5.5) post-processing stack. If you don’t already have it, you have to [download on the asset store here](https://assetstore.unity.com/packages/essentials/legacy-image-effects-83913).

Once you have the post-processing stack, you can simply **add the Bloom script to your main camera**. Any colors that are extremely bright will bleed into neighboring pixels, causing them to look like they’re glowing. Here’s what our tuning looked like:

![bloom](../../assets/46ea8ac2062692bc.png)


In retrospect, I wish that I had just used Unity’s new post-processing stack. It’s just as easy, but I was confused and short on time during the game jam XD You can download the [new post-processing effects on on the asset store](https://assetstore.unity.com/packages/essentials/post-processing-stack-83912), and the [instructions to use it are here](https://docs.unity3d.com/2018.1/Documentation/Manual/PostProcessing-Stack-SetUp.html). It’s basically as easy as the old stack!

## Fairy Particle Effect

The small fairies in the background of the game are simply a **particle effect using Unity’s particle effect system.**

The most important part of this effect is that we tuned them so that they would **fade in and out** at the beginning and end of their life. We did this by checking the “Color over Lifetime” box in the Particle System editor, and **set the beginning and end color to be transparent**:

![particleColor](../../assets/867c668a011ca466.png)


## Faux Fog

Instead of dealing with figuring out how to do fog in 2D, I cheated and just created a translucent fog texture and put it in between the background and first layer of the forest. The fog is a gradient from solid white at the bottom to transparent at the top. Now that’s how you save time during a game jam! XD

## Fading Text

The last effect that I implemented was the fading text at the beginning of the game. It looks like this:

![fadingText](../../assets/08b24287224f7b95.gif)


This was controlled completely using a script that changed the text.a (alpha) property of the Text component. You can [view the script here](https://github.com/thelindseyreid/GGJ18/blob/master/Assets/Subtitles.cs).

Basically, the script has two different states, Fade and Linger. When the script is in the Fade state, it decreases the alpha value of the text. When the alpha value is lower than 0, it plays the next title and switches to Linger.

In the Linger state, the script increases the alpha value of the text, and doesn’t switch states until it passes a time threshold, at which point it fades out again. The cycle repeats until the script has passed through all of the text to display.

I could have written a much fancier state machine for this, but for the sake of time, I went with simple spaghetti code!

## Fin

I hope you learned a thing or two from this tutorial! If you have any questions about how it was implemented, remember you can view and download the entire project from GitHub. You can also hit me up in the comments below or [on Twitter](https://twitter.com/so_good_lin) with questions!

Good luck,

Lin Reid [@so_good_lin](https://twitter.com/so_good_lin)