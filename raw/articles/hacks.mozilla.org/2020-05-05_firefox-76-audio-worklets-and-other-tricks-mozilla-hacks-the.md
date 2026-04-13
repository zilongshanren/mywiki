---
title: 'Firefox 76: Audio worklets and other tricks – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2020/05/firefox-76-audio-worklets-and-other-tricks/
author: Chris Mills
published: '2020-05-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

*Note: This post is also available in: 简体中文 (Chinese (Simplified)), 繁體中文 (Chinese (Traditional)), Español (Spanish).*

Hello folks, hope you are all doing well and staying safe.

A new version of your favourite browser is always worth looking forward to, and here we are with Firefox 76! Web platform support sees some great new additions in this release, such as [Audio Worklets](https://developer.mozilla.org/docs/Web/API/AudioWorklet) and [ Intl improvements](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl), on the JavaScript side. Also, we’ve added a number of nice improvements into Firefox DevTools to make development easier and quicker.

As always, read on for the highlights, or find the full list of additions in the following articles:

## Developer tools additions

There are interesting DevTools updates in this release throughout every panel. And upcoming features can be previewed now in [Firefox Dev Edition](https://www.mozilla.org/firefox/developer/).

### More JavaScript productivity tricks

Firefox JavaScript debugging just got even better.

#### Ignore entire folders in Debugger

Oftentimes, debugging efforts only focus on specific files that are likely to contain the culprit. With “blackboxing” you can tell the [Debugger](https://developer.mozilla.org/docs/Tools/Debugger) to ignore the files you don’t need to debug.

Now it’s easier to do this for folders as well, thanks to [Stepan Stava](https://bugzilla.mozilla.org/user_profile?user_id=652974)‘s new context menu in the Debugger’s sources pane. You can limit “ignoring” to files inside or outside of the selected folder. Combine this with “Set directory root” for a laser-focused debugging experience.

#### Collapsed output for larger console snippets

The [Console](https://developer.mozilla.org/docs/Tools/Web_Console)‘s [multi-line editor mode](https://developer.mozilla.org/docs/Tools/Web_Console/The_command_line_interpreter#Multi-line_mode) is great for iterating on longer code snippets. Early feedback showed that users didn’t want the code repeated in the Console output, to avoid clutter. Thanks to [thelehhman](https://github.com/thelehhman)‘s contribution, code snippets with multiple lines are neatly collapsed and can be expanded on demand.

#### Copy full URLs in call stack

Copying stacks in the Debugger makes it possible to share snapshots during stepping. This helps you file better bugs, and facilitates handover to your colleagues. In order to provide collaborators the full context of a bug, the [call stack pane](https://developer.mozilla.org/docs/Tools/Debugger/UI_Tour#Call_stack)‘s “Copy stack trace” menu now copies full URLs, not just filenames.

#### Always offer “Expand All” in Firefox’s JSON preview

Built-in previews for JSON files make it easy to search through responses and explore API endpoints. This also works well for large files, where data can be expanded as needed. Thanks to a contribution from [zacnomore](https://github.com/zacnomore), the “Expand All” option is now always visible.

### More network inspection tricks

Firefox 76 provides even easier access to network information via the [Network Monitor](https://developer.mozilla.org/docs/Tools/Network_Monitor).

#### Action Cable support in WebSocket inspection

WebSocket libraries use a variety of formats to encode their messages. We want to make sure that their payloads are properly parsed and formatted, so you can read them. Over the past releases, we added support for Socket.IO, SignalR, and WAMP [WebSocket message inspection](https://developer.mozilla.org/docs/Tools/Network_Monitor/Inspecting_web_sockets). Thanks to contributor [Uday Mewada](https://bugzilla.mozilla.org/show_bug.cgi?id=1590046), Action Cable messages are now nicely formatted too.

#### Hiding WebSocket Control Frames

WebSocket control frames are used by servers and browsers to manage real-time connections but don’t contain any data. Contributor [kishlaya.j](https://bugzilla.mozilla.org/show_bug.cgi?id=1566780) jumped in to hide control frames by default, cutting out a little more noise from your debugging. In case you need to see them, they can be enabled in the sent/received dropdown.

#### Resize Network table columns to fit content

Network request and response data can be overwhelming as you move from scanning real-time updates to focus on specific data points. Customizing the visible Network panel columns lets you adapt the output to the problem at hand. In the past, this required a lot of dragging and resizing. Thanks to [Farooq AR](https://twitter.com/Farooq_AR), you can now double-click the table’s resize handles to scale a column’s width to fit its content, as in modern data tables.

#### Better Network response details and copying

We’ve received feedback that it should be easier to copy parts of the network data for further analysis.

Now the “Response” section of Network details has been modernized to make inspection and copying easier, by rendering faster and being more reliable. We’ll be adding more ease of use improvements to Network analysis in the near future, [thanks to your input](https://twitter.com/FirefoxDevTools/status/1255209764541263872).

### Community contributions

[Laurențiu Nicola](https://bugzilla.mozilla.org/show_bug.cgi?id=1549773)fixed the network request[“Copy as cURL”](https://developer.mozilla.org/docs/Tools/Network_Monitor/request_list#Copy_as_cURL)menu to be more reliable by adding`--globoff`

to the generated command.[Patricia Lee](https://bugzilla.mozilla.org/show_bug.cgi?id=1612276)added a “Reveal in Inspector” context menu option in the Console as another way to jump from logged DOM elements to their position in the DOM tree.[sankalp.sans](https://bugzilla.mozilla.org/show_bug.cgi?id=1424863)improved the copied format in[Inspector’s “Changes” panel](https://developer.mozilla.org/docs/Tools/Page_Inspector/How_to/Examine_and_edit_CSS#Track_changes). “Copying CSS Rules” now inserts empty lines between rules, so they can be re-used more easily in editors.[Basavaraj](https://bugzilla.mozilla.org/show_bug.cgi?id=1574456)fixed an issue that caused[Network query parameters](https://developer.mozilla.org/docs/Tools/Network_Monitor/request_details#Params)that contained “+” to not be displayed[Aarushivij](https://bugzilla.mozilla.org/show_bug.cgi?id=1339558)fixed the rendering for[Network’s performance analysis](https://developer.mozilla.org/docs/Tools/Network_Monitor/Performance_Analysis)to be more responsive to smaller sizes

### Fresh in Dev Edition: CSS Compatibility Panel

[Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) is Firefox’s pre-release channel, which offers early access to tooling and platform features. Its settings enable more functionality for developers by default. We like to bring new features quickly to Developer Edition to gather your feedback, including the following highlights.

Foremost, in the release of Dev Edition 77 we are seeking input for our new compatibility panel. This panel will inform you about any CSS properties that might not be supported in other browsers, and will be accessible from the Inspector.

Please try it out and use the built-in “Feedback” link to report how well it works for you and how we can further improve it.

## Web platform updates

Let’s explore what Firefox 76 brings to the table in terms of web platform updates.

### Audio worklets

Audio worklets offer a useful way of running custom JavaScript audio processing code. The difference between audio worklets and their predecessor — [ ScriptProcessorNode](https://developer.mozilla.org/docs/Web/API/ScriptProcessorNode)s — worklets run off the main thread in a similar way to web workers, solving the performance problems encountered previously.

The basic idea is this: You define a custom [ AudioWorkletProcessor](https://developer.mozilla.org/docs/Web/API/AudioWorkletProcessor), which will handle the processing. Next, register it.

```
// white-noise-processor.js
class WhiteNoiseProcessor extends AudioWorkletProcessor {
process (inputs, outputs, parameters) {
const output = outputs[0]
output.forEach(channel => {
for (let i = 0; i < channel.length; i++) {
channel[i] = Math.random() * 2 - 1
}
})
return true
}
}
registerProcessor('white-noise-processor', WhiteNoiseProcessor)
```


Over in your main script, you then load the processor, create an instance of [ AudioWorkletNode](https://developer.mozilla.org/docs/Web/API/AudioWorkletNode), and pass it the name of the processor. Finally, you connect the node to an audio graph.

```
async function createAudioProcessor() {
const audioContext = new AudioContext()
await audioContext.audioWorklet.addModule('white-noise-processor.js')
const whiteNoiseNode = new AudioWorkletNode(audioContext, 'white-noise-processor')
whiteNoiseNode.connect(audioContext.destination)
}
```


Read our [Background audio processing using AudioWorklet](https://developer.mozilla.org/docs/Web/API/Web_Audio_API/Using_AudioWorklet) guide for more information.

### Other updates

Aside from worklets, we’ve added some other web platform features.

#### HTML `<input>`

s

The HTML [ <input>](https://developer.mozilla.org/docs/Web/HTML/Element/input) element’s

[and](https://developer.mozilla.org/docs/Web/HTML/Element/input#attr-min)

`min`

[attributes now work correctly when the value of](https://developer.mozilla.org/docs/Web/HTML/Element/input#attr-max)

`max`

`min`

is greater than the value of `max`

, for control types whose values are periodic. (Periodic values repeat in regular intervals, wrapping around from the end back to the start again.) This is particularly helpful with `date`

and `time`

inputs for example, where you might want to specify a time range of 11 PM to 2 AM.`Intl`

improvements

The `numberingSystem`

and `calendar`

options of the [ Intl.NumberFormat](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat),

[, and](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/DateTimeFormat)

`Intl.DateTimeFormat`

[constructors are now enabled by default.](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Intl/RelativeTimeFormat)

`Intl.RelativeTimeFormat`

Try these examples:

```
const number = 123456.789;
console.log(new Intl.NumberFormat('en-US', { numberingSystem: 'latn' }).format(number));
console.log(new Intl.NumberFormat('en-US', { numberingSystem: 'arab' }).format(number));
console.log(new Intl.NumberFormat('en-US', { numberingSystem: 'thai' }).format(number));
var date = Date.now();
console.log(new Intl.DateTimeFormat('th', { calendar: 'buddhist' }).format(date));
console.log(new Intl.DateTimeFormat('th', { calendar: 'gregory' }).format(date));
console.log(new Intl.DateTimeFormat('th', { calendar: 'chinese' }).format(date));
```


#### Intersection observer

The [ IntersectionObserver()](https://developer.mozilla.org/docs/Web/API/IntersectionObserver/IntersectionObserver) constructor now accepts both

[and](https://developer.mozilla.org/docs/Web/API/Document)

`Document`

[objects as its root. In this context, the root is the area whose bounding box is considered the viewport for the purposes of observation.](https://developer.mozilla.org/docs/Web/API/Element)

`Element`

## Browser extensions

The [Firefox Profiler](https://profiler.firefox.com/) is a tool to help analyze and improve the performance of your site in Firefox. Now it will show markers when network requests are suspended by extensions’ [blocking webRequest handlers](https://developer.mozilla.org/docs/Mozilla/Add-ons/WebExtensions/API/webRequest/BlockingResponse). This is especially useful to developers of content blocker extensions, enabling them to ensure that Firefox remains at top speed.

Here’s a screenshot of the Firefox profiler in action:

![Firefox profiler extension UI](../../assets/9d5e920fb9762921.png)


## Summary

And that’s it for the newest edition of Firefox — we hope you enjoy the new features! As always, feel free to give feedback and ask questions in the comments.

## About Chris Mills

Chris Mills is a senior tech writer at Mozilla, where he writes docs and demos about open web apps, HTML/CSS/JavaScript, A11y, WebAssembly, and more. He loves tinkering around with web technologies, and gives occasional tech talks at conferences and universities. He used to work for Opera and W3C, and enjoys playing heavy metal drums and drinking good beer. He lives near Manchester, UK, with his good lady and three beautiful children.

Harald "digitarald" Kirschner is a Product Manager for Firefox's Developer Experience and Tools – striving to empower creators to code, design & maintain a web that is open and accessible to all. During his 8 years at Mozilla, he has grown his skill set amidst performance, web APIs, mobile, installable web apps, data visualization, and developer outreach projects.

## 5 comments

Rob LewisMay 6th, 2020 at 09:15Konstantin PaulMay 8th, 2020 at 00:38Mike StarrMay 7th, 2020 at 11:36Albatrosul VerdeMay 7th, 2020 at 14:07GagikMay 17th, 2020 at 05:28