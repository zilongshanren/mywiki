---
title: Adaptive Music with Elias – Tutorial Series – Part 1
url: https://www.gamedeveloper.com/audio/adaptive-music-with-elias-tutorial-series-part-1
author: Dale Crowley
published: '2018-11-12'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Adaptive Music with Elias – Tutorial Series – Part 1

Adaptive music has come a long way in the past several years with custom middleware solutions like Elias. This article provides a step by step guide to re-creating an adaptive music project in Elias Studio.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

(This article was previously published on [DesigningMusicNOW](https://www.designingmusicnow.com/2018/09/17/adaptive-music-with-elias-tutorial-series-part-1/) on September 17,2018. For full disclosure, this article has been republished with permission from Scott Looney by Dale Crowley who currently works for Elias)

Adaptive music has been a staple of AAA dynamic game audio for more than two decades, when it was used in LucasArts games such as Monkey Island 2. Featuring the in-house iMUSE music system, combined with MIDI data, and downloadable sound banks, this game achieved a notable level of musical immersion, with flexible responsiveness and organic development that has only recently been equaled. The emergence of third party audio middleware around that time has since slowly developed in sophistication to the level where adaptive audio creation is now easier and more affordable than ever, yet middleware tools written specifically for composers are still somewhat lacking in terms of features, flexibility, and usability.

The Elias Adaptive Music Engine aims to correct this oversight using terminology and functionality familiar to composers who are experienced with adaptive music creation. In this article, we’ll introduce you the concepts that Elias uses for organizing various elements in the project, and we’ll also look into recreating the basic structure in the Elias Official Demo Theme, by breaking it down into its various components. In future articles we will dive into the sophisticated and cutting edge way that Elias handles MIDI, motifs and more. Like a well designed video game, Elias is easy to learn but takes time to master. Hopefully this article will start you on an exciting journey of adding adaptive music to your games. Let’s get started!

Getting Elias Studio and the Demo project

Before we get started, there are a few things you will need. Those are the Elias Studio, The Official Theme, and the Official Theme Re-Creation.

For directions on downloading and installing Elias Studio, watch [this video.](https://www.youtube.com/watch?v=J1rLP9CcTzo)

Here is a walkthrough of all the steps detailed in this article which you can use as a companion as you step through them:


Also, on the website, under the Resources heading, you’ll find the [Tutorial section](https://eliassoftware.com/tutorials/) with many other example videos to help you out – and of course don’t forget the [full user guide](https://elias-themes.s3.amazonaws.com/manuals/studiomanual.pdf) available from the site as well as the downloaded package.

Elias Conceptual Framework

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/Elias-Basic-Structure.png?resize=630%2C389&ssl=1&width=630&auto=webp&quality=80&disable=upscale)


As stated earlier Elias is a tool for configuring and arranging adaptive music. This means that a composer or editor will generally have already recorded and produced the music content in question and need only bounce it out in their DAW to be able to use it in Elias Studio, which arranges and configures the existing content. To do this, Elias uses a hierarchy of terms that we will become familiar with. In order of size these are Project, Theme, Track, Level, Variation and Segment. Let’s break these down in order:

A Project contains all the music in the game. It also includes all the data used to manage the playback of the adaptive music. The Project is created in a named folder which contains not only the main project file of the same name (which has the .mepro extension), but also all the audio and MIDI assets that will be needed for the project.

A Theme is similar to an individual song in your game, such as the Battle Theme. A Theme must have a specific measure length, time signature and tempo. Themes consist of one or more Tracks that represent the breakout of individual instrumental parts in the Theme. This can be arranged as the composer desires – there’s no specific method required. However a fairly common approach is to break up a Theme into stem mixes of various instrumental groups, such as strings, brass, woodwinds, etc. and place these on different Tracks. Another common approach is to group tracks by audio frequency – having all the bass instruments in one track, all the mid-range instruments in one track, all the high end instruments in a third, and the percussion in a 4th. Since Elias mixes on the fly, it is best to have all of these stems bounced out at the same relative dynamic range. Additionally, there is a mixer in Elias that can fine tune the balance post bounce if needed.\

A Track generally represents one instrument or instrument group as a part of a Theme, though this can vary as need requires. There are two main types of Tracks used in Elias: Loop Tracks and Stinger Tracks. Loop Tracks represent the main body of the music while Stinger Tracks are used for transitions, builds, rewards or even tonal motifs to accent certain events or characters in the game.. There are also two subtypes of Tracks: you can choose to add an Audio or a MIDI track. We’ll look at all of these in more detail later on.

A Level represents a specific vertical location or slot on all of the Tracks in a Theme. The concept of Levels is fairly central to how Elias works so it bears a little explanation, though you may be able to guess its functionality from the name. Basically a Level is a value most often used to express the intensity of a Theme. Generally lower Level values would indicate lower levels of intensity with less Tracks playing at once, while higher Level values represent ‘pulling out all the stops’ and all Tracks playing. This is however only one interpretation, and a composer could choose many different ways to determine what a Level value would do for a specific Theme. Normally the Level changes apply to all Tracks but it can be applied to a single Track (via the Track Groups feature) if desired. Any Level can also have variations, which is the next item.

The Variation represents what is playing for a specific Track at a specific Level value. There are three types of Variations – Single, which play only one or more clips for the Track at a specific Level, Multi, which can randomize or sequence from a list of of clips each time the Level is triggered, and Silent Variations, which as the name states, don’t play at all. We’ll be covering these as well.

The Segment is a subset of a single level on a single track, and it only appears on a Segmented Variation. It is a one bar or longer audio or MIDI file that can be repeated once or multiple times on the track timeline. Imagine a 32 bar song that has a verse-verse-chorus-ending structure. If each were 8 bars long, then you can simply repeat the verse twice followed by the chorus and the ending. The goal of segments is to economize the file size in the case of audio, and increase the number of possible variations in the case of audio and MIDI. Variations with multiple Segments are color coded yellow.



UI Overview

To get started we’re going to open the [Official Elias Audio Demo](https://eliassoftware.com/product/elias-demo-theme/), so you’ll need to uncompress the zip file called ‘official-elias-demo’ which you can get from that link. Next, open up Elias Studio and we’ll open that Project file to introduce you to the overall UI and look and feel.

To open a Project, click the Open Project button, then browse for the folder you just uncompressed. Inside are two subfolders. You’ll want the one labeled ‘Official Elias Audio Demo’ and then inside that folder is the project file you’ll want to open. You should probably see something like this when it opens the first time:

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image010.png?resize=639%2C330&ssl=1&width=639&auto=webp&quality=80&disable=upscale)


The Project window has a few significant subcomponents. We’ll cover the major areas of focus:

Toolbar – this is where you can perform various tasks relating to the whole project. From left to right these are: Analyzing files for Smart Transitions, Saving the project, Exporting the Package, and Studio Settings, where you set the audio interface and buffer settings as well as other global options like Autosave, and Record, which lets you record your playback as a file. The last two icons pertain to your Elias account and the Shop where you can buy already existing themes for your game.

Player – This area is where you can play back your Themes, as well as preview changes and transitions of different kinds. You can make changes manually by setting Levels; jump to specific Themes or bars; trigger Stingers; and preview more automatic changes through triggering Action Presets.

Main Window Tabs – This area actually contains tabs for every major window available.


![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image011.png?resize=669%2C29&ssl=1&width=669&auto=webp&quality=80&disable=upscale)


Each of these tabs can be independently broken out and placed if desired, and the desired window layouts saved. For now we’ll stick with this more compact approach, but if you accidentally end up with windows in undesired places you can reset your layout by going to Windows > Reset Layout – or just use Cmd Shift-L.

Segment View – This area shows the contents of one or more Segments in a Variation as a block.

Inspector – This area shows the settings for items selected in any of the Main Window tabs. We’re not covering the Inspector at the moment, but we’ll definitely get to it as well. Let’s keep going and set up the new blank project.


Setting Up The New Project

To download a simplified Official Demo that we are going to be using for these tutorials, click here: [Elias Official Demo - Recreation](https://www.designingmusicnow.com/download/5048/)

Note that this project is not complete, but it contains all the files you will need to complete the steps in this blog. It also has all the audio files organized in such a way that it makes it easier to rebuild the project from scratch.

For this new one, you’ll select New Project and have the option to name your project in a particular location. Desktop is a good place to put it. For this, we should create a new folder so click the New Folder button on the left and Name your folder. Here I named mine ‘Elias Demo Re-Creation’.

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image012.png?resize=406%2C180&ssl=1&width=406&auto=webp&quality=80&disable=upscale)


When you create this project, note that Elias by default only creates the meproj file – it does not create a folder for audio files. That is left up to the user to further organize as they see fit.

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image013.png?resize=472%2C88&ssl=1&width=472&auto=webp&quality=80&disable=upscale)


For this series we’re going to to be using the Official Elias audio demo, and its files have been presorted into previously created folders in order to more easily be able to find and organize all the files needed. So, we need to copy the audio files from the Official Audio Demo folder to the location of your new project where we can import them. Switch to the Finder (Mac) or Explorer (PC) and find the folder you uncompressed. Find the Official Elias Audio Demo folder and inside there is a folder named ‘audio’. Right click on this to copy and then find the folder where you created your project, right click and select Paste.

Let’s take a look at how things are organized. Open the folder with your new project and you should see something like this:

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image014.png?resize=495%2C180&ssl=1&width=495&auto=webp&quality=80&disable=upscale)


Note how the files are organized by Theme first and then Loop and Stinger Tracks afterwards. This will hopefully help in terms of keeping the project together and help you to more quickly find files to use in each Theme’s Loop and Stinger Tracks.

Create Themes

Okay we’re ready to get going on this re-creation. First, we’ll need to create our Themes, which are our largest and most important organizational element in any Elias project. The Theme is the main musical building block consisting of one or more Tracks, and only one Theme can be active at a time generally. Themes have a specific bar length, tempo, and time signature associated with them. You also cannot currently create tempo maps or have changing time signatures within a single Theme.

Click on the window for the new project you created and go to the Theme menu to create a New Theme. Name this Theme ‘Objective’. Do this again to create another Theme called ‘Objective Battle’.

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image015.png?resize=300%2C132&ssl=1&width=300&auto=webp&quality=80&disable=upscale)


