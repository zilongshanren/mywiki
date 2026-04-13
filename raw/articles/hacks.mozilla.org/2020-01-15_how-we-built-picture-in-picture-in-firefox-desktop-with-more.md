---
title: How we built Picture-in-Picture in Firefox Desktop with more control over video
  – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/01/how-we-built-picture-in-picture-in-firefox-desktop/
author: Mike Conley
published: '2020-01-15'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Picture-in-Picture support for videos is a feature that we shipped to Firefox Desktop users in version [71 for Windows users](https://www.mozilla.org/en-US/firefox/71.0/releasenotes/), and [72 for macOS and Linux users](https://www.mozilla.org/en-US/firefox/72.0/releasenotes/). It allows the user to pull a `<video>`

element out into an always-on-top window, so that they can switch tabs or applications, and keep the video within sight — ideal if, for example, you want to keep an eye on that sports game while also getting some work done.

As always, we designed and developed this feature with user agency in mind. Specifically, we wanted to make it extremely easy for our users to exercise greater control over how they watch video content in Firefox.

![Firefox is shown playing a video, and a mouse cursor enters the frame. Upon clicking on the Picture-in-Picture toggle on the video, the video pops out into its own always-on-top player window.](../../assets/db3726c0cd191aed.gif)


![Firefox is shown playing a video, and a mouse cursor enters the frame. Upon clicking on the Picture-in-Picture toggle on the video, the video pops out into its own always-on-top player window.](../../assets/db3726c0cd191aed.gif)

In these next few sections, we’ll talk about how we designed the feature and then we’ll go deeper into details of the implementation.

## The design process

### Look behind and all around

To begin our design process, we looked back at the past. In 2018, [we graduated Min-Vid](https://medium.com/firefox-test-pilot/min-vid-graduation-report-9ad74dc37c1), one of our [Test Pilot experiments](https://medium.com/firefox-test-pilot/adios-amigo-51bec2a00072). We asked the question: “*How might we maximize the learning from Min-Vid?*“. Thanks to the amazing Firefox User Research team, we had enough prior research to understand the main pain points in the user experience. However, it was important to acknowledge that the competitive landscape had changed quite a bit since 2018. How were users and [other browsers](https://hacks.mozilla.org#comparing-to-other-browsers) solving this problem already? What did users think about those solutions, and how could we improve upon them?

We had two essential guiding principles from the beginning:

- We wanted to turn this into a very user-centric feature, and make it available for any type of video content on the web. That meant that implementing the
[Picture-in-Picture](https://w3c.github.io/picture-in-picture/)spec wasn’t an option, as it requires developers to opt-in first. - Given that it would be available on any video content, the feature needed to be discoverable and straight-forward for as many people as possible.

Keeping these principles in mind helped us to evaluate all the different solutions, and was critical for the next phase.

![Three sketches showing a possible drag and drop interaction for picture-in-picture](../../assets/a18dd774382b1667.png)


![Three sketches showing a possible drag and drop interaction for picture-in-picture](../../assets/a18dd774382b1667.png)

### Try, and try again

Once we had an understanding of how others were solving the problem, it was our turn to try. We wanted to ensure discoverability without making the feature intrusive or annoying. Ultimately, we wanted to augment — and not disrupt — the experience of viewing video. And we definitely didn’t want to cause issues with any of the popular video players or platforms.

![A screenshot of a YouTube page with a small blue rectangle on the right edge of the video, center aligned](../../assets/a894013364b647d9.png)


![A screenshot of a YouTube page with a small blue rectangle on the right edge of the video, center aligned](../../assets/a894013364b647d9.png)

This led us to building an interactive, motion-based prototype using [Framer X](https://www.framer.com/). Our prototype provided a very effective way to get early feedback from real users. In tests, we didn’t focus solely on usability and discoverability. We also took the time to re-learn the problems users are facing. And we learned a lot!

The participants in our first study appreciated the feature, and while it did solve a problem for them, it was too hard to discover on their own.

So, we rolled our sleeves up and tried again. We knew what we were going after, and we now had a better understanding of users’ basic expectations. We explored, brainstormed solutions, and discussed technical limitations until we had a version that offered discoverability without being intrusive. After that, we spent months polishing and refining the final experience!

### Stay tuned

From the beginning, our users have been part of the conversation. Early and ongoing user feedback is a critical aspect of product design. It was particularly exciting to keep Picture-in-Picture in our Beta channel as we [engaged with users like you to get your input](https://hacks.mozilla.org/2019/07/testing-picture-in-picture-for-videos-in-firefox-69/).

We listened, and you helped us uncover new blind spots we might have missed while designing and developing. At every phase of this design process, you’ve been there. [And you still are](https://hacks.mozilla.org#what-are-you-using-picture-in-picture-for). Thank you!

## Implementation detail

The Firefox Picture-in-Picture toggle exists in the same privileged [shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM) space within the `<code><video>`

element as the built-in HTML `<video>`

controls. Because this part of the DOM is inaccessible to page JavaScript and CSS stylesheets, it is much more difficult for sites to detect, disable, or hijack the feature.

### Into the shadow DOM

Early on, however, we faced a challenge when making the toggle visible on hover. Sites commonly structure their DOM such that mouse events never reach a `<video>`

that the user is watching.

Often, websites place transparent nodes directly over top of `<video>`

elements. These can be used to show a preview image of the underlying video before it begins, or to serve an interstitial advertisement. Sometimes transparent nodes are used for things that only become visible when the user hovers the player — for example, custom player controls. In configurations like this, transparent nodes prevent the underlying `<video>`

from matching the [ :hover pseudo-class](https://developer.mozilla.org/en-US/docs/Web/CSS/:hover).

Other times, sites make it explicit that they don’t want the underlying `<video>`

to receive mouse events. To do this, they set [the pointer-events CSS property](https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events) to none on the

`<video>`

or one of its ancestors.To work around these problems, we rely on the fact that the web page is being sent events from the browser engine. At Firefox, we control the browser engine! Before sending out a mouse event, we can check to see what sort of DOM nodes are directly underneath the cursor (re-using much of the same code that powers [the elementsFromPoint function](https://developer.mozilla.org/en-US/docs/Web/API/DocumentOrShadowRoot/elementsFromPoint)).

If any of those DOM nodes are a visible `<video>`

, we tell that `<video>`

that it is being hovered, which shows the toggle. Likewise, we use a similar technique to determine if the user is clicking on the toggle.

We also use some simple heuristics based on the size, length, and type of video to determine if the toggle should be displayed at all. In this way, we avoid showing the toggle in cases where it would likely be more annoying than not.

### A browser window within a browser

The Picture-in-Picture player window itself is a browser window with most of the surrounding window decoration collapsed. Flags tell the operating system to keep it on top. That browser window contains a special `<video>`

element that runs in the same process as the originating tab. The element knows how to show the frames that were destined for the original `<video>`

. As with much of the Firefox browser UI, the Picture-in-Picture player window is written in HTML and powered by JavaScript and CSS.

Firefox is not the first desktop browser to ship a Picture-in-Picture implementation. [Safari 10 on macOS Sierra](https://support.apple.com/en-ca/HT206997) shipped with this feature in 2016, and Chrome followed in late 2018 with [Chrome 71](https://www.chromestatus.com/feature/5729206566649856).

In fact, each browser maker’s implementation is slightly different. In the next few sections we’ll compare Safari and Chrome to Firefox.

### Safari

Safari’s implementation involves [a non-standard WebAPI](https://developer.apple.com/documentation/webkitjs/htmlvideoelement/1631913-webkitpresentationmode) on `<video>`

elements. Sites that know the user is running Safari can call `video.webkitSetPresentationMode("picture-in-picture");`

to send a video into the native macOS Picture-in-Picture window.

Safari includes a context menu item for `<video>`

elements to open them in the Picture-in-Picture window. Unfortunately, this requires an awkward double right-click to access video on sites like YouTube that override the default context menu. This awkwardness is shared with all browsers that implement the context menu option, including Firefox.

![](../../assets/efa74de5f4da6047.png)


![](../../assets/efa74de5f4da6047.png)

Safari users can also right-click on the audio indicator in the address bar or the tab strip to trigger Picture-in-Picture:

![The Safari web browser playing a video, with the context menu for the audio toggle in the address bar displayed. “Enter Picture in Picture” is one of the menu items.](../../assets/19fe3eab688e5137.png)


![The Safari web browser playing a video, with the context menu for the audio toggle in the address bar displayed. “Enter Picture in Picture” is one of the menu items.](../../assets/19fe3eab688e5137.png)

On newer MacBooks, Safari users might also notice the button immediately to the right of the volume-slider. You can use this button to open the currently playing video in the Picture-in-Picture window:

![A close-up photograph of the MacBook Pro touchbar when a video is playing. There is an icon next to the playhead scrubber that opens the video in an always-on-top player window.](../../assets/e8b46d6ff31b384e.png)


![A close-up photograph of the MacBook Pro touchbar when a video is playing. There is an icon next to the playhead scrubber that opens the video in an always-on-top player window.](../../assets/e8b46d6ff31b384e.png)

Safari also uses the built-in macOS Picture-in-Picture API, which delivers a very smooth integration with the rest of the operating system.

#### Comparison to Firefox

Despite this, we think Firefox’s approach has some advantages:

- When
[multiple videos are playing at the same time](http://www.youtubemultiplier.com), the Safari implementation is somewhat ambiguous as to which video will be selected when using the audio indicator. It seems to be the most recently focused video, but this isn’t immediately obvious. Firefox’s Picture-in-Picture toggle makes it*extremely obvious*which video is being placed in the Picture-in-Picture window. - Safari appears to have an arbitrary limitation on how large a user can make their Picture-in-Picture player window. Firefox’s player window does not have this limitation.
- There can only be one Picture-in-Picture window system-wide on macOS. If Safari is showing a video in Picture-in-Picture, and then another application calls into the macOS Picture-in-Picture API, the Safari video will close. Firefox’s window is Firefox-specific. It will stay open even if another application calls the macOS Picture-in-Picture API.

### Chrome’s implementation

#### The PiP WebAPI and WebExtension

Chrome’s implementation of Picture-in-Picture mainly centers around a WebAPI specification being driven by Google. This API is [currently going through the W3C standardization process](https://w3c.github.io/picture-in-picture/). Superficially, this WebAPI is similar to [the Fullscreen WebAPI](https://fullscreen.spec.whatwg.org/). In response to user input (like clicking on a button), site authors can request that a `<video>`

be put into a Picture-in-Picture window.

Like Safari, Chrome also includes a context menu option for `<video>`

elements to open in a Picture-in-Picture window.

![The Chrome web browser playing a video, with the context menu for the video element hovering over top of it. “Picture in Picture” is one of the menu items.](../../assets/b1fefaad7eacea7d.png)


![The Chrome web browser playing a video, with the context menu for the video element hovering over top of it. “Picture in Picture” is one of the menu items.](../../assets/b1fefaad7eacea7d.png)

This proposed WebAPI is also used by [a PiP WebExtension from Google](https://chrome.google.com/webstore/detail/picture-in-picture-extens/hkgfoiooedgoejojocmhlaklaeopbecg). The extension adds a toolbar button. The button finds the largest video on the page, and uses the WebAPI to open that video in a Picture-in-Picture window.

![The Chrome web browser playing a video. The mouse cursor clicks a button in the toolbar provided by a WebExtension which pops the video out into an always-on-top player window.](../../assets/e024f551c16bc67a.gif)


![The Chrome web browser playing a video. The mouse cursor clicks a button in the toolbar provided by a WebExtension which pops the video out into an always-on-top player window.](../../assets/e024f551c16bc67a.gif)

Google’s WebAPI lets sites indicate that [a <video> should not be openable in a Picture-in-Picture player window](https://w3c.github.io/picture-in-picture/#disable-pip). When Chrome sees this directive, it doesn’t show the context menu item for Picture-in-Picture on the

`<video>`

, and [the WebExtension ignores it](https://github.com/GoogleChromeLabs/picture-in-picture-chrome-extension/blob/8013674d7b16a068ede318cb95e48fc82ed60d38/src/script.js#L18). The user is unable to bypass this restriction unless they modify the DOM to remove the directive.

#### Comparison to Firefox

Firefox’s implementation has a number of distinct advantages over Chrome’s approach:

- The Chrome WebExtension which only targets the largest
`<video>`

on the page. In contrast, the Picture-in-Picture toggle in Firefox makes it easy to choose*any*`<video>`

on a site to open in a Picture-in-Picture window. - Users have access to this capability on all sites
*right now*. Web developers and site maintainers do not need to develop, test and deploy usage of the new WebAPI. This is particularly important for older sites that are not actively maintained. - Like Safari, Chrome seems to have an artificial limitation on how big the Picture-in-Picture player window can be made by the user. Firefox’s player window does not have this limitation.
- Firefox users have access to this Picture-in-Picture capability on all sites. Websites are not able to directly disable it via a WebAPI. This creates a more consistent experience for
`<video>`

elements across the entire web, and ultimately more user control.

Recently, Mozilla indicated that we [plan to defer implementation of the WebAPI](https://github.com/mozilla/standards-positions/issues/72) that Google has proposed. We want to see if the built-in capability we just shipped will meet the needs of our users. In the meantime, we’ll monitor the evolution of the WebAPI spec and may revisit our implementation decision in the future.

## Future plans

Now that we’ve shipped the first version of Picture-in-Picture in Firefox Desktop on all platforms, we’re paying close attention to user feedback and bug intake. Your inputs will help determine our next steps.

Beyond bug fixes, we’d like to share some of the things we’re considering for future feature work:

- Repositioning the toggle when there are visible, clickable elements overlapping it.
- Supporting video captions and subtitles in the player window.
- Adding a playhead scrubber to the player window to control the current playing position of a
`<video>`

. - Adding a control for the volume level of the
`<video>`

to the player window.

Are you using the new Picture-in-Picture feature in Firefox? Are you finding it useful? Please us know in the comments section below, or [send us a Tweet](https://twitter.com/intent/tweet?text=@firefox) with a screenshot! We’d love to hear what you’re using it for. You can also [file bugs for the feature here](https://bugzilla.mozilla.org/enter_bug.cgi?assigned_to=nobody%40mozilla.org&blocked=videopip&bug_ignored=0&bug_severity=normal&bug_status=NEW&cf_fission_milestone=---&cf_fx_iteration=---&cf_fx_points=---&cf_status_firefox72=---&cf_status_firefox73=---&cf_status_firefox74=---&cf_status_firefox_esr68=---&cf_status_thunderbird_esr60=---&cf_status_thunderbird_esr68=---&cf_tracking_firefox72=---&cf_tracking_firefox73=---&cf_tracking_firefox74=---&cf_tracking_firefox_esr68=---&cf_tracking_firefox_relnote=---&cf_tracking_thunderbird_esr60=---&cf_tracking_thunderbird_esr68=---&cf_webcompat_priority=---&component=Video%2FAudio%20Controls&contenttypemethod=list&contenttypeselection=text%2Fplain&defined_groups=1&filed_via=standard_form&flag_type-203=X&flag_type-37=X&flag_type-41=X&flag_type-607=X&flag_type-721=X&flag_type-737=X&flag_type-787=X&flag_type-799=X&flag_type-800=X&flag_type-803=X&flag_type-835=X&flag_type-846=X&flag_type-855=X&flag_type-864=X&flag_type-930=X&flag_type-936=X&flag_type-937=X&flag_type-941=X&form_name=enter_bug&maketemplate=Remember%20values%20as%20bookmarkable%20template&op_sys=Unspecified&priority=--&product=Toolkit&rep_platform=Unspecified&target_milestone=---&version=unspecified).

## About
[
Mike Conley ](https://www.mikeconley.ca/blog)

Engineer working on Firefox for Desktop

## 29 comments

KilianJanuary 15th, 2020 at 09:47wesJanuary 16th, 2020 at 01:25VictorJanuary 16th, 2020 at 02:46dc12January 16th, 2020 at 08:42ChrisJanuary 16th, 2020 at 08:50EugeneJanuary 16th, 2020 at 09:36MattJanuary 16th, 2020 at 17:19Mike ConleyJanuary 21st, 2020 at 11:09mtJanuary 16th, 2020 at 19:42MohakJanuary 16th, 2020 at 22:13Mike ConleyJanuary 21st, 2020 at 11:21ØysteinJanuary 16th, 2020 at 22:21alJanuary 17th, 2020 at 02:20ArpitJanuary 17th, 2020 at 08:16ForcJanuary 18th, 2020 at 00:41DanielJanuary 18th, 2020 at 10:01NJanuary 18th, 2020 at 19:16SebasJanuary 19th, 2020 at 17:25Agustina ChaerJanuary 21st, 2020 at 05:18Mike ConleyJanuary 21st, 2020 at 11:21Joel StranskyJanuary 22nd, 2020 at 09:28shamim kulabakoJanuary 23rd, 2020 at 02:07BenniJanuary 24th, 2020 at 02:21Priya SinghJanuary 30th, 2020 at 19:37ChrisJanuary 31st, 2020 at 18:00Bruce WilliamsFebruary 2nd, 2020 at 14:37Bruce WilliamsFebruary 2nd, 2020 at 15:33Michael BruusFebruary 7th, 2020 at 18:22Mike ConleyFebruary 7th, 2020 at 18:32