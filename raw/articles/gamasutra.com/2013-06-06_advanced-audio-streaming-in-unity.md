---
title: Advanced Audio Streaming in Unity
url: https://www.gamedeveloper.com/audio/advanced-audio-streaming-in-unity
published: '2013-06-06'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

# Advanced Audio Streaming in Unity

In the midst of making a simple casual game as part of a personal jam, Ben Long and Fredrik Kaupang uncovered a great trick for streaming audio in Unity.

June 6, 2013

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

Author: by Fredrik Kaupang

In the midst of making a simple casual game as part of a personal jam, Ben Long and Fredrik Kaupang uncovered a great trick for streaming audio in Unity.

One of my favorite learning experiences is the game jam. I'm amazed how these events can teach you the entire spectrum of skills required in this industry. Where else can one get a feel for every aspect of game development in 48 hours?

The GGJ (Global Game Jam) should be mandatory for anyone interested in an industry career (including employees of larger studios). Aside from learning various disciplines, you get direct exposure to what a 'deadline' really is without the pressure of a multimillion dollar production. This becomes a time when creativity is the driving force, and good times are most certain to be had.

Recently, Fredrik Kaupang and I decided to dive right into development of a casual classic and complete it in one weekend. Although we missed the official GGJ event, it made sense to just run a marathon of our own. Since we live in different cities (Denver and Boston), everything happened entirely over Skype.

With the Chinese New Year right around the corner (and the 2013 Year of the Water Snake rapidly approaching), we had a waterproof plan: Make a classic Snake Game in Unity and localize it for both English and Chinese markets! The idea was certainly influenced by my talk at GDC China and the culture shock of seeing Shanghai for the first time, not to mention a lifelong interest in Chinese philosophy, food and kung-fu movies.

![Snake game screenshot Snake game screenshot](../../assets/966f19d89af58913.img)

We proceeded to capitalize on Unity's greatest strength, and set out to deploy our work on every platform possible. This article was almost a portmortem, since [Snake Game](http://www.snakegamestation.com) was ported to iOS, Android, Kindle, and the Chrome Store. Unfortunately, platforms and their owners aren't too fond of developers writing detailed articles about the submission process. Instead of going broad, we'll narrow focus: for this article, we will focus on the sonic side of things.

Snake Game is light on audio, so I was able to step out of my sonic comfort zone and work on art, HTML, and even get up to speed on platform requirements. I've been known to enjoy Photoshop/Illustrator, so it made sense to try my hand at game art. As an audio professional, it's a fun change to work with visuals, even though my skillset there is less flexible. Luckily, we built a sprite-based game where each component (snake body, head, tail and food) is a mere 44 x 44 pixels, and a gameplay background of 640x480 for web. These are our current sprites as of v1.2:

![simple game sprites simple game sprites](../../assets/7d4ef64d9e5536af.img)

Sure, they are crude, but there is something therapeutic about making pixel art. Coloring the giant blocks puts you in a meditative state, but also challenges you to think of the outcome. The time flew by as the sushi details improved, until finally I thought, "Okay! This might work!" It was a microscopic victory, so I posted the PSD to Dropbox and had Fredrik try a few before implementation. After Skype's file sharing became a hurricane of misplaced assets, the cloud-based sharing helped to bring a bit of organization. The pixel art world is deep, and next time I will try free tools like [this one](http://www.aseprite.org/), which is built for the task.

Once the initial web version ready, it was time to connect it with the ancient Chinese belief, which insists that people have a zodiac animal sign, and a specific element. Instead of making a Dragon game, which wouldn't be relevant for 11 years, we decided to make a re-skinnable snake game using the five elements of wood, metal, fire, earth, and water. We built the core game with flexibility in mind -- and the potential to create different gameplay elements for each Chinese element. The first step was to have a unique soundscape for each element game, so the water has an ocean soundscape, the earth has a distant lawnmower, etc.

