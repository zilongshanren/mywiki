---
title: Rapid XR Content Creation, from Reallusion, Pixologic and Noitom to Unity
url: https://www.gamedeveloper.com/art/rapid-xr-content-creation-from-reallusion-pixologic-and-noitom-to-unity
author: Gaspar Ferreiro
published: '2018-11-05'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Rapid XR Content Creation, from Reallusion, Pixologic and Noitom to Unity

A super-fast and easy way to prototype animated characters for Unity, using Reallusion, ZBrush and other common tools.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Being a studio these days means delivering the most challenging content ever created, on-budget, with completely unrealistic deadlines. To help others in our position, we would like to highlight some tools that are affordable, flexible and offer the best return on investment. Please note that like many of you we don’t have the luxury to throw an army of modelers, riggers and texture artists at a project, we work with solutions that empower us to deliver quality work FAST. Among the tools we will use: Reallusion’s [Character Creator](https://www.reallusion.com/character-creator/), ZBrush and Noitom’s Perception Neuron.

Step 1 – Let’s create our base hero using Reallusion’s Character Creator 3 (CC3)

This is the beginning of all things, and luckily one of the easiest parts of the process. In fact, when I describe this process to colleagues, I tell them is like the hero-creation process from an RPG Video Game. We start by selecting our base character (male or female), and then use the CC slider options to customize our hero.

![](../../assets/8f720e3ac5bcb113.img)


*Keep in mind that at this point I have not added any other accessories or character features like hair, because our intent is just to have a base character that we can export to another software.

Once we are happy with our base character, it is time to send her to ZBrush to give her some custom gear. To do this, you simply press the GOZ button in CC3, and then press GoZ on the window that pops up.

Step 2 – Let’s outfit our hero using ZBrush

Our hero won’t be very interesting to our players if she is just naked, so let’s build some gear! With our character imported into ZBrush, we will first subdivide the character so that we can sculpt or modify enough detail on our gear. (usually 4 to 5 sub-levels are good enough).

![](../../assets/3580c7a3f9724125.img)

![](https://eu-images.contentstack.com/v3/assets/blt740a130ae3c5d529/bltdc1ce10939abf783/650ea72ee473145507f1476f/gaspar3(1).png/?width=216&auto=webp&quality=80&disable=upscale)

![](../../assets/1fca6bfce90e5e27.img)


Look at that buttery-smooth character once it’s divided!

We will then use a mask in order to make clothing super-quick. Simply use your mask brush to shade the areas that you want to create clothes for. Also, don’t forget to activate "symmetry" if your clothes are symmetric.

Finally, we use the extract feature to extract an object that will be used as clothes. I recommend a number around .007 for thickness, but that can vary depending on your desired clothes. Once you like the result, remember to click accept, and the extracted sub-tool will appear. Turning off the visibility on the model will allow you to work faster on the clothes.

At this point you can sculpt and modify the clothes as much as possible. My advice is to soften the areas that have high countours from the model (usually chect, abs, and rear - but again, your final goal might not require to do this). Also, you can use masks to extrude parts of the body to make armor plating, or use the panels function.

One thing to keep in mind as you sculpt (specialy for game assets) is that smaller detials like cables, cords, etc.. can be done using texturing in other programs without having to add complexity to the geometry (this will be helpful when we optimize the clothing mesh). I personally like to work with the Move, Mask, Smooth, Inflate and Clay Buildup brushes.. but everyone has their own preferences. Another trick I use is just to mask areas I want to extrude armor from, invert the mast, and then scale it using the scale options, and holding the control key. For the purposes of this piece, I will stay with a very simple/raw piece. It is also a good idea to turn visibility on the original human model from time to time, to make sure you have not reduced the gear too much so it won't fit your model.

![](../../assets/0c706a7a53f31263.img)

![](../../assets/e3054d36d2bad2ba.img)


Once this is done, you will want to use decimation master so that you reduce the amount of ploygons for your gear, and once that is done you will generate UVS for this piece so that we can texture it correctly in other programs.

When you get this done, the next step is to do 2 things. One is to export out of ZBrush so you can textures it in your favorite texture program (I like Substance Painter), and the other part will be to use the GoZ button to send the clothing asset back to Character Creator.

As you make the transfer, make sure to adjust the position as needed, to make sure it’s aligned with the model. Then transfer skin weights, selecting default, so that the clothes conform to your character.

![](../../assets/70c9a6212c3d7876.img)


You can verify that this is done successfully by changing the pose of the character.

The next part is to take the clothing model that you exported out of ZBrush, and bring it for texturing in your preferred tool… Again, we will use Substance painter.

Step 3 – Let’s paint some textures

We won’t get too much into how to use substance painter, and some of the techniques to facilitate your texturing process, like exporting poly-painted textures from ZBrush to facilitate texturing, but we will definitely say that by just using fake UV geometry you can get a very simple piece of gear, and create the illusion of it being highly sculpted. Once done, just export your textures and bring them to Character Creator.

![](../../assets/3debd2d74e65aef9.img)

![](../../assets/4ce95d9d7eed16d4.img)


And once the textures are applied, you should end up with something like this. Then feel free to pose add hair to your character, etc.

Here is a final render of the character.

![](../../assets/4fb04827b051f1d3.img)


Step 4 – Time to get animated


As we mentioned earlier, we plan on using this character for a game, so it is only fitting that we add some animations. With that in mind, we will use the Character Creator button to send the model to Reallusion’s 3D tool, iClone (a good idea is to already have iClone open.) We will then use the tool’s Motion Live capability to select the capture devices to use to animate.

Once you have your animation recorded and selected, then you simply export the FBX and a folder will be created for everything you need (In this case, we selected unity since that is our target game engine).

Step 5 – Let’s get our game on!

The first thing we will do is drag the folder that iClone created into our Unity asset folder. Import the textures and materials, and then fix the materials with the right textures.


Once you have everything looking to your liking, then use your animator controller to set the animation, and test your scene.

![](../../assets/bc02de49714a9193.img)


And there you have it, a super-fast and easy way to prototype animated characters for Unity. For anyone who needs a deeper dive into [Character Creator 3](https://www.reallusion.com/character-creator/), Reallusion has a great overview video intended for the gaming community.

<iframe width="560" height="315" src="https://www.youtube.com/embed/t9MdeeAxi4U" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>

Gaspar Ferreiro is the Founder of [Project GHOST Studios](http://file:///C:/Users/Owner/Documents/Reallusion/projectghoststudios.com), an Atlanta-based VR/AR and game development firm whose work was recently featured at LeapCon.