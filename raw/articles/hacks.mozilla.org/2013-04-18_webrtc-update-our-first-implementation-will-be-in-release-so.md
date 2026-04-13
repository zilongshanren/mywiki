---
title: 'WebRTC Update: Our first implementation will be in release soon. Welcome to
  the Party! But Please Watch Your Head. – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2013/04/webrtc-update-our-first-implementation-will-be-in-release-soon-welcome-to-the-party-but-please-watch-your-head/
author: Adam Roach
published: '2013-04-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

I want to share some useful and exciting updates on Firefox’s WebRTC implementation and provide a sneak peak at some of our plans for WebRTC moving forward. I’ll then ask Adam Roach, who has worked in the VoIP/SIP space on IETF standards for over a decade and who joined the Mozilla WebRTC in November, to provide some historical background on the WebRTC feature itself and how things are progressing in general.

### Getting ready to release our first implementation of WebRTC on Desktop

Firefox has made significant progress with our initial implementation of WebRTC on Desktop in terms of security and stability. For the last several weeks, PeerConnection and DataChannels have been pref’d on by default in [Nightly](http://nightly.mozilla.org/) and Aurora, and we expect to keep them pref’d on for all release phases of Firefox 22 (which means we expect WebRTC will go to Aurora, Beta and General Release).

We also got a chance to update the DataChannels implementation in Firefox 22 to match the recent spec changes (agreed to at IETF last month). Note: [the changes we needed to make](http://mozilla.github.io/webrtc-landing/DataChannel_changes.html) to comply with the spec changes are not backwards compatible with previous DataChannels implementations (in Firefox 21 or earlier). So please use Firefox 22 and later for testing your DataChannels apps.

### TURN support has landed

And there’s more good news. We just added TURN support to Firefox Nightly and are in the process of testing it. This is a big deal since TURN will increase the likelihood that a call will successfully connect, regardless of the types of NATs that the end points are behind.

[TURN (Traversal Using Relays behind NATs)](http://en.wikipedia.org/wiki/Traversal_Using_Relay_NAT) is a standard for managing (allocating, using, and destroying) a relay session on a remote external server. This relay session enables WebRTC to connect when the NATs at both ends would otherwise cause the call to fail. Because TURN can introduce delay, especially if the TURN server is remote to both endpoints, and TURN servers can be expensive (because it has to handle all the media flows during a call), ICE typically uses TURN only when other methods (like STUN) to get media flowing during a call fail to work.

### WebRTC on Firefox for Android is Ready for Experimentation and Feedback

Back in February at Mobile World Congress we showed exciting, new demos of WebRTC calls on Firefox for Android. We have just finished landing this code in [Nightly](http://nightly.mozilla.org/). The code for both getUserMedia (gUM) and PeerConnection is behind a pref (as Desktop was initially), but you can enable it by setting both the `media.navigator.enabled`

pref and the `media.peerconnection.enabled`

pref to “true” (browse to `about:config`

and search for `media.navigator.enabled`

and `media.peerconnection.enabled`

in the list of prefs).

In the same list of prefs, you can also set `media.navigator.permission.disabled`

to “true” to automatically give permission to access the camera/microphone and bypass the permission/selection dialog when testing gUM and WebRTC.

This code is still in the early phases of testing, but we encourage you to try it, [report back problems](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&component=WebRTC), and [ask questions and provide feedback](https://groups.google.com/forum/#!forum/mozilla.dev.media). Please be sure to mention “Android” if you are reporting a problem or providing feedback since we are tracking both Android and Desktop issues now. Like with Desktop, we will be working to improve, stabilize and expand this code over the next year.

### WebRTC on Firefox OS Coming Next

Mozilla is also working hard to get this code running on Firefox OS. WebRTC on Firefox OS is not yet as far along as WebRTC on Firefox for Android, but the Firefox OS team is working to close the gap. You can [follow Bug 750011 ](https://bugzilla.mozilla.org/show_bug.cgi?id=750011) to track this work.

### Future WebRTC Features

Since all our products share the gecko engine, improvements and new features made to core “platform” or gecko code typically benefit all our products. Over the next year we plan to make the following improvements:

- Complete error and state reporting (spec compliant)
- Recording API support
- Persona integration
- Multiple audio and video flows per Peer Connection (beyond 1 video flow and 1 audio flow)
- Persistent permissions support (in the UX/UI)
- AEC improvements
- Improved call quality (especially audio latency)

We hope to do even more, but these are on the top of our list. We also have a [WebRTC documentation and help page](https://developer.mozilla.org/en-US/docs/WebRTC) that we’re working to fill out over the next few weeks and then keep up-to-date. That will have links to what we’ve implemented and what we’re working on, as well as ways for contributors to get involved.

### Moving Forward

Although we can’t wait to release our first implementation of WebRTC on Desktop (which is a huge milestone for Mozilla and the WebRTC feature itself), I am still encouraging all developers experimenting with WebRTC to continue to use Nightly for the foreseeable future because that is where the latest and greatest features from the spec land and bugs get fixed first — and that is where your feedback will be most helpful.

And even more importantly, the WebRTC spec itself is still being standardized. For more details on that, as well as some behind-the-scenes history on WebRTC, I hand the rest of this article off to Adam.

-Maire Reavy, Product Manager, Mozilla’s Media Platform Team

### WebRTC is the Real Future of Communications

This is Adam.

About three years ago, my dear friend and VoIP visionary Henry Sinnreich spent some time over lunch trying to convince me that the real future of communications lay in the ability to make voice and video calls directly from the ubiquitous web browser. I can still envision him enthusiastically waving his smartphone around, emphasizing how pervasive web browsers had become. My response was that his proposal would require unprecedented cooperation between the IETF and W3C to make happen, and that it would demand a huge effort and commitment from the major browser vendors. In short: it’s a beautiful vision, but Herculean in scope.

Then, something amazing happened.

### WebRTC sees the light of day

Over the course of 2011, the groundwork for exactly such IETF/W3C collaboration was put in place, and a broad technical framework was designed. During 2012, Google and Mozilla began work in earnest to implement towards the developing standard.

Last November, San Francisco hosted the first WebRTC expo. The opening keynote was packed to capacity, standing room only, with people spilling out into the hallway. During the following two days, we saw countless demos of nascent WebRTC services, and saw dozens of companies committed to working with the WebRTC ecosystem. David Jodoin shared with us the staggering fact that half of the ten largest US banks are already planning their WebRTC strategy.

And in February, Mozilla and Google drove the golden spike into the WebRTC railroad by [demonstrating a real time video call between Firefox and Chrome](https://hacks.mozilla.org/2013/02/hello-chrome-its-firefox-calling/).

### So Where Are We?

With that milestone, it’s tempting to view WebRTC as “almost done,” and easy to imagine that we’re just sanding down the rough edges right now. As much as I’d love that to be the case, there’s still a *lot* of work to be done.

Last February in Boston, we had a joint interim meeting for the various standards working groups who are contributing to the WebRTC effort. Topics included issues ranging from the calling conventions of the WebRTC javascript APIs to the structure of how to signal multiple video streams – things that will be important for wide adoption of the standard. I’m not saying that the WebRTC standards effort is struggling. Having spent the past 16 years working on standards, I’m can assure you that this pace of development is perfectly normal and expected for a technology this ambitious. What I *am* saying is that the specification of something this big, something this important, and something with this many stakeholders takes a long time.

### Current state of standards

Even if the standards work were complete today, the magnitude of what WebRTC is doing will take a long time to get implemented, to get debugged, to get right. Our golden spike interop moment took substantial work on both sides, and revealed a lot of shortcomings in both implementations. Last February also marked the advent of [SIPit 30](https://www.sipit.net/SIPit30_summary), which included the first actual WebRTC interop testing event. This testing predictably turned up several new bugs (both in our implementation as well as others’), on top of those limitations that we already knew about.

When you add in all the features that I know neither Mozilla nor Google has begun work on, all the features that aren’t even specified yet, there’s easily a year of work left before we can start putting the polish on WebRTC.

We’re furiously building the future of communications on the Internet, and it’s difficult not to be excited by the opportunities afforded by this technology. I couldn’t be more pleased by the warm reception that WebRTC has received. But we all need to keep in mind that this is still very much a work in progress.

![](../../assets/0131eae30f299fea.png)


### Come and play! But please watch your head.

So, please, come in, look around, and play around with what we’re doing. But don’t expect everything to be sleek and finished yet. While we are doing our best to limit how the changing standards impact application developers and users, there will be inevitable changes as the specifications evolve and as we learn more about what works best. We’ll keep you up to date with those changes here on the Hacks blog and try to minimize their impact, but I fully expect application developers to have to make tweaks and adjustments as the platform evolves. Expect us to take us a few versions to get voice and video quality to a point that we’re all actually happy about. Most importantly, understand that no one’s implementation is going to completely match the rapidly evolving W3C specifications for quite a while.

I’m sure we all want 2013 to be “The Year of WebRTC,” as some have already crowned it. And for early adopters, this is absolutely the time to be playing around with what’s possible, figuring out what doesn’t quite work the way you expect, and — above all — providing feedback to us so we can improve our implementation and improve the developing standards.

As long as you’re in a position to deal with minor disruptions and changes; if you can handle things not quite working as described; if you are ready to roll up your sleeves and influence the direction WebRTC is going, then we’re ready for you. Bring your hard hat, and keep the lines of communication open.

For those of you looking to deploy paid services, reliable channels to manage your customer relationships, mission critical applications: we want your feedback too, but temper your launch plans. I expect that we’ll have a stable platform that’s well and truly open for business some time next year.

*Credits: Original hardhat image from openclipart.org; Anthony Wing Kosner first applied the “golden spike” analogy to WebRTC interop.*

## About
[
Adam Roach ](http://sporadicdispatches.blogspot.com/)

Adam Roach works with Mozilla's WebRTC implementation team putting real-time technologies into the core library shared by Firefox and FirefoxOS. He has been crafting the world of Real Time Communications over IP since 1997 by doing protocol standardization, architecture, design, and implementation.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 24 comments

Hervé RenaultApril 18th, 2013 at 06:23Robert Nyman [Editor]April 18th, 2013 at 11:52Doug PeltonApril 18th, 2013 at 21:56KimApril 18th, 2013 at 08:17Robert Nyman [Editor]April 18th, 2013 at 11:54Gervase MarkhamApril 19th, 2013 at 09:11Adam RoachApril 19th, 2013 at 09:55Maire ReavyApril 19th, 2013 at 13:16Gervase MarkhamApril 19th, 2013 at 13:21Maire ReavyApril 19th, 2013 at 13:32cameronApril 20th, 2013 at 20:49Adam RoachApril 22nd, 2013 at 07:28Victor WibisonoApril 23rd, 2013 at 21:12Robert Nyman [Editor]April 24th, 2013 at 04:07Gervase MarkhamApril 24th, 2013 at 06:25FabianApril 26th, 2013 at 00:57LennieMay 4th, 2013 at 01:50jamie McDonnellApril 25th, 2013 at 00:50Robert Nyman [Editor]April 25th, 2013 at 02:09FabianApril 25th, 2013 at 03:25Gene VayngribMay 11th, 2013 at 00:17Robert Nyman [Editor]May 12th, 2013 at 07:22Gene VayngribMay 14th, 2013 at 10:29Robert Nyman [Editor]May 14th, 2013 at 15:31