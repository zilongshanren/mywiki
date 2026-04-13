---
title: Enhance your HTML5 app with audio. – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/04/enhanceyourhtml5appwithaudio/
author: Joe Stagner
published: '2012-04-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When we think of sound in an HTML application we might think of two things: We remember all those sites that started playing loud obnoxious background music when the page loads and then we think about music playing apps.

Sound can however be much more: when building immersive app experiences it can be a crucial attribute. It can enhance tactile feedback or communicate activity or changes in state to the user. A ping sound when a new email arrives or a dismissive sound when there was an error can make things much more obvious for the end user.

Prior to HTML5 most developers had to resort to plug-in technologies like Flash, Quicktime, Real player or Windows Media Player to play audio. These, of course, required that these technologies were installed on the users’ machines and the plugins being active.

With HTML5, we have an [audio element](https://developer.mozilla.org/en/HTML/Element/audio) that natively supports sound playback. As with any HTML element, you can even play nice with older technologies by providing fallback content. For example by simply linking to the audio file:

```
```

As not all browsers support the same audio formats (MP3 not being a free format makes it impossible to decode it in an open source browser) you can provide the same audio in different formats:

Example:

```
```

If you really need to provide a player for all browsers – including the ones that don’t understand HTML5 – [I collected some information in this blog post](http://www.misfitgeek.com/2011/08/play-sound-in-html5-and-cross-browser-support-with-backward-compatability/).

When your application checked that HTML5, Canvas and all the other things needed for your functionality is supported then backward compatibility is less of a concern, however you may still have cross-browser compatibility concerns since browser vendors are not fully converged on common feature implementation. That said, [basic support for audio is available across all major browsers](http://caniuse.com/#feat=audio).

You don’t need to have an audio element in your HTML, you can also create them on the fly in your JavaScript:

```
var aSound = document.createElement('audio');
aSound.setAttribute('src', 'PlayMe.ogg');
aSound.load()
```

However, there may be advantages to using the `<audio>`

tag in your HTML.

- Using the tag adds to the semantic integrity of your markup.
- It makes your code easier to read and understand.
[The](http://www.w3schools.com/html5/att_audio_controls.asp)so the user can play the audio and seek in it with native controls that are also keyboard accessible`<audio>`

tag can display controls- The
`<audio>`

tag has an optional`preload`

attribute that tells to the browser to load the audio before users start playing it. - Browsers have a distinct loading sequence of referenced assets. By leveraging that sequence, it iss possible for you to help improve the performance of your app.

Here are some examples for using the `<audio>`

tag in HTML5.

```
```

In this instance the audio element is not visible and MySound.ogg will only be played by calling the play method on the element instance.

```
document.getElementById('MySound').play();
```

By adding a `controls`

attribute you can display the player controls so that the user can play the audio file by interacting with them.

```
```

These controls differ from browser to browser and operating system to operating system, but all have the same features as shown in the following image:

![audio player with controls](https://hacks.mozilla.org/wp-content/uploads/2012/04/audiotagplayercontrols-250x45.png)


You can easily hide or display the audio element’s controls whenever appropriate (like when the UI state changes) with a simple bit of JavaScript:

```
var myAudio = document.getElementById( "TimerBellSound" );
if ( myAudio.hasAttribute("controls") ) {
myAudio.removeAttribute("controls") ;
}
else {
myAudio.setAttribute("controls", "controls")
}
```

[As Terrill Thompson explains in his blog post HERE](http://terrillthompson.com/blog/32), we can easily create a custom player as well. Not only does this provide us with the flexibility of defining our own user interface but it lets us address accessibility concerns as well. His player looks like this and has a consistent look and feel across browsers and operating systems:

![](https://hacks.mozilla.org/wp-content/uploads/2012/04/customhtml5audiocontrol-250x28.png)


So what could sound do in your app? As an example, consider the follow application prototype:

![](https://hacks.mozilla.org/wp-content/uploads/2012/04/TimerPreview-500x296.png)


This application will be a timer for athletes. When in use, the athletes won’t be sitting in front of the device that is running the app. It will be running on their computer, tablet or phone and, while they may glance at it to check the time, for the most part they will rely on audible feedback for when to start working out, when to rest, and when to increase or decrease the intensity of their workout.

The audio element in HTML5 makes adding sound to your app both easy and straight forward.

## 3 comments

MardegApril 5th, 2012 at 08:52Justin DolskeApril 5th, 2012 at 11:37Ken SaundersApril 12th, 2012 at 14:30