---
title: Simonschreibt.
url: https://simonschreibt.de/wft/watchdog-gallery/
author: Simon
published: '2015-10-04'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

In theory you don’t need to create a gallery but I think it’s important to not only have a lot data but also have a good overview about it. Also it’s very important to be able to show other people a problem by just giving them an **URL** without having them crawling through folders.

![](../../assets/7346087424a920b7.png)


That’s why I wrote a second program which creates HTML files. Those you can easily watch or share their URL with colleagues to show them a particular problem.

The main gallery shows one thumbnail for each image collection we have. This gallery gives you a good impression of the color-variety of your game and sometimes you can see problems just by eyeballing some pictures for example if a whole planet is pink because its texture is missing or something like that.

You can even filter the gallery by typing something into the “Filter”-Field:

To create the gallery you have to iterate over all image-folders and create a DIV-Container per folder with latest image and the folder name as title. Some JavaScript can be used to improve the Gallery-Usability, but most of it isn’t mandatory (see the [JavaScript section below](https://simonschreibt.de#javascript)).

If you click a thumbnail, a new tab opens which brings you to the **sub gallery** (see below):

Here you see a sub gallery which contain some more features:

![](../../assets/43efb079cf81b2dc.png)


Most importantly you can see all the past screenshot-iterations in the thumbnail-section and you can hover over them to watch and compare them:

Pictures which were created at the same day are marked blue. The iteration which is currently shown as big picture is marked green.

![](../../assets/3246cd5868db4b51.png)


Per default the latest screenshot is selected and by hovering over another one you can compare them. If you want to **not** compare with the latest screenshot, then just click another one and it will be the new default.

Not only image data but also meta information like the FPS are shown (the data is read from the TXT files which were created along the images).

In addition you can see performance-bars left to each thumbnail and see how the performance developed over time.

Last but not least you can enter a FPS threshold and based on that the performance bars are colorized depending if the FPS raised or dropped:

Since we’re already reading the data from TXTs we are able to compare the latest FPS values with the ones in the past and send out warning mails if the performance raise/drop is too drastically. This systems needs some additional work and problems we observed are written down [here](http://simonschreibt.de/wft/watchdog-problems#performancemails).

![](../../assets/b46dad03cbe14493.png)


I used some JavaScript but most if it is for the core functionality not even necessary. I used:

[JQuery](https://jquery.com/)+[LazyLoad](http://www.appelsiini.net/projects/lazyload)to load the images only when you see them (by scrolling down)- A JQuery function to be able to filter the main gallery
- A simple swap image function which exchanges pictures and performance data in the sub gallery
- A function which colorises the FPS bars depending if the FPS dropped or raised
- A function which returns URL parameters (
[source](http://stackoverflow.com/questions/11582512/how-to-get-url-parameters-with-javascript))

Now we’re more or less done. We get mails when something is wrong and we’ve overview about the data. If you’re interested in getting known the problems we were facing during development, read the next section! :)