Next go back to the Theme menu select the desired Theme and choose Theme Settings. You’ll set the settings for each theme, so you’ll be doing this twice.

The Theme settings display a length in bars or measures, a time signature and a tempo in BPM. Set your Themes to the following settings:

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image017.png?zoom=1.5&resize=259%2C269&ssl=1&width=259&auto=webp&quality=80&disable=upscale)

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image016.png?zoom=1.5&resize=252%2C269&ssl=1&width=252&auto=webp&quality=80&disable=upscale)


Note that if you change the length, you may get a confirmation dialog explaining that you are changing the structure of your Theme, which is a somewhat significant action and will change a number of other settings and timings of sub-elements like Stingers. Thus it’s best to set the length early on and not change it too much if possible later on – especially if you shorten the length. For example if you had a 32 bar Theme with a Stinger that was playing at bar 25 and then shortened the Theme length to 24 bar, that Stinger’s settings would be void and may have to be set again from scratch.

Adding Tracks

Go to the Themes menu and select the Objective Theme. Now we can get to adding Tracks to our Themes. As stated before, Tracks are the main organizational element within a Theme and there are four types of these:

Loop Tracks contain the majority of the music you’ll hear in the Project, and generally will break up the instruments involved in a Theme into individual parts or categories. In this case we’ll be creating the same tracks as the Official Audio Demo has, but keep in mind that the naming and assignments of Tracks are completely up to you.

