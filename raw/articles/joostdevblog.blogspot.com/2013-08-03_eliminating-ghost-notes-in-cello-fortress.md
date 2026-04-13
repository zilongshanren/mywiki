---
title: Eliminating ghost notes in Cello Fortress
url: http://joostdevblog.blogspot.com/2013/08/eliminating-ghost-notes-in-cello.html
author: Joost van Dongen
published: '2013-08-03'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

[previous blogpost](http://joostdevblog.blogspot.nl/2013/05/how-cello-controls-game-in-cello.html)(which is already quite a while ago, sorry for that: I have been really busy on the graphics for Cello Fortress), I explained how my algorithm works for detecting what the cello plays in

[Cello Fortress](http://www.cellofortress.com). The big missing part there, was that the algorithm I use not only finds the notes that are being played, but also tons of notes that are

*not*being played. Most of those erroneous notes can easily be detected and removed, so let's have a look at how to find and eliminate them.

![](../../assets/a811de6a5bbebc9b.jpg)

**Octaves**

The first problem is octaves. Because of the way my algorithm works, for every note that is found, its octaves are usually also found. Octaves are notes at exactly double the frequency, and double of that, etc. For example, A2 is 110hz, so the octaves that are also found are A3 (220hz), A4 (440hz), A5 (880hz), etc. Finding octaves is inherent to how my algorithm works: I detect notes for which both the own frequency and the overtones (multiples) are strong. The octaves are all exactly at the overtones.

The solution to this is rather simple: if an octave is found, I just throw it away. If I detect A2 and A3, I just throw away A3. This is simple, but unfortunately also a limitation: on the cello it is possible to actually play an octave chord and I cannot detect that this way. However, the octave is a very boring chord, since it is essentially the same note twice, so I have chosen to simply accept that octaves are treated as a single note in my algorithm. Fixing this would require switching to a completely different algorithm altogether, which I do not think is worth it.

**Limiting the range**

The second improvement is to remove all notes outside the playing range of my cello. For some reason the very low and very high frequencies seem to contain quite a lot of noise, causing notes to be detected where there are none. In my case specifically there is a very low frequency with a strong constant noise in it; I suppose this might be a fan interrupting the computer's internal audio cable magnetically or something like that. The solution is again simple: a cello never goes beneath C2 (65hz), so I simply ignore everything beneath that.

Removing high frequencies is a bit more problematic, since there is no clear limitation to how high a cello can go. However, there is a limitation to me: I can smoothly play up to A4 (440hz), which is one octave above the open A string of the cello. I can go beyond that, but since the quality of my playing quickly decreases there, it is a good idea to not use that for public improvised performances. So despite that I could in theory play higher, I can safely ignore everything above A4. This does pose a problem when other cellists play: I recently met another cellist whom I let play Cello Fortress. It turned out he was much more skilled than me at playing in the higher ranges, so the game limited him there.

![](../../assets/3d870b1992c50ed6.jpg)

So in practice, I only detect notes between 65hz and 440hz. Everything outside that is simply ignored. This is the main reason why Cello Fortress does not work with other instruments at the moment: they have a different range. However, this can easily be remedied by changing some settings. I recently tried controlling Cello Fortress with a violin (roughly G3 to E6, or 196hz to 1319hz), and after tweaking the range it turned out this worked perfectly right away. This is good news for ever doing a "

*Multi-Instrument Fortress*"! (If anyone can come up with a better name for that, please post it in the comments...)

**Large chords**

Another trick to remove non-existing notes, is to remove notes that are too far above the lowest note being played. Since only strings next to each other can be played on a cello, not all chords are easily possible. In particular, doing really large chords is difficult. I can use this knowledge to remove notes that are too far above the highest detected note. For example, if I play a chord with an open C-string (C2) and also play a very high note on the G-string next to it (anything above F#4), then the high note can safely be thrown away. Again, this does limit certain things that a really good cellist could do, but it fits my own skills nicely and reduces the amount of false notes detected.

**Resonating notes**

Another category of notes to remove is those caused by resonance. If I play one note really loudly, often some other notes will be audible very softly. This is mostly due to other strings resonating with the main note, or due to scratching because of the loud playing. The pattern here is that such notes are strong enough to be detected, but much softer than the main note. That means I can simply remove notes that are too weak in comparison to the loudest one. This might seem like a limitation, since in practice, playing a chord where one note is very loud and another is very soft is possible. However, this isn't all that doable or useful anyway, so nothing relevant is lost here.

**Fifths**

The final trick is a lot more subtle than the ones described so far. It is in fifths. Say for example I play an A3 (220hz). This will have overtones at 440hz, 660hz, 880hz, 1100hz, 1320hz, etc. Now the interesting thing if that the fifth to this note, the E4 at 330hz, shares a bunch of these overtones. |The overtones of E4 are 660hz, 990hz, 1320hz, etc. As you can see, two of those overtones are also overtones of A3. In fact, all odd overtones of E4 are also in A3. The result is that if A3 is strong, the total strength of the overtones of E4 is

*also*quite strong! This might seem okay, since there is no base note at 330hz, but it turns out that a little bit of noise or scratching can already cause E4 to be erroneously detected as a note.

![](../../assets/d6750f9d30fa6b50.gif)

I saw this happen quite a lot, and it turns out there is a really simple solution to this problem: if a note has really strong

*odd*overtones, but really weak

*even*overtones, then apparently it is not really being played. So I simply filter based on that to make sure that, in the case of our example, I only detect the E4 when it is actually being played.

The result of combining all of the tricks above is not quite perfect. Some ghost notes are still detected. However, few enough remain that at this point the algorithm is now actually very usable to control a real game. I am still looking into other tricks to remove even more ghost-notes from my detection algorithm, but even if I don't find any further improvements, the results are good enough.

Most of the tricks described in this blogpost have in common that they limit what the cellist can do. However, these limitations are rather subtle and plenty of possibilities remain, so I am quite happy with the balance I have struck here.

CLEARLY, in that picture, you've missed out on the "beard range" section of the cello, approx. 1/4th of the normal range by my estimation.

ReplyDeleteThe beard-range is so epic that pointing it out in a picture would make the picture too large to upload to the internet...

DeleteOrchestra Fortress? Instrumental Fortress? Musical Fortress? Concertmaster Fortress?

ReplyDeleteDamn, this sounds really cool. Although I would vote to raise the top detectable note to at least D or E so that "thumb position" (thumb on the A harmonic) notes can still be used.

ReplyDeleteIf I ever release the game for other cellists to play, I will make such things so that the cellist can set them himself. However, I myself can play in thumb positions, but not well enough to use it in improvisations in front of a live audience. So until I improve my skill there, it is fine at the A instead of the higher D for me personally. :)

Delete