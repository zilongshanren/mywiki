---
title: What's new for Web Developers in Firefox 7 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2011/09/whats-new-for-web-developers-in-firefox-7/
author: Christopher Blizzard
published: '2011-09-27'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today we’re releasing Firefox Update 7. This update contains work that’s been stabilizing over the last 3 months and there are quite a few interesting things to talk about.

To be clear, this is not the canonical list of changes, just highlights. As always, we’ve created a page to track the changes that web developers will care about. For the full list please see the [Firefox 7 for developers page.](https://developer.mozilla.org/en/Firefox_7_for_developers)

**Firefox now supports text-overflow: ellipsis**

Firefox now supports the `<a href="https://developer.mozilla.org/En/CSS/text-overflow">ellipsis</a>`

mode for the `text-overflow`

property. This property is supported in [other browsers](https://developer.mozilla.org/En/CSS/text-overflow#Browser_compatibility) which means developers should be able to start using it in the wild. Here’s an example of how text-overflow ellipsis works:

HTML:

```
I am some very long text!
```

CSS:

```
div.inner {
width: 120px;
text-overflow: ellipsis;
white-space:nowrap;
overflow:hidden;
color: red;
border: 1px dashed #333;
margin: 20px;
padding: 10px;
}
```

Result:

![](../../assets/f90b5c4d19bd34cf.png)


As you can see, it’s pretty easy to make text that cuts off in a sane way with this new property. Our [developer page for the property](https://developer.mozilla.org/En/CSS/text-overflow) also contains sample syntax for other browsers.

**WebSockets: Updated protocol and available on mobile**

First, WebSockets is now enabled by default for Firefox for Mobile. For mobile networks that are high-latency and have high connection setup-up costs, WebSockets offers an opportunity to create a much better experience than is available with polling HTTP.

Second, we’ve updated to the most recent draft version of the [WebSockets](https://developer.mozilla.org/en/WebSockets) protocol from the IETF. Somewhat confusingly, this is version 8 of the protocol, but is [draft version 10](http://tools.ietf.org/html/draft-ietf-hybi-thewebsocketprotocol-10). This will be mostly of interest to people who are building applications on top of WebSockets and tool vendors, but is worth calling out since it affects backwards compatibility.

Since the WebSockets work is ongoing, the namespace for WebSockets remains moz-prefixed to indicate that it’s not yet finalized.

**An even faster Canvas element**

The `canvas`

element in Firefox 7 is even faster. We’ve revised our code for Canvas based on what we learned in previous Firefox releases and how people are using Canvas in the wild. Based on that you are likely to see much snappier performance on many demos when drawing to canvas elements. For an example, see our [Runfield](https://developer.mozilla.org/en-US/demos/detail/runfield) demo.

**Web sites can no longer resize your main browser window**

It’s no longer possible for a web site to change the default size of a window in a browser, according to the [following rules](https://bugzilla.mozilla.org/show_bug.cgi?id=565541#c24):

- You can’t resize a window or tab that wasn’t created by window.open.
- You can’t resize a window or tab when it’s in a window with more than one tab.

**Support for the new Navigation Web Timing Spec**

Firefox Update 7 now supports the [Navigation Timing spec](https://dvcs.w3.org/hg/webperf/raw-file/tip/specs/NavigationTiming/Overview.html). This allows a web page author to monitor parts of web page performance in the page itself. For people who are interested in page load and navigation performance, they can send that back to the server which can give them a better view into real-world performance.

There are a couple of other specs in this space – the [User Timing](https://dvcs.w3.org/hg/webperf/raw-file/tip/specs/UserTiming/Overview.html) and [Resource Timing](http://www.w3c-test.org/webperf/specs/ResourceTiming/) – but those are still under discussion in working groups and as such we have not yet implemented them.

## About
[
Christopher Blizzard ](http://www.0xdeadbeef.com/weblog)

Making the web better, one release at a time.

## 23 comments

Der CaspersSeptember 27th, 2011 at 09:17Olivier clémeneSeptember 27th, 2011 at 11:12melchior blausandSeptember 27th, 2011 at 11:23mohammadSeptember 27th, 2011 at 11:25BorisSeptember 28th, 2011 at 12:34Paul RougetSeptember 30th, 2011 at 01:39FrancisSeptember 27th, 2011 at 11:27BorisSeptember 28th, 2011 at 12:32Div DiversonSeptember 27th, 2011 at 13:19Der CaspersSeptember 28th, 2011 at 22:54BorisSeptember 27th, 2011 at 14:16BorisSeptember 27th, 2011 at 14:17BorisSeptember 27th, 2011 at 14:17SkouaSeptember 27th, 2011 at 15:04maciejSeptember 28th, 2011 at 13:10DemianOctober 5th, 2011 at 05:22DemianOctober 5th, 2011 at 05:24BorisOctober 6th, 2011 at 19:18FrancisSeptember 28th, 2011 at 16:44BorisSeptember 28th, 2011 at 18:31JohanOctober 1st, 2011 at 08:14BorisOctober 1st, 2011 at 20:28JordiOctober 19th, 2011 at 00:09