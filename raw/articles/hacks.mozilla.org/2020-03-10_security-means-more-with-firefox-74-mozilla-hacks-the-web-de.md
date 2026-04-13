---
title: Security means more with Firefox 74 – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2020/03/security-means-more-with-firefox-74-2/
author: Chris Mills
published: '2020-03-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Today sees the release of Firefox number 74. The most significant new features we’ve got for you this time are security enhancements: Feature Policy, the `Cross-Origin-Resource-Policy`

header, and removal of TLS 1.0/1.1 support. We’ve also got some new CSS text property features, the JS optional chaining operator, and additional 2D canvas text metric features, along with the usual wealth of DevTools enhancements and bug fixes.

As always, read on for the highlights, or find the full list of additions in the following articles:

**Note**: In the *Security enhancements* section below, we detail the removal of TLS 1.0/1.1 in Firefox 74, however we reverted this change for an undetermined amount of time, to better enable access to critical government sites sharing COVID19 information. We are keeping the infomation below intact because it is still useful to give you an idea of future intents. *(Updated Monday, 30 March.)*

## Security enhancements

Let’s look at the security enhancement we’ve got in 74.

### Feature Policy

We’ve finally enabled [Feature Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Feature_Policy/Using_Feature_Policy) by default. You can now use the `<iframe>`

`allow`

attribute and the [ Feature-Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Feature-Policy) HTTP header to set feature permissions for your top level documents and IFrames. Syntax examples follow:

`<iframe src="https://example.com" allow="fullscreen"></iframe>`


`Feature-Policy: microphone 'none'; geolocation 'none'`


### CORP

We’ve also enabled support for the [ Cross-Origin-Resource-Policy (CORP)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cross-Origin_Resource_Policy_(CORP)) header, which allows web sites and applications to opt in to protection against certain cross-origin requests (such as those coming from

`<script>`

and `<img>`

elements). This can help to mitigate speculative side-channel attacks (like Spectre and Meltdown) as well as Cross-Site Script Inclusion attacks.The available values are `same-origin`

and `same-site`

. `same-origin`

only allows requests that share the same scheme, host, and port to read the relevant resource. This provides an additional level of protection beyond the web’s default same-origin policy. `same-site`

only allows requests that share the same site.

To use CORP, set the header to one of these values, for example:

`Cross-Origin-Resource-Policy: same-site`


### TLS 1.0/1.1 removal

Last but not least, Firefox 74 sees the removal of TLS 1.0/1.1 support, to help raise the overall level of security of the web platform. This is vital for moving the TLS ecosystem forward, and getting rid of a number of vulnerabilities that existed as a result of TLS 1.0/1.1 not being as robust as we’d really like — they’re in need of retirement.

The change was first announced in October 2018 as a shared initiative of Mozilla, Google, Microsoft, and Apple. Now in March 2020 we are all acting on our promises (with the exception of Apple, who will be making the change slightly later on).

