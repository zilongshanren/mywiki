---
title: Prototyping a subcontinent scale sculpture in A-Frame – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2017/01/prototyping-a-subcontinent-scale-sculpture-in-a-frame/
author: Joel Lewis
published: '2017-01-11'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Back in 2016, I submitted a concept in response to the [British Council](https://www.britishcouncil.org/) call for entries to their [UK-India 2017 Digital Open Call](https://www.britishcouncil.org/arts/about/uk-india-2017-digital-open-call). Titled “A piece of Art as big as India”, the idea was to create an augmented reality sculpture that the people of India could not only view via mobile devices but sculpt themselves. As I said in the original proposal:


Imagine a virtual layer of silk as big as the subcontinent, seeming to float in the sky above…

![apieceofartasbigasindiasketch](../../assets/e10955b05db543e1.jpg)


I was keen to make the installation viewable on as many devices as possible and after receiving seed funding from the British Council to develop the idea, I researched several platforms that would allow that to happen. It quickly became clear that the most popular mobile phone OS in India was Android, so I started looking for libraries that would allow me to create augmented 3D content in real time. [A-Frame](https://aframe.io/) came to my attention via the [three.js](https://threejs.org/) community and after discovering a fantastic AR prototype by Mozilla employee [Dietrich Ayala](http://metafluff.com/), I knew that it was the perfect front-end library for this project:

AR with

[@aframevr]+ getUserMedia + Firefox on Android.[#quack][pic.twitter.com/ZXnkterwgu]— dietrich ayala (@dietrich)

[August 3, 2016]

I started [blogging about every step of the project](http://joelgethinlewis.com/category/projects/a-piece-of-art-as-big-as-india/), as well as [ sharing all my experiments on GitHub](https://github.com/JGL/APieceOfArtAsBigAsIndia/) and [GitHub pages](https://jgl.github.io/APieceOfArtAsBigAsIndia/). My friend [Ross Cairns](http://rosscairns.com/) helped me get my development environment set up, utilising A-Frame as well as the following technologies:

Via the [Awesome A-Frame collection on GitHub](https://github.com/aframevr/awesome-aframe), I discovered several different 3D landscape components. [Kevin Ngo](http://ngokevin.com/), one of the maintainers for A-Frame, had created a Mountain component fitted my requirements, and after chatting with him on the [A-Frame Slack](https://aframevr-slack.herokuapp.com/), he even led me through submitting my [first-ever pull request on GitHub](https://github.com/ngokevin/kframe/pull/9), to allow the component to be viewed from below as well as above.

Dietrich and I collaborated remotely to integrate his AR demo code with Kevin’s updated mountain component, eventually making a version for both [Android](https://jgl.github.io/APieceOfArtAsBigAsIndia/releaseAR.html) and [iOS](https://jgl.github.io/APieceOfArtAsBigAsIndia/releaseStaticPanorama.html). (Apple hasn’t implemented the `getUserMedia()`

in mobile Safari, so we had to use a static panorama instead.)

![2016_11_10_macbookprograb](../../assets/fc4baac8f186c47a.jpg)


The British Council conducted audience testing in India during the last weeks of November 2016 – unfortunately, I didn’t get through to the next stage of the project but I’ll be using A-Frame for all of my future online VR/AR projects and am very grateful to the entire A-Frame community for all their help and support.

## About
[
Joel Lewis ](http://www.joelgethinlewis.com)

Joel Gethin Lewis is an artist based in London. He is currently an associate lecturer on the MFA Computational Arts course at Goldsmiths University. A proponent of open source practices throughout society, he founded the interaction design meet-up This happened…. He is working on a series of web-based projects including a tool for self expression designed for people on the Autistic spectrum, Reactickles3.