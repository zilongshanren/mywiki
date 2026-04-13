---
title: Last.fm Scrobble Fetcher & Mapper
url: https://theinstructionlimit.com/lastfm-scrobble-fetcher-mapper
author: Author Renaud Bédard
published: '2010-06-27'
source_blog: The Instruction Limit
source_site: https://theinstructionlimit.com
category: graphics
fetched: '2026-04-13'
---

**Update May 15th 2016** : New v3.0 build on [the GitHub project page](https://github.com/renaudbedard/scrobblemapper/releases/tag/3.0) with many fixes and additions.

*Update August 26th 2010 : New v2.1 build on google code that fixes the “Invalid XML Characters” issue! Try that one if you had errors when fetching scrobbles.*

*Updated June 26th 2010 : This project is now hosted on Google Code! I’m new to this so bear with me, but I’ll try to make it nice so that people can contribute. (Google Code no longer exists and the project is now on GitHub)*

*Updated March 5th 2010 : You shouldn’t need to install both iTunes and WMP for it work, just the one you want to use! Finally.*

Original March 15th 2009 post follows.

**Downloads**

Get the freshest releases (source or binaries) on [the GitHub project page](https://github.com/renaudbedard/scrobblemapper/releases).

**Description**

The **Last.fm Scrobble Fetcher & Mapper** does exactly that. It fetches all your scrobbles from your (or anyone’s, really) [Last.fm](http://www.last.fm/) account, assembles them in terms of *Play Count* and *Date Last Played* for each music track, and then exports this data to either Windows Media Player 11 or iTunes.

I’ve been working on this application on and off for some time now and I think it’s ready for deployment. I built it because I have quite an extensive music library, I like my playlists smart and automatic, and I have poor luck with music players, hardware failure and vendor lock-in.

It seems that the “Play Count” and “Date Last Played” metadata fields are not part of a file’s ID3 tags, but rather is stored in the player’s local library. This is usually fine, and probably more efficient than writing to files all the time, but it means that if your player’s database gets corrupted (as happened to me with Windows Media Player) or that you decide/are forced to use another player such as iTunes because your iPhone doesn’t want to sync with anything else, then you’re screwed. And same thing of course if you reinstall your machine or get a new one.

I feel that this metadata is important because I like to have automatic “best-of” playlists that are based upon it, and sometimes it’s nice to listen to a comfortable, time-proven playlist.

Thankfully, if like me you’ve been using the Last.fm services since they were called Audioscrobbler, you’ve gathered an impressive amount of playback information in your account over the years. And using their web services, and my application, now you can take it back home!

**Technology**

I wanted this application to be my cleanest, most error-tolerant and most efficient piece of work yet in application design. I also tried to exploit all C# 3.5 features, having accumulated some months of experience with LINQ, lambda expressions, etc.

Here’s a rundown of its tech features :

-
**Multi-threaded**- Uses the
[Parallel Extensions for .NET](http://blogs.msdn.com/pfxteam/)June 2008 CTP and a little home-made framework for progress-reporting asynchronous foreground tasks. - Most operations will use multiple cores thanks to the Task Parallel Library’s capabilities, and will seldom lock because of its lockless concurrent data structures.

- Uses the
-
**WCF-enabled**- Uses the
[Windows Communication Foundation](http://en.wikipedia.org/wiki/Windows_Communication_Foundation)classes in .NET 3.5 to communicate with Last.fm’s RESTful API. - All the response data objects are deserialized automatically from XML using the built-in XmlSerializer.

- Uses the
-
**Error tolerant**- Since Last.fm track data will not always match your library’s perfectly, I used the
[Levenshtein distance](http://en.wikipedia.org/wiki/Levenshtein_distance)string metric and “neutralized” strings (removes all accentuated characters, symbols, whitespace, etc.) to get accurate matches. - Will (should!) recover gracefully from errors, both caused by user input or unexpected conditions. It also allows graceful cancelation of long-running operations.

- Since Last.fm track data will not always match your library’s perfectly, I used the

**Screenshots**

**Closing notes**

– This code uses a Community Technical Preview version of the Parallel Extensions for .NET, and one that is almost a year old… So it’s delivered as-is, and you cannot (and should not) use that library in commercial products. Although I have functionally tested the program pretty extensively, I cannot guarantee it’s not going to corrupt your library or overwrite some information. Use at your own risk!

– I noticed that iTunes checks if the file is writable before setting any metadata concerning it. So you should make your files writables unless you’ll get a ton of errors in the error log after the scrobble-mapping.

– You need to keep the iTunes instance running for the iTunes mapping to work. The COM interface requires it to be open, but you can minimize it to the tray.

– The code is released under the [Creative Commons Attribution-Share Alike 2.5](http://creativecommons.org/licenses/by-sa/2.5/ca/) license.

If you encounter anything unusual, if you have ideas for extensions to this program or have comments/questions about how it works, do ask! That said I will probably blog some more about parts of this program, like the WCF usage or the asynchronous task classes. Enjoy!

Hey, would you mind including a set of instructions? I’ve tried downloading and extracting both zip files, but when I start up the app, It immediately gives me an error message of “Scrobble Fetcher And Mapper has stopped working”

It wasn’t working cause I didn’t have iTunes open?!? Oy vey :)

That’s odd, it’s supposed to start iTunes automatically… but glad it worked in the end. :P

I an error message “Internal Server Error” when I hit the fetch scrobbles button.

That means either that their server is too busy or has problems, or that your connection has problems, or that the username that you entered doesn’t exist.

I get his error:

This user does not exist, or there was an error fetching his scrobbles.

Details: The HTTP-service on http;//ws.audioscrobbler.com/2.0/?method=user.getweeklychartlist7user=Toommmm7api_key=62b743e5de48ef452744c7151feca07 is buzy.

Tom

me too, same “buzy” error message. help please, would be great for me if this worked

Seems like it was a last.fm site problem and nothing with the program, today it worked perfectly, thanks!

Glad to hear it! :)

Holy s**t, this program is a dream come true! I’ve searched this kind of gadget for a very long time and finally found one! Beautifully working, no problems whatsoever.

Merci beaucoup monsieur Renaud

Hey there. I just want to start out by saying that I really, really like the idea of this program. However, I had a few questions in mind that I was hoping the creator of this program (or anyone else, for that matter) could answer for me.

I guess I will start by explaining the purpose I am actually planning to use this for. I would like to somehow download as much of my scrobbled last.fm data as possible (which I have a lot of, since I’ve been a member for about 2 years now) and transfer that data to the songs in my iTunes or WMP library, so I can then upload THAT information back to a brand new last.fm profile. I understand that the process is fairly easy… you simply connect the scrobbler to your profile by entering your user name and password, and make it import the playcount data contained in library. Anyways, now for my questions. I know this is long, but please try to bear with me!

1. I wont even begin trying to understand the process of HOW all this works. However, I was wondering… exactly what data does this change? Does it simply update the playcount for the files? And, if the file name doesn’t match the last.fm tags, does it go and change that as well? Or does it simply try to find the best match and update the playcount for said file?

2. Does it base the decision on the file name WITHIN THE LIBRARY or the actual file name for the song itself? An example of what I mean… in the library, I have a song named “The Quiet Things The No One Ever Knows” but the actual file name for it in my music FOLDER says something like “02 the_quiet_things_that_no_one_ever_knows”

3. On that note, I have scrobbled some songs on last.fm with symbols in them (i.e., Miss Sweeney [*] which had a symbol to notate a ‘bonus track’), but have since gone and renamed the songs without those symbols. What happens to those? Will it be able to find the track name and simply update it based on how similar the names are?

4. Another scrobbling question. I’m guessing that, if the files aren’t found in the library, then those songs are just tossed away… right? The reason I ask is because I have many artists with just one or a few plays due to me listening to them on the last.fm radio, but I do not have the artist in my library. I know this is probably a senseless question, but I was thinking maybe there was a way to get those plays as well. If not, I wouldn’t mind since I really don’t listen to those artists anyways.

5. And finally, my last question. I plan on testing this out on my WMP library, since it’s the one I use the least. However, iTunes is probably the player I use most of all. Now, if I do end up mapping the data to my iTunes library, is there any chance at all that it would somehow corrupt the data, songs, library, or anything along those lines? Until I get a response, I’m assuming that all it’s going to do is update the playcounts for the songs… which would be ideal, seeing how I only started using iTunes a few months ago and it is way behind my last.fm stats.

I aplogize so much for all these questions, but I’m just really excited to use this program and needed reassurance on a few things. If you could respond to this, I would appreciate it VERY much! :D

Wow, glad to see you’re that interested. :)

1. First, the playcount information does not reside in the MP3/AAC files, but in the players’ metadata library. I’m sure that this is the case for WMP, I assume iTunes does the same thing.

What my program does is fetch all the scrobbles from last.fm, loop through the results, find the appropriate library entry using the player’s programming interface, and change the playcount. It does not change other metadata like artist/title/filename, and doesn’t upload anything back to last.fm.

2. It uses the “Title” and “Artist” metadata information from the player’s database, which corresponds with the same information from the files’ ID3 tags. The filename doesn’t matter, as long as your metadata is accurate. My program doesn’t speak with the filesystem, only the player APIs.

3. I mention in the features that I used “neutralized” strings, by that I mean that I remove all symbol characters, whitespace, case information and accents from both the last.fm data and the player local data before making lookups. That means that “Miss Sweeny [*]” would become “misssweeny”.

4. For each last.fm scrobble, it tests the “string edit distance” to each local library entry, so how similar titles and artists metadata are. When there’s a single direct match, it just updates it. If there’s multiple matches, it asks which you want to update. If it doesn’t find anything, it just doesn’t prompt and moves on. So files that you don’t own anymore won’t cause any problem.

5. It can’t corrupt songs. It shouldn’t corrupt the library, and I’ve tested for a while now, and haven’t heard any problems from other users. It does only change the playcount (and “last played date” on iTunes because it can), doesn’t touch any other information. So it’s pretty safe.

Final note, you mentioned wanting to throw back the data to last.fm, my program doesn’t do that. It works one-way, from last.fm to your player libraries. I don’t plan to do that in the near future either, sorry…

Wow, thank you for your quick response! I really appreciate it. Also, I understand that this program will not throw back the data to last.fm. I was just stating how I am downloading this program to update the playcounts and whatnot for my iTunes/WMP library, and then I plan on using the last.fm scrobbler itself to upload those playcounts to a completely new last.fm profile. Like I mentioned before, I’ve read that if you are a new user/create a completely new profile, all you need to do is tell the scrobbler program to “import data from library” and it will upload the information to the website. So, in short, use this Scrobble Fetcher & Mapper -> fetch scrobbles from current profile -> update library playcounts -> upload information to new last.fm profile using the scrobbler program. I’ll try this out on my WMP library first, and maybe create a test profile to see the results. Hopefully it will be able to upload mostly correct playcounts and also the dates played, so I can still have overall charts and whatnot (i.e., overall plays, 12 month charts, 3 month charts, etc. . .). Again, thank you very much for all your help.

Hey! Thanks for posting the source to this, I have wanted something like this for a while and it’s great that you’re making use of the 3.5 framework.

1) I found a huge problem however.

When I first ran the program (after downloading only the binaries) it crashed right away. So I downloaded the source and found it erroring during start up when it instantiates the iTunesAppClass and it gives the error “Retrieving the COM class factory for component with CLSID {DC0C2640-1415-4644-875C-6F4D769839BA} failed due to the following error: 80040154.”

Since this was not a trapped error, you have to be debugging to find it. This happened because I loathe iTunes and *do not have it installed* but it is an untested, untrapped assumption of the code that it is on my machine.

Once I commented out the line in MainForm() that instantiates the class, the program was able to load. These objects are only needed once you are trying to map the last.fm data to your library so creating them at start up is unnecessary, and as you see in my case, prevents the program from functioning without giving any feedback as to why if one of the players is missing.

I would suggest having a property of the form where the getter creates the class (and stores as a field) when it is requested, all with proper try-excepts and nice error messages about the product not being installed… or just disable the buttons based on the install state.

2) It should also be an option of whether to increment your playcount or reset them. I can see the common use case (for me the only way I’d run it) for just re-running the app to get it to update to have it synched between computers. Last.fm becomes the ultimate source and for me it can assume that if I’ve listened to a song 15 more times, those are logged with Last.fm so their count is current.

Aye, good point about detecting which apps are installed and initialize them selectively (and lazily/at the right time). I’ll update + post the fixed version some time soon.

By default the application only locally updates play counts that are inferior to the ones in last.fm… So what you’re suggesting is an “override” option that updates it even if it’s lower on last.fm than locally? Sure it’s easy, but it sounds dangerous. :P

Great program – I am still going though it and fixing all the manual matches (I had a few years worth of scrobbing and 55k plus songs in my library).

Since I haven’t gone through this completely – I was wondering if it goes through the whole process each time or is a log kept?

One suggestion that would be a great help to me. I really don’t want all the matching songs to get the credit for the play – I prefer that only the original version gets the play credit – is there anyway to add the option for songs that are 100% matches to select the one with the earliest year? This would work great for me as my tags are up all marked with the year.

You could even take this a step futher and indicate if no year – then pick the one that has the word(or words) – Greatest in it (this would cover the majority of greatest hits CD’s). With a large collection like mine it would prevent a lot of the 1200 manual ones I had to go through.

Still a great idea. Thanks.

Thanks a lot!

The program has no knowledge of past runs. It does not keep logs and will be confused about the same fuzzy matches if you re-run it.

The “year” metric for determining the original version makes sense, but it is a bit arbitrary and coarse. I don’t have any support for “custom rules” and adding them would almost mean a redesign… So I don’t think I’ll go into that.

But it’s open source! I encourage you to play with the code and try to build it in, if you’re into this sort of thing… :) Or find a bored C# programmer to do it for you.

Hi! I am trying to use this, but am not sure how to run it. What do you use to open .sln file extensions? Thanks!

@Becky : Go in the ScrobbleMapperbinRelease directory and run ScrobbleMapper.exe. All that you really need is in the Release directory, the rest is the source code files.

As soon as I attempt to execute the file, windows stops it. Why would this be?

@Chris : Make sure you have the .NET Framework 3.5 SP1 installed. You can get it from http://www.microsoft.com/downloads/details.aspx?FamilyID=AB99342F-5D1A-413D-8319-81DA479AB0D7&displaylang=en

I cannot fault this program. Does exactly what I want it to do :D Thanks

Hello Renaud — Thank you so much for sharing this; I used it this evening and it worked exactly as you said. A quick question from someone who doesn’t know much about this sort of thing: Is there an easy way to make the Mapper add a user’s lastfm counts to the existing iTunes play count so that the result is the sum and not just the larger of the two? I created a new account not too long ago, but am starting to miss all of the scrobbles from my previous one. What I’m looking to do is import the stats from one account (after iTunes’ counts have been set to 0) and then the other, so I can create yet another profile with the combined stats. Any ideas/solutions would be greatly appreciated! Thanks again.

Hello,

Your application looks promising.

If I’ve understood properly, your application only makes changes to the iTunes library and the tags and files are not changed either by your soft or iTunes, am I right?

Thanks

That is correct. Unless iTunes has a custom tag for “play count” and “date last played” inside MP3/AAC files, which I doubt.

But it won’t try to write any other information.

thank you sooo much!!! that’s exactly what i wanted!

Crashes immediately with .net 3.5 installed.

That might be because it’s registering for the WMP11 and iTunes APIs on start, even if you’re not going to use one of them.

I need to look back at the code and fix this issue and some others, but I’m lazy/busy. Try to install WMP11 and/or the latest iTunes as a temp. workaround!

I’ve finally tested your application and I can say it’s very powerful and pretty quick.

What took me some time were the fuzzy matches. I have a lot of doubles in my library.

If you think of improving your app, you can think of adding user chosen rules to help automatize this specific process, eg prefer single artist albums to compilations,…

Thanks for this great app,

Sheugel

Thank you for the great app! It rocks!

This is a great idea and well designed. Thank you.

I am having a problem though. Both your program and the LastFM2Itunes perl script don’t find all my scrobbles. For example: My top played song should be “Chiodos – The Words ‘Best Friend’ Become Redefined” with 102 plays (last.fm username: millerjosh89). Scrobble Fetcher and Mapper only finds 29 plays.

It seems music that I’ve added to my library more recently has the correct number of scrobbles. Is there some issue that would make it unable for scrobbles before a certain date to be transfered? The only reason I can think of is my original iTunes account had almost 10,000 plays before I learned about last.fm. This would explain all my missing scrobbles, but then is there any way to get them back?

Any help would be very appreciated.

Josh

New Feature Idea:

After submitting my above post I spent some more time on last.fm and am now quite sure I’m right about your Scrobble Fetcher not counting the plays I imported when I started my last.fm account. This led to an idea for a partial fix.

After collecting an account’s scrobbles by week, Scrobble Fetcher could compare it’s totals with last.fm’s top overall tracks and update tracks with any inconsistencies. While this only accounts for the top so many (500?) tracks, it would correct the user’s most important tracks.

Thanks again for making this program available. It’s the best one I’ve found in my journey to restore iTunes. And again, any ideas that may help me with my issue would be greatly appreciated.

Josh

Great work, thanks a lot.

Is it possible to add a feature so that the user can enter a start date to begin fetching from last.fm?

‘ta, works pretty well

GREAT APPLICATION!

I have the same question as koray – is it possible to modify the start date so I don’t have to deal with the fuzzy matches again?

Thanks!

Seems to be a nice program, but I always get an error at about 23 %. “This user does not exist, or there was an error fetching his scrobbles.

Detail: Error in XML-document (804,20)”

Tried another user name and it worked right away.

Thanks for help!

I’m getting the following error message on iTunes 9:

An error occured when updating the library.

Details : Unable to cast COMobject of type ‘iTunesLib.iTunesAppClass’ to interface type ‘iTunesLib.liTunes’. This operation failed because the QueryInterface call on the COM component for the interface with IID ‘{9DD6670B-3EDC-40DB-A771-E6FE4832E34A}’ failed due to the following error: The RPC server is unavailable. (Exception from HRESULT: 0x800706BA).

This error is repeatable but does not crash the program, nor crash iTunes.

Disregard that; restarting the program fixed it. However, it doesn’t maintain settings for relevance – I keep trying to knock it down to 80, but it doesn’t stick.

@Kelvin P : Try setting your default relevance in Tools -> Options, this setting should stick around.

I keep getting this when I try to map it to iTunes Library:

An error occured when updating the library.

Details : Unable to cast COMobject of type ‘iTunesLib.iTunesAppClass’ to interface type ‘iTunesLib.liTunes’. This operation failed because the QueryInterface call on the COM component for the interface with IID ‘{9DD6670B-3EDC-40DB-A771-E6FE4832E34A}’ failed due to the following error: The RPC server is unavailable. (Exception from HRESULT: 0×800706BA)

I’ve tried restarting the program like Kelvin P above but it doesn’t seem to work.

I just wanted to say amazing app and thank you for saving me so much time!

Everytime I try it keeps popping up with

This user does not exist, or there was an error fetching his scrobbles.

Can someone help?

Would it be possible to add a little more filtering on fuzzy matches? I have about 1500 and in some cases I have 5 or so tracks with the same name due to live CDs etc.

What I’d really like is to say “Pick the 100% match and if more that one 100% match exists just pick one”

For now I’ll just make do, really like the tool and even though it’s going to take ages I like that I can make sure the correct track is picked.

Hmmm, could it be, that this tool changed 50% of my tags!?

the problem is, that the most tags are cut at the end :/

seems so, that the id3v1 tags have been written into the id3v2… or what the fuck?! ^^

Huh? It really shouldn’t have changed any tags at all. It only writes to the media player’s library using its API, it never changes the files directly.

But this means that the iTunes API (I assumed you mapped to iTunes?) wrote to files and somehow changed your ID3 tags… worrying stuff.

Sorry about that, of course there’s no “undo” and there’s not much I can do even to fix it.

The program crashes immediately for me even with .net 3.5 installed and I attempted to download wmp11 like you suggested to someone else previously, but apparently my version of Windows isn’t valid or something..? Please find some way to resolve this issue.

Are you using Windows 7? I haven’t tested on Win7 + WMP12 yet, so I’m going to try that tomorrow.

If not, I’d like details on your Windows version and what version of iTunes you have installed.

OK, I just tested both WMP12 and the latest iTunes on Windows 7 Home Premium retail and it works fine.

Hey Renaud,

Thank you for this app! It was just the thing I wanted. I only have one suggestion – you should probably modify the API check when the app tries to boot up. I’m not sure if you’re aware of this but it crashes if either WMP or Itunes aren’t installed.

The workaround is ofcourse to install both of them (even if its temporary) but I know I almost gave up after the first couple of crashes. You’ll garner a lot more fans if you fix that small issue because WMP/Itune fans are usually pretty divisive and only have one of them installed at a time.

Anyway, continue the good work and I hope Last.fm picks up API up for their app sometime :)