MIDI Loop Tracks are similar to Loop Tracks but these contain MIDI information instead of audio information.

Stinger Tracks contain various non-looped clips of music that are triggered at specific times, frequently at moments of transition between Levels or Themes but sometimes Stingers can be triggered incidentally at various points to accentuate game actions or states, or even to increase tension in the game.

MIDI Loop Tracks are similar to Stinger Tracks but contain MIDI data instead of audio. We’ll focus on the MIDI Tracks in a later article. For now we’ll be concentrating on the audio based tracks.


To create Tracks go to the Track menu and select Add New Track:

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image018.png?resize=383%2C176&ssl=1&width=383&auto=webp&quality=80&disable=upscale)


Choose Audio Loop Track and create and name the following Loop Tracks:

‘Choir’, ‘Strings’, ‘Brass’, ‘Percussion’, and ‘Other’.

This should result in five Audio Loop Tracks, like so:


![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image019.png?resize=600%2C58&ssl=1&width=600&auto=webp&quality=80&disable=upscale)


Notice that each Track allows Solo and Mute options. The icon on the right side indicates that the Track is a Audio Track. MIDI Tracks would have a different icon.

Next, create and name the following Audio Stinger Tracks:‘1 Bar Pickup Stinger, ‘Hits’, ‘Tonal Brass Stinger’, ‘Level Complete’,’Game Over’ and ‘Theme Transition Stinger’.

