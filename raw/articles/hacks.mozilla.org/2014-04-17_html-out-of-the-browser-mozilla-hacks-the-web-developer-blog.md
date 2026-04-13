---
title: HTML out of the Browser – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2014/04/html-out-of-the-browser/
author: Raymond Camden
published: '2014-04-17'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Amongst my friends, I’m known as something of a Star Wars nerd. My longtime nick has been cfjedimaster (a combination of two passions, the other being ColdFusion), I work in a room packed to the gills with Star Wars toys, and I’ve actually gotten inked up twice now with Star Wars tats. That being said, it was *another* movie that had the most influence on my current career – Tron.

![Tron_poster](https://hacks.mozilla.org/wp-content/uploads/2014/04/Tron_poster-250x373.jpg)


I had already discovered an interest in computers before then, but it was Tron that really crystallized the idea for me. All of sudden I imagined myself being the programmer – creating intelligent programs and dominating the grid. Yeah, I know, I was a nerd back then too.

My dreams, though, ran into reality rather quickly during my time as a Comp Sci major in college. First – I discovered that “Hey, I’m good at math!” means crap all when you hit Calculus 3, and secondly, I discovered that I really wasn’t that interested in the performance of one sort versus another. I switched to English as a major (always a good choice) but kept messing around with computers. It was during this time that I was exposed to Mosaic and the early web.

I quickly jumped into the web as – well – I’ll put it bluntly – easier programming than what I had been exposed to before. I can remember LiveScript. I can remember my first Perl CGI scripts. This wasn’t exactly light cycle coding but it was simpler, fun, and actually cutting edge. I’ve spent a good chunk of my adult life now as a web developer, and while I certainly have delusions of the web being a pristine environment, it has been good to me (and millions of others) and I’m loving to see how much it evolves over time.

One of the most fascinating ways that web technologies have grown is *outside* of the web itself. In this article I’m going to look at all the various ways we can reuse our web-based technologies (HTML, JavaScript, and CSS) in non-web based environments. While it would be ludicrous to say that one shouldn’t learn other technologies, or that web standards work everywhere and in every situation, I feel strongly that the skills behind the web are ones open to a large variety of people in different disciplines – whether or not you got that PhD in computer science!

## Mobile

This is typically the point where I’d discuss how important mobile is, but it’s 2014 and I think we’re past that now. Mobile development has typically involved either Java (Android) or Objective-C (iOS). Developers can also use web standards to build native applications. One solution is [Apache Cordova](http://cordova.apache.org) (AKA PhoneGap).

Cordova uses a web view wrapped in a native application to allow web developers to build what are typically referred to as *hybrid* applications. Along with providing an easy way to get your HTML into an app, Cordova provides a series of different plugins that let you do more than what a typical web page can do on a device. So for example, you have easy access to the camera:

```
navigator.camera.getPicture(onSuccess, onFail, { quality: 50,
destinationType: Camera.DestinationType.DATA_URL
});
function onSuccess(imageData) {
var image = document.getElementById('myImage');
image.src = "data:image/jpeg;base64," + imageData;
}
function onFail(message) {
alert('Failed because: ' + message);
}
```

You can also work with the accelerometer, GPS, contacts, the file system, and more. Cordova provides a JavaScript API that handles the communication to native code in the back end. Best of all, the same code can be used to build native applications for multiple different platforms (including [Firefox OS, now supported in Cordova & PhoneGap](https://hacks.mozilla.org/2014/02/building-cordova-apps-for-firefox-os/)).

To be clear, this isn’t a case of being able to take an existing web site and just package it up. Mobile applications are – by definition – completely different from a simple web site. But the fact that you can use your existing knowledge gives the developer a huge head start.

Another example of this (and one that is hopefully well known to readers of this site) is [Firefox OS](http://www.mozilla.org/en-US/firefox/os/). Unlike Cordova, developers don’t have to wrap their HTML inside a web view wrapper. The entire operating system is web standards based. What makes Firefox OS even more intriguing is support for *hosted* applications. Firefox OS is a new platform, and the chance that your visitors are using a device with it is probably pretty slim. But with a hosted application I can easily provide support for installation on the device while still running my application off a traditional URL.

Consider a simple demo I built called [INeedIt](http://ineedit.raymondcamden.com). If you visit this application in Chrome, it just plain works. If you visit it in a mobile browser on Android or iOS – it just works. But visit it with Firefox and code will trigger to ask if you want to install the application. Here is the block that handles this.

```
if(!$rootScope.checkedInstall && ("mozApps" in window.navigator)) {
var appUrl = 'http://'+document.location.host+'/manifest.webapp';
console.log('havent checked and can check');
var request = window.navigator.mozApps.checkInstalled(appUrl);
//silently ignore
request.onerror = function(e) {
console.log('Error checking install '+request.error.name);
};
request.onsuccess = function(e) {
if (request.result) {
console.log("App is installed!");
}
else {
console.log("App is not installed!");
if(confirm('Would you like to install this as an app?')) {
console.log('ok, lets try to install');
var installRequest = window.navigator.mozApps.install(appUrl);
installRequest.onerror = function() {
console.log('install failure: '+this.error.name);
alert('Sorry, install failed.');
};
installRequest.onsuccess = function() {
console.log('did it');
alert('Thanks, app installed!');
};
}
$rootScope.checkedInstall=true;
}
};
} else {
console.log('either checked or non compat');
}
```

Pretty simple, right? What I love about this is that the code is 100% ignored outside of Firefox OS but automatically enhanced for folks using that operating system. I risk nothing – but I get the benefit of providing them a way to download and have my application on their device screen.

![FF OS prompting you to install the app](../../assets/90f3e903481bb478.png)


## Desktop

Of course, there are still a few people who sit in front of a gray box (or laptop) for their day to day work. Many desktop applications have been replaced by web pages, but there are still things that outside the scope of web apps. There are still times when a desktop app makes sense. And fortunately – there’s multiple ways of building them with web standards as well.

So you know the code example I just showed you? The one where Firefox OS users would be given a chance to install the application from the web page? That *exact* same code works on the desktop as well. While still in development (in fact, the application I built doesn’t work due to a bug with Geolocation), it will eventually allow you to push your web based application both to a mobile Firefox OS user as well as the other billion or so desktop users. Here’s the application installed in my own Applications folder.

![INeedIt as a desktop app](../../assets/6383d69d72798499.png)


As I said though – this is still relatively new and needs to bake a bit longer before you can make active use of it. Something you *can* use right now is [Node Webkit](https://github.com/rogerwang/node-webkit). This open source project allows you to wrap Node.js applications in a desktop shell. Executables can than be created for Windows, Mac, and Linux. You get all the power of a “real” desktop application with the ease of use of web standards as your platform. There’s already a growing [list](https://github.com/rogerwang/node-webkit/wiki/List-of-apps-and-companies-using-node-webkit) of real applications out there making use of the framework – some I had even used before what realizing they used Node Webkit behind the scenes.

As an example, check out [A Wizard’s Lizard](http://www.wizardslizard.com/), a RGP with random dungeons and great gameplay.

## Native App Extensions

In the previous section we covered applications built with web standards. There are also multiple applications out there today, built natively, that can be *extended* with web standards. As a web developer you are probably already familiar with Firefox Add-Ons and Chrome extensions. There is an *incredibly* rich ecosystem of browser extensions for just about any need you can think of. What interests me however is the move to use web standards to open other products as well.

Did you know Photoshop, yes, *Photoshop*, now has the ability to extended with Node.js? Dubbed “Adobe Generator”, this extensibility layer allows for a script-based interface to the product. One example of this is the ability to generate web assets from layers based on a simple naming scheme. If you’ve ever had to manually create web assets, and update them, from a PSD, you will appreciate this. The entire feature though is driven by JavaScript and all makes use of a public API you can build upon. The [code, and samples, are all available via GitHub](https://github.com/adobe-photoshop/generator-core).

## What Next?

Coming from the perspective of someone who has been in this industry for *way* too long, I can say that I feel incredibly lucky that web standards have become such a driving force of innovation and creativity. But it is not luck that has driven this improvement. It is the hard work of many people, companies, and organizations (like Mozilla) that have created the fertile landscape we have before us today. To *continue* this drive requires all of us to become involved, evangelize to others, and become proponents of a web created by everyone – for everyone.

## About
[
Raymond Camden ](http://www.raymondcamden.com)

Raymond Camden is a developer for Adobe. His work focuses on client side development, mobile applications, Node.js and ColdFusion. He's a published author and presents at conferences and user groups on a variety of topics. Raymond can be reached at his blog (www.raymondcamden.com), @raymondcamden on Twitter, or via email at raymondcamden@gmail.com.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 14 comments

Brett ZamirApril 17th, 2014 at 04:59EvertApril 17th, 2014 at 10:07Brett ZamirApril 17th, 2014 at 16:39Evert PotApril 17th, 2014 at 16:52Brett ZamirApril 22nd, 2014 at 19:12Brett ZamirApril 22nd, 2014 at 19:45Raymond CamdenApril 17th, 2014 at 08:59Brett ZamirApril 17th, 2014 at 16:19Patryk ZawadzkiApril 18th, 2014 at 00:59Brett ZamirApril 22nd, 2014 at 19:40AdamApril 22nd, 2014 at 08:58Brett ZamirApril 22nd, 2014 at 19:15Robert Nyman [Editor]April 22nd, 2014 at 23:56MarcoMay 8th, 2014 at 13:55