Keep getting this error message when I try to map:

Unable to cast COMobject of type ‘iTunesLib.iTunesAppClass’ to interface type ‘iTunesLib.liTunes’. This operation failed because the QueryInterface call on the COM component for the interface with IID ‘{9DD6670B-3EDC-40DB-A771-E6FE4832E34A}’ failed due to the following error: The RPC server is unavailable. (Exception from HRESULT: 0×800706BA)

one word…LEGEND

Got tired of waiting on the fifth time of

Finalizing Action:

Matching Scrobble.

Bla bla.

Thanks ANYWAY. :)

I keep getting the same error message as James:

Unable to cast COMobject of type ‘iTunesLib.iTunesAppClass’ to interface type ‘iTunesLib.liTunes’. This operation failed because the QueryInterface call on the COM component for the interface with IID ‘{9DD6670B-3EDC-40DB-A771-E6FE4832E34A}’ failed due to the following error: The RPC server is unavailable. (Exception from HRESULT: 0×800706BA)

I’ve tried restarting Itunes and restarting the scrobble mapper. The error message still appears when I try to map to Itunes. What is the RPC server referring to?

Actually, I misread the error message the first time, I think instead it was:

Unable to cast COMobject of type ‘iTunesLib.iTunesAppClass’ to interface type ‘iTunesLib.liTunes’. This operation failed because the QueryInterface call on the COM component for the interface with IID ‘{9DD6680B-3EDC-40DB-A771-E6FE4832E34A}’ failed due to the following error: No such interface supported (Exeption from HRESULT: 0x80004002 (E_NOINTERFACE)).

