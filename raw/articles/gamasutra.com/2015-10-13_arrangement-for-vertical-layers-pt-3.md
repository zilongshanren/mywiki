---
title: Arrangement for Vertical Layers Pt. 3
url: https://www.gamedeveloper.com/audio/arrangement-for-vertical-layers-pt-3
author: Winifred Phillips
published: '2015-10-13'
source_blog: Gamasutra.com - Expert Blogs
source_site: https://www.gamasutra.com/blogs/expert/
category: game programming
fetched: '2026-04-13'
---

![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)


![Game Developer Logo Game Developer Logo](../../assets/2f51b74e2f257c6f.png)

**Featured Blog | **This community-written post highlights the best of what the game industry has to offer. Read more like it on the __Game Developer Blogs.__

# Arrangement for Vertical Layers Pt. 3

The third installment of a three-part article series on arrangement for dynamic music systems, with examples from the LittleBigPlanet franchise. Part 3 explores arrangement techniques used for creating harmonic support in a complex vertical arrangement.

![Game Developer Game Developer logo in a gray background | Game Developer](../../assets/de0d06fe69cb2dbe.png)

![Arrangement for Vertical Layers - Winifred Phillips Arrangement for Vertical Layers - Winifred Phillips](../../assets/32eba4b697c584ae.jpg)


Okay, all caught up now? Ready? Let's go!

# Harmonic support / chords

![Harmonic support / chords - Winifred Phillips Harmonic support / chords - Winifred Phillips](../../assets/e0cca2e1a0993f99.png)


Here's a nicely simple video demonstration of this concept produced by the music tutorial site Rhythmic Canada. Let's take a look at the most famous and popular harmonic progression: dominant seventh to tonic.

The progression of chords can lend a sensation of momentum to any composition, implying moments of tension and release as chords proceed in logical and aesthetically desirable ways. As an arranger, it's our job to decide what instruments will carry what notes within the chords, and how each individual chord will be voiced. Let's start with the concept that should be pretty familiar by now: it's occupied the top of our list of considerations in the past two installments of this blog series!

## Effective technique: voice leading / step-wise movement

![](../../assets/e1a11ceb31335db9.jpg)


## Effective technique: close position voicing

In creating chord progressions, we have to consider how we want to space the individual notes of the chord. Close together, or far apart? There are valid reasons to choose either approach, but the Vertical Layering system tends to favor one technique over the other. First, let's look at them both.

![Open Position Voicing - Winifred Phillips Open Position Voicing - Winifred Phillips](../../assets/a9034bd376a92f1e.jpg)


![Close Position Voicing - Winifred Phillips Close Position Voicing - Winifred Phillips](../../assets/b301a7d21e71be76.jpg)


Close position voicing can be especially useful in Vertical Layers, because the frequency range is specific and limited. A layer with close voiced chords will occupy a very specific slice of the available frequency range of the overall mix, so when the layer is deactivated, the removal of that frequency range will be sharply noticeable. Close voiced chords also leave lots of room in the composition for other elements - such as melodies and countermelodies.

Here's an example from LittleBigPlanet 3 The Pod - this is the music from the LittleBigPlanet 3 videogame that greets us at the beginning of the game and whenever we return to the main menu. The harmonic structure is carried and reinforced by a women's choir singing close position chords. Notice how the chords are fully and satisfyingly voiced in a somewhat limited range:

Let's hear how the same section of the composition sounds with the fuller mix now active:

The closely-packed notes of the women's choir fit snugly into the mix without interfering with other musical elements, including the melody and countermelody.

## Effective technique: inversions

![Chord inversions - Winifred Phillips Chord inversions - Winifred Phillips](../../assets/a7d847cc751fa19b.jpg)

