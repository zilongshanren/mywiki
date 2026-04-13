---
title: 34-key Kalimba music theory analysis
url: https://gametorrahod.com/34-keys-kalimba-seeds-pisces/
author: Sirawat Pitaksarit
published: '2021-09-01'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

Seeds Instruments made a pretty interesting 34-key Kalimba called the Pisces!

I wanted a Kalimba to add interesting calming arps when composing game music for long. As soon as I see this arrangement which is currently not many brands are doing, I felt adventurous and wanted to explore. I love when a brand try to pioneer something and there are not much information anywhere else, I wanted to be at the frontier and experiment. Just like how I was messing around with Unity DOTS.

And so with magic of today's e-commerce, it finally appears before me. Let's get the research started.

In this article, I analyze the implication of this 34-key layout what possibilities are opened up. This assumes we will not re-tune the Kalimba to fit the song we want to play. We want the added flexibility of more tines to counter that!

If you wondered why this kind of article appears in a Unity game programming blog like this, I picked up some instruments in lockdown and the diagrams here were made with Unity..! And also just so you know the Kalimba sound is leaning nice into game soundtrack territory. This sonic character could be in calming village music or fantasy forest theme.

This Unity project I quickly whipped up in about an hour can ask all the tines to number itself according to either major or minor scale interval starting from any note and hide unrelated ones, so we could reveal interesting properties visually.

![](../../assets/65cb88d9a1f0e811.png)

This article requires a bit of music theory knowledge. (How many notes are there and their distances, key, chords, interval, diatonic, chromatic.) This maybe the first article taking the 34-key Kalimba seriously on the net since I can't find anything elsewhere, the 17-key version is so popular it dominates the scene. Therefore, let's start at 17-key.

## Recap the 17-key version's arrangement

![](../../assets/0c543849ea0a9a26.png)

The popular 17-key version is **diatonic centered around major scale.** It is literally centered, the root note is on the center tine. So it means either you bring the tuning hammer with you all the time in order to play all songs or you transpose any other song to this key you choose. Note that the hammer can't fix everything since tine length gets more limited on the edge, not only we can't get higher, shorter tines has less decay time as well and require more force to compensate.

It has alternating tines left and right to form a major scale starting from the center tine going left first. Numbers in the picture are note/key agnostic, it is the member of your major key.