Either that, or I got both this error message AND the error message in the previous post above. Sorry for the double post.

It looks as if this is a brilliant application, if only it worked for me!

I do not have WMP installed, which seems to be the problem. I have the latest version of iTunes. Apparently the program crashed because I do not have any version of WMP installed at all, and I can’t download it because my version of Windows ‘isn’t valid’.

Please try to fix this issue, I’ve been attempting to get my playcounts back for months now.

Hey Renaud.. I guess it was Itunes, damn I hate it ;)

Thanks for this, I didn’t want to have to install Perl and your app saved me the time. Kudos my friend

Can someone explain to me what I need to download other than the zip file above? Like what program I need to run it, where I can download it, and what exactly I need to do once I have the program installed and the zip folder downloaded. I am completely technologically inept, so all help is much appreciated.

So, do I have to have BOTH ITunes and Windows Media Player installed for this to work? I hope not. I hate iTunes. Can’t ever get it completely uninstalled.

Actually the new version (v2) that I just uploaded should work fine without iTunes installed, if you only use WMP mapping. And vice versa.

Sorry for the wait, I finally got around to do it… :P

Hi, Nice work on this! Worked fine except it skipped 246 songs, is there any reason for this?

Songs with the number of plays (in your player library) that is lesser or equal to last.fm’s scrobble count are skipped. Also if it doesn’t find the song in your library for a scrobble, as per your tolerance range and everything, it’ll skip them.

