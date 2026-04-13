---
title: The gross imperfections of tuning in music
url: http://joostdevblog.blogspot.com/2014/08/the-gross-imperfections-of-tuning-in.html
author: Joost van Dongen
published: '2014-08-10'
source_blog: Joost's Dev Blog
source_site: http://joostdevblog.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

*any*pitch, not just at the pitches of real notes. This gives endless possibilities, but it also means that if you put your finger just one millimeter too high or low, it already sounds out of tune and horrible.

![](../../assets/aa263dc0dc85d02f.jpg)

Playing in tune has always been a big topic to me, always striving for that oh-so-difficult 'perfect pitch'. Not that I am horribly good at it, but that is exactly why I practice so much to get closer to it. This is why it came as such a shock to me to learn that there is no such thing as 'perfect pitch': several tuning systems exist and they all come with different opinions on what the exact frequency of specific notes should be. They are also all flawed in their own way. Our modern tuning system is called

*equal temperament*and this is not because it allows for perfect pitch, but because it spreads the pain and problems equally everywhere, instead of having some parts perfection and some parts complete horror.

How can this be? Why is there no perfect system for tuning? To understand this, let's have a look at the frequencies of notes in our modern musical system, and how they relate to each other:

| Note | Frequency | Difference with previous note | Percentage higher than previous note |
| A | 440hz | ||
| A# | 466.16hz | 26.16hz | 5.95% |
| B | 493.88hz | 27.72hz | 5.95% |
| C | 523.25hz | 29.37hz | 5.95% |
| C# | 554.37hz | 31.11hz | 5.95% |
| D | 587.33hz | 32.96hz | 5.95% |
| D# | 622.25hz | 34.92hz | 5.95% |
| E | 659.26hz | 37hz | 5.95% |
| F | 698.46hz | 39.2hz | 5.95% |
| F# | 739.99hz | 41.53hz | 5.95% |
| G | 783.99hz | 44hz | 5.95% |
| G# | 830.61hz | 46.62hz | 5.95% |
| A' | 880hz | 49.39hz | 5.95% |

What you can see here, is that each next note has a higher frequency than the previous, and A' is exactly twice as high as A. This way playing an octave (A and A' at the same time) sounds really good, because their frequencies are exactly double. In fact, it sounds almost like a single note.

What you can also see here, is that the distance between two notes grows the higher we get. This way every time we jump 12 notes for an octave, we get exactly the double frequency. Each next note is approximately 5.95% higher than the previous, so notes are spaced equally when measured relatively.

This all looks fine and dandy, and it is something I have known for years. However, it gets hairy when we look at the distance towards that base note, the A. Note the last column:

| Note | Frequency | Percentage above A |
| A | 440hz | |
| A# | 466.16hz | 5.95% |
| B | 493.88hz | 12.25% |
| C | 523.25hz | 18.92% |
| C# | 554.37hz | 25.99% |
| D | 587.33hz | 33.48% |
| D# | 622.25hz | 41.42% |
| E | 659.26hz | 49.83% |
| F | 698.46hz | 58.74% |
| F# | 739.99hz | 68.18% |
| G | 783.99hz | 78.18% |
| G# | 830.61hz | 88.77% |
| A' | 880hz | 100.00% |

This may look fine, but keep in mind that I previously mentioned that an octave sounds so pleasing because the frequencies are exactly doubled. This goes for other intervals as well. The second-best-sounding interval is at exactly 1.5x the base frequency, so that would be A (440hz) plus E (660hz). However, now look at the table again and note that E is not at 660hz, but at 659.26hz. Slightly out of tune! The same goes for the fourth interval (A+D): the D is not the pleasing 33.33% higher, but the slightly off 33.48%.

This may seem like a tiny difference, but it is actually quite audible, and these aren't even the worst: the major third (A + C#) is at 25.99% instead of at 25%, which is a much bigger difference.

To really understand the problem, you need to hear it. This video explains it quite well by putting perfect chords (50% higher, 33%, 25%) next to the chords of a normal modern instrument (49.83%, 33.48%, 25.99%). Listen carefully to note the difference:

So why don't we fix this up by changing the frequencies to allow for perfect intervals? We could indeed do this, but this would

*only*fix the intervals on top of A. In fact, all intervals would become different depending on what the base note is, because we wouldn't be keeping that 5.95% interval from note to note. No matter how you try, there is no system that results in perfect intervals everywhere. I even tested this with other numbers of notes per octave (instead of the standard 12), but there is no system with perfect intervals.

Letting go of the requirement that all distances are equal, we can choose new tunings that make sure that certain intervals produce perfect chords, while others may sound much worse. This is indeed how tuning worked in the 18th century: some chords sounded perfectly in tune, while others sounded much worse than they do today, making them practically unusable. I guess this explains why baroque music with many sharps or flats is extremely rare: it just doesn't sound acceptable with the tuning used back then.

The system used in the 18th century is called

*meantone temperament*, while our current system is called

