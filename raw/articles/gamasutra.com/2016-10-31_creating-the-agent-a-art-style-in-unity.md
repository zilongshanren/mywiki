---
title: Creating the Agent A art style in Unity
url: https://www.gamedeveloper.com/art/creating-the-agent-a-art-style-in-unity
author: Mark White
published: '2016-10-31'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Creating the Agent A art style in Unity

From paper to final art, this is a behind the scenes look at what goes in to creating the art style of Agent A in Unity!

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](../../assets/8f54c6b7cbe55c18.jpg)


Marketing is one of the most important aspects in creating a successful indie game. Often an element that gets overlooked as a marketing tool is simply your game art! A unique and beautiful art style will not only help you gain sales on the store but also assist in capturing the attention of the press and most importantly, the editors who choose whether or not to feature your game. In this article we delve step by step, from paper to final art, into what it takes to bring the art style of Agent A to mobile devices with Unity and hopefully provide some helpful insights to aspiring developers!

My name is Mark White, I am the Art Director at Yak & Co and alongside Jason Rawlings (Lead Programmer) we developed ‘Agent A: A puzzle in disguise’, a spy themed puzzle game for iOS, Android and… shoePhones!?

Agent A was awarded one of Apple’s Best of for 2015, Editors Choice in 30 countries and Best New Game in over 100 countries. It reached number 1 puzzle & adventure game in 43 countries and was selected as a PAX Aus Indie Showcase Winner!

