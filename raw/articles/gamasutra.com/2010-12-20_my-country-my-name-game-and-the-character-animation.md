---
title: My Country, My Name game and the character animation
url: https://www.gamedeveloper.com/art/my-country-my-name-game-and-the-character-animation
author: Alexandre Sa
published: '2010-12-20'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# My Country, My Name game and the character animation

A small article about how Vortex Game Studio animation team did the My Country, My Name character animations... A little of their work, the problems and solutions.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

This is our first post here at Gamasutra, and we will talk a little about how we build and animated the My Country, My Name characters.

We did some tests with full traditional 2D animation in the alpha release, and the result was amazing but the work you need was very huge!!!

We are a small team, so we need to find a better and easy way to do that but we didn't like to lose the animation quality. In the traditional animation Zé was doing all the character animation ALONE! Yes just one guy doing all the 8 characters drawing each frame one by one, and the last time we talked about that he said, "dude, there more than 60 animations"... And we are talking about a standard animation, the artwork is vector but the animation was done in a very traditional way, with no bones...

One option was Flash and another one was to destroy all the characters in small pieces to mount again in a 3D software, doing something like this can help us to cut some time from the software development and in the animation but giving a very nice animation result.

![](http://blogs.vortexgamestudios.com.br/mycountrymyname/files/2010/09/engenheiro-separado-266x300.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Here the first test result... This art was done just for a small research to try our theory. I'll say, we lost probably one day to understand the best way to prepare the model... And wasn't a easy work -_-'

![](http://blogs.vortexgamestudios.com.br/mycountrymyname/files/2010/12/charshape.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Here is how we did all the characters, with LOTS of shapes with textures! :D

So, doing this we can keep the classic 2D game aspect like the oldies 16 or 32 bits games with all the easy animation features and flexibility of a 3D model!

![](http://blogs.vortexgamestudios.com.br/mycountrymyname/files/2010/09/Torque-ShowTool-Test-300x180.jpg?width=1280&auto=webp&quality=80&disable=upscale)


Yes, there something wrong there, but, we made it work!

That problem was caused by the wrong z-order, to solve this problem we build a custom Torque exporter to force the order from back to front... That was the biggest problem we had doing this.

And the final result was very good! and here a very nice animated gif done with bones and UVW manipulation.

![](http://blogs.vortexgamestudios.com.br/mycountrymyname/files/2010/09/mcmn-engineer.gif?width=1280&auto=webp&quality=80&disable=upscale)


Ok, we did everything work very fine, but, yes! MCMN is a 2D action game, and how I said early to save our time and our money (we are a small indie studio, we didn't have much money :'( hahaha) we are doing all animations in a 3D animation software. And you might be wondering, what the difference between the traditional 2D animation and this kind of animation with a 3D software... And here is the difference, we have 8 characters in the current beta demo, and in a traditional animation we have to do all the animations each time... and some of these animations are very similar! And in a 2D animation is almost impossible to use these similar animation in every character without re-animate each one... :(

So the solution is, build a common bone to use in every character and do all the animation in a 3D software, and it solved our problem and saved a month of traditional animation work! And there many other nice features with a 3D models like animation blend, we use this feature to create the transitions between the animations, mount to put weapons and items (we will use this feature to customize the characters in the final version) and many others!!!

So, I didn't found how can I embbed a YouTube video here, but in this link ([http://www.youtube.com/watch?v=hYKC7jfwRh4](http://www.youtube.com/watch?v=hYKC7jfwRh4)) you can see how we did the bones and all the engineer animations :)

Thanks for reading, post your comments or just say hi ;).

And follow our Twitter @MyCountryMyName and our Facebook page at [http://www.facebook.com/vortexstudios](http://www.facebook.com/vortexstudios) :D And you can check our devblog at [http://blogs.vortexgamestudios.com.br/mycountrymyname/](http://blogs.vortexgamestudios.com.br/mycountrymyname/)