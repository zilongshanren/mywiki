---
title: HTML5 Video preload attribute supported in Firefox 4, autobuffer attribute
  removed – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2010/08/video_preload_attribute/
author: Paul Rouget
published: '2010-08-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*This is a re-post from Chris Pearce’s blog. To comply with the HTML5 specification, we replaced the autobuffer attribute with the tri-state preload attribute. We encourage you to update your code. See the documention on MDC.*



Late last week I landed support on Firefox trunk for the [HTML5 video ‘preload’ attribute](http://www.whatwg.org/specs/web-apps/current-work/multipage/video.html#attr-media-preload). This replaces the ‘autobuffer’ attribute, which we previously supported. If you were previously using the autobuffer attribute on your HTLM5 videos, you need to update to using the preload attribute as well.

The preload attribute provides a hint to the browser as to how much downloading is sensible for a given media. The preload attribute can have three values:

- “
**none**” – suggests to the browser that it doesn’t need to load this media at all until the user plays the resource. The browser will delay any network traffic required to load the media until the users tries to play the resource, or explicitly loads the resource. I suggest using this preload value, along with the poster attribute, when it’s unlikely that the user will play the resource. This is probably most useful in a mobile environment, where data can be expensive. - “
**metadata**” – suggests to the browser that it isn’t necessary to load the entire resource in advance. The browser will suspend the load after loading metadata, displaying the first video frame (if there’s no poster image), and ensuring it can play the media. This is the default behaviour, and prevents excess network traffic when the web developer isn’t certain the video will definitely be played. If you don’t specify a preload value, Firefox will automatically do this. This was also the default behaviour in Firefox 3.5 and 3.6 in the absence of the autobuffer attribute. This default behaviour is a suitable compromise between bandwidth saving and user convenience. - “
**auto**” – suggests to the browser that it should load as much of the resource as possible. As long as the browser’s own media cache isn’t full, it will keep on downloading. I suggest this is most useful in the “YouTube” case, when you’ve got a media which the user is almost certainly going to watch, and so having the user download the media is not likely to be wasting server bandwidth. This behaviour is the same as using the autobuffer attribute in Firefox 3.5 and 3.6

Since the autobuffer attribute is no longer present in Firefox 4, and the preload attribute is not present in Firefox 3.5 and 3.6, **if you want a media to download completely, you should include both preload=”auto” and autobuffer in the video element**, *e.g.*:

<video autobuffer preload=”auto” src=”video.ogg”></video>

**If you want the video to only be downloaded if the user actually plays the video, you should not include either the preload or the autobuffer attribute.** The default behaviour in Firefox 3.5, 3.6, and the upcoming Firefox 4 is to only load up to the first frame and then suspend the download.

## About
[
Paul Rouget ](http://paulrouget.com)

Paul is a Firefox developer.