Note that you can resize the width of any Track header on the right side, so as to see its title or Level Variations below more clearly if needed. Your Stinger Tracks should look something like this when finished:

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image020.png?resize=660%2C44&ssl=1&width=660&auto=webp&quality=80&disable=upscale)


Adding Variations To Tracks

Now we get to adding our Variations. To simplify things we’re just going to start with the Loop Tracks and to simply focus on one Track for the moment, the Strings track. To add a Variation, all you need to do is to drag over the sound file you want to the Level slot on that particular Track you want. But seeing as how there are quite a few files to look through, let’s look at the contents of the audio folder we copied from the Official Demo.

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image021.png?resize=483%2C58&ssl=1&width=483&auto=webp&quality=80&disable=upscale)


Since we’re on the Objective Theme and we’re filling a Loop Track we’ll be looking here in the ‘LoopTracks’ folder for what we want. We’ll need a file called ‘Strings 1 p’ so search for that, and when you’ve found it, drag it over the first slot on the Strings track like so:

(make gif of dragging and placing clip as Variation)

Congrats! You just created a Single Variation, the most basic and common type of all Variations. You can right click to Audition the file, make it Silent, or Clear the contents of the Variation, leaving it blank.

Now do this again, this time we’ll use the ‘Strings 2 mf’ file in that same subfolder. Drag this over to the slot immediately below the occupied slot. Your track should look like this when finished, with the two variations on top of each other:

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image022.png?zoom=1.5&resize=186%2C139&ssl=1&width=186&auto=webp&quality=80&disable=upscale)


Let’s do one more. Find the ‘Strings 4 mf melody’ file, and drag it over the Level 4 slot. Your track should now look like this:

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image023a.png?resize=395%2C286&ssl=1&width=395&auto=webp&quality=80&disable=upscale)


Note that I’ve manually resized the track width as well to expose the file name and relative path of each of these Variations as well as the Level indicator on the left side. This can easily be done by clicking the triangle icon on the Level. Any active Variations on a Track at that Level will be visible.

This is also a good time to point out the paramount importance of file naming and organization when working with Elias Studio. Since this demo consists of nearly 100 sound files, if we had named any of these files generically like ‘Audio 1’ or something like that, we would not know its content without having to listen to those files, and also note that by naming files in the Finder or Explorer after the fact we would change its reference in Elias Studio and it would no longer work properly when re-opened. This restriction is the same if we were to create folders in the Finder or Explorer after we imported our files, to organize them. So the Pro tip here is to have all the naming and folder organization done before you import these into Elias Studio.

Let’s hear what this sounds like using the Player section (that’s Section B in our UI screenshot)

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image024.png?resize=331%2C318&ssl=1&width=331&auto=webp&quality=80&disable=upscale)


For this we’ll use the green playback button in the upper right corner to start playback (or just press spacebar), and when we do this we’ll hear our Strings playing at Level 1. Now, while the track is playing, look at the bottom of the area and you’ll see a long slider and a number on the right.

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image025.png?resize=327%2C84&ssl=1&width=327&auto=webp&quality=80&disable=upscale)


That’s the level number that we’re playing. Change this value to 2 and click the (Re-)Activate Level button. You can also press PageUp key on your keyboard, or drag the slider. You should hear an immediate change. While the change in question is the correct segment, it does so quickly and without regard to the tempo. We don’t want that in this case. We want a gradual change instead of an immediate one, and to do this we’ll click on the Strings Track header and look in the Inspector to see its settings.

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image026.png?resize=317%2C379&ssl=1&width=317&auto=webp&quality=80&disable=upscale)


The settings you can configure are one of the things that make the Elias Engine so flexible. For now we’re just going to focus on the Agility settings and the Fade Settings. The rest of these settings are covered thoroughly in the [User Guide](https://elias-themes.s3.amazonaws.com/manuals/studiomanual.pdf).

Agility Settings – this covers exactly when Elias Studio will trigger the Variation once its Level is active. You can set it to Anytime(immediately), on the Beat, on the Bar, or at a Custom time. For these String clips the composer needs them to be triggered in every other bar, so we’ll need to select Custom for this Track. When this is done you’ll see a window where you can insert the exact bars you want to trigger the clips.

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image027.png?zoom=1.5&resize=212%2C289&ssl=1&width=212&auto=webp&quality=80&disable=upscale)


