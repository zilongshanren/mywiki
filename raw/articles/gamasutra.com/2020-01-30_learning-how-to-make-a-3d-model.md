---
title: Learning how to make a 3D model
url: https://www.gamedeveloper.com/art/learning-how-to-make-a-3d-model
author: Oliver Smith
published: '2020-01-30'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Learning how to make a 3D model

I recently made a new player character for my game, and since I'm a beginner at Blender I thought I'd share how that went as someone who is pretty new to 3D modelling.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![Learning how to make a 3D model in Blender Learning how to make a 3D model in Blender](../../assets/4e70de13cf09ca3c.png)



[This article was originally posted on my website, [Jellygon](https://www.jellygon.com/news/012920-astronaut-model/)]


I recently made a new player character for my game [Starsteaders](https://www.jellygon.com/starsteaders), and since I'm a beginner at Blender I thought I'd share how that went as someone who is pretty new to 3D modelling.

[Blender](https://blender.org) is a free and open source "3D creation suite", meaning it's a single program that can do pretty much everything you need to create 3D models and animations suitable for games. Over the years I've cobbled together a basic understanding of Blender from watching videos, but I've never felt very comfortable using it, so I decided to get a book as well. The book I got is ["Learning Blender" by Oliver Villar](https://www.amazon.com/Learning-Blender-Hands-Creating-Characters/dp/0134663462/). It's for an older version of Blender (pre-2.8), but whenever it said something wrong I just looked it up online. Getting this book was well worth it over just watching tutorial videos online (though doing that helped too). It looks like there's an updated edition of the book coming later this year, so be sure to check if you're reading this in the future. The main differences I saw are that Blender 2.8 overhauled some of the UI, and there's a newer rendering engine called Eevee that the book doesn't cover.

Getting started, the first thing was just to learn a bit about Blender's UI. Blender is some of the most complicated software I've ever used - basically nothing is intuitive, so you'll have to memorize lots of keyboard shortcuts and learn the proper terms for things. I definitely don't recommend just diving in and trying to figure things out. Instead, make a test file and spend a while just learning the interface and the basic modelling concepts. Understanding Blender's concept of an object and "object data" is enlightening (and too much to go into here).

Don't be discouraged, though - Blender is pretty well designed for what it does and it's honestly amazing that it's free and open source. Plus, you can press spacebar at any time to bring up a command search, which is incredibly useful when you don't even know the term for what you're looking for.

![Blender's command search Blender's command search](../../assets/a51ef0832da8008a.png)


## Pre-Production

As per the book, creating a 3D character actually starts outside Blender. The first step was to design and draw my idea in a 2D paint program. It's hard to overstate how helpful this step was, because when you're trying to learn some really complicated software the last thing you need is to also be making lots of decisions about what your model is supposed to look like. So don't slack on this step!

The first thing was to draw a bunch of silhouettes. The idea is that it's super fast to draw them, so you can iterate through a bunch of ideas quickly. Also, if your character is recognizable from just a silhouette, that can be a mark of good design. I'm not very comfortable drawing without a reference and I really wanted to stop after the 3rd one, but I forced myself to keep going anyway, and I'm glad I did because I think they improved over time.

![Character silhouettes Character silhouettes](../../assets/fa4d861dcb2198b7.png)


I wanted something that left a lot to the player's imagination, and that would look good from a distance, so I picked M even though it's not necessarily my favorite design.

Next, I fleshed out the design in detail. You could draw various action poses and clothing alternatives to make sure everything looks good, but eventually you want to end up with something like the below images that can be imported into Blender and used as a reference while you model. It's important to get everything lined up correctly because you'll actually be modelling directly over these images.

![Character reference images Character reference images](../../assets/5b72dc244a9af10b.png)


## Creating the 3D model

Next was to import the reference images into Blender and start modelling. I did this by creating a primitive like a cube or sphere, and then using Blender's various tools to add more and more vertices, nudging them around and extruding faces until it looked like a 3D version of my reference images. You only have to do one side of the body because Blender can automatically mirror your changes to the other side. For the most part, modelling wasn't too hard and was actually pretty fun, but I'm glad my character's face isn't visible because the helmet and hands were tough enough without having to do a nose, ears and eyes.

The trickiest part was getting the topology to be decent. Topology is the word for the specific layout of the vertices and polygon faces in the model. Basically, your model could look the same externally but have any number of different polygon arrangements. For instance, it could be made up of all triangles, or all quads (four-sided polygons), or it could have 5000 vertices or 100000 vertices. These topology choices can really affect how the model looks and animates, and I think understanding how to make good topology choices must come with experience because I had a lot of trouble with it. In particular, you're supposed to avoid triangles and only use quads, but sometimes you end up with a triangle and then it's really hard to get rid of it.

But eventually I had something I was fairly happy with!

![The finished model The finished model](../../assets/adbca350ce05e684.png)


## Adding colors and texture

To add colors and details to your character, you first have to "unwrap" your model, which is the process of assigning every vertex to a position in a 2D image. Each vertex gets a 2D coordinate called a UV (which is just the X and Y coordinates in the image, except they're called U and V instead). It's basically the same thing as taking a globe of the earth and turning it into a 2D wall map. You have to "unwrap" the sphere so that every position on the 3D earth has a corresponding position on the 2D map. If you can imagine that in reverse, then whatever you draw on the 2D map will show up in the corresponding position in 3D - that's how you draw details on the model.

Blender did most of this for me - you just give it a few hints, and tell it to unwrap, and it does a pretty good job. Then you can make adjustments by dragging pieces around and resizing parts you want to have more or less resolution in the image. Here's the map of every piece of my model to its UV position in 2D.

![UV map UV map](../../assets/dd479fbc76107352.png)


So now if I draw directly on the above image and tell Blender (or my game engine) to use it as a texture for my model, my drawing will show up in 3D. However, I found this to be much easier said than done. Because the map is flat and the 3D model has curves, if you want a straight line on the model, you might have to draw it as a weird curve in 2D. Anything you draw in 2D gets distorted in unexpected ways when mapped in 3D. So that was really frustrating and I think I need to do more research on best practices before I try again.

But I was able to stumble through, so here's my final texture map (the polygon outlines aren't there in the real version, this is just for demonstration purposes).

![Textured map Textured map](../../assets/1f3f3b5c1ea59b04.png)


And here it is applied to the model (note it's missing the logo on the chest because I just couldn't get it to look good).

![Textured image Textured image](../../assets/7e12aa82e5d7527a.png)


You can use the UV map for other things, too - it's just a way of relating a 2D texture to the 3D model. I also had Blender bake out an ambient occlusion texture that tells my game engine which parts of the character should have extra dark shadows at runtime.

## Rigging the model

In order to animate a 3D model, you have to "rig" it with something Blender calls an "armature". Basically, you create a skeleton for your character and tell Blender how each bone connects to the others and how they are allowed to move. This can get complicated, but the book I was reading led me through it pretty well and I mainly just re-created the rig from the book, minus the face parts.

You can see from my armature below how complex it got around the hands and feet, so having the book was very helpful here. Seeing the model I had created move was exciting! But it also revealed some problems - when the character moves in certain ways, you can see empty space between the torso and the legs! I hadn't thought to make sure every position would be fully covered in all poses. Also, my model probably needs more vertices in some areas to avoid weird jagged edges showing up when animating, but that's hard to go back and fix now. I think this is all the kind of thing you get better at with experience.

![Textured image Textured image](../../assets/151408e441094b78.png)


## Putting it in the game

I got to cheat a little bit here because I already have animations I made for my old player model (which was just a stick figure). Because all humanoid characters have more or less the same configuration (a head, two arms, two legs, etc), my game engine (Unity) is able to retarget an animation built for my old character to my new one. So I didn't need to make any new animations this time (but you can use Blender to do that too).

Unity can import the Blender file directly, which is convenient. I just had to do a bit of configuration to tell it which bones are which, and it all just worked. Any special materials/shaders you set up in Blender won't import into Unity, so I had to create a material or two, but I already knew how to do that.

Here's what it looks like in my game! My model definitely doesn't stand up to close scrutiny, but fortunately it's pretty small in my game so a lot of the flaws aren't noticeable. Overall I'm really happy with what I've learned and it has made the whole concept of modelling in Blender seem a lot more approachable.


[I'm an indie game developer and aspiring artist at [Jellygon](https://jellygon.com). If you want, follow me on Twitter at [@all_iver](https://twitter.com/all_iver).]