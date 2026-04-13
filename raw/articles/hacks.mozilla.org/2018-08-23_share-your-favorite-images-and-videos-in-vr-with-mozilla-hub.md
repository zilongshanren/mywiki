---
title: Share your favorite images and videos in VR with Mozilla Hubs – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2018/08/share-your-favorite-images-and-videos-in-vr-with-mozilla-hubs/
author: Josh Marinacci
published: '2018-08-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Last April we released [Mozilla Hubs](http://hubs.mozilla.com/), a VR chat system that lets you walk and talk in VR with your friends, no matter where in the world they are. Now we [have a game changing new feature:](https://blog.mozvr.com/new-in-hubs-images-videos-and-3d-models/) you can share virtually any kind of media with everyone in your Hubs room by just pasting in a URL. Anything you share becomes a virtual object that everyone can interact with. From images to videos to 3D models, Hubs is the best way to collaborate across devices (laptops, phones, headsets) and OSes. Let’s look at a few details.

## What can I share?

Hubs supports the common image formats: PNG, JPG, and even animated GIFs.

![](../../assets/377b1c86505f8b57.png)


Hubs also supports streaming media files like MP3s and MP4s, as well as 3D models in GLB format (the compact binary form of [GLTF](https://en.wikipedia.org/wiki/GlTF)). And finally, Hubs has special support for content from certain websites.

If you paste in a URL to a model on [Sketchfab](https://sketchfab.com/) (an online community and marketplace of 3D artists and makers), Hubs will fetch the model and import it into the room, no extra work required. As long as the model is less than 100MB and marked as downloadable, the Hubs server will process the webpage to find the link to the actual 3D model and import only that. Hubs can also perform this same trick with URLs from [Giphy](https://giphy.com/), [Imgur](https://imgur.com/), [Google Poly](https://poly.google.com/) (only objects made in Blocks, not panoramas), and even [YouTube](https://www.youtube.com/) videos. The media is cached into the Hubs server before sending to Hubs clients.

### Is it secure?

Yes. When someone in your Hubs room pastes in a URL it does not immediately go to every client logged into the room. Instead the URL is processed by the Hubs server which hosts the encrypted media, sending only the validated data to the other clients. This helps to protect from [XSS attacks](https://en.wikipedia.org/wiki/Cross-site_scripting) as well.

The Hubs server will host all content for up to 48 hours after the last time it is accessed, so once everyone is done interacting with it, the media file will eventually disappear. It is never copied anywhere else. The server also encrypts the data, so only clients in your Hubs room can see it. Additionally, Hubs does not track logins, so content has no user-identifiable data that could be used for tracking.

### What can I do with content in Hubs?

You can pick up any kind of content object then move it, throw it, or leave it stuck in one place by holding still for a moment before releasing. If you have a 6DoF controller then you can also resize the object.

For audio and video you can click to play and pause the media stream. For PDFs you can advance one page at a time, making Hubs the best way to share presentations in VR, or just join your friends for some YouTube binging.

### Are there any other requirements?

Nope. Any content you have on the web you can share. Since the server acts as a proxy you don’t need to worry about CORS. If the content you want to share is not web accessible then you can upload the file directly to Hubs, which will then host and share it automatically. You can even use content from your public Dropbox folder. It all just works.

If you have content that you want to ensure users can share within Hubs, then just make it publicly accessible from the web in one of the file formats we support (as listed above). For data you don’t want to stay public permanently, you can serve up a randomly generated URL which expires after 10 minutes. Once the data is imported into the Hubs server it no longer needs to be accessible on the web.

### What now?

Play with it. Join your friends in a room to hang out, work on a presentation, or just watch some videos. All with real-time voice communication as well. As always, Hubs will work on any device with a browser, from 2D desktop to standalone VR headset to smartphone. Hubs will adapt to the device you have available. Just share a link to your room and go.

## About
[
Josh Marinacci ](https://joshondesign.com/)

I am an author, researcher, and recovering engineer. Formerly on the Swing Team at Sun, the webOS team at Palm, and Nokia Research. I spread the word of good user experiences. I live in sunny Eugene Oregon with my wife and genius Lego builder child.

## 10 comments

Jörg Holler CrofortAugust 23rd, 2018 at 13:59Josh MarinacciAugust 24th, 2018 at 10:16Não edvaldoAugust 25th, 2018 at 21:01Hector Gonzalez MontesAugust 23rd, 2018 at 20:06Guy EvrardAugust 24th, 2018 at 00:28DEV KUMAR TIWARIAugust 24th, 2018 at 00:48Yakob FantaAugust 24th, 2018 at 02:52AlexaAugust 25th, 2018 at 23:34Josh MarinacciAugust 27th, 2018 at 08:41IbonAugust 27th, 2018 at 03:27