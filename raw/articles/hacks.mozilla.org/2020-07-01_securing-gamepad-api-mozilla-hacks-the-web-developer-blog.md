---
title: Securing Gamepad API – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/07/securing-gamepad-api/
author: Marcos Caceres
published: '2020-07-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

### Firefox release dates for Gamepad API updates

As part of Mozilla’s ongoing commitment to improve the privacy and security of the web platform, over the next few months we will be making some changes to how the [Gamepad_API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API) works.

Here are the important dates to keep in mind:

- 25 of August 2020 (Firefox
**81 Beta/Developer Edition**): `.<a href="https://developer.mozilla.org/en-US/docs/Web/API/Navigator/getGamepads">getGamepads()</a>`

method will only return game pads if called in a “secure context” (e.g., https://).- 22 of September 2020 (Firefox
**82 Beta/Developer Edition**): - Switch to requiring a permission policy for third-party contexts/iframes.

We are collaborating on making these changes with folks from the Chrome team and other browser vendors. We will update this post with links to their announcements as they become available.

### Restricting gamepads to secure contexts

Starting with Firefox 81, the [Gamepad API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API) will be restricted to what are known as “[secure contexts](https://www.w3.org/TR/secure-contexts/)” ([bug 1591329](https://bugzilla.mozilla.org/show_bug.cgi?id=1591329)). Basically, this means that Gamepad API will only work on sites served as “https://”. But don’t worry, it also works on http://localhost too while you are debugging!

For the next few months, we will show a developer console warning whenever `.getGamepads()`

method is called from an insecure context.

From Firefox 81, we plan to require secure context for `.getGamepads()`

by default. To avoid significant code breakage, calling `.getGamepads()`

will return an empty array. We will display this console warning indefinitely:

![Firefox developer console](../../assets/aaec98d23f8bffd6.png)

The developer console nows shows a warning when `.getGamepads()`

method is called from insecure contexts

### Permission Policy integration

From Firefox 82, third-party contexts (i.e., `<iframe>`

s that are not same origin) that require access to the Gamepad API will have to be explicitly granted access by the hosting website via a [ Permissions Policy](https://w3c.github.io/webappsec-feature-policy/).

In order for a third-party context to be able to use the Gamepad API, you will need to add an “allow” attribute to your HTML like so:

```
<iframe allow="gamepad" src="https://example.com/">
</iframe>
```


Once this ships, calling `.getGamepads()`

from a disallowed third-party context will throw a JavaScript security error.

You can our track our implementation progress in [bug 1640086](https://bugzilla.mozilla.org/show_bug.cgi?id=1640086).

### WebVR/WebXR

As WebVR and WebXR already require a secure context to work, these changes

shouldn’t affect any sites relying on `.getGamepads()`

. In fact, everything should continue to work as it does today.

### Future improvements to privacy and security

When we ship APIs we often find that sites use them in unintended ways – mostly creatively, sometimes maliciously. As new privacy and security capabilities are added to the web platform, we retrofit those solutions to better protect users from malicious sites and third-party trackers.

Adding “secure contexts” and “permission policy” to the Gamepad API is part of this ongoing effort to improve the overall privacy and security of the web. Although we know these changes can be a short-term inconvenience to developers, we believe it’s important to constantly evolve the web to be as secure and privacy-preserving as it can be for all users.

## 6 comments

ConstantinJuly 2nd, 2020 at 08:07Marcos CaceresJuly 5th, 2020 at 22:01Jim HarrisJuly 2nd, 2020 at 11:24Marcos CaceresJuly 5th, 2020 at 21:53AnonymousJuly 22nd, 2020 at 05:55Marcos CaceresJuly 22nd, 2020 at 06:44