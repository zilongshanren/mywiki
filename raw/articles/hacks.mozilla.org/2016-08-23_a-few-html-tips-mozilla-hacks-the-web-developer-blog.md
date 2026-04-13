---
title: A few HTML tips – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/08/a-few-html-tips/
author: Belén Albeza
published: '2016-08-23'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A while ago I wrote an article with [some CSS tips](https://hacks.mozilla.org/2016/05/css-coding-techniques/), now it’s time to give some polish to our HTML! In this article I’ll share some tips and advice about HTML code. Some of this guidance will be best suited for beginners – how to properly build paragraphs, use headings, or improve forms, but we will also discuss SVG sprites for icons, a somewhat more advanced topic.

## Text

### Paragraphs

Most of our writing is structured in paragraphs, and there is an HTML element for that: `<p>`

. **Do not use the line break tag**

`<br>`

to separate blocks of texts into pseudo-paragraphs, since line breaks are not meant for that.**Avoid:**

```
Cupcake ipsum dolor sit. Amet chupa chups chupa chups sesame snaps. Ice cream pie jelly
beans muffin donut marzipan oat cake.
<br>
Gummi bears tart cotton candy icing. Muffin bear claw carrot cake jelly jujubes pudding
chocolate cake cheesecake toffee.
```


**Recommended:**

```
<p>Cupcake ipsum dolor sit. Amet chupa chups chupa chups sesame snaps. Ice cream
pie jelly beans muffin donut marzipan oat cake.</p>
<p>Gummi bears tart cotton candy icing. Muffin bear claw carrot cake jelly jujubes
pudding chocolate cake cheesecake toffee.</p>
```


A legit use for line breaks would be, for instance, to break verses of a poem or song:

```
<p>So close, no matter how far<br>
Couldn’t be much more from the hearth<br>
Forever trusting who we are<br>
And nothing else matters</p>
```


### Headings

Headings tags, from `<h1>`

to `<h6>`

, have an implicit rank assigned to them, from `1`

(most important) to `6`

(less important).

[To handle semantics properly,](https://www.w3.org/TR/html5/sections.html#headings-and-sections) **pick your heading rank in sequential order**, not just because of the size that the browser will use to render the heading. You can – and should!– use CSS for this, and pick a suitable rank instead.

**Avoid:**

```
<article>
<h1>Monkey Island</h1>
<h4>Look behind you! A three-headed monkey!</h4>
<!-- ... -->
</article>
```


**Recommended:**

```
<article>
<h1>Monkey Island</h1>
<h2>Look behind you! A three-headed monkey!</h2>
<!-- ... -->
</article>
```


Another thing to take into account is how to **create subheadings or tag lines** to accompany headings. [The W3C recommendation](https://www.w3.org/TR/html5/common-idioms.html#common-idioms) is to use regular text markup rather than a lower-rank heading.

**Avoid:**

```
<header>
<h1>Star Wars VII</h1>
<h2>The Force Awakens</h2>
</header>
```


**Recommended:**

```
<header>
<h1>Star Wars VII</h1>
<p>The Force Awakens</p>
</header>
```


## Forms

### Placeholders

The placeholder attribute in `<input>`

form elements will let you show an example value to the user that is automatically erased once the user types anything in the field. Placeholders are meant to show examples of **formatting** valid for a field.

Unfortunately, in the wild there are a lot of placeholders acting as `<label>`

elements, informing of what the field *is* instead of serving as an example of a valid input value. This practice is not [accessible](https://developer.mozilla.org/en-US/docs/Web/Accessibility), and you should avoid it.

**Avoid:**

```
<input type="email" placeholder="Your e-mail" name="mail">
```


**Recommended:**

```
<label>
Your e-mail:
<input type="email" placeholder="darth.vader@empire.gov" name="mail">
</label>
```


### Keyboards in mobile devices

It is crucial to **provide typing hints** for people browsing from a mobile device, like a phone or a tablet. We can easily achieve this by picking the [correct type](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#Attributes) for our `<input>`

elements.

For instance, `type="number"`

will make a mobile phone display the numeric keypad instead of the regular alphanumeric keyboard. The same goes for `type="email"`

, `type="tel"`

, etc.

**Avoid:**

```
<label>Phone number: <input type="text" name="mobile"></label>
```


**Recommended:**

```
<label>Phone number: <input type="tel" name="mobile"></label>
```


Here is a comparison: on the left, the keyboard that shows up when using `type="text"`

; on the right, the keyboard for `type="tel"`

.

![keyboard comparison](../../assets/46ae2d6ec7e2aac2.png)


## Images

Say hi to **SVG files**! Not only can you use vector graphics in `<img>`

tags like this:

```
<img src="acolyte_cartoon.svg" alt="acolyte">
```


You can also use **SVG sprites to implement vector icons** in your website, instead of using a Web Font – which is a hack, and might not yield perfect results. This is because browsers treat Web Font icons as text, and not as images. And there are other potential problems, like content/ad blockers disabling the download of Web Fonts. If you would like to learn more about this, watch [this talk by Sarah Semark](http://wordpress.tv/2016/05/28/sarah-semark-stop-using-icon-fonts-love-svg/) about why using SVG for icons is better than using a Web Font. You can also read more about this technique on [CSS-Tricks](https://css-tricks.com/svg-sprites-use-better-icon-fonts/).

The idea of SVG sprites is very similar to [CSS sprites](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Images/Implementing_image_sprites_in_CSS). The implementation consists of merging all your SVG assets in a single image file. In the case of SVG, every asset is wrapped in a `<symbol>`

tag, like this:

```
<svg>
<symbol id="social-twitter" viewBox="...">
<!-- actual image data here -->
</symbol>
</svg>
```


Then, the icon can be used in your HTML with a `<svg>`

tag like this, so we point to the symbol ID in the SVG file:

```
<svg class="social-icon">
<use xlink:href="icons.svg#social-twitter" />
</svg>
```


Does creating an SVG spritesheet seem tedious? Well, that’s why there are tools like [gulp-svgstore](https://github.com/w0rm/gulp-svgstore) to automate the process and generate a spritesheet from your individual asset files.

And remember, since we are using a `<svg>`

tag instead of an `<img>`

to include the picture, we can then use CSS to apply styles. So all the cool things you can do with Web Font icons, can be done with these SVG icons as well!

```
.social-icon {
fill: #000;
transition: all 0.2s;
}
.social-icon:hover {
fill: #00f;
}
```


There are some CSS limitations though: when using SVG this way, with `<use>`

linking to a `<symbol>`

, the image gets injected in [Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Shadow_DOM) and we lose some CSS capabilities. In this case, we can’t cherry-pick which elements of the SVG to apply the styling to, and some properties (e.g., fill) will only be applied to those elements that have them undefined. But hey, you can’t do this with Web Font icons either!

In the demo below, you can see an example of a SVG sprite in action. When you mouse over the image, the torch’s fire will change its color via CSS.

See the Pen [SVG acolyte demo](http://codepen.io/ladybenko/pen/OXBQZq/) by ladybenko ([@ladybenko](http://codepen.io/ladybenko)) on [CodePen](http://codepen.io).

I hope that these tips are helpful. If you have any questions, or would like to share your own tip, please leave a comment!

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.

## 36 comments

Gerd NeumannAugust 24th, 2016 at 01:54Belén AlbezaAugust 24th, 2016 at 02:13Pablo CarballedaAugust 24th, 2016 at 03:15Mike SwansonAugust 24th, 2016 at 05:05Derek johnstonAugust 24th, 2016 at 06:05FrancuteAugust 24th, 2016 at 06:49Belén AlbezaAugust 24th, 2016 at 07:02FrancuteAugust 24th, 2016 at 07:57Christian WilkieAugust 24th, 2016 at 10:47ArjunAugust 24th, 2016 at 07:20Belén AlbezaAugust 25th, 2016 at 01:54CornelisAugust 24th, 2016 at 08:01Havi Hoffman [Editor]August 24th, 2016 at 16:02SalvaAugust 24th, 2016 at 09:02Jens AndersenAugust 25th, 2016 at 15:07Belén AlbezaAugust 26th, 2016 at 01:42Jens AndersenAugust 26th, 2016 at 02:12Belén AlbezaAugust 26th, 2016 at 02:33Adrian RoselliAugust 26th, 2016 at 07:36Belén AlbezaAugust 26th, 2016 at 08:16sunAugust 24th, 2016 at 11:29Belén AlbezaAugust 25th, 2016 at 01:34sunAugust 26th, 2016 at 02:58vogonsPoetryAugust 24th, 2016 at 11:41MichałAugust 24th, 2016 at 13:01Belén AlbezaAugust 25th, 2016 at 01:26SaaAugust 24th, 2016 at 13:25Yousef ShanawanyAugust 24th, 2016 at 15:45ChristianAugust 24th, 2016 at 20:54Belén AlbezaAugust 25th, 2016 at 01:44DavidAugust 24th, 2016 at 22:54LukeAugust 25th, 2016 at 22:08Chris HillsAugust 25th, 2016 at 23:37Belén AlbezaAugust 26th, 2016 at 02:02Wim MostmansAugust 26th, 2016 at 00:54jotarunSeptember 5th, 2016 at 23:18