For example, in C key Kalimba 1 is C, 6 is A. In music theory, there is no "black" notes since actually we have 12 notes lined up **linearly**. These 7 notes C D E F G A B C we see as a result of C major scale here looks linear but **they aren't,** only because of English alphabet tricks your eye but each one is 2 semitones apart, except BC and EF. So 7 notes looping can't be equally spaced, we need 12 notes and 2 kinds of distance : 1 semi + 2 semi. This is [maximal evenness](https://en.wikipedia.org/wiki/Maximal_evenness). In parallel world, we might have A B C D E F G H I J K L as notes and there is no sharp or flats since those would give the nearby alphabet without exceptions, if the English guys discovered chromatic before diatonic or something.

### Easy tonic chords glissando

The alternating tines are probably for ergonomics of distributing notes to both thumbs but that is not all, it allows single thumb 3 notes glissando to form **tonic chords **perfectly. Tonic chords means not just any chord but they could "work" together to create a song in a given key of music, creating tension and resolve back.

![](../../assets/5d44a5f221fb26de.png)

![](../../assets/740aaeffb714c3d0.png)

The green arrows are tonic major chords and red arrows are tonic minor chords. You can easily get your : I, ii, iii, IV, V, vi, vii chord of the tuning of your Kalimba with a gentle slide starting from the number that you want and going outwards. It automatically skips notes of an interval too close to the previous one automatically, which that would sound dissonance. To play the popular chord progression I -> IV -> V -> I, just find any number printing on the tines literally saying 1, 4, 5, 1 then slide away.

Piano players know keys close by could be used to form interesting uncommon chords to spice things up. Kalimba made the spice impossible when randomly brushing around. As a result if you left the Kalimba for other not knowing music to mess around, it would still sounds quite pleasant unlike if someone randomly press piano keys.

Also if you want to play ii minor chord, you can do 2 4 6 on the left side, but it also is available on the right side higher up! Talking about extremely lucky coincidence that there are 7 notes so by alternating left and right we get both even and odd numbers in one side. The 17-key arrangement is a very good idea, no wonder why it is popular.

I skipped 7 2 4, the diminished sounding chords, in the image to highlight all available major and minor chords. Of course you can play that for occasional spooky sound.

### 4-Note Chords

![](../../assets/368814ad6c0298b5.png)

We are even luckier that brushing 4 consecutive tines automatically get us the bluesy sounding **seventh chords **like 1 3 5 7 one, or 2 4 6 1 one.

- Blue arrows are
**major seventh chords.**Notice that we have 2 "1 3 5 7" position to play. - Magenta arrows are
**minor seventh chords**. Notice that we only have room to play the seventh version of vi chord, the 6 1 3 5, on the left side since the other one on the right starts late and the "seventh" component fell off the edge... - We can play
**dominant seventh**chord on the yellow arrow too, which would play G7 in this case.

Of course you can continue to get the rich **ninth chord **sound, etc.

### Range

![](../../assets/0c543849ea0a9a26.png)

Notice that the 1 note spans about 2 octaves, then we get a little 2 and 3 over and thats it.

If you play major key song in the same key as Kalimba, the "home" is probably 1 on the left side so you can go both up and down. Depending on song, if it gets emotional it maybe higher than then range that you need to move the "home" down to the center 1. (Which may gets too low to your liking, but thats "Kalimba arrangement" for you.)

### Another major scale choice (Mixolydian mode-like)

![](../../assets/c2d14e88b19523ff.png)

We can **somewhat** play the major scale of 5th member of the Kalimba's key too! In the case of C Kalimba, then this is how G major scale would play out. (G is perfect fifth from C.)

"Somewhat" means that **one tine will be wrong** if you really play Mixolydian of C scale compared to the real G major scale. So please play almost Mixolydian.

That tine is the "7" note. This note is a component of quite important V chord (5 7 1) so keep that in mind, and also iii (5 3 7). The vii (7 2 4) is rarely used, luckily. This note 7 is also used in a melody to lead into 1 so this will impact some songs doing that.

The wrong tine by the way, if you go ahead and play it in place of 7 in the context of G major scale then it is a sharpened 6 (or flattened 7) instead. You can use this fact to play new chords that has sharpened 6 as a component.

Also the flattened 7 wrong note has a name, the [subtonic](https://en.wikipedia.org/wiki/Subtonic). It also has many uses different from the correct one ([leading-tone](https://en.wikipedia.org/wiki/Leading-tone)). I would not consider playing in this position that "wrong".

Note that in harmonica, trying to play G major scale on C harmonica is called the 2nd position or the "cross harp". The blues player play in this position, the reason is because the "wrong" note happen to be exactly what blues want, it feels bluesy. So when playing G major blues song, harmonica finds a C major one and play in this position.

### Yet another major scale choice (Lydian mode-like)

![](../../assets/4e1c4e336f490d30.png)

Closely related to the perfect fifth above root is the perfect fourth, or in other words going counter clockwise in the Circle of fifths instead. In C Kalimba, the 4th member is F. This is how it looks like if we make the 4 note instead our new home.

If you really go ahead and play Lydian of C as a makeshift F major scale, you will also hit **one wrong note **in the same reason as the G major scale vs. C major scale but "to the other way". This time the missing note is the 4 note, which is a component of ii (2 4 6), IV (4 6 1), vii (7 2 4). The vii chord is rare so we are lucky, but missing ii or IV chord maybe problematic.

### Minor scale play (Aeolian mode)

You can play the **relative minor scale** of your Kalimba's key for some emotional songs and get the same glissando chord benefit. The home moves to note 6 and if you choose the 6 on the left side as your home then you get a bit higher upper range than the major scale playing.

Let's see if we look at the note 6 as a new 1 for our minor scale, what would it looks like. All tines are correct, naturally!

![](../../assets/df7f884ea559d752.png)

By shifting the numbers, range are affected. For example there is only 1 instance of 2 4 6 glissando remaining now. Poor II chord! (The II chord switched from vii that was in major scale.)

### Playing in Dorian or Phrygian mode for more minor scale choices

Same reasoning as when we want to play 2 more major scales with 1 wrong tine, you can do the same starting from A minor scale we can naturally play and go clockwise and counter clockwise. Therefore it is D (note 2 of C) and E (note 3 of C) minor scale we could also somewhat play with 1 missing note.

Here's how D minor scale on our C major Kalimba looks like. The missing note is 6. (It was 4 in major scale.)

![](../../assets/c43e382837134554.png)

Some observations :

- We have 1 3 5 glissando available to play the home minor chord on both sides.
- We also have 5 7 2 for minor scale version of V chord.
- 3 5 7 is also cool.
- 7 2 4 on both sides are not so useful in most songs.

Here's how E minor scale on our C major Kalimba looks like. The missing note is 2. (It was 7 in major scale.)

![](../../assets/cef18d9cc00215b2.png)

Some observations :

- We have 1 3 5 glissando available to play the home minor chord on both sides still but the position moved a bit.
- 5 7 2 no longer possible. (which is probably quite a big deal since it is a V chord)
- 3 5 7 is still possible.
- Now we can do 4 6 1 and 6 1 3 on both sides too.

Compared to major version, because the missing note is not 7, you don't get the leading-tone-to-subtonic benefit.

## Recap the 21-key version's arrangement

The extra 4 tines are added for extended **bass **sound.

![](../../assets/46e0a2a2a85f96f1.png)

They are jammed right in the middle as low 7 5 4 6 tines, so the center is **no longer your root note** of your key. You can still perform glissando chord trick from new bass notes, for example from the new low 4 6 into the original 1, or the new low 5 7 then onto the original 2.

These are also good idea since now you are able to lay down interesting interval **under** your melody as a representative of chords in the song.

## Here comes the 37-key arrangement

![](../../assets/a65621fc2614ea72.png)

The idea is to make a 2-row Kalimba where the first row is exactly like 17-key version (alternating major scale), then move the 4 extra bass tines of the 21-key out of the way to 2nd layer, **then fill the remaining upper tines with a sharpened note of the first layer. (one half step higher)**

This is a diagram from Seeds Kalimba Pisces :

![](../../assets/fbabcf33c3ab0724.png)

### Accidentally chromatic

Many call this "chromatic Kalimba" but notice that the upper tines aren't equivalent of black keys on the piano. They may ended up covering all notes chromatically "accidentally" but the upper tines do not care about that, they just want to **sharpen the lower one**.

First, the upper row 7 5 4 6 are **special,** they are not sharpened tines but your extra bass notes **in the major scale of lower row** that are now made "optional", inspired by 21-key design. You reach up for them when needed instead of having them breaking the flow of beautiful alternating 17-keys. These rows aren't adding any chromatic quality from 17-key design that was diatonic.

Now the sharpened tines are the real deal that adds chromaticity (that is a word?). Because playability is still centered around the lower row having major scale ready for you, using these upper tines for **accidental notes** that music composer added for spice maybe a good idea rather than trying to play in arbitrary keys.

However remember that among 12 notes in one octave, BC and EF are only 1 half step apart unlike the other guys. Therefore the sharpened 7 is 1 and the sharpened 3 is 4 in all major scale. We can see that the upper tines therefore sometimes include duplicated sound of the lower one. The upper tines are really meant for **sharpening**, not for covering all notes.

![](../../assets/a65621fc2614ea72.png)

### Make use of the duplicated sharpened notes

Having 2 more "1" note and "4" note available up there may comes in handy sometimes.

You can perform exact pitch unison with 2 same notes to amplify it, or you can **trill **the note with both of your thumb for style like some other instruments!

The 1 note is likely to sound good as an interval with the other tines in many situation since it is the root of the key that you are playing, assuming you are playing the same key as the Kalimba's key.

Any interval pair in your key with 1 and 4 is going to give you some more choices. So look out for them.

You can also perform this cool trick, **vertical glissando. **But you can only do it on 1 -> 7 and 4 -> 3. There are 4 positions you can do this. If you prepare your other thumb to add 6 and 2 respectively, it sounds quite like believable you just brushed with one thumb! Or you can drag diagonally and play other nearby interval as well. Might looks flashy in your Kalimba video..

### Bonus high-4 note

![](../../assets/be48c28ad5c127af.png)

Note that **the rightmost 4** is not exactly a duplicate since it is on doubly high octave. This give more variation for you to perform unison interval of various instances of 4.

Perhaps more importantly, it extends your range by 1 note in the key of C as if there is one more tine to the right of the rightmost tine, you just move up instead. This is because 3->4 is one of two place where we only need 1 semitone up to get to the next scale tone, lucky!

When playing on minor scale song and you start at 6 (to be your new 1), note 3 (the final lower tine) is the "5" of minor scale. 5th tone of any diatonic scale is the [dominant](https://en.wikipedia.org/wiki/Dominant_(music)), well documented as very important to the song. Therefore this bonus 4 will give you the "6" of minor scale, the [submediant](https://en.wikipedia.org/wiki/Submediant). So when you use the Pisces, you are able to play minor key songs that use this submediant-feel in the composition on high notes, provided that you transpose it to A minor first.

Most Kalimba stops at high 3 (E6 note, if in C tuning). Be warned that this bonus 4 tine is very short and hard, most low quality Kalimba would not sound great but it works on the Pisces, perhaps thanks to unibody metal saddle design.

### Arps from bass tines

It moves up the 4 bass tines from 21-key to above. If you want to arp from lower notes, then you cannot just brush your fingers. Instead to play the 4 available triad of your scale degree : 4 5 6 7 (**4** 6 1, **5** 7 2, **6** 1 4, **7** 2 4) starting from the bass tines, and send off to the higher octave, you follow a pattern like this :

![](../../assets/c17dd70a4ed35d27.png)

Some observations :

- All chords are one handed from bass tines, but at the moment you hit all 3 notes, the next one will be
**on the other hand**which you continue like the usual 17-key format. This works the same as in 21-key format, if you want to arp several times it would alternate sides. - Because the 3-note chord is splitted up into upper part and lower part, remember that the 4 and 5 chord will play the upper one 2 times, but 6 and 7 will play the lower one 2 times to not get confused.
- 2-note glissando as a part of chord maybe possible. If you want more challenge you can even do vertical one. (e.g. in 4 6 1, instead of glissando at 4 6, try 6 1 instead.)

### Sharpening minor chords into major

![](../../assets/1e48224f851d5523.png)

Since the upper tines are strictly sharpening the lower one, every time you play minor chord on the lower tines you can change the 2nd note to the upper one to instead get major chord. (But you can't glissando, do an arp instead.) Also the upper one must not be one of the special 4 bass tines.

It will be out of key, but some song use this trick to spice things up. (It sounds emotional in a certain progression, when listener think they get a minor next but instead it is a major.)

Available chords : 2 (right side), 3 (both sides), 6 (both sides). You cannot sharpen the 2 chord on the left side since it collides with the 7 bass tine, that one is not sharpening your note.

Inverse is possible, if you play major chords on the upper tines then you can turn it into a minor. But in your Kalimba's key, it is unlikely that you can play major chord on upper tines. (If you play C# major key on upper tines though this is very possible, explained later.)

### Now we have more scales for real!

Remember how we could only play perfect major key of the key of Kalimba and its relative minor key song, but when we push them further then there are tines missing?

Now that we have sharpened tines plus the bass tines, let's see how it turns out!

### Mixolydian-like (C major -> G major)

![](../../assets/bddc37eba7872ee7.png)

Instead of missing the 7 note now we have **one 7 note **waiting up there on the right side! Therefore it is now possible to play the G major scale on the middle range, or compose missing chords using that one lifeline we now have. We knew the wrong note was a flattened version of the right one, and luckily the sharpened tine give us that up above.

Note that it is possible to perform 5 on the right side and then **diagonal vertical glissando 7 2 **to perform 5 7 2, the essential V chord sound needed to finally go back home to I chord. Looks like that 7 will be your buddy when playing in this position!

Also notice that the 4 bass tines covers note 1, 2, 3 of the key on this position. Having deep 1 bass in that position will be very convenient.

Note that the fact that it is weird that we get only one 7 note in an entire board is because of "wrench" than the upper bass tines threw in. We likely get one more 7 if there is no bass tines there.

### Lydian-like (C major -> F major)

![](../../assets/f8770cc1aed440b4.png)

Recall that we were missing the 4 note. The sharpened tines gives us 4 notes on both sides. This make the 4th of home scale very usable!

Let's look at the chords that were missing :

- VI (4 6 1) has
**diagonal vertical glissando**of 4 1 available on the left and right side, then you just add 6 nearby to get it. The right side is difficult since the upper 4 has short tine. - Then ii (2 4 6) should be done with alternating thumbs since there are no nearby tines. We get one lucky vertical 2 6 on the bass tine area, if you would like a bassy ii chord.
- Lastly vii (7 2 4) is rarely used anyways.

Once again the 4 bass tines has 1, 2, 3 of the key. Now 1 is even on dead center!

### Aeolian (C major -> A minor)

![](../../assets/ae16f639afe62393.png)

What do we get more if we play relative minor? We get 1 and 2 bass to use. Two 6, two 3.

### Dorian-like (C major -> A minor -> D minor)

![](../../assets/7697b33de7e2e79a.png)

The 6 note was missing, now we get it on both sides. Unfortunately minor scales will not get the 4 bass tines cover the root note. Instead, we get a 4 and 5 bass tine that maybe useful for going back to the minor home.

### Phrygian-like (C major -> A minor -> E minor)

![](../../assets/698eae610b15b88b.png)

The missing note 2 was filled with one tine, at the same spot as 7 that was filled in our Mixolydian-as-new-major case. Music theory!

### Upper tines keys?

Inversely, there are possibilities that we could play some other keys that mainly use the new upper tines so we can instead be glissando up there for a lot and occasionally come down! This way 4 bass tines are likely out of key, but let's explore keys that has many in-key notes on the upper tines.

### C major -> C# major (+1 semi major)

![](../../assets/083a6c65f3e39ddd.png)

Playing one half step of your source key is the shortest way to sharpen all the things. And this works to our purpose!

- Useful chords all on upper tines. Left : vi (6 1 3), I (1 3 5), iii (3 5 7), V (5 7 2). Right : V (5 7 2), vii (7 2 4), ii (2 4 6), vi (6 1 3). We have V and vi on both sides. The home chord I is only on one side's glissando so we will have to pay attention to that.
- Only two 1 notes available, and they are all high pitch. This may force the range to be narrow, you many not be able to play songs that are too dynamic on this position.
- Important to note that if you ignore the 4 bass tines (ok the center one works as a note 3 bass),
**all upper tines are correct.**You just need to remember where are the 1 and center yourself around them. - Bass notes are limited. You only got low 7 and low 3 at your disposal. May need rearranging to brighter style to fit this.

If you have Seeds Instruments Pisces in C then look for songs in key of C# major. You can comfortably nail about 1.2 octave of this key via the upper tines. Tuning without hammers!

Another important implication : **1 semitone** **key shift. **Some songs shift keys **up** briefly to be emotional (e.g. Connect, Madoka OP, at the beginning) therefore if you transpose the song to C major (comfortably play on lower tines), then you get an easy shift to C# major by moving to this position on the same Kalimba.

### C major -> G# major (+8 semi major)

![](../../assets/681e5743eb173d65.png)

We get interesting clusters here. 6 consecutive notes on the left, 2 sets of 3 notes chord on the right. All 7 notes fell down.

### C major -> F# major (+6 semi major)

![](../../assets/8a7472efb772703f.png)

Only one 1 note on the board, this will be challenging! Probably the most difficult among the feasible major scales we can play on 34-key Kalimba.

### C major -> A# minor (+10 semi minor)

![](../../assets/8cc7675ae53c9759.png)

This is how to get the most of upper tines on minor key, in other words it is a relative minor of that C# major scale we explored earlier because we have almost the same right notes and same wrong notes except the bass upper tines.

Bass upper tines are all out of keys. This looks really playable, and there are tons of 2 notes. (Was 7 on the C# major scale earlier.)

Because this is the same pattern as C# major earlier, you can again perform **1 semitone key shift up **easily from A minor key. To get easy shift on minor key songs, transpose it to A minor then when the song gets emo to A# minor then play on upper tines. Bass notes are 2 and 5 only. Luckily we still have 2 instance of 1 note, with the low 1 almost fell off.

### C major -> F minor (+5 semi minor)

![](../../assets/30e508108fbc0e58.png)

This position gives you the root bass on upper center plus considerable amount of in-key tines on the 2nd layer. This is quite a spacious minor scale with three 1 notes available.

### C major -> D# minor (+3 semi minor)

![](../../assets/680d96b3100a46db.png)

This minor position also have a single 1 3 5 combo in an entire board on the right side, and one more high pitched 1 on the left. If you want to play song in D minor, it is allowed to dip under the 1 note for a bit but no more room over the next 1.

## The six practical positions for major and minor scales

In total I discovered 6 positions each for major and minor scales. For each type, 3 are centered around lower tines and 3 centered around upper tines. Upper tines version are on slight disadvantage since the center bass tines threw some wrenches in the equation

I will give my personal suitability rating as well and sort according to it.

Start with the lower tine-based shiftings in major :

- Main key ⭐️⭐️⭐️⭐️⭐⭐
- Mixolydian-like (+7 Major) ⭐️⭐️⭐️⭐️⭐
- Lydian-like (+5 Major) ⭐️⭐️⭐️⭐

And minors :

- Aeolian (Relative minor key, +9 Minor) ⭐️⭐️⭐️⭐️⭐️⭐
- Phrygian-like (+4 Minor) ⭐️⭐️⭐️⭐️⭐
- Dorian-like (+2 Minor) ️⭐️⭐️⭐️⭐

Then upper tines-based starts from 3 stars. The reason because middle upper tines are occupied by the basses and needs to be avoided most of the time unless stars really aligned. Plus when you play you need to be more careful not to accidentally hit the lower one.

- +1 Major ⭐️⭐️⭐️
- +8 Major ⭐️⭐
- +6 Major ⭐

Minors :

- +10 Minor ⭐️⭐️⭐️
- +5 Minor ⭐️⭐
- +3 Minor ⭐

This is the legend of stars :

- ⭐⭐⭐⭐⭐⭐ : Perfect, everything playable on lower tines.
- ⭐⭐⭐⭐⭐ : One note on upper tines required to complete.
- ⭐⭐⭐⭐ : Still centered on lower tines, but more notes on the upper.
- ⭐⭐⭐ : Centered around upper tines. Few notes required on the lower.
- ⭐⭐ : ️Slightly harder than 3 stars. More notes needed on the lower.
- ⭐ : ️Yet harder than 2 stars. Probably the hardest that is still practical.

Because each star has major and minor, C major Kalimba can play practically in 12 keys out of all common 24 keys (major & minor *12)! Though with varying difficulties, but thats something to practice on right? It's a skill ceiling!

Why don't we try making a table assuming the Kalimba is in other key, what keys could it practically play? Seeds Instrument 34-key Pisces is available in C and B. But just in case other companies follow suit with more keys.

![](../../assets/959ac3db8834a322.png)

Or if sorted by major/minor keys :

![](../../assets/20d00577be72c79a.png)

The table also reveals that the upper tine positions (3 stars difficulty and lower) are all sharpened of lower tines. (e.g. C G F -> C# G# F#, A E D -> A# F D#) This is because one semitone higher is an effective way to "blacken" everything in piano keys perspective, shifting the correct notes all up.

Remembering the "plus" from main key will be difficult, so for me personally I would like to rename them based on those stars I gave, inspired by Harmonica's "straight harp", "cross harp", double-cross harp" positions.

This is my personal "Sirawat's 34-key Kalimba positions". Naming format is by tines row which it is mainly on (upper or lower) and ordered by playability (1, 2, or 3) and finally is it a major or minor.

- ⭐⭐⭐⭐⭐⭐ : 1st lower major/minor position. (1LP Major/Minor)
- ⭐⭐⭐⭐⭐ : 2nd lower major/minor position. (2LP Major/Minor)
- ⭐⭐⭐⭐ : 3rd lower major/minor position. (3LP Major/Minor)
- ⭐⭐⭐ : 1st upper major/minor position. (1UP Major/Minor)
- ⭐⭐ : ️2nd upper major/minor position. (2UP Major/Minor)
- ⭐ : ️3rd upper major/minor position. (3UP Major/Minor)

Replacing the previous table, we get :

![](../../assets/00bd2ad5f2a1f814.png)

![](../../assets/5bcfd8684f120173.png)

To make good use of these stars on my practice with my C key 34-key Kalimba, I of course should look to play C major and A minor key songs on mainly lower tines first. (Or transpose other songs to C major or A minor)

In addition, G major and E minor will be great and satisfying to pull of, and F major and D minor will be more challenging. Once I am good with that, it is time to explore 6 more upper tine-based positions once again.

Not sure if this result was intended by Seeds Pisces designer or not. But yeah, you created a monster! (That's a compliment)

That table's CSV was assembled from strings printed from Unity too. Thanks Unity!

![](../../assets/3e8c3a1a2ceb5350.png)

![](../../assets/3552e4fc764a3638.png)

![](../../assets/6732a17ca863bc74.png)

Just in case you want to do something with it :

```
C,A,G,E,F,D,C#/Db,A#/Bb,G#/Ab,F,F#/Gb,D#/Eb
C#/Db,A#/Bb,G#/Ab,F,F#/Gb,D#/Eb,D,B,A,F#/Gb,G,E
D,B,A,F#/Gb,G,E,D#/Eb,C,A#/Bb,G,G#/Ab,F
D#/Eb,C,A#/Bb,G,G#/Ab,F,E,C#/Db,B,G#/Ab,A,F#/Gb
E,C#/Db,B,G#/Ab,A,F#/Gb,F,D,C,A,A#/Bb,G
F,D,C,A,A#/Bb,G,F#/Gb,D#/Eb,C#/Db,A#/Bb,B,G#/Ab
F#/Gb,D#/Eb,C#/Db,A#/Bb,B,G#/Ab,G,E,D,B,C,A
G,E,D,B,C,A,G#/Ab,F,D#/Eb,C,C#/Db,A#/Bb
G#/Ab,F,D#/Eb,C,C#/Db,A#/Bb,A,F#/Gb,E,C#/Db,D,B
A,F#/Gb,E,C#/Db,D,B,A#/Bb,G,F,D,D#/Eb,C
A#/Bb,G,F,D,D#/Eb,C,B,G#/Ab,F#/Gb,D#/Eb,E,C#/Db
B,G#/Ab,F#/Gb,D#/Eb,E,C#/Db,C,A,G,E,F,D
```


You can use these stars rating effectively like this : if you want to jam together with others perhaps while drinking with an acoustic guitar, a common problem is that they don't want to transpose the song just for you to be able to play on 1st position, but transpose down a bit from the original key mainly so the singer is more comfortable. (We are chilling so we don't want to get too high, and inexperienced singer that can't get high could join.) Guitar players can use a capo, but Kalimba player can't use a tuning hammer that fast. So you can remember this if you own a C Kalimba : C G F C# G# F# (major), or A E D A# F D# (minor) (all the playing positions in ascending star difficulty order) and ask for a compromise if we could get the key to be one of these.

### Diagrams recap, lower tine positions :

![](../../assets/a65621fc2614ea72.png)

![](../../assets/bddc37eba7872ee7.png)

![](../../assets/f8770cc1aed440b4.png)

![](../../assets/ae16f639afe62393.png)

![](../../assets/698eae610b15b88b.png)

![](../../assets/7697b33de7e2e79a.png)

### Diagrams recap, upper tine positions :

![](../../assets/083a6c65f3e39ddd.png)

![](../../assets/681e5743eb173d65.png)

![](../../assets/8a7472efb772703f.png)

![](../../assets/8cc7675ae53c9759.png)

![](../../assets/30e508108fbc0e58.png)

![](../../assets/680d96b3100a46db.png)

### New chord possibilities

With all the scales explored, also we have more ways to play chords that has out-of-key component.

For example, any time you play a major chord and its middle component lands on upper tine, you can move that down to instantly transform it to minor chord! And vice versa, any minor chord on lower tines can be turned into major by moving the middle component up. Quite good amount of songs unexpectedly play the major-minor inverted version of the chord to defy expectation of listener, we can now cover that with this 34-key Kalimba.

Other exotic chords may appear accidentally, like augmented or suspended chords that requires some notes closer to each other. I have not look closely at these yet but it will be interesting to play these sounds.

## Conclusion

34-key arrangement on Seeds Instruments Pisces adds tons of entangled possibilities, just like how 6 open guitar strings gave birth to million of both practical and impractical chord shapes. If we figured out music theory behind a particular "system" produced by the instrument, chances are we will have a lot of fun stuff we could practice on! Overall, I am content with my 34-key Kalimba purchase and I will try to get better on it.

Ps. They made a new monster again called the Columbus. 24-key, but in ascending order, diatonic, allowing complete L-R hand multitasking like the piano. Some sick constant chords running while melody doing its own thing on the right side is now easier. Glissando always go from left to right. The most important appeal for me is that it goes **high, **a blessing for minor key music lover like me since when you play in A minor (relative minor of C major that most Kalimba came with), the upper range gets eaten up by the shift and make emotional part of the song fell off the edge.. This also looks fun! But I don't have any more spare cash to get another.. for now. 😂 Maybe, I will be back with an another analysis on the Columbus in the future!