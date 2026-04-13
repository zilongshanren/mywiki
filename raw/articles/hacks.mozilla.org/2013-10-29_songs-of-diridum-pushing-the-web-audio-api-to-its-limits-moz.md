---
title: 'Songs of Diridum: Pushing the Web Audio API to Its Limits – Mozilla Hacks
  - the Web developer blog'
url: https://hacks.mozilla.org/2013/10/songs-of-diridum-pushing-the-web-audio-api-to-its-limits/
author: Tom Söderlund
published: '2013-10-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When we at [Goo Technologies](http://www.gootechnologies.com) heard that the Web Audio API would be supported in an upcoming version of Mozilla Firefox, we immediately started brainstorming about what we could build with that.

We started discussing the project with the game developers behind “Legend of Diridum” (see below) and came up with the idea of a small market place and a small jazz band on a stage. The feeling we wanted to capture was that of a market place coming to life. The band is playing a song to warm up and the crowd has not gathered around yet. The evening is warm and the party is about to start.

We call the resulting demo [“Songs of Diridum”](http://www.gooengine.com/mozilla-web-audio-demo-built-in-goo-engine/).

## What the Web Audio API can do for you

We will take a brief look at the web audio system from three perspectives. These are game design, audio engineering and programming.

From a game designer perspective we can use the functionality of the Web Audio API to tune the soundscape of our game. We can run a whole lot of separate sounds simultaneously while also adjusting their character to fit an environment or a game mechanic. You can have muffled sounds coming through a closed door and open the filters for these sounds to unmuffle them gradually as the door opens. In real time. We can add reflecting sounds of the environment to the footsteps of my character as we walk from a sidewalk into a church. The ambient sounds of the street will be echoing around in the church together with my footsteps. We can attach the sounds of a roaring fire to my magicians fireball, hurl it away and hear the fireball moving towards its target. We can hear the siren of a police car approaching and hear how it passes by from the pitch shift known as doppler effect. And we know we can use these features without needing to manage the production of an audio engine. Its already there and it works.

From an audio engineering perspective we view the Web Audio API as a big patch bay with a slew of outboard gear tape stations and mixers. On a low level we feel reasonably comfortable with the fundamental aspects of the system. We can work comfortably with changing the volume of a sound while it is playing without running the risk of inducing digital distortion from the volume level changing from one sample to another. The system will make the interpolation needed for this type of adjustment. We can also build the type of effects we want and hook them up however we want. As long as we keep my system reasonably small we can make a nice studio with the Web Audio API.

From a programmer perspective we can write the code needed for our project with ease. If we run into a problem we will usually find a good solution to it on the web. We don’t have to spend our time with learning how to work with some poorly documented proprietary audio engine. The type of problem we will be working with the most is probably related to how the code is structured. We will be figuring out how to handle the loading of the sounds and which sounds to load when. How to provide these sounds to the game designer through some suitable data structure or other design pipelines. We will also work with the team to figure out how to handle the budgeting of the sound system. How much data can we use? How many sounds can we play at the same time? How many effects can we use on the target platform? It is likely that the hardest problem, the biggest technical risk, is related to handling the diversity of hardware and browsers running on the web.

## About Legend of Diridum

This sound demo called “Songs of Diridum” is actually a special demo based on graphics and setting from the upcoming game [“LOD: Legend of Diridum”](http://www.lodsaga.com). The LOD team is led by the game design veteran Michael Stenmark.

LOD is an easy to learn, user-friendly fantasy role playing game set on top of a so called sandbox world. It is a mix of Japanese fantasy and roleplaying games drawing inspiration from Grandia, Final Fantasy, Zelda and games like Animal Crossing and Minecraft.

The game is set in a huge fantasy world, in the aftermath of a terrible magic war. The world is haunted by the monsters, ghosts and undead that was part of the warlocks armies and the player starts the game as the Empire’s official ghost hunter to cleanse the lands of the evil and keep the people of Diridum safe. LOD is built in the Goo Engine and can be played in almost any web browser without the need download anything.

## About the music

The song was important to set the mood and to embrace the warm feeling of a hot summer night turning into a party. Adam Hagstrand, the composer, nailed it right away. We love the way he got it very laid back, jazzy. Just that kind of tune a band would warm up with before the crowd arrives.

## Quickly building a 3D game with Goo Engine

We love the web, and we love HTML5. HTML5 runs in the browser on multiple devices and does not need any special client software to be downloaded and installed. This allows for games to be published on nearly every conceivable web site, and since it runs directly in the browser, it opens up unprecedented viral opportunities and social media integration.

We wanted to build Songs of Diridum as a HTML5 browser game, but how to do that in 3D? The answer was WebGL. WebGL is a new standard in HTML5 that allows games to gain access to hardware acceleration, just like native games. The introduction of WebGL in HTML5 is a massive leap in what the browser can deliver and it allows for web games to be built with previously unseen graphics quality. WebGL powered HTML5 does not require that much bandwidth during gameplay. Since the game assets are downloaded (pre-cached) before and during gameplay, even modest speed internet connections suffice.

But building a WebGL game from scratch is a massive undertaking. The [Goo Platform](http://www.gooengine.com) from Goo Technologies is the solution for making it much easier to build WebGL games and applications. In November, Goo Create is released making it even more accessible and easy to use.

Goo is a HTML5 and WebGL based graphics development platform capable of powering the next generation of web games and apps. From the ground up, it’s been built for amazing graphics smoothness and performance while at the same time making things easy for graphics creators. Since it’s HTML5, it enables creators to build and distribute advanced interactive graphics on the web without the need for special browser plugins or software downloads. With Goo you have the power to publish hardware accelerated games & apps on desktops, laptops, smart TVs, tablets or mobile devices. It gives instant access to smooth rich graphics and previously unimagined browser game play.

**UPDATE:** Goo Technologies has just launched their interactive 3D editor, [Goo Create](http://www.gootechnologies.com/products/create/), which radically simplifies the process of creating interactive WebGL graphics.

## Building Songs of Diridum

We built this demo project with a rather small team working for a relatively short time. In total we have had about seven or so people involved with the production. Most team members have done sporadic updates to our data and code. Roughly speaking we have not been following any conventional development process but rather tried to get as good a result as we can without going into any bigger scale production.

The programming of the demo has two distinct sides. One for building the world and one for wiring up the sound system. Since the user interface primarily is used for controlling the state of the sound system we let the sound system drive the user interface. It’s a simple approach but we also have a relatively simple problem to solve. Building a small 3D world like this one is mostly a matter of loading model data to various positions in 3D space. All the low level programming needed to get the scene to render with the proper colors and shapes is handled by the Goo Engine so we have not had to write any code for those parts.

We defined a simple data format for adding model data to the scene, we also included the ability to add sounds to the world and some slightly more complex systems such as the animated models and the bubbly water sound effect.

The little mixer panel in which you can play around with to change the mix of the jazz band is dynamically generated by the sound system:

![](../../assets/30af03a6fe3e7903.png)


Since we expected this app to be used on touch screen devices we also decided to only use clickable buttons for interface. We would not have enough time to test the usability of any other type of controls when aiming at a diffuse collection of mobile devices.

### Using Web Audio in a 3D world

To build the soundscape of a 3D world we have access to spatialization of sound sources and the ears of the player. The spatial aspects of sounds and listeners are boiled down to position, direction and velocity. Each sound can also be made to emit its sound in a directional cone, in short this emulates the difference between the front and back of loudspeaker. A piano would not really need any directionality as it sounds quite similar in all directions. A megaphone on the other hand is comparably directional and should be louder at the front than at the back.

```
if (is3dSource) {
// 3D sound source
this.panNode = this.context.createPanner();
this.gainNode.connect(this.panNode);
this.lastPos = [0,0,0];
this.panNode.rolloffFactor = 0.5;
} else {
// Stereo sound source “hack”
this.panNode = mixNodeFactory.buildStereoChannelSplitter(this.gainNode, context);
this.panNode.setPosition(0, this.context.currentTime);
}
```


The position of the sound is used to determine panning or which speaker the sound is louder in and how loud the sound should be.

The velocity of the sound and the listener together with their positions provide the information needed to doppler shift all sound sources in the world accordingly. For other worldly effects such as muffling sounds behind a door or changing the sound of the room with reverbs we’ll have to write some code and configure processing nodes to meet with our desired results.

For adding sounds to the user interface and such direct effects, we can hook the sounds up without going through the spatialization, which makes them a bit simpler. You can still process the effects and be creative if you like. Perhaps pan the sound source based on where the mouse pointer clicked.

### Initializing Web Audio

Setting up for using Web Audio is quite simple. The tricky parts are related to figuring out how much sound you need to preload and how much you feel comfortable with loading later. You also need to take into account that loading a sound contains two asynchronous and potentially slow operations. The first is the download, the second is the decompression from some small format such as OGG or MP3 to arraybuffer. When developing against a local machine you’ll find that the decompression is a lot slower than the download and as with download speeds in general we can expect to not know how much time this will require for any given user.

### Playing sound streams

Once you have a sound decompressed and ready it can be used to create a sound source. A sound source is a relatively low level object which streams its sound data at some speed to its selected target node. For the simplest system this target node is the speaker output. Even with this primitive system, you can already manipulate the playback rate of the sound, this changes its pitch and duration. There is a nice feature in the Web Audio API which allows you to adjust the behaviour of interpolating a change like this to fit your desires.

### Adding sound effects: reverb, delay, and distortion

To add an effect to our simple system you put a processor node between the source and the speakers. us audio engineers wants to split the source to have a “dry” and a “wet” component at this point. The dry component is the non-processed sound and the wet is processed. Then you’ll send both the wet and the dry to the speakers and adjust the mix between them by adding a gain node on each of these tracks. Gain is an engineery way of saying “volume”. You can keep on like this and add nodes between the source and the speakers as you please. Sometimes you’ll want effects in parallel and sometimes you want them serially. When coding your system its probably a good idea to make it easy to change how this wiring is hooked up for any given node.

## Conclusion

We’re quite happy with how “Songs of Diridum” turned out, and we’re impressed with the audio and 3D performance available in today’s web browsers. Hopefully the mobile devices will catch up soon performance-wise, and HTML5 will become the most versatile cross-platform game environment available.

Now go [play “Songs of Diridum”](http://www.gooengine.com/mozilla-web-audio-demo-built-in-goo-engine/)!

## About
[
Tom Söderlund ](http://www.gooengine.com)

Digital jack-of-all-trades and overall fixer at Goo Technologies, currently working with growth and special projects.

## About Marcus Krüger

Founder & Executive Chairman of Goo Technologies. Loves the web. Tireless globetrotter.

## About Michael Stenmark

Game designer veteran and head of the game developer Cloud Engine Studios, now fast at work on building ["Legend of Diridum"](http://www.lodsaga.com/).

## About Oskar Åsbrink

Hacker, sound engineer, and game designer all wrapped in one package. Developer on the Goo team. Building a web-based flight simulator for the ancient Swedish jet "Tunnan" in his spare time.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 18 comments

phi2xOctober 29th, 2013 at 12:19Chris WilsonOctober 30th, 2013 at 01:19poochyenaOctober 29th, 2013 at 14:36Tom SöderlundOctober 30th, 2013 at 01:30WoolyssOctober 30th, 2013 at 15:41VeryNiceOctober 30th, 2013 at 17:41AlexOctober 31st, 2013 at 09:33JoaquínNovember 1st, 2013 at 07:16TomNovember 2nd, 2013 at 10:13MikeNovember 3rd, 2013 at 15:36Sam LillekerNovember 6th, 2013 at 03:26JoaquínNovember 6th, 2013 at 10:57GreenGeneNovember 6th, 2013 at 11:58Tom SöderlundNovember 6th, 2013 at 14:12ccchipsNovember 7th, 2013 at 09:45NenadNovember 12th, 2013 at 09:58Brad IsbellNovember 12th, 2013 at 20:30JoaquínNovember 18th, 2013 at 02:21