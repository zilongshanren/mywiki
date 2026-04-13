---
title: GIF vs webM/MP4
url: https://simonschreibt.de/webm/
published: '2014-05-08'
source_blog: Simonschreibt.
source_site: https://simonschreibt.de
category: graphics
fetched: '2026-04-13'
---

This is a test for using [webM](http://www.webmproject.org/)/MP4 videos. It would be awesome if you could write me feedback if it does/doesn’t works for you ([mail](mailto:simon@simonschreibt.de), [twitter](https://twitter.com/simonschreibt), [facebook](https://www.facebook.com/simonschreibtblog)). The general advantages would be:

- Loads faster because if smaller file size
- You can start/stop the animation if it annoys you while reading (just hover over the video with your cursor)
- You can fast-forward/rewind the video or jump to a special point for a deeper look

Size: **5.70 MB**

Size: **0.91 MB**

- Not supported by Safari/IE

Size: **0.67 MB**

- Supported by every Browser i tested
- But on Chrome/FF i saw a blank/empty frame everytime the animation starts again/loops

Let’s try to let the browser choose which format is the best. I hand him webM and MP4 and if the one isn’t supported, it should choose the other one:

- Works well because Chrome/FF use webM which works very well there
- Safari/IE should use MP4 instead which works perfect there

Here’s the code which makes the browser choose the correct format:

If you have any problems (or a strong opinion about webM), please contact me ([mail](mailto:simon@simonschreibt.de), [twitter](https://twitter.com/simonschreibt), [facebook](https://www.facebook.com/simonschreibtblog)) and tell me what browser you’re using.

Doesn’t work on OSX :(

Firefox 30 beta -> “Kein Video mit unterstütztem Format und MIME-Typ gefunden.”

Chromium -> empty, grey box

Safari -> video box with ‘Loading…’ and nothing happens

Thx for testing! I added MIME tags and the correct codec to the HTML tag. But IE doesn’t work either. Have to check tomorrow.

Chrome 34: None of the videos can be paused by clicking on the video, only on the play button itself. The MP4 alone won’t scrub and refuses to re-play after pausing. The webm becomes a mess when scrubbing, though it cleans up when re-playing. The webm/mp4 is playing webm, so same problems.

Firefox 28: All 3 videos play/pause/scrub perfectly.

Internet Explorer 10: None of the videos can be paused by clicking on the video, only on the play button itself. The webm is black with an error message. MP4 plays and scrubs fine, same for webm/mp4.

Thank you for all the testing! Scrubbing/Pausing is cool but in comparision with the vanilla GIF it’s already awesome when it just plays/loops (but of course with smaller filesize). Your video setup is really cool! But i think for my blog it’s better to have the videos played automatically. :) By the way, this MMO stuff looks really cool!