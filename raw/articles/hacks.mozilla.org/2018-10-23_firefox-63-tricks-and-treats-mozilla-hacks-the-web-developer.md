---
title: Firefox 63 – Tricks and Treats! – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2018/10/firefox-63-tricks-and-treats/
author: Sergi Mansilla
published: '2018-10-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It’s that time of the year again- when we [put on costumes](https://mozilla.github.io/FirefoxColor/?theme=XQAAAAIQAQAAAAAAAABBqYhm849SCia2CaaEGccwS-xNKlhMjgHXI2DYk6tUZL6Q64nyQ2hKMbyHnlNXq12cENl4ikTlGFp5QlEGQ5HvnBct055iGX6HZqUhXGc4DQNMjaGXx04P1g4B-hopGGKHtbXPY2hqk-Tr8y6UbaLezNT9hVORF2QWUNHTVzEDZ6GY-EcvNUS72u4RxX-ttVhrqbXJTARvV5-YCcfI3z6zcXN0DSB7p5A6hiwbmu2w5u0MXL_SQlTAZHkGaoIX_BcSwA) and pass out goodies to all. It’s Firefox release week! Join me for a spook-tacular 1 look at the latest goodies shipping this release.

## Web Components, Oh My!

After a [rather](https://hacks.mozilla.org/2013/08/introducing-brick-minimal-markup-web-components-for-faster-app-development/) [long](https://hacks.mozilla.org/2015/06/the-state-of-web-components/) [gestation](https://hacks.mozilla.org/2015/11/an-update-on-web-components-and-firefox/), I’m pleased to announce that support for modern Web Components APIs has shipped in Firefox! Expect a more thorough write-up, but let’s cover what these new APIs make possible.

### Custom Elements

To put it simply, [Custom Elements](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements) makes it possible to define new HTML tags outside the standard set included in the web platform. It does this by letting JS classes extend the built-in `HTMLElement`

object, adding an API for registering new elements, and by adding special “lifecycle” methods to detect when a custom element is appended, removed, or attributes are updated:

```
class FancyList extends HTMLElement {
constructor () {
super();
this.style.fontFamily = 'cursive'; // very fancy
}
connectedCallback() {
console.log('Make Way!');
}
disconnectedCallback() {
console.log('I Bid You Adieu.');
}
}
customElements.define('fancy-list', FancyList);
```


### Shadow DOM

The web has long had reusable widgets people can use when building a site. One of the most common challenges when using third-party widgets on a page is making sure that the styles of the page don’t mess up the appearance of the widget and vice-versa. This can be frustrating (to put it mildly), and leads to lots of long, overly specific CSS selectors, or the use of complex third-party tools to re-write all the styles on the page to not conflict.

*Cue frustrated developer:*

There has to be a better way…


Now, there is!

The [Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM) is not a secretive underground society of web developers, but instead a foundational web technology that lets developers create encapsulated HTML trees that aren’t affected by outside styles, can have their own styles that don’t leak out, and in fact can be made unreachable from normal DOM traversal methods (`querySelector`

, `.childNodes`

, etc.).

```
let shadow = div.attachShadow({ mode: 'open' });
let inner = document.createElement('b');
inner.appendChild(document.createTextNode('I was born in the shadows'));
shadow.appendChild(inner);
div.querySelector('b'); // empty
```


Custom elements and shadow roots can be used independently of one another, but they really shine when used together. For instance, imagine you have a `<media-player>`

element with playback controls. You can put the controls in a shadow root and keep the page’s DOM clean! In fact, Both Firefox and Chrome now use Shadow DOM for the implementation of the `<video>`

element.

Expect a deeper dive on building full-fledged components here on Hacks soon! In the meantime, you can plunge into [the Web Components docs on MDN](https://developer.mozilla.org/en-US/docs/Web/Web_Components) as well as see the code for a bunch of [sample custom elements on GitHub](https://github.com/mdn/web-components-examples).

## Fonts Editor

![a screenshot of the fonts panel being used to adjust a variable font](../../assets/fba4237650244fa9.png)


The Inspector’s Fonts panel is a handy way to see what local and web fonts are being used on a page. Already useful for debugging webfonts, in Firefox 63 the Fonts panel gains new powers! You can adjust the parameters of the font on the currently selected element, and if the current font supports Font Variations, you can view and fine-tune those paramaters as well. The syntax for adjusting variable fonts can be a little unfamiliar and it’s not otherwise possible to discover all the variations built into a font, so this tool can be a life saver.

Read all about how to use the [new Fonts panel on MDN Web Docs](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Edit_fonts).

## Reduced motion preferences for CSS

Slick animations can give a polished and unique feel to a digital experience. However, for some people, animated effects like parallax and sliding/zooming transitions can cause vertigo and headaches. In addition, some older/less powerful devices can struggle to render animations smoothly. To respond to this, some devices and operating systems offer a “reduce motion” option. In Firefox 63, you can now detect this preference using [CSS media queries](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion) and adjust/reduce your use of transitions and animations to ensure more people have a pleasant experience using your site. CSS Tricks has a [great overview](https://css-tricks.com/introduction-reduced-motion-media-query/) of both how to detect reduced motion and why you should care.

## Conclusion

There is, as always, a bunch more in this release of Firefox. [MDN Web Docs](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox/Releases/63) has the full run-down of developer-facing changes, and more highlights can be found in the [official release notes](https://www.mozilla.org/en-US/firefox/63.0/releasenotes/). Happy Browsing!

[1.] not particularly spook-tacular