*equal temperament*, as all chords sound only a little bit off and none are completely broken. I guess the reason equal temperament replaced meantone temperament is that it allows for much more variation in chord progressions: equal temperament allows all chords in all positions, while meantone temperament only allows specific ones. Those specific ones do sound better though in meantone temperament.

Knowing that the western system with 12 notes per octave is not perfect also explains why other cultures have different numbers of notes. Arabian music for example has 24 notes per octave. This means that in between every one of our notes, they have one extra note. This creates a very different system of musical theory and a very different sound to Arabian music.

![](../../assets/1d7a97953388c1f9.jpg)

Most software for writing music makes it quite difficult to compose with more than the western standard 12 notes, but I have been told that some of the older Prince Of Persia games are notable because the composer abused the MIDI system to play real 24 tone Arabian music. I couldn't find any info on this online though, so I don't know whether that is true.

It is interesting to hear 24 tone music since it sounds quite alien and weird to the western ear, especially when used in a way like this on a special kind of piano:

So why is this all relevant today, now that equal temperament is the golden standard that nearly everyone in the wester world uses? First, it is important to realise that it is not perfect and thus pitch is also not perfect. Comparing a note I play on my cello to one other note might make it sound in tune, while comparing that very same note with another note might result in an interval that is slightly off. This is not because I am playing it wrong, but because the intervals are simply not perfect in our modern equal temperament system.

The second reason this is important to me is that until recently I played in the

[Kunstorkest](http://www.kunstorkest.nl), a small amateur orchestra that plays baroque music. Indeed, this is music from the age of meantone temperament, so knowing how it was originally intended is important to us! Not that a hobby musician like myself has the skill to play all the subtleties of this difference, but it helps to at least understand what is going on here and why sometimes the director wants a note played slightly differently. To conclude, here's a short recording of a piece we played with the Kunstorkest:

"No matter how you try, there is no system that results in perfect intervals everywhere."


ReplyDeleteI wonder if this problem is solvable with modern technology? If you have an instrument that goes through MIDI as an intermediary step, perhaps you could have a computer analyze the music and dynamically re-tune the intervals on the fly.

If you re-tune every interval than all your notes slowly shift. If your A starts at 440hz then it generally ends up at some random other frequency at the end due to all the shifting. You can only do what you propose if you don't mind that.

DeleteHmm, you're right. I guess there are a couple of issues at play here if I'm understanding the problem correctly.








Delete1. Assuming a base note/tonic, intervals based on ratios sound better[1] than intervals based on fixed cent distances.

2. Compsers and musicians need the freedom to change the base note (modulate).

3. It's important that modulations bring us back to our starting point. If we go on a crazy modulation adventure, the starting A has to be the same as the ending A.

That last point feels particularly sticky because it seems like it's kind of intrinsically tied to equal temperament. On the other hand…

It seems that we can get pretty far in regards to point 3 if inverting an interval results in the starting note. (In other words, A440 + 5th + 4th == A440, A440 + major 3rd + minor 6th == A440, etc.) Looking at an example of just intonation ratios[2], I see that the only intervals that aren’t invertible are major seconds, minor sevenths, and augmented fourths/diminished fifths[3]. I believe this means that if you a) avoid modulating by those specific intervals, and b) always match the interval of your modulation with a modulation by its inverse at some point in the sequence[4], the pitches for all your keys will be consistent. This means that something like the circle-of-fifths A-E-B-F#-C#… modulation will no longer result in the same starting A (since it’s 12 perfect fifths instead of 6 P5s and 6 P4s), but maybe that’s actually musically consistent/"correct".

As an example, take the following progression: A-D-b-F#-d-F#-A. Assume that the intervals over each base note get dynamically re-tuned for each modulation. The modulation intervals are P4, M6, P5, m6, M3, m3. Each interval is matched with its inverse. The math, then, is as follows: 440 * (4/3) * (5/3) * (3/2) * (8/5) * (5/4) * (6/5) == 440 * 8. Because we followed the rules, A, F#, and D retain their pitches (modulo octave) between modulations, and we still get the benefit of just intonation.

Did that make any sense? I probably got a bunch of things wrong, but this is pretty fun to think about.

[1]: Better physically/mathematically, anyway. Just intonation sounds kind of weird and out-of-tune to most people because equal temperament is so ubiquitous. I got to experience this first-hand in a music class I took!

[2]: http://www.kylegann.com/tuning.html

[3]: For M2/m7: 9/8 * 9/5 == 2.025. For A4 * A4: 45/32 * 45/32 == 1.978. For every other interval, multiplying its ratio by the ratio of its inversion results in an even 2.

[4]: In other words, if you modulate up to a major 3rd, you need to always have a minor 6th modulation somewhere in your piece.

OK, so I got a little carried away and made a frequency chart: https://docs.google.com/spreadsheets/d/1rzO1jJMVrAfDFlzE_-biXrIBShRYunTIw4BSMEATd9A/edit#gid=0