To add a point, click the Add button. You’ll see the first entry showing up as 1:1. The indicator above is what bar and beat you’ll set, and when you click the Add button the value will show up. The screen below shows that I’ve set up the first four trigger points at Bar 1,3,5 and 7, all on Beat 1 of the bar. Keep adding these until you’ve got a list with the following progression: 1:1,3:1,5:1,7:1,9:1,11:1,13:1,15:1,17:1,21:1,25:1,29:1. Note that those last three starting from Bar 17 are four bars apart, not two. Obviously you can see this requires very intimate knowledge of the music in advance, but you can also try different settings to see what works best for you.

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image028.png?zoom=1.5&resize=195%2C179&ssl=1&width=195&auto=webp&quality=80&disable=upscale)


With this set let’s look further down at the Fade Settings. These are fairly easy to determine the function of. Enable this and set it to the following:

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image029.png?resize=415%2C126&ssl=1&width=415&auto=webp&quality=80&disable=upscale)


In this case, Fade In means if the previous Level was silent it would fade in in 100 ms. If the transition is between two clips of audio it will crossfade over 1000 ms, and if the next Level is silent, it will Fade Out in 100 ms.

All right, let’s go back and listen to the music again at Level 1, and this time slowly keep changing our Level to Level 3. Notice that our transitions are much smoother and more well placed, and that both adjacent Levels flash during the transition period and turn solid when the next Level is playing. Also notice what happens at Level 3. We’re still hearing the Level 2 music. Now change to Level 4 and listen to that, then switch back to Level 3. Notice that you’re still hearing Level 4’s music.

This brings up a useful point. Blank Level Variations are not silent. They will usually contain the music of the Level that was most recently triggered. However if you want a blank Variation to be silent you can right click and select Make Silent. Try this out. The Variation will be red colored. At that point Level 3 will in fact be silent at all times when the Level arrives, so you’ll get to hear the more immediate Fade Out and Fade In time. To undo this, select that Level, right click again and choose Clear.

Level selection on blank Level Variations is actually a pretty complex thing in Elias Studio, because each Track can have its own Level Selection Strategy in the Track Inspector – they don’t all have to change to the same Level in the same way.

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image030.png?resize=432%2C82&ssl=1&width=432&auto=webp&quality=80&disable=upscale)


Let’s quickly cover the four major selection methods available:

Closest Above – this means than when Elias encounters a blank Level it will continue to play the material at the nearest Level above (in other words at the lower Level value since Level numbers are from top to bottom).

Closest Below – this means than when Elias encounters a blank Level it will play the material at the nearest filled Level below it (in other words at the higher Level value).

Closest To Target – Elias will choose the closest filled Level whether above or below.

Least Possible Change – This one’s a bit tricky. If there’s already a Level playing, Elias will continue play that Level, but if not, it will pick the closest filled Level and play it instead.

Exact – This setting will only play the Level specified. Thus, it is more like a switch that acts like an automatic Silence Variation for blank Levels. Basically if there is a blank Level on that Track, it will silence the output. This may be a little confusing since we just stated that blank Levels aren’t usually silent unless you use the Silent Variation and Make Silence, but with a Silent Variation you can have the Level selection behave in a particular way for most of the blank Levels on the Track and then override default behavior for particular Levels you wish to be Silent.


For more info on this, please consult the [User Guide](https://elias-themes.s3.amazonaws.com/manuals/studiomanual.pdf).

Multiple Variations

We’ve covered Single and Silent Variations, and now we’ll look a Multiple Variation. To do this we’ll first switch to the Choir Loop Track by clicking its header, then look at your Track Settings in the Inspector and set them to the following:

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image032.png?resize=252%2C300&ssl=1&width=252&auto=webp&quality=80&disable=upscale)


Next, we need to bring in audio elements to our Choir Loop Track. First, look in the LoopTracks folder under the ObjectiveTheme folder. We need to find the Choir loops shown below:

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image033.png?zoom=1.5&resize=269%2C190&ssl=1&width=269&auto=webp&quality=80&disable=upscale)