Since we were making multiple versions of this game, it needed a place to live on the web, so I grabbed [snakegamestation.com](http://www.snakegamestation.com) and dove right in. Our goal was to get the web version stable and use it for porting to the various web app and mobile app stores.

Each of the six games has their own looping music track, which is an ambient soundscape and what I call "wallpaper music." When creating such pieces of music, I always start with a general theme that then goes through several revisions. This is a subtractive approach, where layers and parts get axed until the piece is not interfering with gameplay too much.

Usually, walking away from it for several days will reveal some element that feels too dense and detracts from the game. Each one is stripped away until the piece can easily fall into the periphery of the player. At least, that's how I would like it work!

The background pieces are a work in progress and I'm slowly but surely getting them online. There are also UI clicks, and event sounds for the snake appearance, eating and when leveling up. A death sound is triggered when you crash into the wall, or your very own snake-self. All of these sounds were small enough to be WAV files.

We decided to stream all the audio assets, to make them changeable on the fly, improving the overall soundscape. This allowed me to make ongoing updates to the audio via FTP uploads. It also freed up Fredrik from getting bombarded with constant audio revisions! The background music/ambient track is an OGG file, which is a format vastly superior to MP3 in sound quality, size, and looping capabilities. The background track was roughly 3.5 minutes in length and weighed in at a hefty 37.8 MB. An audio file this size would not be streamed efficiently, so it was converted to OGG, which reduced the size to 2.6 MB. I used [media.io](http://www.media.io), which is a free web-based audio conversion tool that inputs any standard audio file and coverts it to a wide range of formats.

Being able to change audio by simply uploading new files to FTP and audition them live was amazing. In the past, I have had to beg and plead for a way to hear my work in-game. With this setup, I can make creative changes while testing levels and EQ on a wide variety of computers. The built-in MacBook Pro speakers became the measuring stick, since they seem to faithfully represent the current state of consumer listening environments. This allows me to tweak and refine the sonic environment, forever! The streaming tech really blew my mind, and the possibilities for collaborations, are excellent. It's possibly the ultimate setup for game audio folks looking to hone their sound and get a feel for web playback.

The web streaming did introduce a few issues, as excepted. I noticed that sometimes, depending on the internet connection, the background sound track would play immediately when visiting the site, but often skip a bit. When I told Fredrik about this, he informed me that the streaming buffer was set to 5 percent, and we could increase that a bit for more a more stable playback. All in all, calculating a buffer of around 20 seconds usually does the job.

Fredrik explains the streaming code and buffering example:

"In order to make sure that our build size was as small as possible, we also decided to stream all the sound effects. While the initial build was 5.4 Mb, streaming the background music made the game 1 mb. After streaming all the sound effects at runtime, the initial download size of the Wall Snake landed at 528 kb (!). Success."

Working with audio in Unity can be a daunting task, especially when dealing with some of the lower level audio functions, or callbacks. However, we organized the audio mainly into two scripts. First, have a look at the stream_audio.js:

We realized while deploying a build to the server that the audio didn't loop at all, even though the audio.loop is set to true. This was only the case when streaming the audio, so I did some simple debugging, and found a workaround. Since the Chinese Wall track is mostly ambient at the looping point, and does not require sample accurate looping, the solution was more than ideal:

To change which game is currently deployed, we simply change the AllAppInfo.reskin_type, and the correct audio track will be streamed. Certainly, setting the audio.loop = true, could be called after the www request is finished streaming, and loaded into memory. This might solve the looping problem, and look like this:

yield (www);

audio.loop = true;

FTP streaming has been working out very well, and for shorter audio tracks, it might be well worth to set the streaming percentage to 20-25 percent of the track length, or calculate 20 seconds of the total track, which equals 882,000 samples at 44.100.

The streaming of the SFXs was slightly more complex, and the SFXManager.js script is slightly more brain teasing, yet very simple to manage. For any Composer/Sound Designer it's a dream come true when sound design can be swapped and tested in real time. Which, for us, deploying and maintaining 6 Snake Games of various character yields for a strong pipeline. For a simple game like this, we organized the audio clips as enums. As they might change later, it will be useful to reference them by enum name, rather than a non-contextual number in other scripts:

![code snippet enum declaration code snippet enum declaration](../../assets/d89820acf6e2504e.img)

When we had a list over all the audio clips, and their respective type, we wanted to stream them by order, so we could prioritize them based on usage in the game. Hopefully, the Game Over sound is the last sound you hear, but could also be among the first!

We kept all the audio volumes in the game constant at 1.0, so they could easily be mastered and adjusted in Pro Tools by Ben. It will most certainly result in a higher audio quality than adjusting the volume by the Unity built-in volume controller, thus ideal for any 2D game. The script creates an array of AudioClips, and stores them into memory once streamed, based on the prioritized order. This is the remainder of the script:

Similar to the audio streamer script, it also selects the SFX based on which game is selected. However, in this case, the streaming should be set to false:

www.GetAudioClip (false, false, AudioType.OGGVORBIS);

When loaded into memory, it'll avoid popping and other artifacts that could appear when streaming. The AUDIO_TYPES[_index] section can be expanded to include any types, though we decided to stick with .ogg and .wav for SFX. It's possible to add another else that points to AudioType.unknown as a fallback. I encourage playing around with these functions and implementing them in your own games. Call up your local sound designer and reskin those audioscapes!

The last section of this script is a Game Jam nugget. Right, because there's little time to set up a proper audio manager during a GJ, and a quick solution is a great timesaver. For the last Game Jam, I managed to implement more than 10 sound effect into our game in the last 15 min of the jam. The code looked more similar to this:

static function PlayAudio (_clip : String) {

ourAudio.PlayOneShot(Resources.Load("SFX/" + _clip), 1.0);

}

The great benefit about the function above, is that it can be called from any other script. Simply name the script above SFXManager and add it to a singleton object. You can call it from any other scripts:

SFXManager.PlayAudio("start_game");

This assumes that you have already created a folder named SFX under the Resources folder, and that you create a reference to a static AudioSource from the Awake() function.

All in all, the audio system works very well, and has great potential to be extended further. As a challenge, we would love to hear your suggestions for improvements. Some useful improvements that came to our minds:

Swapping between two or three audio sources to risk any audio cutoffs

Adding fallback sounds if the current audio is not currently streamed yet

A block of code that makes the script recognize the audio type on the server


We encourage you to explore, as there are endless possibilities here. If you have not dug into Unity audio, or audio steaming for web yet, this is the perfect time. We decided to share these scripts with you, so you can get both the stream_audio.js and SFXManager.js

Feel free download the scripts by clicking [here](http://www.snakegamestation.com/AudioScriptExamples.zip).

This article first appeared on the Game Audio 101 [here](http://gameaudio101.com/Unity-Audio-Streaming.php).