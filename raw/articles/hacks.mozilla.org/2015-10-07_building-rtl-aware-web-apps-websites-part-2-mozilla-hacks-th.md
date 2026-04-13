---
title: 'Building RTL-Aware Web Apps & Websites: Part 2 – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2015/10/building-rtl-aware-web-apps-websites-part-2/
author: Ahmed Nefzaoui
published: '2015-10-07'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Pushing the Web forward means making it better for developers and users alike. It means tackling issues that our present Web faces; this is especially true for making responsive RTL design and development easier to achieve.

Before we move on to bleeding edge RTL topics, here’s a video tutorial with a practical example to refresh your mind on how to code RTL properly today:


Picking up where we left off in our last post, it’s time to dive into some advanced topics around Right-To-Left UI implementation. In Part 1 we covered [the basics of RTL](https://hacks.mozilla.org/2015/09/building-rtl-aware-web-apps-and-websites-part-1/). In this second post we will cover how-tos for bidirectional (BIDI) user interfaces on the bleeding edge. This is the alpha state of the Web, and we can take a look at what the future of RTL holds in store.

**RTL on the bleeding edge**

The core of RTL UI design and development on the Web is found in CSS properties and, as with every other aspect of web development, these properties keep improving over time.

Here are the CSS properties you can start using today in alpha versions of several modern browsers. (This information is likely to change as browser updates are released.):

**Text alignment:** In the past we used to explicitly set the horizontal alignment of text with `text-align left`

or `right`

(e.g. `text-align: left`

). We now have start and end values that can be used instead. For instance, `text-align: start`

will give a different result depending on whether the content is set to RTL or LTR. `start`

indicates left in LTR and right in RTL, and vice versa for `end`

.

Example using left/right:

```
#content {
text-align: left:
}
html[dir="rtl"] #content {
text-align: right;
}
```


Example using start/end:

```
#content {
text-align: start;
}
```


With start/end, there’s no need for an RTL rule.

*Browser support: Chrome 1.0+, Safari 3.1+, Firefox 3.6+, Android, iOS. Not supported by Internet Explorer at this time.*

**Padding, margin, and border:** there are a couple of improvements regarding these properties.

Each of them now can take an additional suffix of `-inline-start`

or `-inline-end`

, for example you can write `padding-inline-end`

or `margin-inline-start`

. These new keywords give the same result as start and end in text alignment: `padding-inline-start`

equates to `padding-left`

in LTR and is `padding-right`

in RTL. `margin-inline-end`

gives the effect of `margin-right`

in LTR and `margin-left`

in RTL.

Example using left/right:

```
#content {
padding-left: 12px:
margin-right: 20px;
}
html[dir="rtl"] #content {
padding-left: 0;
padding-right: 12px;
margin-left: 20px;
margin-right: 0px;
}
```


Example using start/end:

```
#content {
padding-inline-start: 12px:
margin-inline-end: 20px;
}
```


Again, there’s no need for an RTL rule; `margin-inline-end`

will act as `margin-right`

in LTR and act as `margin-left`

for RTL, for example.

*Browser support: Firefox 41+ only.*

**Absolute positioning:** `left`

and `right`

are CSS properties that have always been key to absolute positioning, but very soon you’ll be writing much smarter CSS for your users with the new `offset-inline-start`

and `offset-inline-end`

properties.

It is also worth mentioning that top and bottom can be substituted by offset-block-start and offset-block-end.

Example using left/right:

```
#content {
position: absolute;
left: 5rem;
}
html[dir="rtl"] #content {
left: auto;
right: 5rem;
}
```


Example using start/end:

```
#content {
offset-inline-start: 5rem;
}
```


Once again, the start/end concept has saved us a rule in our CSS file.

*Browser support: Firefox 41+ only.*

**Floats:** `float: left`

and `float: right`

have been around and used for a long time, but very soon you will be able to use `float: inline-start`

and `float: inline-end`

in Firefox Nightly. `inline-start`

will float your element left in an left-to-right (LTR) layout, and right in a right-to-left (RTL) layout.

Example using start/end:

```
#content {
float: left;
}
html[dir="rtl"] #content {
float: right;
}
```


Using start/end:

```
#content {
float: inline-start;
}
```


*Browser support: Firefox 44 (soon to land in Firefox Nightly).*

Firefox OS gives you a great opportunity to try some of the very latest CSS property implementations — there is a reference page on the Mozilla Wiki for all the new [BIDI-relevant CSS properties and values](https://wiki.mozilla.org/Gaia/CSS_Guidelines#Direction_.28RTL.2FLTR_and_BiDi.29).

**Web components:** Web components are reusable user interface widgets ([see MDN for more information](https://developer.mozilla.org/en-US/docs/Web/Web_Components)). If you’ve worked with web components you’ll know that CSS styles defined inside the shadow DOM are scoped, so by default you can’t get the direction of the overall page from the component’s scoped CSS using `html[dir=”rtl”]`

. However, the shadow DOM introduces a new selector called `:host-context()`

, which can be used to select a shadow host element based on a matching parent element.

Let’s make this clearer with an example — say you have an element inside your shadow DOM tree with a class name called *back*. In a normal situation where there isn’t a shadow DOM you would just use `html[dir=”rtl”] .back {}`

, however you can’t use this syntax from inside a web component. Scoped and encapsulated, remember? The equivalent selector when `.back`

is inside a web component scope would look like this:

```
.back:host-context(html[dir="rtl"]) { }
```


The exact browser support status of this syntax is not clear currently, however you can use [this polyfill](https://github.com/webcomponents/webcomponentsjs) to plug holes in support.

Want to use a polyfill for shadow CSS but still want to play around with RTL in web components in browsers that already support it such as Firefox (currently hidden behind the `dom.webcomponents.enabled`

flag) and Google Chrome? You can do this using [Mutation Observers](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver) by observing the `document.documentElement.dir`

property. Code for the observer would look similar to this example:

```
var dirObserver = new MutationObserver(updateShadowDir);
dirObserver.observe(document.documentElement, {
attributeFilter: ['dir'],
attributes: true
});
```


Also don’t forget to initialize your function for the first time once the page loads, right after the observer logic:

`updateShadowDir();`


Your `updateShadowDir()`

function would look something like this:

```
function updateShadowDir() {
var internal = myInnerElement.shadowRoot.firstElementChild;
if (document.documentElement.dir === 'rtl') {
internal.setAttribute('dir', 'rtl');
} else {
internal.removeAttribute('dir');
}
};
```


That’s all you should be doing on the JavaScript side — now, since the first child element of your web component has a changing dir attribute, your CSS will depend on it as a selector instead of the HTML element. Say you are using a span — your selector would look like this:

` span[dir="rtl"] rest-of-the-selectors-chain { … } `


This might look a little hacky, but fortunately the future is brighter, so let’s take a look at what the W3C has in store for us in the future regarding Right-To-Left.

**The future of RTL on the Web**

**Informing the server of text direction:** Currently in text inputs and text areas, when a form is submitted, the direction of the page/form elements is lost. Servers then have to come up with their own logic to estimate the direction of the text that was sent to them.

To solve this problem and be more informative about the text being sent as well as about its direction, W3C has added a new attribute to the HTML5 forms spec called `dirname`

, which browser vendors will be implementing in the future.

As the spec states, including the `dirname`

“on a form control element enables the submission of the directionality of the element, and gives the name of the field that contains this value during form submission. If such an attribute is specified, its value must not be the empty string.”

**Translation:** Adding this attribute to your <input> or <textarea> makes their direction get passed along with the GET or POST string that is sent to the server. Let’s see a real-world example — first, say you have this form:

```
<form action="result.php" method="post">
<input name="comment" type="text" dirname="comment.dir"/>
<button type=submit>Send!</button>
</form>
```


After submitting the form, the POST string sent to the server will include a field called comment, and another called `comment.dir`

. If the user types Hello into the text area and submits it the result string will be:

`comment=Hello&comment.dir=ltr`


But if they type “مرحبا” it will look like this:

`comment=%D9%85%D8%B1%D8%AD%D8%A8%D8%A7&comment.dir=rtl`


Note: In order for Arabic characters to be displayed correctly in URLs in your browser the characters are encoded in UTF-8 and each Arabic letter now uses 4 characters and is separated in the middle with a % sign.

For example, if you have this link: [http://ar.wikipedia.org/wiki/نجيب_محفوظ](https://ar.wikipedia.org/wiki/%D9%86%D8%AC%D9%8A%D8%A8_%D9%85%D8%AD%D9%81%D9%88%D8%B8)

When you visit it, the link in your browser will be transformed to

**Better ways to manage backgrounds and images in RTL:** Tired of using `transform: scaleX(-1)`

to mirror your background images? The W3C is introducing a new CSS keyword called `rtlflip`

, which is used like so:

`background-image: url(backbutton.png) rtlflip;`


This keyword saves you the hassle of manually mirroring your images through the `transform: scaleX(-1)`

property.

It can also be used to style list item markers like this:

`list-style-image:url('sprite.png#xywh=10,30,60,20') rtlflip;`


The [spec page](http://www.w3.org/TR/html-bidi/#image-flip) also states that this keyword can be used along with all of the other possible ways that an image can be specified in CSS3 Images, e.g. `url`

, `sprite`

, `image-list`

, `linear-gradient`

, and `radial-gradient`

.

**Internationalization APIs**

We covered the JavaScript Internationalization APIs before in [an introductory post](https://hacks.mozilla.org/2014/12/introducing-the-javascript-internationalization-api/). Let’s recap the important lesser-known parts relevant in the context of working on right-to-left content.

Internationalization API support covers a wide variety of languages and their derivatives. For example it not only supports Arabic as a language, but also Arabic-Egypt, Arabic-Tunisia, and the whole list of other variations.

**Using Eastern Arabic numerals instead of Western Arabic:** In some Arabic variants, Eastern Arabic numerals (١٢٣) are used instead of the Western Arabic (123). The International APIs allow us to specify when to show ١٢٣ and when to show 123.

`console.log(new Intl.NumberFormat('ar-EG').format(1234567890));`


This states that we want to format 1234567890 to Arabic-Egypt numbers.

Output: ١٬٢٣٤٬٥٦٧٬٨٩٠

`console.log(new Intl.NumberFormat('ar-TN').format(1234567890));`


Here we’re saying we want to output the same number in Arabic Tunisia format; since Tunisia uses Western Arabic, the output is: 1234567890

**Showing dates in the Hijri/Islamic calendar instead of the Gregorian:** During the Ramadan month, Google made [google.com/ramadan](http://google.com/ramadan) to show content related to the occasion. One of the essential pieces of information shown was the day of the month in the Hijri calendar. Google used a polyfill to get this information. With the Internationalization APIs you can extract the same information with one line of JavaScript instead of a whole JavaScript library.

Here’s an example:

`console.log(new Intl.DateTimeFormat("fr-FR-u-ca-islamicc").format(new Date()));`


This line states that we want to format the current date to the Islamic Calendar date and show it in fr-FR numerals (Western Arabic). Output: 16/12/1436

`console.log(new Intl.DateTimeFormat("ar-SA-u-ca-islamicc").format(new Date()));`


This is doing the same thing, but formatted for display in the Arabic-Saudi-Arabia locale which uses Eastern Arabic numerals.

Output: ١٦/١٢/١٤٣٦

**Final words**

In this article, we wrap up our in-depth look at doing RTL on the Web the right way. We hope this has been helpful in encouraging you to get started adding RTL support to your websites/products! If you are a Firefox OS contributor this will be your guide to for adding RTL to [Gaia](https://github.com/mozilla-b2g/gaia/).

As always, let us know in the comments below if you have any questions!

## About Ahmed Nefzaoui

RTL (Right-To-Left) connoisseur. Front-End Web Developer. Firefox OS UI hacker and a Mozilla Technical Speaker.

## One comment

NawfelOctober 8th, 2015 at 15:40