Drag ‘Choir 1 Boy’ to Level 1, and ‘Choir 3 Boy and Women’ to Level 3. Next, drag ‘Choir 5 plus flute V2’ and ‘Choir 5 plus flute’ to Level 5. That’s right – you’re going to drag two files over the same Level location. Do this one file at a time, dragging the second file directly over the slot occupied by the first file. Once you do this, the Variation will turn into a Multiple Variation and be colored blue. You can also expand the level before dragging, and then drag the two files over the darker area below the level. If you do this correctly, the two files will become variations. If not, they will be dropped into two adjacent levels. You can also edit this behavior in your Studio Settings, as shown here (Edit->Studio Settings):

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image034.png?resize=476%2C65&ssl=1&width=476&auto=webp&quality=80&disable=upscale)


By default, “Add across levels” is selected. This can be overridden when you expand the level – Elias simply detects that and adds them to new levels.

Once you have added the clips to the level, on the far left of the level text, a number will be shown, indicating the number of items in this level. In our case, this should look like the image below, with the <2> in front of the level name. You can use the arrow on the left side of the Track Loops window to see the contents of any Multiple Variation.

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image035.png?resize=345%2C183&ssl=1&width=345&auto=webp&quality=80&disable=upscale)


When Elias gets to a Level with a Multiple Variation on it, it will select a Level based on the Progression Mode settings, which we’ll look at here, just below the Level Selection Strategy:

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image031-e1529872432809-300x75.png?resize=300%2C75&ssl=1&width=300&auto=webp&quality=80&disable=upscale)


These can be set in one of three different ways:

Random – Elias will randomly select a Variation. This may result in repeats of the previously triggered Variation.

Sequential – Elias will play through the Variations in order

Shuffle – Elias will randomly select a Variation but will not repeat it until all Variations have been played.


Let’s work on the Brass Track next. First though, let’s go over to the Strings track and we’ll look at another feature for Track Agility Settings. You recall the Custom Agility settings we did for the Strings? We are going to need something like that on the Brass Track. However, rather than having to enter all of our data from scratch, we can start from a copy of the Custom data from another Track and then edit it. All we need to do is click the Copy button on the side and we can then switch to the other Track and on its Custom settings, click Paste.

Pro Tip: The copying between Custom Agility settings is generic, which means you can paste from the Clipboard directly into a text editor to make it more convenient, then copy from there and paste it back into Elias. Nifty! Just remember to keep the formatting similar with the colon between the numbers and a carriage return on each line.


As mentioned, the Brass Track has different Custom Agility Settings. These should be as follows: 1:1,2:1,3:1,5:1,7:1,9:1,11:1,13:1,17:1,19:1,21:1,23:1,25:1,27:1,29:1. Hopefully the editing of these should be easier starting from the Strings settings, though as you can see they’re clearly not identical. Fade Settings should be set as follows:

Once you’re finished find the ‘Brass Horn melody’ file and drag it over Level 5. Here’s what the first three Tracks should look like up to Level 5:

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image037.png?resize=502%2C219&ssl=1&width=502&auto=webp&quality=80&disable=upscale)


Okay we’re in the home stretch. We have one more Variation type to cover and that’s the Segmented Variation. We’ll switch to the Percussion Track for this one. You should have already created this track earlier, but if not use Cmd-T(Ctrl-T on PC) to create a Loop Track called ‘Percussion’. Set the Track Settings in the Inspector as shown here:

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image038.png?resize=366%2C279&ssl=1&width=366&auto=webp&quality=80&disable=upscale)


Okay we’re ready to add our Segmented Variation. To do this, we don’t actually drag our file over the Level in question as we did for Single and Multiple Variations. Instead we use the Segment View located at the bottom as area D in our overview screenshot:

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image039.png?resize=644%2C58&ssl=1&width=644&auto=webp&quality=80&disable=upscale)


The Segmented Variation is useful when a particular timed arrangement or order of clips is desired. To start this out, find Level 6 on the Percussion Track and click on it. You’ll see a frame will highlight around this Level.

Next find the ‘Perc 6 S 4bars b1 b5 b17.ogg’ file and drag it over the Segment View. be sure to release the cursor at the location you want. It’s a bit finicky but you can move the position later on. You’ll get a dialog asking you to fill in some details:

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image040.png?resize=416%2C183&ssl=1&width=416&auto=webp&quality=80&disable=upscale)