Ahhh makes sense now, thanks for the quick reply!

The application looks wonderful, however even though I have iTunes installed the ‘Map to’ button is greyed out and iTunes doesn’t start automatically at any point.

More importantly I am also getting ‘This user does not exist, or there was an error fetching his (or her ;-)) scrobbles.

Details: Error in XML-Document (486,24)

I just updated iTunes yesterday and am on XP pro 32-bit. Maybe it’s a Last.FM problem. I’ll try again later – this software is simply too good not to be true. :)

The iTunes/WMP buttons will remain grayed out as long as you don’t have the scrobbles downloaded and parsed locally. But the error seems to indicate a bug in either their XML feed or my program…

Can you email me your Last.FM username so that I can debug? renaud.bedard@gmail.com

Hi Renaud,

have you had the time to take a look at what may have been the problem with using my last.fm account with your software?

merci for an answer and your creative efforts,

Fabian Kondziella

Hey, great app, but I have a little problem anyway.

It fetches my last.fm history perfectly, but when I’m trying to map my scrobbles to WMP library it stops at about 17% and quits, and when I’m doing it with iTunes it doesn’t even start.

Is it possible that it happens because I use Vista?

Uuuh, definitely not normal. And it should support XP, Vista and 7… Make sure you have the latest versions of iTunes and WMP, but otherwise if we’re going to fix this I’ll need to contact you by e-mail and send you debug builds of the application! My email address is 3 comments above.