![](https://madewith.unity.com/sites/default/files/01.png?width=640&auto=webp&quality=80&disable=upscale)



#### Why Unity?

First of all, why did we choose the Unity game engine to build our game with? Both Jason and I have used Unity for many years in our previous jobs and as an artist I personally find it very easy to work with. The biggest positive for our small indie company is that we can simply develop once and deploy to many platforms. If you are smart at the beginning of the project and plan your layouts to work responsively this means going from one platform to another will be even easier.

With Agent A, not only is the UI responsive but the 3D camera view is as well. We designed each scene to scale between 16:9 and 4:3 without cutting off any important hit zones which allows our game to play on any screen size from small phones, to large tablets and TVs.

To do this, in the original scene designs, I used guides to make sure that anything important like collectables or portals would not go outside of our safe zone.

![](https://madewith.unity.com/sites/default/files/02.png?width=640&auto=webp&quality=80&disable=upscale)



The safe zone is the area inside the borders that never gets cut off on the various screen sizes. It always scales to fit the screen. So on a wide device like a Samsung Galaxy S6 we would scale until the safe zone hits the top and bottom of the screen and then stop, this would reveal a bit more of the scene on the sides. On a taller device like an iPad it would scale out to the sides and stop, revealing a bit more at the top and bottom of the screen.

![](../../assets/072f8c4e87bfb5c5.gif)



Scaling the scene allows the player to easily see everything that is important in the game even if they are playing on a very small screen.

#### Where to begin?

To use our visual style as a marketing tool we knew a lot of time would need to go into the creation of the art to make sure it stood out, so streamlining the process was very important for our timelines.

First of all, despite our game being in 3D, all artwork is initially designed in 2D. The reason for this is to speed up the iteration process. It takes a lot longer to model an item than to simply sketch it in and with all the other elements to plan (textures, lighting, hit zones, portals, collectables, puzzles and the overall look) a lot of iteration was required for each scene.

#### The first step.

The first step for each scene was to look for reference imagery. This step is really handy to give you ideas for an initial direction to head in, often the hardest part of design is just making a start. Being a 60s inspired spy game I wanted all the scenes to capture that Connery-Bond era type feel. I collected (or pinned on Pinterest) imagery that could be used as reference for each scene from architecture, film or 50/60s illustration to create mood boards.

![](../../assets/7d46931ceef1abd7.png)



#### Doodlin’

After the reference was gathered I sketched a few rough thumbnail layout options on paper. After choosing one of the layouts to pursue I would then use a Wacom and Photoshop to sketch them out in a bit more detail.


![](../../assets/f59af1a7e899ef96.jpeg)



![](https://madewith.unity.com/sites/default/files/06_0.png?width=600&auto=webp&quality=80&disable=upscale)


#### Little Tip.

Recently we purchased an iPad pro + Pencil. In short, if you would like to speed up your art process, this device is incredible. When you pair it with Procreate, a digital painting app, you’ll find sketching ideas becomes a lot quicker and actually more enjoyable too because it is so accurate, faster to erase or change than paper, has great UX and the device is portable too so you are not confined to your desk.

#### Colour/Lighting mocks.

Once happy with the initial layout sketch I designed the overall colours and lighting of the scene so that I have them in mind when doing the final mockup. I got the idea to work this way from Pixars design process and how they create Colour Scripts for their movies to help capture the mood for each shot. [http://pixar-animation.weebly.com/colour-script.html](http://pixar-animation.weebly.com/colour-script.html)

I do these designs all with vector shapes inside Photoshop. By utilising vector shapes I’m able to tweak the colours very quickly and by using Photoshop instead of Illustrator I’m able to utilise the excellent layer adjustment features such as ‘Colour Balance’ to tweak the overall colour scheme.

![](https://madewith.unity.com/sites/default/files/07.png?width=640&auto=webp&quality=80&disable=upscale)


#### Final 2D Mockup.

The final mockup is a combination of my sketches and colour mocks with added detail, texture and the final lighting. At this stage it is not uncommon for the overall layout to change around as I start adding in a touch more detail. To achieve the Agent A style I use a lot of angles. It’s something I noticed in a lot of the old Bond movie set designs. Angles can be achieved through the geometry of the room and with the light cutting through the scene. As you can see here I tried a few different configurations before settling on a final layout for the foyer scene.

![](https://madewith.unity.com/sites/default/files/08_0.png?width=640&auto=webp&quality=80&disable=upscale)


#### From 2D art to 3D models.

Besides the UI and some animation, Agent A is entirely 3D. There are a couple of reasons for this but the main reason is efficiency, for both performance and app file size. By choosing 3D, each scene goes from about 30mb of 2D art to an FBX at about 500kb plus minimal textures (which I explain below). In 3D we are also able to zoom in for closeups as opposed to having to design those up as separate scenes and adding even more file size.

![](../../assets/2b0be8df31a5dd0d.gif)


Early on, at the sketch stage, we create very simple grey box models of each scene that Jason can then start developing with. This allows art and development to be in production at the same time.

Here is an example of an early grey box model vs a final model:

![](https://madewith.unity.com/sites/default/files/10_3.png?width=640&auto=webp&quality=80&disable=upscale)


The final 2D mockup is used as reference to model the 3D scene. One thing to be aware of at this stage is that not everything can be replicated from 2D to 3D, so we just aim to get the model looking as close to the 2D as possible.

Our 3D package of choice is Blender, it’s fairly powerful considering it’s free and covers most of our needs. While modelling in Blender we setup one light to roughly get an idea of the overall scene lighting, this makes it easier when moving over and trying to setup the look inside Unity.

#### Lighting, colouring and texturing — the technical nitty gritty.

If you were wondering why the final model has some strange colours inside Blender it’s because all of the final colours and texturing are completely done inside Unity. The reason for this is because what you see is what you get with Unity. It has such an easy to use editor and the shaders that Jason created are also very simple to use, so the fastest way ended up being to do all colouring/texturing inside Unity and avoid any double handling (colouring in Blender, then tweaking colours with the different lighting setup once inside Unity).

The art style of Agent A contains a lot of gradients so it was apparent early on that we would need a way of creating these gradients inside Unity in an efficient way. Using a shader to draw the gradients at runtime would have added a lot of overhead to each scene and we really wanted to make sure Agent A could run on as many low spec’d devices as possible. Jason came up with a solution to use tiny pixel textures that stretch out and create a gradient. In Photoshop I create a 1px high image and add as many horizontal pixels as I need to create the gradient e.g. a smooth grey scale transition from Black to White would just be 1px Black next to 1px White. Inside Unity we then leverage bilinear filtering with our tiny textures, which when stretched over an entire mesh gives you a smooth gradient. Jason then added a rotational slider to the shader so that I could spin the gradient 360 degrees on the face it was assigned to, which allowed me to try and replicate my 2D gradient art.

Here is an example of a 2 pixel texture magnified 3200%:

![](https://madewith.unity.com/sites/default/files/11_2.png?width=243&auto=webp&quality=80&disable=upscale)


This is how it appears inside Unity once it is applied to a material:

![](https://madewith.unity.com/sites/default/files/12.gif?width=640&auto=webp&quality=80&disable=upscale)



Tip: Make sure your texture is set to Clamp in the inspector under Wrap mode to remove bleeding from the edges.

The shader is based off Unity’s legacy diffuse or unlit shaders and Jason added a bit of his own code in to create the rotational UV’s:

// slider property [0 to 2xPI]


_Rotation (“Rotation”, Range(0.0, 6.2831853071)) = 0.0

// define a vertex function for your shader

#pragma surface surf Lambert vertex:vert

// apply a rotatated transform matrix

float _Rotation;

void vert ( inout appdata_full v ) {

v.texcoord.xy -= 0.5;

float s = sin( _Rotation );

float c = cos( _Rotation );

float2x2 rotationMatrix = float2x2( c, -s, s, c );

rotationMatrix *= 0.5;

rotationMatrix += 0.5;

rotationMatrix = rotationMatrix * 2–1;

v.texcoord.xy = mul ( v.texcoord.xy, rotationMatrix );

v.texcoord.xy += 0.5;

}

#### An odd way to UV map…

In order for the rotational slider to work you will need to unwrap your UV’s in a slightly unusual way. Every face on an object needs to be unwrapped flat and fill in the entire UV map. That means that if (done correctly) you were to select all faces and look at their UV’s at the same time they would all be sitting on top of one another.

We’re not trying to make a traditional UV map like so (all faces of the control panel are selected):

![](https://madewith.unity.com/sites/default/files/13_3.png?width=640&auto=webp&quality=80&disable=upscale)



What we want is this lovely mess of overlapping faces (again all faces of the control panel are selected):

![](https://madewith.unity.com/sites/default/files/14_0.png?width=640&auto=webp&quality=80&disable=upscale)



When selecting each individual face it will look a lot nicer (only the front face of the control panel is selected):

![](../../assets/aeab59176e91ff6c.png)



With this method, each face that you want control over will need a separate material in your model. That way, when you select the object in Unity you have multiple materials that you can use to control the colour, gradient and texture of each face.


![](../../assets/02b718e1ef60feb1.png)



![](https://madewith.unity.com/sites/default/files/17_0.png?width=640&auto=webp&quality=80&disable=upscale)



#### Light it up.

We have found that one directional light per scene and sometimes an extra point light is about the limit of how far we can push it on mobile without dropping the frame rate. The reason that we try to use diffuse shaders as much as possible instead of unlit is so that we can use the realtime shadows from the directional light for when items in the scenes move around e.g. a secret spy console unfolding from behind a painting!

The scenes ambient light is usually set to a mid tone grey but sometimes I add a slight bit of colour in to tint things e.g. a bit of yellow to make the scene feel a bit warmer.

![](https://madewith.unity.com/sites/default/files/18_0.png?width=640&auto=webp&quality=80&disable=upscale)


#### Texturing.

The textures in the art style play a big part in creating the unique style. All textures are either from real photography, painted from scratch in Photoshop or a mix (PhotoChopped). The way that they are then applied to the object is via a channel inside Jason’s shader. We have 2 options that are then applied to all the various shaders (diffuse, unlit etc). The 2 options for texture blending are Multiply and Additive. Depending on the particular look I’m aiming to achieve I would select a shader that had either a Multiply or Additive channel and then drop my texture into the slot. This texture slot also has the 360 degree rotational slider and also a slider to control the strength of the Multiply or Additive texture blending. The Multiply/Additive slot could also be used with a gradient which would then be applied over the top of what ever texture you dropped into the base slot.

Here are some examples of how the shaders were used in the foyer scene:


![](https://madewith.unity.com/sites/default/files/19.png?width=640&auto=webp&quality=80&disable=upscale)



![](../../assets/5c51b747ef555c6c.png)



This is another code snippet from Jason’s shader to add in the extra texture slot for Multiply and Additive:

void surf (Input IN, inout SurfaceOutput o) {


// note: we combine textures in a single surface shader pass

half4 c = _Color * tex2D (_MainTex, IN.uv_MainTex); // base texture & colour

c *= (tex2D (_Multiply, IN.uv2_Multiply) * _MultiplyStrength) + (1.0f-_MultiplyStrength); // multiply texture

o.Albedo = c.rgb;

o.Alpha = c.a;

}

void surf (Input IN, inout SurfaceOutput o) {

half4 c = _Color * tex2D (_MainTex, IN.uv_MainTex); // base texture & colour

c += tex2D (_Additive, IN.uv2_Additive) * _AdditiveStrength; // additive texture

o.Albedo = c.rgb;

o.Alpha = c.a;

}

And finally here is the foyer scene art in game:

![](../../assets/71e207d3d59f7142.png)


#### Conclusion.

So there we have it, the entire step by step process to create the Agent A art style in Unity. We hope that you found this guide helpful in some small way! If you happen to take anything away from it, we’d love to hear from you, so please do say hello on Twitter!

Mark White [@elwhiteo](http://www.twitter.com/elwhiteo)

Jason Rawlings [@JasonRawlings](http://twitter.com/JasonRawlings)

More information on ‘Agent A: A puzzle in disguise’ can be found here: [www.agentagame.com](http://www.agentagame.com/)