Delete(Ignore C == 440, I wanted standard frequency but didn't want to start my lettering with A...)

Each column represents the full 12 tone scale starting on the listed base note, tuned with the ratios given in the link above. The starting pitch for each base note is taken from the C scale. The cells with the stricken-out frequencies represent the base pitch for each column, while the bold/italic cells represent the P4 and P5 intervals. Each cell with a matching color represents a frequency that matches the same note in the C scale. (By comparison, the equal temperament chart would be entirely colored in.)

What I’m seeing from this little experiment is that with some limits, it’s entirely possible to maintain tonal consistency throughout your piece while using dynamic tuning. Whenever you want two pitches to match, simply ensure that they’re both colored in. (So, for example, F in the key of C and F in the key of A would be the same pitch, but not F in the key of G.) Furthermore, when you’re modulating to a different key and plan to stay there a while, you could put away the old chart and use a chart centered on the new key, thus severing your connection to the original set of frequencies aside from your base pitch. The only requirement would be finding matching squares between the two charts in order to get back to the frequency of your original key when you’re modulating back.

While your pitches might diverge during the course of a piece, my hunch is that it doesn’t actually matter. It’s all context-dependent! While you’d want your A to return to 440 when modulating from A to E and back to A, the note A as a major second to the key of G doesn’t have to match that frequency since it’s used for a different purpose. Or imagine this: a piece of music modulates to a very remote key where the frequency of your starting pitch is no longer the same. Isn’t that rhetorically powerful? The listener would really *feel* the distance of that modulation. Maybe it’s better to separate the notion of a scale tone from that of a fixed frequency altogether!

While this would be far too complex for improvised or even live music, a composer could consult charts like this while composing. (Or better yet, use a piece of software that does all the math for them and gives them a pitch possibility space.) The music produced by this system would be mathematically "perfect", though more limited in what it can do than an equally-tempered piece. (And perhaps those limitations could be addressed with some careful mathematical analysis.)

This might seem overly complex, but my gut feeling is that this is what music should actually sound like. We’ve simply been ignoring this complexity in favor of easier tuning. I can’t help but wonder what a well-written piece of classical music would sound like with the intervals all done up correctly!

Sorry if this sounds totally insane!

Hi Archagon,






DeleteYou typed so much text that I didn't get around to digesting it properly until now, sorry for the long delay.

Since you seem to have figured out an interesting tuning, have you tried to create a piece of music and compare how it sounds in Archagon tuning and in normal tuning?

I tried the intervals you mentioned and they indeed come back to the beginning. The first number is standard tuning, the second number is stacked perfect intervals.

A 440hz 440hz

D 587.33hz 586.6666666667hz

B 493.88hz 488.8888888889hz

F# 739.99hz 733.3333333333hz

D 587.33hz 586.6666666667hz

F# 739.99hz 733.3333333333hz

A 440hz 440hz

For me personally such tuning systems are not very useful: they are limiting to the composition, which I dislike, and I very much like playing music on real instruments, which is nearly impossible this way. Nevertheless, I would love to hear how your ideas sound and I am curious about experiments with it. :)

This comment has been removed by the author.

ReplyDeleteI've thought about this issue quite a bit over the years, and have reached a few personal conclusions:






ReplyDeleteFirstly, I had always been enamoured with the idea that, holding the tonic constant, every scale built off of that temperament within the just intonation system would have different character. This would open up a whole world of possibility! Eb would be unique! D minor would truly be the saddest key!

It turns out that playing a song in a C-intoned D scale (or any other combination) just makes it sound like you're modulating a very full sounding C chord, because everything is based around the harmonic series of the fundamental, and that is a sound that should be immensely familiar to everyone who listens to natural instruments' overtone patterns. It's boring, and while the D scale would sound different than the E scale, it all just ended up sounding like C.

Secondly, I remember reading somewhere about experimental systems using X-tone Equal Temperament to get the benefits of equal temperament while having a reduced pitch errors. IIRC the next best thing is 24-tone ET (though it might have been something weird like 18-tone or 32-tone), which was briefly considered around the introduction of the ET system (keyboards with twice as many keys in a octave, wow), but was concluded at the time to be too much trouble to play with to be worth the benefit it gave.

This of course brings up the following wikipedia article, which I'm sure you can find many interesting things from. http://en.wikipedia.org/wiki/72_equal_temperament

This, however, is something I have never heard of before. Interesting! http://en.wikipedia.org/wiki/Limit_(music)

It sounds to me like the difference between D-based-on-C and pure D would be really subtle, would this really be worth pursuing? It would be horribly impractical to use tunings like that.

DeleteOf further interest to Archagon is that Dynamic Tonality is actually a thing with a following. As a live instrumentalist, I've always been concerned with fixed tuning schemata, but it's definitely a cool concept. I like the idea of polyphonic tuning bends, and the linked piece , in which every chord is apparently Dmajor is interesting.

ReplyDelete