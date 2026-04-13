---
title: Firefox 62 – Tools Cool for School! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/09/firefox-62/
author: Sergi Mansilla
published: '2018-09-06'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Hello there! It’s been six-odd weeks, and the march of progress continues to, uh… march… progressingly. That means we have a brand new Firefox to share, with an abundance of bug fixes, performance improvements, and (in particular) sweet developer tool treats! So tuck in your napkin and enjoy this tasting menu of some of what’s new in Firefox 62.

## Shape Up Your Floats

CSS Shapes lets a floated element sculpt the flow of content around it beyond the classic rectangular bounding box we’ve been constrained to. For instance, in the above screenshot and linked demo, the text is wrapping to the shape of the grapes vs the image’s border. There are properties for basic shapes all the way up to complex polygons. There are of course [great docs](https://developer.mozilla.org/en-US/docs/Web/CSS/shape-outside) on all of this, but Firefox 62 also includes new tooling to both inspect and visually manipulate CSS Shapes values.

You can learn more in [Josh Marinacci’s post on the new CSS Shapes tooling](https://hacks.mozilla.org/2018/09/make-your-web-layouts-bust-out-of-the-rectangle-with-the-firefox-shape-path-editor/) from yesterday.

## Variable Fonts Are Here!

No punny title, I’m just excited! OpenType Font Variations allow a single font file to contain multiple instances of the same font, encoding the differences between instances. In addition to being in one file, font creators can expose any number of variation axes that give developers fine-grained control on how a font is rendered. These can be standard variations like font weight (font weight 536 looks right? no problem!) or things that were never previously available via CSS (x-height! serif-size!). In addition to the candy-store possibilities for typography nerds, being able to serve a single file with multiple variants is a major page weight savings. [Dan Callahan](https://hacks.mozilla.org/2018/09/variable-fonts-arrive-in-firefox-62/) goes much deeper on the grooviness to be found and how Firefox makes it easy to tweak these new custom values.

## Devtools Commands

The Developer Toolbar was an alternate command [repl](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) input in the Firefox Developer tools, apart from the Web Console. I say “was” because as of Firefox 62, it has been removed. It was always a bit hard to find and not as well-advertised as it could be, but did encapsulate some powerful commands. Most of these commands have been progressively migrated elsewhere in the devtools, and this is wrapped up in Firefox 62, so we’ve removed the toolbar altogether.

One of the last commands to be migrated is `screenshot`

, which is a power-user version of the “take a screenshot” button available in the devtools UI. The [ screenshot command is now available as :screenshot in the Web Console!](https://blog.nightly.mozilla.org/2018/08/23/screenshots-from-the-console/) For example, have you ever needed a high-res screenshot of a page for print? You can specify a higher pixel density for a screenshot via the command:


```
:screenshot --dpr 4
```


There are a bunch of other options as well, such as specifying output filenames, capture delays, and selector-cropped screenshots. [Eric Meyer wrote a great primer](https://meyerweb.com/eric/thoughts/2018/08/24/firefoxs-screenshot-command-2018/) on the power of `:screenshot`

on his blog, and it will change your page capture game!

🌠 *Did You Know: In addition to :screenshot, there are a bunch of other helpful commands and magic variables available from within the Web Console? You can learn about them on MDN Web Docs.*

## Mo’ Pixels, Mo’ Panels

Do you have a 4k monitor? Do your browser windows bathe in a wash of ample screen real-estate? Let your devtools stretch their legs with a new [3-column mode](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/3-pane_mode) in the Page Inspector. You can now pop the CSS Rules view into its own column, to let you view style information and the excellent Grid tooling or Animations panel side-by-side.

![](../../assets/e0391d1402e688dc.png)


![](../../assets/e0391d1402e688dc.png)

## Streamlining MediaStream

If you’ve worked with WebRTC’s [ getUserMedia API](https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia), you may be familiar with a bit of branching logic when attaching a MediaStream object to a

`<video>`

or `<audio>`

tag:```
navigator.mediaDevices.getUserMedia({ audio: true, video: true })
.then(function(stream) {
if ("srcObject" in video) {
videoEl.srcObject = stream;
} else {
videoEl.src = URL.createObjectURL(stream);
}
});
```


It’s true that earlier support for WebRTC required the use of the `URL`

API, but this was non-standard and is no longer necessary. Firefox 62 removes support for passing a MediaStream to `createObjectURL`

, so be sure you’re using a proper capability check as above.

## Why stop here?

I’ve shown you a glimpse of what’s new and exciting in Firefox 62, but there’s more to learn and love! Be sure to check out the [product release notes](https://www.mozilla.org/en-US/firefox/62.0/releasenotes/) for user-facing features as well as a more complete list of developer facing changes on [MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/62).

Happy building!