---
title: Living on the Edge – new Adobe animation tool sparks necessary conversations
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2011/08/living-on-the-edge-new-adobe-animation-tool-sparks-necessary-conversations/
author: Chris Heilmann
published: '2011-08-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Adobe made quite some splash in the last days by releasing [Edge](http://labs.adobe.com/technologies/edge/), a Flash-like tool to create HTML5/CSS3/JS driven animations. There is a need for a tool like that and I for one am very happy to see that Adobe are recognising this. Other tools that try to tackle the same task are already around, with the yet to be released [Animatable](http://animatable.com/) being shown at quite a few conferences and [Radi](http://radiapp.com/) leading the way.

I am even happier that this sparked quite a conversation amongst the developer community – there are far too many truisms thrown around about HTML5 and CSS3, so anything that makes us re-evaluate the current state is a great idea.

Edge, [according to Adobe themselves has been downloaded 50,000 times in the first 24 hours](http://blogs.adobe.com/conversations/2011/08/adobe-edge-hits-50000-downloads-in-first-24-hours.html) and looks much like Flash used to a long time ago:

![Edge showing the wheel demo Edge showing the wheel demo](../../assets/b6f011119aa47a22.jpg)


The initial feedback was very polarised, whereas fans of Adobe products heralded this as a new dawn of standards-based animations, others were less impressed [as the UK based .net magazine reports](http://www.netmagazine.com/features/devs-respond-adobe-edge). This is to be expected, as everything with the HTML5 stamp these days gets that kind of treatment.

## So what is going on under the hood of Edge?

Anna Debenham was one of the first to have a go at [reviewing Edge](http://maban.co.uk/58) and having a play with it:

As you can see in the frame above, the animations generated with it are fixed in size (either pixels or ems) and all consist of a mix of JavaScript and CSS3 transitions. The engine behind the animations is jQuery. Looking it up in Firebug, we are faced with a lot of DIV elements with positioning and CSS transition information:

![firebugoutput](../../assets/3f34b248d4607ccc.jpg)


This is in stark contrast to tools that try to turn Flash into open technology solutions like the conversions done by Google’s [Swiffy](http://googlecode.blogspot.com/2011/06/swiffy-convert-swf-files-to-html5.html). Swiffy uses SVG to simulate the path-based nature of Flash; Edge doesn’t and relies on DOM animation of DIV elements instead.

## A total lack of HTML5 in the output

This caused the main confusion amongst developers and [sparked a longer discussion on the Adobe forums](http://forums.adobe.com/thread/884525) initiated by Rob Hawkes. The original problem Rob found with Edge is that it doesn’t use HTML5 technologies like Canvas or other W3C animation and painting technologies like SVG:

Why has Edge gone with div-based animation over other technologies like canvas and SVG? I was deeply saddened to see that not only were divs used in the example files that you released, but that divs are the default option for the stage and any other element that is added to it.


Adobe’s answer was that [animating DOM elements simply is faster](http://forums.adobe.com/message/3833054#3833054) and allows for more browser compatibility, especially on mobiles:

We seriously considered Canvas, but current performance on mobile browsers (especially iOS) is very bad. We didn’t want to have the first experience produce content that couldn’t run acceptably. Note that this may be changing in iOS 5, so that’s good. Finally, SVG can be a little slow, though we do support bringing in SVG elements and animating them – just not reach into them.


The performance argument is something that keeps cropping up in discussions. A lot of the animations by Google also moved DIV elements around rather than using Canvas and/or SVG (remember the [exploding balls logo](http://www.wait-till-i.com/2010/09/07/google-goes-bubbly-interactive-logo-today-on-the-uk-homepage-plus-source/)?) whilst sporting the HTML5 label.

HTML5 Games developer and co-organiser of the [onGameStart conference](http://ongamestart.com/) Kamil Trebunia, [questioned the concerns over Canvas being too slow on mobile devices](http://forums.adobe.com/message/3835209#3835209). The great news is that in a backchannel discussion on Twitter, Paul Bakaus, CTO of Zynga Germany pointed out that they are doing intensive research into the subject at the moment and [that they are happy to share the outcome at a later stage](http://twitter.com/#!/pbakaus/status/98407711699505152). So this is something very cool to look forward to and something to complement the [HTML5 games performance research by Facebook a few months ago](http://developers.facebook.com/blog/post/460/).

## Lack of semantics in the output

The other issue with Edge that puzzled developers is the HTML that gets generated. As [Morena Fiore](http://www.morenafiore.com/) asked with [her Edge demo](http://www.morenafiore.com/edge/why/) it seems weird that Adobe doesn’t use SVG and Canvas for animating when the output of the tool doesn’t feature any semantic HTML whatsoever:

The text content, the tweens and positioning and all the other information of the animation is in JSON objects instead:

[Adobe’s original answer](http://forums.adobe.com/message/3833002#3833002) to these concerns was that they don’t want to touch the original HTML as developers don’t like that:

Our approach is that we separate out the stuff you add from the underlying HTML *AND* we don’t try to edit the HTML in the way old-style tools did – in general a lot of people don’t like when tools muck with HTML.

That said, we will be looking at ways of trimming down the HTML that gets added to a page in the future if that’s what people want.


That sounds like a slippery slope to me. As Tobias Leingruber [showed in his firmly tongue-in-cheek demo done with Edge](http://tobi-x.com/adobe_edge_test/) a lack of semantics and enhancing existing markup just means that we now create Flash tunnel pages in a different technology and makes you wonder if the main use case of Edge would be interactive ads that are not blocked by Flashblockers.

This is a challenge that any tool faces: how do I not only allow people to create but also make them aware that web content is not only pretty moving pictures? The [Madmaninmation](http://animatable.com/demos/madmanimation/) demo of animatable is a great example — it is a pure animation but when you check the source code it falls back to a list with the script of the animation. This allows everybody to know what is going on and helps your product to be understood by search engines. Will every user of animatable go through that level of support for the web or simply create animations?

With Edge, Adobe has a chance to do a very cool thing for open web technologies. It will be interesting to see where it goes.

As Bruce Lawson of Opera put it:

Designers will require authoring tools that can help them turn their creativity into code, and Adobe have a great track record on making IDEs that designers find user-friendly.


So the ball is in Adobe’s court to do the right thing for the web and move Edge further along (with help from the research the discussion sparked). And they are well on the way and [declared that they are actively looking for feedback](http://forums.adobe.com/message/3832667#3832667):

Edge will be evolving rapidly – the product is by no means feature complete. We expect to add support for more and more of the HTML universe over time. Edge does currently support SVG graphics (you can File > Import an SVG image), but you can’t yet reach into those graphics and animate their components. The good news is that our JS runtime is capable of animations that include all sorts of HTML Elements, SVG Elements and even Canvas graphics, so we have not boxed ourselves in.

Which of these enhancements would you like to see Edge tackle first? Canvas? Embedded SVG? Ability to select HTML tags other than DIV?


I, for one am excited to see Adobe start to wave the flag of open web technologies higher than before. Their new [The Expressive Web](http://beta.theexpressiveweb.com/) showcase site is a proof of that. It is up to us now to cry foul at what they do or work side by side to bring the best experiences to the web for our users out there.

## About
[
Chris Heilmann ](http://christianheilmann.com)

Evangelist for HTML5 and open web. Let's fix this!

## 13 comments

bartazAugust 3rd, 2011 at 05:48Chris HeilmannAugust 3rd, 2011 at 07:48Mark AndersAugust 3rd, 2011 at 12:22Chris HeilmannAugust 3rd, 2011 at 16:04bartazAugust 3rd, 2011 at 08:17Chris ColemanAugust 3rd, 2011 at 10:33TobyAugust 4th, 2011 at 05:06Adrian TschubarovAugust 4th, 2011 at 06:41Chris LAugust 4th, 2011 at 06:44WebdesignAugust 4th, 2011 at 06:50DavidSeptember 14th, 2011 at 00:48Amanjeet SinghDecember 27th, 2011 at 23:02Mark AndersDecember 28th, 2011 at 00:31