The upshot is that you’ll need to make sure your web server supports TLS 1.2 or 1.3 going forward. Read [TLS 1.0 and 1.1 Removal Update](https://hacks.mozilla.org/2019/05/tls-1-0-and-1-1-removal-update/) to find out how to test and update your TLS/SSL configuration. From now on, Firefox will return a [Secure Connection Failed](https://support.mozilla.org/en-US/kb/secure-connection-failed-firefox-did-not-connect) error when connecting to servers using the older TLS versions. **Upgrade now**, if you haven’t already!

![secure connection failed error message, due to connected server using TLS 1.0 or 1.1](../../assets/b02e36f205b1a345.png)


**Note**: For a couple of release cycles (and longer for Firefox ESR), the *Secure Connection Failed* error page will feature an override button allowing you to Enable TLS 1.0 and 1.1 in cases where a server is not yet upgraded, but you won’t be able to rely on it for too long.

To find out more about TLS 1.0/1.1 removal and the background behind it, read [It’s the Boot for TLS 1.0 and TLS 1.1](https://hacks.mozilla.org/2020/02/its-the-boot-for-tls-1-0-and-tls-1-1/).

## Other web platform additions

We’ve got a host of other web platform additions for you in 74.

### New CSS text features

For a start, the [ text-underline-position](https://developer.mozilla.org/en-US/docs/Web/CSS/text-underline-position) property is enabled by default. This is useful for positioning underlines set on your text in certain contexts to achieve specific typographic effects.

For example, if your text is in a horizontal [writing mode](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Handling_different_text_directions), you can use `text-underline-position: under;`

to put the underline below all the descenders, which is useful for ensuring legibility with chemical and mathematical formulas, which make frequent use of subscripts.

```
.horizontal {
text-underline-position: under;
}
```


In text with a vertical [ writing-mode](https://developer.mozilla.org/en-US/docs/Web/CSS/writing-mode) set, we can use values of

`left`

or `right`

to make the underline appear to the left or right of the text as required.```
.vertical {
writing-mode: vertical-rl;
text-underline-position: left;
}
```


In addition, the [ text-underline-offset](https://developer.mozilla.org/en-US/docs/Web/CSS/text-underline-offset) and

[properties now accept percentage values, for example:](https://developer.mozilla.org/en-US/docs/Web/CSS/text-decoration-thickness)

`text-decoration-thickness`

`text-decoration-thickness: 10%;`


For these properties, this is a percentage of `1em`

in the current font’s size.

### Optional chaining in JavaScript

We now have the JavaScript [optional chaining operator](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Optional_chaining) (`?.`

) available. When you are trying to access an object deep in a chain, this allows for implicit testing of the existence of the objects higher up in the chain, avoiding errors and the need to explicitly write testing code.

`let nestedProp = obj.first?.second;`


### New 2D canvas text metrics

The [ TextMetrics](https://developer.mozilla.org/en-US/docs/Web/API/TextMetrics) interface (retrieved using the

[method) has been extended to contain four more properties measuring the actual bounding box —](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/measureText)

`CanvasRenderingContext2D.measureText()`

[,](https://developer.mozilla.org/en-US/docs/Web/API/TextMetrics/actualBoundingBoxLeft)

`actualBoundingBoxLeft`

[,](https://developer.mozilla.org/en-US/docs/Web/API/TextMetrics/actualBoundingBoxRight)

`actualBoundingBoxRight`

[, and](https://developer.mozilla.org/en-US/docs/Web/API/TextMetrics/actualBoundingBoxAscent)

`actualBoundingBoxAscent`

[.](https://developer.mozilla.org/en-US/docs/Web/API/TextMetrics/actualBoundingBoxDescent)

`actualBoundingBoxDescent`

For example:

```
const canvas = document.createElement('canvas');
const ctx = canvas.getContext('2d');
const text = ctx.measureText('Hello world');
text.width; // 56.08333206176758
text.actualBoundingBoxAscent; // 8
text.actualBoundingBoxDescent; // 0
text.actualBoundingBoxLeft; // 0
text.actualBoundingBoxRight; // 55.733333333333334
```


## DevTools additions

Next up, DevTools additions.

### Device-like rendering in Responsive Design Mode

While [Firefox for Android](https://blog.mozilla.org/futurereleases/2020/01/17/a-brand-new-browsing-experience-arrives-in-firefox-for-android-nightly/) is being relaunched with [GeckoView](https://mozilla.github.io/geckoview/) to be [faster and more private](https://blog.mozilla.org/firefox/firefox-android-new-features/), the DevTools need to stay ahead. Testing on mobile should be as frictionless as possible, both when using [Responsive Design Mode](https://developer.mozilla.org/en-US/docs/Tools/Responsive_Design_Mode) on your desktop and on-device with [Remote Debugging](https://developer.mozilla.org/en-US/docs/Tools/about:debugging).

Correctness is important for Responsive Design Mode, so developers can trust the output without a device at hand. Over the past releases, we rolled out major improvements that ensure [meta viewport](https://developer.mozilla.org/en-US/docs/Mozilla/Mobile/Viewport_meta_tag) is correctly applied with *Touch Simulation*. This ties in with improved device presets, which automatically enable touch simulation for mobile devices.

![animated gif showing how responsive design mode now represents view meta settings better](../../assets/00f1ddda7748920e.gif)


Fun fact: The team managed to make this simulation so accurate that it has already helped to identify and fix rendering bugs for Firefox on Android.

**DevTools Tip:** Open Responsive Design Mode without DevTools via the tools menu or Ctrl + Shift + M on Windows/Cmd + Opt + M on macOS.

We’d love to hear about your experiences when giving your site a spin in RDM or on your Android phone with [Firefox Nightly for Developers](https://play.google.com/store/apps/details?id=org.mozilla.fennec_aurora).

### CSS tools that work for you

The [Page Inspector’s](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector) new in-context warnings for inactive CSS rules have received a lot of positive feedback. They help you solve gnarly CSS issues while teaching you about the intricate interdependencies of CSS rules.

Since its launch, we have continued to tweak and add rules, often based on user feedback. One highlight for 74 is a new detection setting that warns you when properties depend on positioned elements – namely [ z-index](https://developer.mozilla.org/en-US/docs/Web/CSS/z-index),

[,](https://developer.mozilla.org/en-US/docs/Web/CSS/top)

`top`

[,](https://developer.mozilla.org/en-US/docs/Web/CSS/left)

`left`

[, and](https://developer.mozilla.org/en-US/docs/Web/CSS/bottom)

`bottom`

[.](https://developer.mozilla.org/en-US/docs/Web/CSS/right)

`right`

![Firefox Page Inspector now showing inactive position-related properties such as z-index and top](../../assets/5744426e48f2a528.png)


Your feedback will help to further refine and expand the rules. Say hi to the team in the [DevTools chat](https://chat.mozilla.org/#/room/#devtools:mozilla.org) on [Mozilla’s Matrix instance](https://wiki.mozilla.org/Matrix) or follow our work via [@FirefoxDevTools](https://twitter.com/FirefoxDevTools).

### Debugging for Nested Workers

Firefox’s [JavaScript Debugger](https://developer.mozilla.org/en-US/docs/Tools/Debugger) team has been focused on optimizing [Web Workers](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Using_web_workers) over the past few releases to make them easier to inspect and debug. The more developers and frameworks that use workers to move processing off the main thread, the easier it will be for browsers to prioritize running code that is fired as a result of user input actions.

Nested web workers, which allow workers to spawn and control their own worker instances, are now displayed in the Debugger:

![Firefox JavaScript debugger now shows nested workers](../../assets/3b6dccb9bd207706.png)


### Improved React DevTools integration

The [React Developer Tools add-on](https://addons.mozilla.org/en-US/firefox/addon/react-devtools/) is one of many [developer add-ons](https://addons.mozilla.org/en-US/firefox/collections/4757633/webdeveloper/) that integrate tightly with Firefox DevTools. Thanks to the [WebExtensions API](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions), developers can create and publish add-ons for all browsers from the same codebase.

In [collaboration](https://github.com/facebook/react/issues/17681) with the React add-on maintainers, we worked to re-enable and improve the context menus in the add-on, including *Go to definition*. This action lets developers jump from React Components directly to their source files in the Debugger. The same functionality has already been enabled for jumping to elements in the Inspector. We want to build this out further, to make [framework workflows](https://addons.mozilla.org/en-US/firefox/collections/4757633/webdeveloper/) seamless with the rest of the tools.

### Early-access DevTools features in Developer Edition

[Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) is Firefox’s pre-release channel which gets early access to tooling and platform features. Its settings also enable more functionality for developers by default. We like to bring new features quickly to Developer Edition to gather your feedback, including the following highlights.

#### Instant evaluation for Console expressions

Exploring JavaScript objects, functions, and the DOM feels like magic with instant evaluation. As long as expressions typed into the [Web Console](https://developer.mozilla.org/en-US/docs/Tools/Web_Console) are side-effect free, their results will be previewed while you type, allowing you to identify and fix errors more rapidly than before.

#### Async Stack Traces for Debugger & Console

Modern JavaScript code depends heavily upon stacking [ async/await](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function) on top of other


[async operations](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous)like

[events](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events),

[promises](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Promises), and

[timeouts](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous/Timeouts_and_intervals). Thanks to better integration with the JavaScript engine, async execution is now captured to give a more complete picture.

Async call stacks in the Debugger let you step through events, timeouts, and promise-based function calls that are executed over time. In the Console, async stacks make it easier to find the root causes of errors.

![async call stack shown in the Firefox JavaScript debugger](../../assets/c5e2b14cc98d1326.png)


#### Sneak-peek Service Worker Debugging

This one has been in Nightly for a while, and we are more than excited to get it into your hands soon. Expect it in Firefox 76, which will become [Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) in 4 weeks.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

## 5 comments

JoeMarch 12th, 2020 at 23:30anonymousMarch 14th, 2020 at 10:44Chris MillsMarch 16th, 2020 at 02:26MetalAnonMarch 26th, 2020 at 15:22Chris MillsMarch 27th, 2020 at 03:39