[Assaf Tal](https://www.youtube.com/user/MangoldProject/about) for his video series Piano Quickie:

Inversions can be especially useful for Vertical Layering. Often we need to add a sense of chord structure to a layer, so that it will be satisfying when played in isolation. At the same time, another layer may also have needed a harmonic foundation in order to work well when playing alone. So, how do we keep these two chord progressions differentiated from each other? By using different chord inversions in the two layers! That way, we can create a sense of uniqueness in the two chord progressions, while still providing a satisfying harmonic foundation for each layer. Let's listen to an example:

In the LittleBigPlanet Cross Controller game, the player navigates whimsical platforms and obstacles while advancing through an oddball science-fiction epic. The HenOMorph track provided music for a particularly wacky portion of the adventure. Two of the layers included chord progressions. The first layer would often play when our character floated in outer space. A floaty synth carries the chord progression, which gives an impression of downward movement:

The next layer consisted of a countermelody and a chord progression carried by an electric piano. Notice that the chords are now inverted, and this change causes the chords to convey some upward movement:

Now let's listen to that portion of the composition with all layers active:

This example also demonstrates another effective technique, so let's briefly discuss it:

## Effective technique: masking

![Masking - Winifred Phillips Masking - Winifred Phillips](../../assets/e71967965a854e40.jpg)


In the HenOMorph example (above), the gentle synth chord progression sounds effectively floaty and surreal - ideal for weightless spacewalks. When the layer is played alone, it conveys a very distinct atmosphere. However, when we activate the other layer that carries a similar chord progression, the synth is masked by the stronger and more aggressive tone of the electric piano. The two sounds blend. This is useful, because the two sounds are able to coexist in the full mix, and still create very different textures when their layers are played alone.

## Questionable technique: dense chord voicing between layers

While it's possible to include chord progressions in multiple layers and vary the chords with inversions and disparate voicings in order to not exactly duplicate musical content, we should be careful not to create too dense a texture when the layers are played together. Vertical layering is all about simultaneous independent musical content, and compositions created for this system tend to already be busy by nature. By stacking chords up and down so that they occupy a wide range of frequencies, we may effectively fill up all available sonic space. The final result could turn into a wall of sound through which no melody or countermelody could hope to be heard clearly.

![Wall of Sound - Winifred Phillips Wall of Sound - Winifred Phillips](../../assets/363da92a165db6c7.jpg)


## Questionable technique: modulation

Ah, the key change! Bringer of epic drama to music throughout the ages. Modulation, otherwise known as the key change, is a powerful tool for an arranger to elevate the energy level of a piece or extend it into yet another emotional repetition of that awesome chorus. Here's a fun video produced by the music group [CDZA](https://twitter.com/cdzamusic) that demonstrates epic key changes as they occurred in lots of successful pop songs:

While key changes are wonderful for infusing drama into a composition, they can be a real problem for interactive music (and for game music in general). Music for video games is often designed to loop. This means that when the track reaches the end of its running time, it will immediately return to the beginning and start playing again. Composing music to seamlessly loop is an art form in and of itself - one that I explore at length in my book, [A Composer's Guide to Game Music](http://amzn.com/0262026643). I won't go into a full discussion of that topic here, but I will mention that creating an effective loop entails a musical structure that doesn't include any startling or arresting moments. Such attention-grabbing moments would be instantly recognized when they play again, alerting the listener to the looping nature of the track. A key change is precisely one of those arresting details that would definitely be remembered and acknowledged upon repetition.

There are, however, ways to get around this problem and still employ modulation in our arrangements. To make this work, we have to create a precedent that modulation is a naturally occurring phenomenon in our piece, taking place at regular intervals. If key changes happen multiple times, rather than just in one big instance, our listeners will be less likely to recognize any of the individual modulations when they play again.

# Conclusion

So we've reached the end of this three-part blog series on the art of arrangement for dynamic music systems in games. We've covered a lot of ground, and explored a lot of issues that confront arrangers working with an interactive system based on Vertical Layers. If you have any questions, observations or personal experiences you'd like to share, please feel free to post them in the comments!


![Composer Winifred Phillips Composer Winifred Phillips](../../assets/00c2c1b9bace2643.png)

[A COMPOSER'S GUIDE TO GAME MUSIC](http://amzn.com/0262026643), published by the Massachusetts Institute of Technology Press. As a VR game music expert, she writes frequently on the future of music in virtual reality video games.

Follow her on Twitter [@winphillips](http://www.twitter.com/winphillips).