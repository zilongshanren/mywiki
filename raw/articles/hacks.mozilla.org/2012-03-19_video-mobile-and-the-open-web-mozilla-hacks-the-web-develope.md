---
title: Video, Mobile, and the Open Web – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/03/video-mobile-and-the-open-web/
author: Brendan Eich Posted; Firefox; Video
published: '2012-03-19'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Also [posted](http://brendaneich.com/2012/03/video-mobile-and-the-open-web/) at [brendaneich.com](http://brendaneich.com/).]

I wrote [The Open Web and Its Adversaries](http://brendaneich.com/2007/03/the-open-web-and-its-adversaries/) just over **five years ago**, based on the first [SXSW](http://sxsw.com/) [Browser Wars](http://www.pcmag.com/slideshow_viewer/0,3253,l%253D202844%2526a%253D202844%2526po%253D34,00.asp?p=n) panel (we just had our [fifth](http://schedule.sxsw.com/2012/events/event_IAP12185), it was great — thanks to all who came).

### Some history

The [little slideshow](https://developer.mozilla.org/presentations/sxsw2007/the_open_web/) I presented is in part quaint. WPF/E and Adobe Apollo, remember those? (Either the code names, or the extant renamed products?) The Web has come a long way since 2007.

But other parts of my slideshow are still relevant, in particular the part where Mozilla and Opera committed to an unencumbered <video> element for [HTML5](http://dev.w3.org/html5/spec/Overview.html):

- Working with Opera via
[WHATWG](http://whatwg.org/)on <video>- Unencumbered Ogg Theora decoder in all browsers
- Ogg Vorbis for <audio>
- Other formats possible
- DHTML player controls


We [did](http://brendaneich.com/2007/08/video-tag-progress/) what we said we would. We fought against the odds. We carried the unencumbered HTML5 <video> torch even when it burned our hands.

We were called naive (no) idealists (yes). We were told that we were rolling a large stone up a tall hill (and how!). We were told that we could never overcome the momentum behind [H.264](http://en.wikipedia.org/wiki/H.264/MPEG-4_AVC) (possibly true, but Mozilla was not about to give up and pay off the patent *rentiers*).

Then in **2009** Google [announced](http://www.google.com/intl/en/press/pressrel/ir_20090805.html) that it would acquire On2 ([completed](http://investor.google.com/releases/2010/0219.html) in 2010), and Opera and Mozilla had a [White Knight](http://www.answers.com/main/ntquery?gwp=13&s=white%20knight).

At Google I/O in **May 2010**, Adobe [announced](http://blogs.adobe.com/flashplatform/2010/05/adobe_support_for_vp8.html) that it would include VP8 (but not all of WebM?) support in an upcoming Flash release.

On **January 11, 2011**, Mike Jazayeri of Google [blogged](http://blog.chromium.org/2011/01/html-video-codec-support-in-chrome.html):

… we are changing Chrome’s HTML5 <video> support to make it consistent with the codecs already supported by the open Chromium project. Specifically, we are supporting the WebM (VP8) and Theora video codecs, and will consider adding support for other high-quality open codecs in the future. Though H.264 plays an important role in video, as our goal is to enable open innovation, support for the codec will be removed and our resources directed towards completely open codec technologies.

These changes will occur in the next couple months….


A [followup post](http://blog.chromium.org/2011/01/more-about-chrome-html-video-codec.html) three days later confirmed that Chrome would rely on Flash fallback to play H.264 video.

### Where we are today

It is now **March 2012** and the changes promised by Google and Adobe have not been made.

What’s more, any such changes are irrelevant if made only on desktop Chrome — not on Google’s mobile browsers for Android — because authors typically do not encode twice (once in H.264, once in WebM), they instead write Flash fallback in an <object> tag nested inside the <video> tag. Here’s an example adapted from an [Opera developer document](http://dev.opera.com/articles/view/simple-html5-video-flash-fallback-custom-controls/):

<video controls poster="video.jpg" width="854" height="480"> <source src="video.mp4" type="video/mp4"> <object type="application/x-shockwave-flash" data="player.swf" width="854" height="504"> <param name="allowfullscreen" value="true"> <param name="allowscriptaccess" value="always"> <param name="flashvars" value="file=video.mp4"> <!--[if IE]><param name="movie" value="player.swf"><![endif]--> <img src="video.jpg" width="854" height="480" alt="Video"> <p>Your browser can't play HTML5 video. </object> </video>

The Opera doc nicely carried the unencumbered video torch by including

<source src="video.webm" type="video/webm">

after the first <source> child in the <video> container (after the first, because of an iOS WebKit bug, the Opera doc said), but most authors do not encode twice and host two versions of their video (yes, you who do are to be commended; please don’t spam my blog with comments, you’re not typical — and YouTube is neither typical nor yet completely transcoded [[1]](https://hacks.mozilla.org#fn1)).

Of course the ultimate fallback content could be a link to a video to download and view in a helper app, but that’s not “HTML5 video” and it is user-hostile (profoundly so on mobile). Flash fallback does manage to blend in with HTML5, modulo the loss of expressiveness afforded by DHTML playback controls.

Now, consider carefully where we are today.

Firefox supports only unencumbered formats from Gecko’s <video> implementation. We rely on Flash fallback that authors invariably write, as shown above. Let that sink in: *we, Mozilla, rely on Flash to implement H.264 for Firefox users*.

Adobe has [announced](http://blogs.adobe.com/conversations/2011/11/flash-focus.html) that it will not develop Flash on mobile devices.

In spite of the early 2011 Google blog post, desktop Chrome still supports H.264 from <video>. Even if it were to drop that support, desktop Chrome has a [custom](http://www.pcworld.com/businesscenter/article/250455/for_flash_on_linux_chrome_will_be_users_only_choice.html) [patched](http://www.pcworld.com/article/250114/google_chrome_update_fixes_highseverity_vulnerabilities_patches_flash_player.html) Flash embedding, so the fallback shown above will work well for almost all users.

### Mobile matters most

Android stock browsers (all Android versions), and Chrome on Android 4, all support H.264 from <video>. Given the devices that Android has targeted over its existence, where H.264 hardware decoding is by far the most power-efficient way to decode, how could this be otherwise? Google has to compete with Apple on mobile.

Steve Jobs may have dealt the [death-blow](http://www.apple.com/hotnews/thoughts-on-flash/) to Flash on mobile, but he also [championed](http://www.youtube.com/watch?v=904GQGkK84w) and invested in H.264, and [asserted](http://blogs.fsfe.org/hugo/2010/04/open-letter-to-steve-jobs/) that “[a]ll video codecs are covered by patents”. Apple sells a lot of H.264-supporting hardware. That hardware in general, and specifically in video playback quality, is the gold standard.

Google is in my opinion not going to ship mobile browsers this year or next that fail to play H.264 content that Apple plays perfectly. Whatever happens in the very long run, Mozilla can’t wait for such an event. Don’t ask Google why they bought On2 but failed to push WebM to the exclusion of H.264 on Android. The question answers itself.

So even if desktop Chrome drops H.264 support, Chrome users almost to a person won’t notice, thanks to Flash fallback. And Apple and Google, along with Microsoft and whomever else might try to gain *mobile* market share, will continue to ship H.264 support on all their mobile OSes and devices — hardware-implemented H.264, because that uses far less battery than alternative decoders.

Here is a chart of H.264 video in HTML5 content on the Web from [MeFeedia](http://blog.mefeedia.com/html5-dec-2011):

And here are some charts showing the rise of mobile over desktop from [The Economist](http://www.economist.com/node/21531109):

These charts show [Bell’s Law of Computer Classes](http://en.wikipedia.org/wiki/Bell%27s_Law_of_Computer_Classes) in action. Bell’s Law predicts that the new class of computing devices will replace older ones.

In the face of this shift, Mozilla must advance its [mission](http://www.mozilla.org/about/mission.html) to serve users above all other agendas, and to keep the Web — including the “Mobile Web” — open, interoperable, and evolving.

### What Mozilla is doing

We have successfully launched [Boot to Gecko](http://www.mozilla.org/b2g/) ([B2G)](http://joshcarpenter.ca/Boot-to-Gecko) and we’re preparing to release a [new](http://starkravingfinkle.org/blog/2012/01/firefox-for-android-after-the-reboot/) and improved Firefox for Android, to carry our mission to mobile users.

What should we do about H.264?

[Andreas Gal](http://andreasgal.com/) [proposes](https://groups.google.com/group/mozilla.dev.platform/msg/d234e486003d430e?hl=en) to use OS- and hardware-based H.264 decoding capabilities on Android and B2G. That [thread](https://groups.google.com/group/mozilla.dev.platform/browse_frm/thread/fb14de8b9ad84e15?hl=en&scoring=d&) has run to over 240 messages, and spawned some online media coverage.

Some say we should hold out longer for someone (Google? Adobe?) to change something to advance WebM over H.264.

Remember, dropping H.264 from <video> only on desktop and not on mobile doesn’t matter, because of Flash fallback.

Others say we should hold out indefinitely and by ourselves, rather than integrate OS decoders for encumbered video.

I’ve heard people blame software patents. I hate software patents too, but software isn’t even the issue on mobile. Fairly dedicated DSP hardware takes in bits and puts out pixels. H.264 decoding lives completely in hardware now.

Yes, some hardware also supports WebM decoding, or will soon. Too little, too late for HTML5 <video> as deployed and consumed this year or (for shipping devices) next.

As I [wrote](https://groups.google.com/group/mozilla.dev.platform/msg/8b6711a1418dd813?hl=en) in the newsgroup thread, Mozilla has never ignored users or market share. We do not care *only* about market share, but ignoring usability and market share can easily lead to extinction. Without users our mission is meaningless and our ability to affect the evolution of open standards goes to zero.

Clearly we have principles that prohibit us from abusing users for any end (e.g., by putting ads in Firefox’s user interface to make money to sustain ourselves). But we have never rejected encumbered formats handled by plugins, and OS-dependent H.264 decoding is not different in kind from Flash-dependent H.264 decoding in my view.

**We will not require anyone to pay for Firefox**. We will not burden our downstream source redistributors with royalty fees. We may have to continue to fall back on Flash on some desktop OSes. I’ll write more when I know more about desktop H.264, specifically on Windows XP.

What I do know for certain is this: H.264 is absolutely required right now to compete on mobile. I do not believe that we can reject H.264 content in Firefox on Android or in B2G and survive the shift to mobile.

Losing a battle is a bitter experience. I won’t sugar-coat this pill. But we must swallow it if we are to succeed in our mobile initiatives. Failure on mobile is too likely to consign Mozilla to decline and irrelevance. So I am fully in favor of Andreas’s proposal.

### Our mission continues

Our [mission](http://www.mozilla.org/about/mission.html), to promote openness, innovation, and opportunity on the Web, matters more than ever. As I said at SXSW in 2007, it obligates us to develop and promote unencumbered video. We lost one battle, but the war goes on. We will always push for open, unencumbered standards first and foremost.

In particular we must fight to keep [WebRTC](http://www.webrtc.org/) unencumbered. Mozilla and Opera also lost the earlier skirmish to mandate an unencumbered default format for HTML5 <video>, but WebRTC is a new front in the long war for an open and unencumbered Web.

We are researching downloadable JS decoders via [Broadway.js](http://github.com/mbebenita/Broadway), but fully utilizing parallel and dedicated hardware from JS for battery-friendly decoding is a ways off.

Can we win the long war? I don’t know if we’ll see a final victory, but we must fight on. Patents expire (remember the [LZW](http://en.wikipedia.org/wiki/Graphics_Interchange_Format#Unisys_and_LZW_patent_enforcement) patent?). They can be invalidated. (Netscape paid to do this to certain obnoxious patents, based on prior art.) They can be worked around. And patent law can be reformed.

Mozilla is here for the long haul. **We will never give up, never surrender**.

/be

[[1]](https://hacks.mozilla.org#r1) Some points about WebM on YouTube vs. H.264:

- Google has at best transcoded only about half the videos into WebM. E.g.,
[this YouTube search](http://www.youtube.com/results?search_query=cat&oq=cat&aq=f&aqi=g10&aql=&gs_sm=3&gs_upl=63375l63797l0l64594l3l3l0l0l0l0l169l380l1.2l3l0)for “cat” gives ~1.8M results, while the same one[for WebM videos](http://www.youtube.com/results?search_query=cat&oq=cat&aq=f&aqi=g10&aql=&gs_sm=3&gs_upl=63375l63797l0l64594l3l3l0l0l0l0l169l380l1.2l3l0&webm=1)gives 704K results. - WebM on YouTube is presented only for videos that lack ads, which is a shrinking number on YouTube. Anything monetizable (i.e., popular) has ads and therefore is served as H.264.
- All this is moot when you consider mobile, since there is no Flash on mobile, and as of yet no WebM hardware, and Apple’s market-leading position.

## 144 comments

Matthew CaseMarch 19th, 2012 at 07:49NanashiMarch 19th, 2012 at 08:04FerdinandMarch 19th, 2012 at 13:48ZizzleMarch 19th, 2012 at 08:45Matthew CaseMarch 19th, 2012 at 10:36NeilMarch 19th, 2012 at 09:01TestMarch 19th, 2012 at 09:11Brendan EichMarch 19th, 2012 at 09:15Ryan ParmanMarch 19th, 2012 at 09:22ShmerlMarch 19th, 2012 at 10:31Chris AdamsMarch 20th, 2012 at 06:35ShmerlMarch 20th, 2012 at 10:43KennethMarch 19th, 2012 at 12:10Brendan EichMarch 19th, 2012 at 10:17zzenMarch 19th, 2012 at 10:22Brendan EichMarch 19th, 2012 at 10:24Marcos CaceresMarch 19th, 2012 at 10:36aphidMarch 19th, 2012 at 10:55ZizzleMarch 19th, 2012 at 10:57Brendan EichMarch 19th, 2012 at 11:04ZackMarch 19th, 2012 at 14:05ianjoMarch 19th, 2012 at 11:14Paul LockettMarch 19th, 2012 at 13:28Brendan EichMarch 19th, 2012 at 14:10ZackMarch 19th, 2012 at 14:13Asa DotzlerMarch 19th, 2012 at 14:36A.J.March 19th, 2012 at 15:09Maxim FridentalMarch 19th, 2012 at 15:47EpicanisMarch 19th, 2012 at 15:53EpicanisMarch 19th, 2012 at 15:55samMarch 19th, 2012 at 16:20TestMarch 19th, 2012 at 16:20Brendan MillerMarch 19th, 2012 at 16:43Brendan EichMarch 19th, 2012 at 17:25Brendan EichMarch 19th, 2012 at 17:34TestMarch 19th, 2012 at 18:04Brendan EichMarch 19th, 2012 at 18:12TestMarch 19th, 2012 at 18:47EpicanisMarch 19th, 2012 at 18:52ZizzleMarch 19th, 2012 at 19:00ZizzleMarch 19th, 2012 at 19:04ReikachuMarch 20th, 2012 at 07:25Brendan EichMarch 19th, 2012 at 19:08Brendan EichMarch 19th, 2012 at 19:17Brendan EichMarch 19th, 2012 at 19:21TestMarch 19th, 2012 at 19:35ZizzleMarch 19th, 2012 at 19:38EpicanisMarch 19th, 2012 at 20:10EpicanisMarch 19th, 2012 at 20:24Denver GingerichMarch 19th, 2012 at 20:40Brendan EichMarch 20th, 2012 at 10:29Brendan EichMarch 19th, 2012 at 21:57EpicanisMarch 19th, 2012 at 22:18Brendan EichMarch 19th, 2012 at 22:30SunilMarch 20th, 2012 at 01:43Robert NymanMarch 20th, 2012 at 01:51Jean-Yves PerrierMarch 20th, 2012 at 02:28samMarch 20th, 2012 at 01:43Robert NymanMarch 20th, 2012 at 01:53peteMarch 20th, 2012 at 03:49StevenMarch 20th, 2012 at 05:19Robert NymanMarch 20th, 2012 at 06:19JoelMarch 20th, 2012 at 05:48Robert NymanMarch 20th, 2012 at 06:23TestMarch 20th, 2012 at 07:19ArialiaMarch 20th, 2012 at 08:41ZackMarch 20th, 2012 at 08:45Brendan EichMarch 20th, 2012 at 10:12Brendan EichMarch 20th, 2012 at 10:23ZackMarch 20th, 2012 at 11:21Brendan EichMarch 20th, 2012 at 14:08JebemtiMarch 20th, 2012 at 11:43Jean-Yves PerrierMarch 20th, 2012 at 12:04jebemtiMarch 20th, 2012 at 13:23Brendan EichMarch 20th, 2012 at 14:17jebemtiMarch 20th, 2012 at 15:31ZizzleMarch 20th, 2012 at 12:26TestMarch 20th, 2012 at 13:00Brendan EichMarch 20th, 2012 at 14:24samMarch 20th, 2012 at 13:04Brendan EichMarch 20th, 2012 at 14:29ZizzleMarch 20th, 2012 at 14:36Brendan EichMarch 20th, 2012 at 14:47TestMarch 20th, 2012 at 14:01Brendan EichMarch 20th, 2012 at 14:31samMarch 20th, 2012 at 15:04ZizzleMarch 20th, 2012 at 14:14Brendan EichMarch 20th, 2012 at 14:33ZizzleMarch 20th, 2012 at 14:47Brendan EichMarch 20th, 2012 at 15:08ZizzleMarch 20th, 2012 at 15:40Denver GingerichMarch 20th, 2012 at 15:21ZackMarch 20th, 2012 at 15:39Brendan EichMarch 20th, 2012 at 16:29Brendan EichMarch 20th, 2012 at 16:27TestMarch 20th, 2012 at 16:28Brendan EichMarch 20th, 2012 at 16:39Brendan EichMarch 20th, 2012 at 16:49Brendan EichMarch 20th, 2012 at 17:02ZizzleMarch 20th, 2012 at 17:22Brendan EichMarch 20th, 2012 at 17:54TestMarch 20th, 2012 at 17:25Brendan EichMarch 20th, 2012 at 17:37TestMarch 20th, 2012 at 17:55Brendan EichMarch 20th, 2012 at 18:00chico sajovicMarch 20th, 2012 at 18:20ZizzleMarch 21st, 2012 at 18:36TestMarch 20th, 2012 at 18:24Wolfgang SpraulMarch 20th, 2012 at 19:28samMarch 20th, 2012 at 19:49samMarch 20th, 2012 at 19:54JasonMarch 21st, 2012 at 09:25Brendan EichMarch 21st, 2012 at 10:33samMarch 21st, 2012 at 10:56samMarch 21st, 2012 at 12:16Robert NymanMarch 21st, 2012 at 18:04TestMarch 21st, 2012 at 12:36TestMarch 21st, 2012 at 12:46JohnSmithMarch 23rd, 2012 at 11:08HeWhoEMarch 23rd, 2012 at 13:05Paul LockettMarch 24th, 2012 at 03:32Brendan EichMarch 24th, 2012 at 12:09JohnSmithMarch 24th, 2012 at 16:45Brendan EichMarch 25th, 2012 at 14:28ZizzleMarch 25th, 2012 at 15:24Brendan EichMarch 25th, 2012 at 17:18ZizzleMarch 26th, 2012 at 08:25Brendan EichMarch 26th, 2012 at 17:04Brendan EichMarch 25th, 2012 at 19:02Brendan EichMarch 25th, 2012 at 21:58Denver GingerichMarch 26th, 2012 at 08:06Brendan EichMarch 26th, 2012 at 13:04Denver GingerichMarch 26th, 2012 at 15:37CassandraMarch 27th, 2012 at 19:53Robert NymanMarch 29th, 2012 at 11:26KiseMarch 31st, 2012 at 01:58JoelMarch 31st, 2012 at 11:47SamApril 4th, 2012 at 07:47JemskiApril 25th, 2012 at 14:10AndreSeptember 13th, 2012 at 13:13avnerDecember 9th, 2012 at 05:54uffoDecember 10th, 2012 at 03:07avnerDecember 10th, 2012 at 05:40TestMarch 7th, 2013 at 13:35