Well, it looks like there’s something wrong with my system, now your app doesn’t even ‘reads’ that i have iTunes installed. Actually, last.fm scrobbler also can scan only WMP, and I don’t get any information whether my library is really scanned or not. I must have messed sth up with my Windows – rights, permissions etc. I think there are some problems in communication between applications. I’m going to reinstall my system soon so possibly everything will go easier with ‘clear’ system. Anyway, thanks for your reply.

i keep getting an error report from windows..

it won’t let me run the scrobblermapper.exe

any idea what the problem is?

okay, so i got it to work,

but there’s quite a few scrobbles it doesn’t get back.

That would be because either it can’t match them (i.e. your local files have ID3 tags that differ too much from last.fm’s)… or there’s a bug.

well it looks like there are weeks that it isn’t getting the scrobbles from.

from what I see anyway.

I still can’t get past 50%. would it be possible to keep the first 50% or to keep importing from the point where it last failed?

Just a few ideas, not complaining – it’s cool this software exists at all. ;-)

cheers,

tak

p.s.: last.fm account in question still ‘linkshander’ without the quotes

Any specific reason why this has playcounts way way way lower than the ones on my last.fm?

“Any specific reason why this has playcounts way way way lower than the ones on my last.fm?” – I’m having this problem as well. Brilliant app though!

Love this application!! Thank you

Hello I am getting this error

this used does not exist, or there was an error fetching his scrobbles.

Details : the HTTP service located at http://ws/audioscrobbler.com/2.0/?method=user.getweeklychartlist&user=canicora&api_key=62b743e5de48ef452744c7e151feca07 is too busy.

is there something I am doing wrong? I hope I can get this to work because it seem to be exactly what I have been searching for

Thanks in advance

so I figured out my error from above was that my last.fm acciunt was less than a week old so I didn’t have a weekly chart built yet. I love this program and thank you for making it. Is there a way to set it to fetch exact date and time played? As I just used this to update my iTunes all the play counts that it changed read last played 7/18/10 12:00pm because this is the end of the weekly chart form last.fm

Hiya! Glad it worked out in the end.

I can’t really fetch the last played date because last.fm’s API only gives me the week it played in, and there’s no unique identifier for a scrobble (that’s published anyway).

So the best I can do is know the first or last or middle weekday of that week it’s been played…

Thank for the response it will still help me tremendously in keeping up with my library the way I want to while listing on different devices. Guess I’ll have to just cross my fingers and hope last.fm will make the exact play time available sometime in the future. Thanks again for developing this :)

Its only finding srobbles for like 19 for my songs, why is this? :l ‘ve used it before on my old account and it worked fine :/ my new account is 3 weeks old btw.

The application collects data from the “weekly scrobbles list”, so it won’t find the scrobbles for this week or maybe even the week before, depending when last.fm updates their data.

I tried using this, and it can’t update (for some reason) about 2300 of my tracks. What am I doing wrong?

What do you mean by “Can’t update”? You’re just noticing that songs have 0 Play Count or there’s an error dialog or something?

Hello Renaud,

Lovely software, but I’m confused… I did the process, it gathered all of my old songs, and now I would like to put all of the scrobbled songs from my old account (2006-2009) onto my new account (2009-now). Is there a way to accomplish this? If so, provide links or a step-by-step explanation of how to do it.

Thanks,

-Tim

Hi Tim, the application is not made for that purpose unfortunately. It just allows you to bring your scrobbles back to your players’ libraries. I don’t know of another app that will do the reverse process.

Tim, just uninstall and then re-install the last.fm scrobbler.

When you run it for the first time it will allow you to upload all your playcounts to your new account. ;)

