---
title: Testing Picture-in-Picture for videos in Firefox 69 Beta and Developer Edition
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2019/07/testing-picture-in-picture-for-videos-in-firefox-69/
author: Mike Conley
published: '2019-07-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Editor’s Note: We updated this post on July 11, 2019 to mention that the Picture-in-Picture feature is currently only enabled Firefox 69 Beta and Developer Edition on Windows. We apologize for getting your hopes up if you’re on macOS or Linux, and we hope to have this feature enabled on those platforms once it reaches our quality standards.
*

Have you ever needed to scan a recipe while also watching a cooking video? Or perhaps you wanted to watch a recording of a lecture while also looking at the course slides. Or maybe you wanted to watch somebody stream themselves playing video games while you work.

We’ve recently shipped a version of Firefox for Windows on our [Beta and Developer Edition release channels](https://www.mozilla.org/en-US/firefox/channel/desktop/) with an experimental feature that aims to make this easier for you to do!

Picture-in-Picture allows you to pop a video out from where it’s being played into a special kind of window that’s always on top. Then you can move that window around or resize it however you need!

There are two ways to pop out a video into a Picture-in-Picture window:

## Via the context menu

If you open the context menu on a `<video>`

element, you’ll sometimes see the media context menu that looks like this:

![Showing the default context menu when opened on a video element, with the Picture-in-Picture menu item highlighted.](../../assets/2ccca4d39efe270e.png)


There’s a Picture-in-Picture menu item in that context menu that you can use to toggle the feature.

Many sites, however, make it difficult to access the context menu for `<video>`

elements. YouTube, for example, overrides the default context menu with their own.

You can get to the default native context menu by either holding Shift while right-clicking, or double right-clicking. We feel, however, that this is not the most obvious gesture for accessing the feature, so that leads us to the other toggling mechanism – the Picture-in-Picture video toggle.

## Via the new Picture-in-Picture video toggle

The Picture-in-Picture toggle appears when you hover over videos with the mouse cursor. It is a small blue rectangle that slides out when you hover over it. Clicking on the blue rectangle will open the underlying video in the Picture-in-Picture player window.

![Showing the Picture-in-Picture toggle overlaying a video element on YouTube.](../../assets/65c0ce4d7443a8a0.png)


Note that the toggle doesn’t appear when hovering all videos. We only show it for videos that include an audio track that are also of sufficient size and play length.

The advantage of the toggle is that we think we can make this work for most sites out of the box, without making the site authors do anything special!

## Using the Picture-in-Picture player window

The Picture-in-Picture window also gives you the ability to quickly play or pause the video — hovering the video with your mouse will expose that control, as well as a control for closing the window, and closing the window while returning you to the tab that the video came from.

## Asking for your feedback

We’re still working on hammering out keyboard accessibility, as well as some issues on how the video is displayed at extreme window sizes. We wanted to give Firefox Beta and Developer Edition users on Windows the chance to try the feature out and let us know how it feels. We’ll use the information that we gather to determine whether or not we’ve got the UI right for most users, or need to go back to the drawing board. We’re also hoping to bring this same Picture-in-Picture support to macOS and Linux in the near future.

We’re particularly interested in feedback on the video toggle — there’s a fine balance between discoverability and obtrusiveness, and we want to get a clearer sense of where the blue toggle falls for users on sites out in the wild.

So grab yourself an up-to-date copy of Firefox 69 Beta or Developer Edition for Windows, and give Picture-in-Picture a shot! If you’ve got constructive feedback to share, [here’s a form you can use to submit it.](https://forms.gle/e5vtkHNeNkUPDQjs6)

Happy testing!

## About
[
Mike Conley ](https://www.mikeconley.ca/blog)

Engineer working on Firefox for Desktop

## 20 comments

Jigar ShahJuly 10th, 2019 at 07:56Mike ConleyJuly 11th, 2019 at 14:30dbgarzaJuly 11th, 2019 at 22:40RobertJuly 10th, 2019 at 09:26Mike ConleyJuly 11th, 2019 at 14:32KaiJuly 11th, 2019 at 13:56Mike ConleyJuly 11th, 2019 at 14:33dbgarzaJuly 11th, 2019 at 22:42Josh BricknerJuly 13th, 2019 at 19:58Mike ConleyJuly 18th, 2019 at 10:17PaulJuly 18th, 2019 at 01:24Mike ConleyJuly 18th, 2019 at 10:18PatrickJuly 18th, 2019 at 08:47Mike ConleyJuly 18th, 2019 at 10:19javier encisoJuly 19th, 2019 at 05:09Will FriendJuly 19th, 2019 at 12:54DmitryAugust 2nd, 2019 at 00:34Mike ConleyAugust 2nd, 2019 at 06:41SimonAugust 2nd, 2019 at 00:43Jim LeyAugust 9th, 2019 at 03:49