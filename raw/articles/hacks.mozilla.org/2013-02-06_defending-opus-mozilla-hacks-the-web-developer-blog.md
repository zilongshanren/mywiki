---
title: Defending Opus – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2013/02/defending-opus/
author: Jean-Marc Valin
published: '2013-02-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

On January 18th, France Telecom filed an [IPR disclosure](https://datatracker.ietf.org/ipr/1949/) against [Opus](https://hacks.mozilla.org/2012/09/its-opus-it-rocks-and-now-its-an-audio-codec-standard/) citing a single patent under non-royalty free terms. This raises a key question – what impact does this have on Opus? A close evaluation indicates that it has no impact on the [Opus specification](http://tools.ietf.org/html/rfc6716) in any way.

## Summary:

A careful reading of the FT patent reveals that:

- The FT patent does not cover the Opus reference implementation because critical limitations of the claim are absent;
- The patent is directed to encoders, therefore it cannot affect the Opus specification, which only includes conformance tests for the decoder, and
- With a simple change, we can make non-infringement even more obvious.

Let’s expand on those points a bit. If you don’t want to hear about patent claims, you should stop reading this article now.

## Details:

IETF IPR disclosures are a safe course of action for patent holders: they prevent unclean hands arguments or implied license grants. However, because the IETF requires specific patent numbers in these disclosures, we can analyze the claims. The patent in question is [EP0743634B1](http://www.google.com/patents/EP0743634B1), and the corresponding U.S. and other related foreign patents: “Method of adapting the noise masking level in an analysis-by-synthesis speech coder employing a short-term perceptual weighting filter”. It has a single independent claim, Claim 1. All of the other claims are “dependent claims” built on top of Claim 1. If Opus does not infringe Claim 1, it cannot infringe any other claim.

### The FT patent doesn’t cover Opus

To establish infringement, all of the elements of a claim must be present in an implementation. Key elements of Claim 1 are not present in the Opus reference implementation, including, among others

*The way the*In Claim 1, two parameters γ[bandwidth expansion](http://en.wikipedia.org/wiki/Bandwidth_expansion)coefficients are used.1and γ2are used to shape the quantization noise added by the lossy compression by “minimizing the energy of an error signal resulting from the filtering of the difference between the speech signal and the synthetic signal.” Opus doesn’t do this. Instead, the Opus encoder uses a single parameter`BWExp2`

to shape the noise, and uses a different parameter`BWExp1`

to shape the*input*signal, and also applies an additional gain to the filtered input to match the volume of the original.*The optimization criterion.*Opus doesn’t compute the “difference between the speech signal and the synthetic signal”. We**want**to code a signal that differs from the original speech, so we don’t compare what we code to the original speech. This is actually one of the main innovations in Opus: it’s the reason the SILK layer doesn’t need a post-filter like many other codecs do.

Thus Opus doesn’t perform the steps of the claim and cannot infringe the FT patent by definition. Of course this is not a legal opinion, but it doesn’t take a lawyer to figure this out. While we don’t know why FT disclosed this patent, we welcome the opportunity to evaluate such disclosures and remove any real or perceived encumbrances. This is one of the benefits of the IETF process.

### The FT patent cannot threaten the specification

The FT patent covers perceptual noise weighting, which is specific to an encoder. The claim is about the “difference between the speech signal and the synthetic signal”, when a decoder — by definition — doesn’t have access to the input speech signal.

The Opus specification only demands specific behavior from decoders, leaving the encoder largely unspecified. Even if France Telecom were to continue to assert its patent against Opus, there’s no limit to what we could change in the encoder to avoid whatever theory they have. No deployed systems break. There’s no threat to the Opus standard. We can safely say that the FT patent doesn’t encumber Opus for this reason alone.

### We can always make things even safer if needed

While we don’t believe that the Opus encoder ever infringed on this patent, we quickly realized there is a simple way to make non-infringement obvious even without analyzing complex DSP filters.

This can be done with a simple change ([patch file](http://opus-codec.org/downloads/constant_bwexp.patch)) to the code in silk/float/noise_shape_analysis_FLP.c (an equivalent change can be made to the fixed-point version).

Original code:

strength = FIND_PITCH_WHITE_NOISE_FRACTION * psEncCtrl->predGain; BWExp1 = BWExp2 = BANDWIDTH_EXPANSION / ( 1.0f + strength * strength );delta = LOW_RATE_BANDWIDTH_EXPANSION_DELTA * ( 1.0f - 0.75f * psEncCtrl->coding_quality ); BWExp1 -= delta; BWExp2 += delta;

New code:

BWExp1 = BWExp2 = BANDWIDTH_EXPANSION;delta = LOW_RATE_BANDWIDTH_EXPANSION_DELTA * ( 1.0f - 0.75f * psEncCtrl->coding_quality ); BWExp1 -= delta; BWExp2 += delta;

Yup, that’s all of two lines changed. This makes the filter parameters depend only on the encoder’s bit-rate, which is clearly not, “spectral parameters obtained in the linear prediction analysis step,” as required by Claim 1. Below is the quality comparison between the original encoder and the modified encoder (using [PESQ](http://en.wikipedia.org/wiki/PESQ)). As you can see, the difference is so small that it’s not worth worrying about.

## About
[
Jean-Marc Valin ](https://jmvalin.ca/)

Jean-Marc Valin has a B.S., M.S., and PhD in Electrical Engineering from the University of Sherbrooke. He is the primary author of the Speex codec and one of the main authors of the Opus codec. His expertise includes speech and audio coding, speech recognition, echo cancellation, and other audio-related topics. He is currently employed by Mozilla to work on next-generation multimedia codecs.

## About
[
Timothy B. Terriberry ](http://people.xiph.org/~tterribe/)

Timothy B. Terriberry is a long-time volunteer for the Xiph.Org foundation, working on codecs such as Theora, Vorbis, CELT, and Opus. He has been contributing to Mozilla's media support since 2008 and hacking on WebRTC since 2010.

## About Greg Maxwell

Greg has worked on unencumbered multimedia codecs with the Xiph.Org Foundation since 1999 and is currently working for Mozilla on next-generation royalty-free video coding standards.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 7 comments

?February 6th, 2013 at 07:34Timothy B. TerriberryFebruary 6th, 2013 at 07:38Omega XFebruary 6th, 2013 at 13:21DynamicFebruary 6th, 2013 at 14:23Sam WatkinsFebruary 8th, 2013 at 10:18gnuzerFebruary 14th, 2013 at 17:00Omega XFebruary 17th, 2013 at 04:25