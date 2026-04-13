---
title: A DIY Guide to Optimizing SFX for Mobile and Web (For Non-Audio Nerds)
url: https://www.gamedeveloper.com/audio/a-diy-guide-to-optimizing-sfx-for-mobile-and-web-for-non-audio-nerds-
author: Game Developer
published: '2012-03-05'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# A DIY Guide to Optimizing SFX for Mobile and Web (For Non-Audio Nerds)

Optimizing File space, while still maintaining quality. Plus Other fun Stuff. Includes links for a free audio editor, and a SFX file to follow along with.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

A DIY Guide to Optimizing SFX for File Space, and Quality

- For Non-Audio Nerds

By: Daniel

-------------------------------------------------------------------

This is a basic guide for optimizing File space, while still maintaining quality. I feel this is something all Indie developers should be conscious about when working with Web, or mobile devices, as it could be drop the total download, and load time of your game drastically.

This is also something that can help you if you are trying to fit more things in your game, such as pictures, or more music files.


Total Time To Complete : ~40 mins

-------------------------------------------------------------------

Includes

- Basic Audio Trimming, and Fades

- Time Stretching, and Pitch Shifting.

- Adding Reverbs

- Normalizing Audio

- Resampling Audio bitrates

- Exporting SFX to Various File Formats (Including tips on sample rates for optimum space)

- Various ways to convert SFX from stereo to mono (for further space saving)

-------------------------------------------------------------------

Things Needed

