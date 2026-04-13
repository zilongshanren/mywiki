---
title: H.264 video in Firefox for Android – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2012/11/h264-video-in-firefox-for-android/
author: Chris Peterson
published: '2012-11-29'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[
Firefox for Android](https://play.google.com/store/apps/details?id=org.mozilla.firefox&hl=en) has expanded its HTML5 video capabilities to include H.264 video playback. Web developers have been using Adobe Flash to play H.264 video on Firefox for Android, but Adobe no longer supports Flash for Android. Mozilla needed a new solution, so Firefox now uses Android’s “Stagefright” library to access hardware video decoders. The challenges posed by

[H.264 patents and royalties](https://hacks.mozilla.org/2012/03/video-mobile-and-the-open-web/)have been documented elsewhere.

![](../../assets/6446dccb47ea5a14.jpg)


## Supported devices

Firefox currently supports H.264 playback on any device running Android 4.1 (Jelly Bean) and any Samsung device running Android 4.0 (Ice Cream Sandwich). We have temporarily blocked non-Samsung devices running Ice Cream Sandwich until we can fix or workaround some bugs. Support for Gingerbread and Honeycomb devices is planned for a later release ([Bug 787228](https://bugzilla.mozilla.org/show_bug.cgi?id=787228)).

To test whether Firefox supports H.264 on your device, try playing this [“Big Buck Bunny” video](http://camendesign.com/code/video_for_everybody/test.html).

## Testing H.264

If your device is not supported yet, you can manually enable H.264 for testing. Enter `about:config`

in Firefox for Android’s address bar, then search for “stagefright”. Toggle the “stagefright.force-enabled” preference to `true`

. H.264 should work on most Ice Cream Sandwich devices, but Gingerbread and Honeycomb devices will probably crash.

![](../../assets/6a133a7c67de4eb9.png)


If Firefox does not recognize your hardware decoder, it will use a safer (but slower) software decoder. Daring users can manually enable hardware decoding. Enter `about:config`

as described above and search for “stagefright”. To force hardware video decoding, change the “media.stagefright.omxcodec.flags” preference to `16`

. The default value is `0`

, which will try the hardware decoder and fall back to the software decoder if there are problems ([Bug 797225](https://bugzilla.mozilla.org/show_bug.cgi?id=797225)). The most likely problems you will encounter are [videos with green lines](https://bug797364.bugzilla.mozilla.org/attachment.cgi?id=667489) or crashes.

### Giving feedback/reporting bugs

If you find any video bugs, please [file a bug report here](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&component=Video%2FAudio&rep_platform=ARM&op_sys=Android) so we can fix it! Please include your device model, Android OS version, the URL of the video, and any `about:config`

preferences you have changed. Log files collected from [aLogcat](https://play.google.com/store/apps/details?id=org.jtb.alogcat) or [adb logcat](http://developer.android.com/tools/help/logcat.html) are also very helpful.

## About
[
Chris Peterson ](http://www.cpeterso.com/blog/)

Chris is a developer on Mozilla's Firefox for Android team.

## 24 comments

dotnetCarpenterNovember 29th, 2012 at 12:29Robert NymanNovember 30th, 2012 at 00:44RakshithNovember 29th, 2012 at 13:35Robert NymanNovember 30th, 2012 at 00:44suprsidrNovember 29th, 2012 at 14:10Robert NymanNovember 30th, 2012 at 00:4413xforeverNovember 29th, 2012 at 22:28Robert NymanNovember 30th, 2012 at 00:43RahulNovember 30th, 2012 at 05:36AndreiNovember 30th, 2012 at 08:30Chris PetersonNovember 30th, 2012 at 11:30AndreiNovember 30th, 2012 at 11:35Chris PetersonDecember 1st, 2012 at 12:28mpmediaDecember 1st, 2012 at 11:48pdDecember 2nd, 2012 at 10:36John ThomasDecember 3rd, 2012 at 07:07Chris PetersonDecember 3rd, 2012 at 09:47ShmerlDecember 3rd, 2012 at 11:08SammoFebruary 28th, 2013 at 17:15Robert Nyman [Editor]March 1st, 2013 at 07:57AnthonyMarch 24th, 2013 at 16:43Robert Nyman [Editor]March 25th, 2013 at 04:01MichaelApril 1st, 2013 at 15:51Robert Nyman [Editor]April 2nd, 2013 at 01:06