Notice you cannot edit the Start Bar – it’s determined by where your cursor was when you released it. You do have to indicate the length of the clip, which in this case is 4 bars long (lucky it’s in the filename as well), and we only want it played one time so we set the repeat count to 1. The End bar can also not be edited, but it takes into account both the length and the Repeat count. Click OK and here’s what you should see:

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image041.png?resize=608%2C150&ssl=1&width=608&auto=webp&quality=80&disable=upscale)


You can move the location of this segment to bar 1 but be careful – if you drag it too far left there’s a bug that will make the placement invalid and it will turn your Variation Silent. Just get the left edge of the segment as close to Bar 1 as possible. Hopefully this interaction will be more robust in the future, but for now just be wary of Segments starting right at Bar 1.

Do this action again with the same file at Bar 7, and again at Bar 17. This gives you three copies of the same file placed as segments in various places.

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image042.png?resize=600%2C114&ssl=1&width=600&auto=webp&quality=80&disable=upscale)


Last we’re going to find the ‘Perc 6 S 12bars b21’ and drag this over to Bar 21 right after the last placed Segment. So, overall you should have the following 4 segments as shown:

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image043.png?resize=614%2C215&ssl=1&width=614&auto=webp&quality=80&disable=upscale)


Also notice that the Percussion track’s Level 6 slot shows <1>: for a Single Variation and the next number is the number of Segments in that Variation. Notice also that the Level is colored yellow instead of green, blue or red. Any yellow colored Level slots are automatically Segmented Variations.

For the last bit we’ll look at the last Track here called ‘Other’. Click its header and change the Inspector settings as shown:

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image044.png?resize=345%2C263&ssl=1&width=345&auto=webp&quality=80&disable=upscale)


Last, find the ‘Other 1 Low Pad’ file and drag it over Level 1. Your Loop Tracks should look like this up to Level 6:

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image045.png?resize=649%2C294&ssl=1&width=649&auto=webp&quality=80&disable=upscale)


Give this a playback and play around with Level changes and you’ll see how it’s already beginning to sound a bit like music!

Exporting Your Work From Elias Studio

We’ll be covering this in more detail later, but one of the strengths of Elias is that you can export the project and even convert and rename your files, and then archive everything into a compact zip file. To do this, go up and look at the icons in the Toolbar. Look for the rocket ship icon.

![](https://i0.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image046.png?resize=300%2C88&ssl=1&width=300&auto=webp&quality=80&disable=upscale)


You’ll get this dialog:

![](https://i1.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/06/SL_EliasPt1_image047.png?resize=300%2C260&ssl=1&width=300&auto=webp&quality=80&disable=upscale)


From here you can prepare the project for export. In the top section you can browse to add additional files like directions for the integration/programming team, asset lists, or other things more external to the project that may be useful. Under the Export settings you can Zip the entire project (as long as it’s under 2GB of data). The Rename tracks option will rename all files used in the project based on a numbered naming convention, and should be avoided for now. Lastly, you can export in either WAV (uncompressed) format or Ogg Vorbis, using a selectable bitrate. Note that the exported project will only have the files or clips that are used in a Variation on a Level, and the folder organization you saw earlier will be lost. It will instead place all items under the ‘audio’ folder. We’ll look at bit more in depth at this in the future.

So we’ve just given you a brief exposure to the inside workings of Elias Studio and you can already see what a flexible and versatile tool it is for game composers. Never fear though – we’ll be back to flesh out many more features in the next installment. We’ll be covering Stingers, Action Presets and much more. Stay tuned!

About the Author

![](https://i2.wp.com/www.designingmusicnow.com/wp-content/uploads/2018/09/looney.png?resize=150%2C150&ssl=1&width=150&auto=webp&quality=80&disable=upscale)


Scott R. Looney has been educating students and teachers alike about game audio for over 7 years. He is the co-founder of the Game Audio Institute (GAI), seeking to de-mystify the process and methods behind interactive and adaptive sound and music, as well as co-author of the Essential Guide To Game Audio (2014 published by Focal Press). Follow GAI for exciting news and announcements in the coming months! [www.gameaudioinstitute.com](http://www.gameaudioinstitute.com/)