it tells me i dont exist ;( as a last.fm user. some xml doc problem (226,17), i dont get it. other things i used got all my scrobbles, i have a .scrobble.log file and all, i just need to implement it to itunes/wmplayer/winamp somehow to send it back.

tenko, what’s your last.fm username? I can try it here and see if I can fix it.

There are some problems with last.fm’s XML API, sometimes they send out garbage and there’s nothing I can do about it. I posted in their forums and their answer was basically “tough luck”.

Hopefully you can just delete the offending scrobble(s) and it’ll work.

i dont know what’s this error, i’ve been playing around with my last.fm account for a good while now, i’m trying to get all tracks, correct a few typos that screw up my stats and load it back to last.fm (sure i know it has to be a new account). no matter what it wont load a scrobbler.log file, timeless or not, in my whole listening history’s entirety – it has to be done by wmplayer/itunes/winamp via their listening history. i have no idea how to do this atm, still thinking, and your applications throws me out the same error as month ago :( what the heck, am i cursed or smt…

email me please if you have any ideas about this xml 226,17 error :( it reads some 50%-3/4s of my database there and then suddenly stops.

would it be hard to add an option to input the xml weekly charts manually? i remember having the xml file somewhere.

This issue is now fixed in version 2.1, if anyone else has this problem, download the new version and try it out!

I got a new pc and tried my hardest to keep all my play counts etc on my music…. i followed several website’s instructions word for word but no luck…. Like many i use smart playlists for my iphone but now this isnt possible.

I can use a pc, but when it comes to the techy stuff i have no idea….

so in this file i have the following files…

Application

3 x Application Extensions

CONFIG file

The 3 application extension files and the config file ask me to search the net to find a program to open it with…

And the App files says “the application failed to initialize properly(0xc0000135) Click on OK to terminate the application”.

I really do have no idea what i am meant to do and cant find any step by step instructions…

Anyone care to divuldge?

@Olly : If you’re running Windows XP or Vista, you need to install the .NET Framework 3.5 SP1. If you’re running Windows 7, you shouldn’t need to, but it can’t hurt.

http://www.microsoft.com/downloads/details.aspx?FamilyID=AB99342F-5D1A-413D-8319-81DA479AB0D7&displaylang=en

Afterwards you just need to unzip everything and run the ScrobbleMapper.exe, there’s nothing else to do.

Hi Renaud Bédard, is there a way of getting this program to ADD the plays from last.fm to Windows Media Player? For example if a song has 10 plays on WMP and 3 on last.fm would there be a way of updating it to 13 plays? This would be really useful for me as I have a different computer with lots of plays on its media player and would like to update plays from last.fm onto that one, then create a new profile with the plays from both having been combined. Thanks

Not unless you know how to dabble with C# code!

I could add the functionality but it seems too dangerous to enable by default. I’ll put it in the issue list on Google Code.

Hi Renaud – thanks for the tip – finally got it working. Still have one issue, after scanning all my songs and trying to map to iTunes i get the same error message as a few people above. Can see any answers re this. is there something im doing wrong?

Unable to cast COMobject of type â€˜iTunesLib.iTunesAppClassâ€™ to interface type â€˜iTunesLib.liTunesâ€™. This operation failed because the QueryInterface call on the COM component for the interface with IID â€˜{9DD6670B-3EDC-40DB-A771-E6FE4832E34A}â€™ failed due to the following error: The RPC server is unavailable. (Exception from HRESULT: 0Ã—800706BA)

update…. it does seem to have added some play counts to some of my music but by no means all of it, or to the extent lastfm shows. for example, my most played song on lastfm says 224 plays but on itunes it only shows 35. Is this to do with the above error message – should i do it again or something?

Thank you! This program is amazing. Worked perfectly

@Oily: Running it again shouldn’t change the play count. Looks like it’s either a problem in my code or in last.fm’s API, like it’s not sending all the scrobbles.

There’s already a bug entry on googlecode about this problem, I just need to take the time and look into it. Thanks for the report anyway.

Could you tell me your last.fm username so that I can test with your account? I don’t need the password obviously.

A suggestion which would completely rectify the issues with this application, would be to generate a load of 1 second long mp3 files. Have a folder which contains them, and have them generated for every track scrobbled from the old account.

This way you won’t have to worry about tracks not being found on your computer, bad tagging etc. The tracks would be made and tagged by the scrobbler. Once all uploaded you can just delete the folder and be on your way…

This worked beautifully! I lost my iTunes database a few months ago and was resigned to never having it back. Thanks so much for rescuing my playcounts! If a future version included a ‘date added to library’ update as well, that would be really cool. :) But really, this has rescued so much of what I thought I had lost. Thanks!

Hi,

I’ve got a problem with the program, and I was wondering if you could help me with it please.

I transferred all my music onto an external HD, which lost my play counts on iTunes. I tried updating them manually with the ‘iTunes Store File Validator’, which worked, but then I changed laptops, and again lost my play counts on iTunes, although my last FM was up to date at that point. This means that my last FM has all the correct play counts, but not the dates, as I manually changed the file info. (For example, Song X has 10 play counts, but when I look at the info, it only has 4 dates on which it played). When I used your Scrobble Fetcher, it found only the files with dates played (e.g. the 4, not the 10).

Is there any way to get round this?

(I apologise if I’m asking a really simplistic question, my computer knowledge is minimal).

Thanks

Hi Kieran,

Hmmm right… I think this is an unavoidable side-effect of me using the Weekly Charts to fetch the data.

The problem is that last.fm doesn’t publish any other API that allows me to grab all the plays from an account’s history. So it’s the best I can do, really. :/

Let me start out think you for one of the best apps for iTunes/WMP/last.fm. Recently when I found that iTunes 10 was so buggy — took my 160 GB iPod over 24 hours to sync from scratch then when I made changes in iTunes like delete, uncheck, or make tag changes, I then had 2 copies of the track on my iPod and constantly was getting an error message that I was out of space. iTunes 10 wasn’t deleting anything off my iPod. So I download the last version of iTunes 9 and uninstalled 10 and installed 9. 9 could not use the library from 10 and I move the library so that iTunes 9 would create a new library. At this point I decided instead of importing the .XML file that I would start all over from scratch Now my play count was lost but I knew that the play count was on last.fm and was manually going through the list because the only program that would reverse scobble was iTSfv as I was using it to change the play count — for some reason I could never get it to work on my last.fm charts keep having a .net error. Using the same program, some of the tracks I had stored the play count and the rating count in the POPM and PCNT frames but that wasn’t accurate at all. I currently have about 20,000 tracks in my library (accounts for about half of my music files about 200 GB so you see why it is important for iTunes to delete tracks off my iPod) of which most have been scobbled at least once. Then I stumbled upon your wonderful program that did get the play count.

This brings me to a suggestion. Because I have bought CD’s that have a track or two that also appears on a previous CD, I had about 1000 tracks that need manually mapping. It took me a long time to go through each of these tracks. My suggestion is simply put a check box to update all of the tracks with the play count.

Thanks you,

George

You just saved me from a total nightmare after I lost my iTunes library.

Excellent work!

Hi, guess this is easy for you but would be very much appreciated:

Could you make a feature where I can export the data to an excel/csv/txt file?

Would be great!

Woah, this is amazing. You saved me a lot of work! Thank you!

Excellent work!

I don’t really plan to work on the code in the near future, but it’s an open-source project now. I hope that people can have initiative and add in more features. I’d be glad to help making that happen.

I have been looking for a program like this forever. Thank you for creating it.

I tried running the program and after getting about 5% through it crashed with an error. I noticed that I had iTunes running and was cleaning up my library with TuneUp Companion and shut them down to try again.

The question I have is does this require the iTunes library to be in the standard location or is it intelligent enough to find the actual iTunes library if it is located on an external hard drive? I have all my mp3s on an external drive and the iTunes is mapped from there instead of the My Music Folder in windows. I am hoping this isn’t updating the backup library in the My Music folder I keep there for other 3rd party programs that seem to require the Library location to be in the standard My Music location.

Awesome program again!

Hi Brian! Glad you like it.

It uses the iTunes API to look up the music library that iTunes has in its database. In other words, it never talks to the filesystem, only iTunes. So whatever music files iTunes indexes and publishes with its API, are the ones I play with.

It shouldn’t touch files in My Music if you don’t use those in iTunes.

This program is great and is the only one that seems to achieve its intended purpose without requiring any sort of advanced computer skills. However, for some reason, it only imported about a third of my play count. For example, “Dog Days are Over” by Florence + the Machine, according to Last.fm, has been played 306 times. However, according to the program and its subsequent iTunes sync, it has only been played 122 times. I think the program only synced plays that are in the weekly charts and not those that existed before the account was created.

@Sam : Yes, I do only use the weekly charts because that’s the only API that last.fm gives me to get the sum of all play counts. There’s really not much I can do about this, sorry.

Hi, this sounds awesome, so I downloaded it but had trouble opening the program. After downloading it to my mac, i tried to open scrobblemapper.exe but got the following error message:

Could not extract the file “(B”: The archived file is corrupted.

Am I doing anything wrong? I really want this to work!

thanks

Is there a way to just dump the scrobles into a text file or a csv?

No sir. Not that it would be hard, I just didn’t get around to doing it. It’s open source though, so if you wanna risk yourself at some C# code, go ahead.

hey man, seems like a savior of a program you got here, although i’m running into a problem where after i fetch all my scrobbles, map them to itunes, and select my fuzzy scrobbles, it tells me that an error has occurred and that all my songs have been skipped… resulting in no play count recovery. any reason for this? thank you.

edit: the error is “an attempt to modify a locked property” any idea what this means? thanks again.

Hmm…. That is pretty bizarre. Maybe your MP3 files or the path that leads to it is read-only? Can you check?

I’ll look at the code and get back to you.

they were read only, i hope this solves my problem. thanks again for the program, i’ll let you know how it works out for me from here.

so now it is giving me an error that when i map to itunes it tells me that “the itunes interface could not be loaded. either it could not be found or your version is not supported”. any thoughts?

finally got it to work, thank you again for the wonderful, life-saver of a program Renaud!

Thank you so much Renaud! That was fantastique!

What an excellent utility! Much appreciated.

You haven’t just hacked it together either… I love the fact that you’re using cutting-edge .NET technologies to accomplish this. :-)

Hi!

Is it possible to run this on a Mac? This program sounds REALLY COOL!

:)

Sadly no, it runs on a Windows-specific application framework. Sorry!

Oh, okay, thanks for a fast reply!

Then i’m just going to transfer the itunes library to my other computer, install and use it there, and then transfer the library back to my mac. Really want this program ;)

