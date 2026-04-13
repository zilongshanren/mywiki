---
title: Firefox OS support lands in EnyoJS 2.2 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2013/03/firefox-os-support-lands-in-enyojs-2-2/
author: Jason Robitaille
published: '2013-03-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

![](../../assets/23065367f1f43b28.png)


Originally the app framework for HP webOS, the [Enyo framework](http://enyojs.com/) has since evolved into a full-featured cross-platform cross-device HTML5 framework for the modern web developer. Following the philosophy of reusing code and rapid quality development, Enyo uses an object-oriented encapsulation model, where you build components you can move around, extend upon, and reuse in a modular manner. Hiding the messy platform-specific quirks, if you code an Enyo app once, it’ll work the same in Internet Explorer, Firefox, Google Chrome, iOS, Android, etc. Now, with its latest v2.2 stable release it extended its [list of supported platforms](http://enyojs.com/docs/platforms/) to include Windows 8, Windows Phone 8, BlackBerry 10, and yes, Firefox OS!

*Introduction video/talk to what Enyo is.*

Back in January, I had the pleasure of attending one of the Firefox OS developer workshop events. After testing out Enyo on Firefox OS devices, a few issues were discovered, which I’m happy to say have since been fixed by my recent pull requests to Enyo’s open source repository. So if you’re wanting to use Enyo to create new apps, or even use existing Enyo apps on Firefox OS, below are a few things to keep in mind.

## Platform Detection

As much as much as Enyo aims to be platform-agnostic, sometimes you just need to know what you’re running on. The `enyo.platform`

JavaScript object is here to help in that regard. As a side benefit of the changes I made, if you’re running on Firefox OS, you get the `enyo.platform.firefoxOS`

property, which returns the OS version number (undefined property on other platforms). Thanks to this, you can do conditional changes and features just for Firefox OS:

```
if(enyo.platform.firefoxOS) {
//do super awesome Firefox OS-specific feature
}
```

![](../../assets/b76184eb73b0d918.png)


## The :active:hover Selector Workaround

Whenever a button or control in Enyo is pressed, it simply uses the “:active:hover” to change the styling and look in a pressed-state. However, Firefox OS doesn’t support this out of the philosophy that a finger is not a mouse (at least that’s how it was explained to me). After trying out a few potential workarounds, the easiest solution is by using events to fill in the gap.

The Enyo framework makes itself platform-independent by not only harnessing standard and custom browser events, but also by normalizing, and if necessary, synthesizing events into a standard predictable set of events that then occur on every device. These events include:

- down
- up
- tap
- move
- enter
- leave
- hold
- release
- holdpulse
- flick
- dragstart
- drag
- dragfinish
- drop
- dragover
- dragout

There are a variety of ways to approach the problem, but for simplicity’s sake, it’s easy to focus on the `down`

and `leave`

events. The `down`

event is whenever the mouse clicks down, or a finger touches down on a control, whereas the `leave`

event is when the mouse/finger moves off of the control. We can use the `down`

event to apply a CSS class, then the `leave`

event to remove the styling.

So let’s say, for example, we want to have some text highlighted when clicked/tapped. We could make a “Highlightable” control in the following fashion:

```
enyo.kind({
name: "Highlightable",
classes:"hl-text"
});
```

And define the CSS as:

```
.hl-text:active:hover {
background-color:yellow;
}
```

And then use the “Hightlightable” kind like this:

```
enyo.kind({
name: "App",
components: [
{
kind:"Highlightable",
content:"This is a simple example of text that highlights when clicked/tapped on."
}
]
});
new App().renderInto(document.body);
```

Now to enact our workaround for Firefox OS, we can modify the CSS to:

```
.hl-text.pressed, .hl-text:active:hover {
background-color:yellow;
}
```

From here, it’s a simple matter of adding and removing the `pressed`

class on the events. We can use `enyo.platform.firefoxOS`

to only apply the styling as needed. One little hitch: the [Firefox OS simulator](https://hacks.mozilla.org/2012/12/firefox-os-simulator-1-0-is-here/) does in fact support `:active:hover`

CSS selectors, as the mouse is in-use. Thankfully, we can further filter out the simulator from getting `pressed`

styling applied by checking the value of the `srcEvent.type`

property of the event data. The end result gets us this:

```
enyo.kind({
name: "Highlightable",
handlers: {
ondown: "highlight",
onleave: "unhighlight"
},
classes:"hl-text",
highlight: function(inSender, inEvent) {
if(enyo.platform.firefoxOS && inEvent.srcEvent.type !== "mousedown") {
this.addClass("pressed");
}
},
unhighlight: function(inSender, inEvent) {
if(enyo.platform.firefoxOS && inEvent.srcEvent.type !== "mouseout") {
this.removeClass("pressed");
}
}
});
```

## WebAppInstaller and the WebAppButton Component

To make the process of creating Firefox OS, [Firefox Marketplace](https://marketplace.firefox.com/), and Chrome Webstore apps easier for Enyo developers, the third-party [WebAppInstaller library](http://enyojs.com/gallery/#JayCanuck.WebAppInstaller) consolidates the various installation formats into a unified API with the ability to check if a webapp is installed and to install a hosted webapp. Furthermore, included in the library is an Enyo control called WebAppButton, which is an “Install” button that installs the current hosted webapp, and will either hide itself or turn into an “Update” button depending on the way you configure it.

To demo this functionality, there is [an installable Enyo sampler webapp](http://enyo2-sampler.canuckcoding.ca/) ([source code on GitHub](https://github.com/JayCanuck/enyo2-sampler-webapp))

![](../../assets/c1d8f7588ebb34a7.png)


![](../../assets/1770726fb1085f4f.png)


![](../../assets/01413e8b51a3b9a0.png)


Enyo 2.2 framework is available free under the Apache 2.0 license at [http://enyojs.com](http://enyojs.com/)

WebAppInstaller is available free under the MIT license at [https://github.com/JayCanuck/enyo-2-components/tree/master/webappinstaller](https://github.com/JayCanuck/enyo-2-components/tree/master/webappinstaller)

## About
[
Jason Robitaille ](http://twitter.com/JayCanuck)

A university student working towards a degree in computer science and a former Enyo framework intern, Jason is strongly focused on HTML5 web app development, with experience in webOS and cross-platform. Based in Winnipeg, Canada, he self-publishes his apps on [http://canuckcoding.ca](http://canuckcoding.ca) and regularly contributes to opensource projects on [GitHub](https://github.com/JayCanuck/).

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 6 comments

kataranMarch 6th, 2013 at 08:07Doug ReederMarch 6th, 2013 at 11:48burenMarch 6th, 2013 at 14:11Andre Alves GarziaMarch 6th, 2013 at 15:31Fawad HassanMarch 7th, 2013 at 01:04Robert Nyman [Editor]March 7th, 2013 at 01:21