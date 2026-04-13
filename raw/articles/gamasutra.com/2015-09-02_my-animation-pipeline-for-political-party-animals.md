---
title: My Animation Pipeline for Political Party Animals
url: https://www.gamedeveloper.com/art/my-animation-pipeline-for-political-party-animals
author: Ryan Sumo
published: '2015-09-02'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# My Animation Pipeline for Political Party Animals

I go over my pipeline for making and animating characters using Photoshop and 2Dtoolkit in Unity.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![](../../assets/1e4db3c65e581143.jpg)



As we inch ever slowly to a closed Alpha, we’re slowly building up our social media presence. If you haven’t already, please do follow us and spread the word on [Twitter](https://twitter.com/heypartyanimals) and [Tumblr](https://www.tumblr.com/blog/politicalpartyanimals). We’ve had a pretty good run of bi-weekly testing and for the first time last week the latest version of the game was played by people from outside the team. The results were encouraging, since both our friends Kyle and Gwen had fun playing (see Gwen's victorious pose), but there were definitely numerous things that we still have to work on.


In the meantime, let me show you my process for the creation and animation of our characters. [Previously](http://www.gamasutra.com/blogs/RyanSumo/20140510/217444/Why_I_chose_Hand_Drawn_Animations_over_Puppet_Animations_for_Party_Animals.php), I wrote about my decision to stick to frame by frame animation, mostly because it’s what I know best. Now I’ll go into a little bit more detail in the hopes that you guys might pick up a thing or two from it, or tell me why what I’m doing is terribly wrong. Let’s get started!

## Part 1 : Concept Sketches

![](../../assets/51edc0994526e7b0.jpg)



With each concept sketch I take an animal, assign its occupation, then make some sketches based on those two factors. So for example the Crow is meant to be an investigator or reporter that digs up or fabricates dirt on other candidates. I'll usually spend around 10 hours or so first looking at reference material then sketching out concepts and then coloring them in. If I had the time I would love to spend more time really doing a lot of concepts of each character but as it is I'm squeezing these in after work, which means an hour or two whenever I can find the time.

## Part 2: Vectorizing

![](../../assets/b38c5c2ef1d9bc8a.jpg)



After the conceptualization is done I pick out my favorite concept animal (this is harder than it looks, and sometimes I have to ask my wife to help me choose) and render it in vector. This is important in terms of efficiency because once the animal is in rendered this way it becomes much easier to resize it and use it for multiple purposes. It's also important for me to organize it properly in different layer folders.


So let's say for example that I wanted to make a character portrait for the Investigator. I could just take the body and head part, resize it, and voila! A portrait for the Crow Investigator! It's important for small teams to always keep in mind different ways that they can make work more efficient, which is something I learned having usually worked as the sole artist for many games!

## Part 3: Animate!

![](../../assets/ba029d46caea3bd2.gif)




Now this is the meaty part, the animation! We have a list of animations that each character has, for example we need animations for move, bribe, etc. for this one I will show you the move animation for the Invesigator. The first step is for me to sketch out a very small animation. I sketch it small so that I don't overthink the details and just try to get a good sense of movement going. I wanted him to be all sneaky like to fit his ability to fabricate scandals.


Once that's done I take the original vectorized image and then start making frames based on the smaller animation. If I have time I will go ahead and sketch out larger frame by frame animations as well, but I usually make do with using the small animation as a reference. This is where having separated the different body parts before is really key, as I can I much more easily pick out the body parts I want to animate and move them around rather than having to look through a whole mess of vector layers.


![](../../assets/d02873775029c550.gif)



In about 2-4 hours I will have something like this! I actually had quite a bit of trouble with this and had to refine the previous quick animation some more before I had an animation I was happy with.


![](../../assets/a81d67ec44327a53.jpg)




This is an image showing the frame by frame animation within photoshop, so you have a better idea of how many frames I use.

## Part 4 : Shrinkage

![](../../assets/08f2a67c7176b943.jpg)



Once again this is where doing everything in vector pays off, as I can easily shrink the different frames of animations, flatten them, give them an outline an then save them one by one as pngs for use in the game. We use 2dtoolkit for our animations, which I'm starting to realize may not be the best for a game with multiple animations. The file organization for 2dtoolkit seems pretty primitive, and you can easily be overwhelmed with the sheer amount of individual images. Right now we aleady use 213 sprites, and we're probably at 1/10 of the amount of animations we're planning to do.


![](../../assets/dbfed81a61de0a37.gif)



And finally here is the Investigator in action in the game! His special ability is to fabricate a scandal, which if it's revealed in the district will do massive damage to your opponents reputation.


Thanks for reading. If you have any suggestions about how I can streamline my process without overhauling it entirely I would definitely love to hear from you! To be one of the first people to try our closed alpha, please sign up for our [mailing list](http://heypartyanimals.us8.list-manage.com/subscribe/post?u=460bfede6e630535fc2e7f862&id=09725f1de6)!