One question. The answer is probably in your description or among the other questions, so i’m sorry if i’m wasting your time.

So… If i have played a track a hundred times, but LastFM only thinks i have played it once, will it change the the count from hundred to one?

Hey there quick question just used your program seems to work ok although missing a lot of Scrobbles for an example one of my artists on last.fm has a thousand listens yet only a few hundred appear in itunes? any ideas? or am i being simple?

is there any possibility that I could increase my last.fm playcount using this software ? :/

So this doesn’t work for Winamp?

This is an excellent program. I was hoping that each track would list the day & time it was played, but this is the closest I have found yet. It is very cool!

This is isn’t fecting my most recent scrobbles, is there a fix for this?

You are a god among men! Worked like a charm after I looked at the Perl script stuff! So Easy! Thanks a million!

not working with the current itunes version :(

Huh. I’ll look into it as soon as I can.

wow this looks just like what i need, i wish it supported mac :(

You are a lifesaver! Thank you so much for making this gem!

Hey I tried using this, but the problem was only about a third of the plays on the tracks came up, the play count for each song is a lot shorter than the actual one on Last.FM. I tired using the Google Code link as well but the exact same problem happened. This is a life-saver so it’d be great if you could get back to me. :)

@charlie : This is probably because I’m using the “Weekly Charts” that are generated every week by last.fm. If you scrobble stuff in the past (like with the iPod/iPhone scrobbler), they won’t be registered. Unless they added better APIs to get all the scrobbles, I can’t do it any other way. Sorry!

Can someone explain to me what exactly this does? What exactly is a ‘mapper’? Thanks

Love the program. Maybe my request is too niche and obscure, but I see no reason why this program can’t export all the data last.fm collects, including skip count and tracks loved. I’m not sure if their API supports that, but I’d love it if there were options in the menu to map a 4-star rating to every song I’ve Loved on last.fm…

This is great, but only 4,000 of my 16,000 plays scrobbled, is there anyway to fix this, or is there a program that can scrobble all of my files?

That’s might be because you scrobbled plays “in the past”, like you plugged your iPhone and it scrobbled your plays from the past year or something.

In that case there’s nothing I can do, because I use the weekly-generated plays reports, which are not retroactive if you remove or add scrobbles in weeks earlier than the current one.

I don’t know of any application that does it differently, and to my knowledge there is no API that last.fm provides to grab scrobbles one by one efficiently; weekly play counts are the next best thing.

FINALLY! Great work! Tanks a lot!

Very happy to have found this, but unfortunately still getting the:

The http: service located at……… is too busy

error. I will keep trying. It appears closing and reopening the program might be necessary for retries, as the error seems to appear ‘too’ quickly.

I’m crossing my fingers that this will work!

nothing happens when i click itunes or media player buttons. it only opens them and media player also closes itself.

I just tested with the latest iTunes and Windows Media Player 12 on Windows 7 64-bit, and it seems to be working fine. Make sure both are open before clicking the buttons maybe!

I’m moving over from WMP to iTunes and obviously want to keep my play counts. I’ve been scrobbling for about 4 months now but was wondering. Does this programme only add play counts that were done while i’ve been using Last FM, or will it update all the play counts that are in my WMP library since before i started scrobbling? Thanks!

Only the ones registered in Last.fm, it’s one-way from Last.fm to your media players.

Thanks for the reply. Do you know if it is possible to export the entire last FM play count history to iTunes, rather than just the scrobbled plays?

The API only lets me scrape the “weekly track chart” for each week, which is generated once a week and never updated. I assume it only works from scrobbles, but it could also count plays from the website or apps…? In any case, what I’m using right now is the only way to get data from their site.

http://www.last.fm/api/show/user.getWeeklyTrackChart

Any chance of adding a simple “export to csv/xspf” or similar to your program once the fetch is done?

I second this!!

I’ve fetched the scrobbles from the account i want, i click map to itunes and nothing happens? how do i get these to scrobble to my account? someone please help asap!

This worked great, thank you very much. I have a quick question though, if I sync again, after doing it once already, will it double all my play counts or will it just correct the counts to what they are on last.fm?

Hello.

I’ve downloaded this program, run this, and it’s work properly. But when I try to map to windows media player – it’s nothing happens! How can i solve this problem? Thanks for the answer.

(sorry for my bad English, it’s only my second language)

Really need this for OSX. Any options

Any chance to get this to export data to CSV or similar type of file? This would be extremely useful for those who don’t use iTunes. Thanks.

You my friend, are awesome! Thanks for making this tool for us to use (without making me install Perl :-)

Goddamn thank you for this piece of software.

If I knew C#, I’d expand it to also transfer favorite tracks to iTunes >=12 database… but I don’t know C# and .NET, alas.

As far as I can tell the application (now) works on iTunes 12. Are you having issues?

I am running Windows 7 and have the most current iTunes. It recognizes my Last.fm username and when I press “Fetch Scrobbles” and then “Map to iTunes” it does its thing. Everything seems to work perfectly but after it completes, the playcount in my iTunes remains the same. Am I doing something wrong? Both applications are open. Looking forward to trying to get this fixed.

This dosn`t work :(

You’re right, it broke some time in the last year. I’m working on a fixed version right now, so check back soon!

Can’t wait!

Thanks! (:

Updated! Let me know if the new version works better for you.

You may need to install .NET 4.6.1 : https://www.microsoft.com/en-us/download/details.aspx?id=49981

Hello! Such phenomenal and handy tool. Thank you kindly for updating it. It works perfectly and as intended with the new LFM.

I noticed that one particular facet is missing in the new version though.

In the previous version, this tool used to fetch back deleted scrobbles and scrobbles that were erased after an account reset as well, at least in my past experience.

I’m immensity interested in this and would greatly appreciate it if you could somehow modify it to function the same way as old, in that particular aspect at least.

I’m hoping this tool will help me get them back as I woefully regret having reset my account last year just few days before the launch of new site.

And I know for sure that those scrobbles are still there floating in some abyss because there used to be a bug, which is your reseted scrobbles will count as deleted scrobbles instead of vanishing into the abyss forever, and thus the Restore Deleted Artists utility in the Playground can bring them back for you.

This bug would occur only if you reseted your profile and immediately re-imported your media library thereafter, without allowing 7 days to pass so the reset thing would take effect completely.

Thank you for your time,

Any way to make it fetch the first time a track was played?

Yep that would be possible from the scrobble data, I don’t expose it in the database but it’s known. It should be easy to add it if you want to give it a try, I’m not keen on adding more features to this app at the moment, but it’s open source : https://github.com/renaudbedard/scrobblemapper

I was over the moon when I found this software but after running it several times and getting the same error each time I am now sad that I will not be able to do what I wanted to…

“An error occurred when updating the library.”

Details: Access is denied. (Exception from HRESULT: 0x80070005 (E_ACCESSDENIED))

I hope someone can give me some advice to sort out the problem…

Hi! Does that happen with the iTunes mapping or Windows Media Player mapping?

Hi! With the WMP mapping… :(

Thanks for creating this tool.

Hi! Is it possible to fix this so it can work with iTunes 12.10? I’m desperate, I love this tool and it have stopped working now.