Audacity - Free Audio Editor - [Download Link Here](http://audacity.sourceforge.net/)

A SFX File to Edit - [Download Here](http://www.affordableaudio4everyone.com/AudioTutorials/Weaponry_EMP_Blast_06.wav) (Right Click - Save As)

-------------------------------------------------------------------

Basic Audio Trimming and Fades

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/01.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- Here is a picture of the file download above in Audicity. A couple things you might notice is it is a stereo file by the dual waveform, and in the upper left corner you will see that it is 96000 kHz sample rate.

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/02.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- If you look here you can see that this file has an extra long tail, and a big portion of it isn't really needed.

- If you play the file you may hear the audio in the above darkened region, and you may not.... It is depending on how much Bass frequency your speakers will play. For mobile devices, there is usually almost no Bass, and this extra space is using up a massive 3 whole seconds of wasted space... So to get rid of this, just select the region, and cut it using ctrl X, or command X.

- (Note: If you are cutting out access audio, you should try to do it at the beginning or end of the sfx, unless you are skilled in audio clean-up.)

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/03.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- Now that you have cut out the extra tail in the file, the waveform now quickly cuts off at the end from a volume that can be heard to nothing. You don't want this, as it will be noticable. so you are going to select an appropriate amount of space to do a fade out.

- In this example I went with about a second, as the waveform has a very long tail. (The shorter the tail, the less the fade needs to be)

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/04.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/05.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- In order to do a fade out in Audacity, simply go the the Effects Tab, and scroll down to Fade out, and it will fade out the file where you selected it. (Note: you should test the new file to hear how it sounds. If it is very abrupt, then you should consider staring the fade earlier.)

-------------------------------------------------------------------

Time Stretching and Pitch Shifting

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/06.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/07.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- First off is Time Stretching... This is the process of making the file longer, or shorter (usually shorter) without any pitch change. (You may want to do this to sync up a sound file with an animation.)

- In Audacity in order to do this you have to select Change Tempo under the Effects Tab...... Then it will open the change tempo screen. When changing the scroll bar, right is a shortened file, and left is a lengthened file. I went with 50%, which will make the file play in half the time of the original. (note: Extreme Lengthining of files will cause very unwanted effects.)

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/08.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- Pitch Shifting works exactly like Time Stretching, except it alters the pitch. In order to use Pitch shift in Audacity you need to select "Change Speed" (Not Change Pitch - That changes pitch but keeps the same time, which is used for other effects.)

-------------------------------------------------------------------

Adding Reverbs

- If you are planning on using a basic audio play/stop/pause/resume type system to save on resources, and keep it simple without a designer client, you may want to consider adding your own reverbs to the files depending on the scene. (Note: if you are planning on using a designer client to make interactive reverbs, then you should use SFX without reverb, or "DRY" SFX. As it will give you more control of the reverb, and save on File Space.)

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/08-B.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/09.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- In Audacity, if you add reverb to a file, It will cut off at the end of the file, so it is necessary to add additional space to the end of the file to make space for the added reverb. (Note: The QuickKey to go to the end of the track is K.) (You will need to do this for the next step.)

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/09-2.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/09-3.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/10.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- After going to the end of the file, you can go to the "Generate" Tab, and select Silence... From there just select a time large enough to cover the length of the reverb. I just left it at 30 Seconds.... Then the 30 seconds will be added to the end of the file.

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/11.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/12.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- After setting up the silence, you are ready to add the reverb. It is under the "Effects" Tab (It should be almost at the bottom, you may need to scroll.) After that it will open up the Reverb Effects......

- On the reverb screen, mostly the things that you will be changing are the top two scroll bars. "Roomsize" is how large you want the ambience to sound, and "Reverb Time" Which effects how long the reverb tail will be... There is a preview button available for you to listen to the effects. (For the example I just left it as is.)

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/13.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- After the reverb is created, select the file up to where you can no longer hear anything, and Trim the file of all the extra silence.

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/14.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- Once the File is Trimmed, you can select everything, and join the two files.

-------------------------------------------------------------------

Normalizing Audio

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/15.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/16.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/17.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- You will notice after adding the reverb to the file that the waveforms flatten out at the top, and bottom. If you were to export the file like this, then it would sound like harsh static. This is called "Clipping" Before exporting the file you will want to Normalize it. Under Tab -Effects>Normalize.....

- Once you get to the Normalize screen basically the only thing you will have to worry about is the dB Box. the Numbers start at zero, and go down. (You may want to keep it between 0, and -4)(Note: If you wind up having a bunch of SFX from random places around the internet, it would be good to go through, and normalize all of your audio.)

-------------------------------------------------------------------

Resampling Audio Bitrates

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/18.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/18-A.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/18-B.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- In the lower left corner below the SFX waveform you will see the SFX's bitrate it was imported as. If you wish to change the sfx's bitrate simply go to Tracks>Resample... From there you will see the Resample screen.

- The average bitrate you will use is 44100, however if you need to save on file space 32,000 will sound just fine for mobile speakers. (Note: Ogg only supports 44100, and 48000)(Note2: If working on non-mobile, be sure to use 44100 or greater)(Note3: Conversions only work downward. Changing something from 32000 to 44100 will not improve quality.)

(A basic explaination of Bitrate is whatever number the bitrate is, divide it by 2, and that is how high of frequencies will be played, the lower the bitrate, the less high frequecies will play. I'm sure some audio nerds will tell you that more is better, but honestly 44100 plays audio just fine, as the average speakers play up to around 20,000 Hz anyways.)

-------------------------------------------------------------------

Exporting SFX to Various File Formats

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/19.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/20.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- When you are ready, and the file sounds how you want it to sound, you are ready to export it to whatever file format you will be using in your project.

- Generally the accepted file formats most often used are .Ogg .M4A(AAC) .Wav, and .AIFF. I usually like to think of AAC's, and AIFF to be mainly used with Apple products such as Iphone, and Ipad, and .Ogg, and .Wavs to be used with everything else.

(Please don't use Mp3's. A sound designer cries out in agony when you do.)(If you download a file as an Mp3, then just leave it as an MP3, as recompressing it won't do much. (Unless it's 256 kbps or greater), but generally you want to download .wav, .AIFF files, or .Flac to begin with, and compress it downwards.)

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/22.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- When you first Download Audacity if you plan on converting to .M4A(AAC), then you will have to go to Preferences>Libraries, then click Download, and follow the directions from the website that appears.

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/22-A.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- When you choose either .Wav, or .AIFF, then the file saved will be 16-Bit, and whatever the sample bitrate is that you had set from ^above.^.... When you choose AAC, or Ogg, then a Compression Slidebar will show up. For .Ogg it will be 1-10, and for AAC it will be 10-500.

- For decent quality at a low size, I recommend using a 2 for .Ogg, and around 100 for AAC. If you are super strapped for space, then you can drop the .Ogg to 1, and the AAC to 50. Any lower than those, and the SFX will start sounding like awful garbage.

(Note: Changing one file format of compression to another will not realy improve audio quality. EX. Changing a 96 kbps .mp3 to a .Ogg file will only change the filesize, it will not make the file sound any better. usually if you are doing any compression you want to start with .wav or .aiff file that is at least 16-bit 44.1 kHz.)(Note2: Changing a lower compression setting to a higher will also not change the audio quality. EX. Changing a 64 kbps .Ogg (1) to a 128 kbps .Ogg (4))

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/24.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- After setting the compression settings and clicking o.k., if the Sample Bit rate of the SFX is higher than capable with AAC, or OGG, then a pop-up will also appear asking you to adjust the Sample rates.

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/25.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- Here is a quick Size Comparison for a 6 second file (fairly long file in gaming). These are Stereo as well. The average user will not be able to tell these apart on mobile speakers/$10-$40 headphones. (Note: The Wav was still a 96 kHz bitrate when I took the screenshot, if it were dropped to 32 kHz, it drops in size from 2.4 to 2.3 MB.)

-------------------------------------------------------------------

Various ways to convert SFX from stereo to mono

Generally if you have to use .wav, or .AIFF, then switching as many files to mono as you can will be important for keeping your file size down. (Note: make sure to check how mono files sound through headphones.)

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/28.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/29.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- The first option is splitting a stereo file in half, and keeping either the left or right channel, and making it mono. This can be done by clicking on the arrowed tab on the upper left of the sfx. Then clicking Split Stereo to Mono. After you split the files into two, then just delete one of the two sides.

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/31.jpg?width=1280&auto=webp&quality=80&disable=upscale)

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/32.jpg?width=1280&auto=webp&quality=80&disable=upscale)


- Another Option is to go to Tracks>Stereo Track to Mono, and both the wavforms will be combined. (This is a better option if the SFX file has a lot of Panning)

-------------------------------------------------------------------

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/33.jpg?width=1280&auto=webp&quality=80&disable=upscale)


This is the size comparison for the same files only mono. If you compare to the stereo files shown above, you can see Wav files get the biggest cut in size by being turned to mono.

-------------------------------------------------------------------

Basic Volume Changing

Other than that, only thing I can add is, if you are mixing all your sound volume levels, and one sound is exceptionally louder than another even after being normalized, then you can adjust the volume levels in Audacity using the gain scroll. Then ReExporting.

![](http://www.affordableaudio4everyone.com/AudioTutorials/BasicGuideForMobile_Pictures/34.jpg?width=1280&auto=webp&quality=80&disable=upscale)


-------------------------------------------------------------------



That's it for this guide. Hopefully this was useful for anyone who may have been interested. Hopefully it all makes sense.

Have a good one

Daniel


This guide can also be bookmarked [Here](http://www.affordableaudio4everyone.com/AudioTutorials/SFXPrep_For_Programmers.html)

Also quick shameless promotion

[My SFX Libraries Site](http://www.affordableaudio4everyone.com/Home.html) - 8 libraries 5 aimed at game audio for indie devs.