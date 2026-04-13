---
title: Flash-Free Clipboard for the Web – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2015/09/flash-free-clipboard-for-the-web/
author: Nika Layzell
published: '2015-09-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

As part of our effort to grow the Web platform and make it accessible to new devices, we are trying to reduce the Web’s dependence on [Flash](https://en.wikipedia.org/wiki/Adobe_Flash). As part of that effort, we are standardizing and exposing useful features which are currently only available to Flash to the entirety of the Web platform.

One of the reasons why many sites still use Flash is because of its copy and cut clipboard APIs. Flash exposes an API for programmatically copying text to the user’s clipboard on a button press. This has been used to implement handy features, such as GitHub’s “clone URL” button. It’s also useful for things such as editor UIs, which want to expose a button for copying to the clipboard, rather than requiring users to use keyboard shortcuts or the context menu.

![](../../assets/99de10204102feac.png)


Unfortunately, Web APIs haven’t provided the functionality to copy text to the clipboard through JavaScript, which is why visiting GitHub with Flash disabled shows an ugly grey box where the button is supposed to be. Fortunately, we have a solution. The editor APIs provide [ document.execCommand](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand) as an entry point for executing editor commands. The

`"copy"`

and `cut"`

commands have previously been disabled for web pages, but with Firefox 41, which is currently in Beta, and slated to move to release in mid-September, it is becoming available to JavaScript within user-action initiated callbacks.### Using `execCommand("cut"/"copy")`


The `execCommand("cut"/"copy")`

API is only available during a user-triggered callback, such as a click. If you try to call it at a different time, `execCommand`

will return `false`

, meaning that the command failed to execute. Running `execCommand("cut")`

will copy the current selection to the clipboard, so let’s go about implementing a basic copy-to-clipboard button.

`<pre>// button which we are attaching the event to`


var button = ...;

// input containing the text we want to copy

var input = ...;

button.addEventListener("click", function(event) {

event.preventDefault();

// Select the input node's contents

input.select();

// Copy it to the clipboard

document.execCommand("copy");

});</pre>

That code will trigger a copy of the text in the input to the clipboard upon the click of the button in Firefox 41 and above. However, you probably want to also handle failure situations, potentially to fallback to another Flash-based approach such as [ZeroClipboard](http://zeroclipboard.org/), or even just to tell the user that their browser doesn’t support the functionality.

The `execCommand`

method will return false if the action failed, for example, due to being called outside of a user-initiated callback, but on older versions of Firefox, we would also throw a security exception if you attempted to use the `"cut"`

or `"copy"`

APIs. Thus, if you want to be sure that you capture all failures, make sure to surround the call in a try-catch block, and also interpret an exception as a failure.

`<pre>// button which we are attaching the event to`


var button = ...;

// input containing the text we want to copy

var input = ...;

button.addEventListener("click", function(event) {

event.preventDefault();

input.select(); // Select the input node's contents

var succeeded;

try {

// Copy it to the clipboard

succeeded = document.execCommand("copy");

} catch (e) {

succeeded = false;

}

if (succeeded) {

// The copy was successful!

} else {

// The copy failed :(

}

});</pre>

The `"cut"`

API is also exposed to web pages through the same mechanism, so just `s/copy/cut/`

, and you’re all set to go!

### Feature testing

The editor APIs provide a method `document.queryCommandSupported("copy")`

intended to allow API consumers to determine whether a command is supported by the browser. Unfortunately, in versions of Firefox prior to 41, we returned `true`

from `document.queryCommandSupported("copy")`

even though the web page was unable to actually perform the copy operation. However, attempting to execute `document.execCommand("copy")`

would throw a `SecurityException`

. So, attempting to copy on load, and checking for this exception is probably the easiest way to feature-detect support for `document.execCommand("copy")`

in Firefox.

`<pre>var supported = document.queryCommandSupported("copy");`


if (supported) {

// Check that the browser isn't Firefox pre-41

try {

document.execCommand("copy");

} catch (e) {

supported = false;

}

}

if (!supported) {

// Fall back to an alternate approach like ZeroClipboard

}</pre>

## Support in other browsers

Google Chrome and Internet Explorer both also support this API. Chrome uses the same restriction as Firefox (that it must be run in a user-initiated callback). Internet Explorer allows it to be called at any time, except it first prompts the user with a dialog, asking for permission to access the clipboard.

For more information about the API and browser support, see [MDN documentation for document.execCommand()](https://developer.mozilla.org/en-US/docs/Web/API/Document/execCommand).

## 24 comments

marioSeptember 1st, 2015 at 08:22SergeSeptember 1st, 2015 at 08:48Josh TriplettSeptember 1st, 2015 at 10:24Nika LayzellSeptember 2nd, 2015 at 10:11voracitySeptember 4th, 2015 at 21:524esn0kSeptember 1st, 2015 at 11:24cpeterson@mozilla.comSeptember 2nd, 2015 at 20:27cpeterson@mozilla.comSeptember 2nd, 2015 at 21:06Dmitry PashkevichSeptember 1st, 2015 at 11:34cpeterson@mozilla.comSeptember 2nd, 2015 at 20:36Brett ZamirSeptember 1st, 2015 at 14:07LukeSeptember 1st, 2015 at 20:29cpeterson@mozilla.comSeptember 2nd, 2015 at 16:34_ck_September 1st, 2015 at 14:51Nika LayzellSeptember 2nd, 2015 at 10:15marsjaninzmarsaSeptember 6th, 2015 at 18:09AntoineSeptember 8th, 2015 at 05:12Matthew DouglassSeptember 1st, 2015 at 16:20Nika LayzellSeptember 2nd, 2015 at 10:02Dane MacMillanSeptember 4th, 2015 at 07:39voracitySeptember 4th, 2015 at 22:34zilchSeptember 7th, 2015 at 03:02Zeno RochaSeptember 27th, 2015 at 17:12MadisOctober 1st, 2015 at 06:34