---
title: 'Building RTL-Aware Web Apps & Websites: Part 1 – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2015/09/building-rtl-aware-web-apps-and-websites-part-1/
author: Ahmed Nefzaoui
published: '2015-09-24'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Making the web more accessible to more people, in more languages, is an ongoing effort and a mission we take very seriously at Mozilla.

This post is the first of a series of articles to explain one of the most neglected and least well-known corners of web development: RTL (right-to-left) development. In a web development context it means making your web content compatible with RTL languages like Arabic, Hebrew, Persian, and Urdu, which are all written from right to left.

This area is often neglected by developers because of the lack of teaching resources. In this series, we hope to provide enough information to allow developers to make content that’s accessible to a broader global audience using the RTL capabilities that most web browsers currently provide.

### What actually is RTL?

To make things clear, there is a difference between a language and its script. A script is the text or written form — while the language refers to the spoken form. So technically, right-to-left describing the script in which a language is written, comparable to left-to-right scripts, like English or French, more familiar to many Western readers.

For example, “Marhaban” – which means hello – is a word written in the English script, but has Arabic as its language, while “مرحبا” is both Arabic script and Arabic language.

On the web, as we said earlier, the term Right-To-Left indicates more than just a script for writing. It stands for all facets of developing web apps and websites that do not break or become unreadable when used with Arabic, Urdu or any other RTL script.

Before continuing, let’s just clear up some misconceptions about RTL.

**First, RTL is not about translating text to Arabic:** It means more than translating your website into Arabic and calling it a day. It’s about making every aspect the UI and layout RTL-friendly. And as I always say – and can’t stress it enough – do RTL right or don’t bother! Doing it halfway will lose your audience and credibility.

**Second, RTL is more than just “flip all the things”:** I’m not sure if this issue has been fixed yet or not, but setting your locale to Arabic in Gnome will cause the time to be shown as PM 33:12 instead of 12:33 PM.

Well, that is not how it works. I’m a native Arabic speaker but that doesn’t mean I tell time backwards. There are some exceptions and things to pay attention to about numbers, and we will cover them in this series.

### Why should I care about RTL?

You might have the impression that RTL is hard, scary, and will add a great deal of work to your project! Really, it’s not that difficult. Once you comprehend the basics, the extra effort required is not that great.

You should really care about adding right-to-left support to your web app or website for many, many reasons. There are over 410 million native RTL speakers around the world as of 2010 (That’s a lot of people! Note: The assessment is based on [Wikipedia’s list of all the languages](https://en.wikipedia.org/wiki/List_of_languages_by_number_of_native_speakers).) It’s also millions of potential users and a huge potential market for your app or website. Most companies now add RTL support to their software (e.g. Windows, iOS, Android) and websites, so native RTL speakers expect your website to meet their expectations regarding RTL support. Without this support visitors to your web application may not become repeat users.

In the case of Firefox OS, we only started shipping devices to the Middle East when we had RTL support fully implemented in the system, and thus our partner Orange was able to sell devices with the OS on it. This obviously opens up a whole new market of users to Firefox OS.

### Best practices for RTL

Here are some general rules of thumb to keep in mind when developing RTL-aware websites and web apps:

- Think from the right: In a region with an RTL script and language, books open from the right-hand side. Thus, most UI elements related to readability are going to be mirrored.
- Hardware legacy UI is a thing: In MENA (Middle East and North Africa) and other regions where RTL languages are spoken, people use gadgets too. Audio hardware has the same control layout as anywhere else in the world. So buttons like Play, Fast Forward, Next, Previous have always been the same. And because of that, it’s not a good idea to mirror any of those buttons. Please don’t RTL the media player buttons. Another example of hardware legacy is the physical feature phone keyboard; before there were Blackberries and similar keyboards for handhelds, there was the simple physical numpad — until very recently it was widely popular in MENA countries. For this reason, It is strongly advised to *not* mirror the number keys. A good example of this is Firefox OS. As its initial target was developing countries, we made sure not to make the dialer mirrored in RTL.
Thinking Right-To-Left is not thinking left-handed: Remember not to confuse developing RTL UIs with southpaw-first ones. In RTL regions of the world, right-handed people are a majority, just like in the rest of the world. So anything that is not related to how the user reads the actual content on the page should not be mirrored. An example of this is the Firefox OS A-Z scrollbar (image to the right) in the Contacts App. It is placed on the right because it’s easier to scroll through with the right hand, so such a thing should not go on the other side when your page is in RTL mode.![Firefox OS Contacts App](../../assets/2fd3ee6bd5daaaca.png)


### Down to business: How to RTL content

The first step towards making a web page RTL is adding the code `dir="rtl"`

to the <html> tag:

```
<html dir="rtl">
```


`dir`

stands for direction and setting its value to `rtl`

defaults the horizontal starting point of elements to the right instead of the left.

To target an element with CSS only when the page is RTL:

- Create a copy of any regular CSS rules that target it.
- Add a
`html[dir="rtl"]`

attribute selector onto the front of the selector chain. - Next, whenever you find a property or a value that represents horizontal positioning of some kind in the RTL rule, use its opposite. For example, if you find `float: left` you should change it to
`float: right`

.

As an example, if the original rule is as follows —

```
.someClass {
text-align: left;
padding: 0 10px 0 0;
text-decoration: underline;
}
```


we would paste a copy of it after the original and update it as follows:

```
html[dir="rtl"] .someClass {
text-align: right;
padding: 0 0 0 10px;
}
```


Notice that the `text-decoration: underline;`

declaration has been removed. We don’t need to override it for the RTL version because it doesn’t affect any direction-based layout elements. Thus, the value from the original rule will still be applied.

Here’s an even more detailed example you can hack on directly:

See the Pen [dYGKQZ](http://codepen.io/anefzaoui/pen/dYGKQZ/) by Ahmed Nefzaoui ([@anefzaoui](http://codepen.io/anefzaoui)) on [CodePen](http://codepen.io).

Of course, real-life cases won’t be quite as simple as this. There are applications with a huge number of CSS rules and selectors, and there are multiple strategies you could adopt. Here is one recommended approach:

**Copy and clean up:**First, copy the content of your stylesheet to another file, add`html[dir="rtl"]`

to all the rules, then clear out any properties that do not relate to horizontal direction setting. You should end up with a more lightweight file that deals purely with RTL.

**Mirror the styles:**Change all of the properties left in the new file to their opposites: e.g.`padding-left`

becomes`padding-right`

,`float: right`

becomes`float: left`

, etc. Note: if you originally had`padding-left`

and you changed it to`padding-right`

, remember that the original`padding-left`

still exists in the original rule. You*must*add`padding-left: unset`

alongside`padding-right`

, otherwise the browser will compute both properties: the`padding-left`

from the original CSS rule and the new`padding-right`

in the RTL rule. The same is true for any property that has multiple direction variants like the`margin-left`

|`right`

,`border-left`

|`right`

…**Paste back:**After you’ve completed the previous steps, paste the newly created rules back into the original file, after the originals. I personally like to add a little comment afterwards such as:`/* **** RTL Content **** */`

for the sake of easier differentiation between the two parts of your style file.

### A better way: isolating left/right styles completely

Sometimes you will find yourself facing edge cases that produce code conflict. This involves properties inheriting values from other properties, meaning that sometimes you won’t be sure what to override and what not to. Maybe you’ve added the `margin-right`

to the RTL rule but are not sure what to set as the value for the original `margin-left`

? In all real-world cases it is advisable to adopt another approach, which is better in general but more long-winded. For this approach we isolate direction-based properties completely from the rules for both the LTR and the RTL cases. Here’s an example: say we have `.wrapper .boxContainer .fancyBox`

listed like this:

```
.wrapper .boxContainer .fancyBox {
text-align: left;
padding-left: 10px;
text-decoration: underline;
color: #4A8CF7;
}
```


Instead of adding another property for RTL with both `padding-left`

and `padding-right`

, you can do this:

```
.wrapper .boxContainer .fancyBox {
text-decoration: underline;
color: #4A8CF7;
}
html[dir="ltr"] .wrapper .boxContainer .fancyBox {
text-align: left;
padding-left: 10px;
}
html[dir="rtl"] .wrapper .boxContainer .fancyBox {
text-align: right;
padding-right: 10px;
}
```


This solution consists of 3 parts:

- The original rule/selector with
*only*non-direction based properties, because they are shared by the LTR and the RTL layout. - The left to right case —
`html[dir="ltr"]`

— with*only*the direction-based CSS properties included, their values set to match your LTR layout. - The right to left case —
`html[dir="rtl"]`

— with the same properties as the LTR case, only with their values set according to what you want in your RTL layout.

Notice that in the second rule we had `padding-left`

only and in the third one we had `padding-right`

only. That’s because each one of them is exclusive to the direction that was given to them in the `dir`

attribute. This is a nice, clean approach that doesn’t require unsetting of properties. This is the exact approach we use when adding RTL support to Firefox OS. (Note: the `unset`

keyword [isn’t supported in all browsers](http://caniuse.com/#search=unset). For the best compatibility you may need to explicitly re-declare the desired value for any properties you want to unset.)

### How do we get and set the direction of the page using JavaScript?

It’s fairly easy, and requires only one line of code: `document.documentElement.dir`


You can assign this line to a variable, and have it outputted to the console to see for yourself:

`var direction = document.documentElement.dir; console.log(direction);`


Or try this example:

See the Pen [WQxWQQ](http://codepen.io/anefzaoui/pen/WQxWQQ/) by Ahmed Nefzaoui ([@anefzaoui](http://codepen.io/anefzaoui)) on [CodePen](http://codepen.io).

To set the direction of the page, just use the following:

`document.documentElement.dir = "rtl"`


And here’s an example of both getting and setting the direction value for a web page:

See the Pen [gaMyPN](http://codepen.io/anefzaoui/pen/gaMyPN/) by Ahmed Nefzaoui ([@anefzaoui](http://codepen.io/anefzaoui)) on [CodePen](http://codepen.io).

### Automatic RTL solutions

Enough talk about manual ways to do RTL. Now let’s take a look at some automated approaches.

#### css-flip

Twitter has developed a solution to automate the whole process and make it easier for bigger projects to implement RTL. They have open sourced it and you can find it [on Github](https://github.com/twitter/css-flip).

This NPM plugin covers pretty much all the cases you could find yourself facing when working on RTL, including edge cases. Some of its features include:

- no-flip: To indicate to the mirroring engine that you don’t want a certain property flipped, just add
`/* @noflip*/`

at the beginning of the property. So, for example, if you write`/* @noflip*/ float: left`

, it will stay as`float: left`

after css-flip is run. - @replace: When you have background images that differ between LTR and RTL, you can specify a replacement image by including
`/*@replace: url(my/image/path)`

before the original property. Let’s say you have`background-image: url(arrow-left.png)`

. If you update the line to

`/*@replace: url(arrow-rightish.png) */ background-image: url(arrow-left.png);`


You will end up with`background-image: url(arrow-rightish.png);`

in the RTL layout.

You can use css-flip through the command line by executing

`css-flip path/to/file.css > path/to/file.rtl.css`

or by requiring css-flip in your page. More about that on their [github repo](https://github.com/twitter/css-flip). css-flip is being actively used on Twitter properties.

#### rtlcss

Another option for automatic conversion is a tool from Mohammad Younes called rtlcss — this is also available on [github](https://github.com/MohammadYounes/rtlcss) and provides some pretty nifty features. With this one engine you can:

- Rename rule names (e.g. renaming
`#boxLeft`

to`#boxRightSide`

). - Completely ignore rules from the mirroring process.
- Ignore single properties.
- Append/prepend new values.
- Insert new property values in between other property values.

Basic usage is via the command line — you can create your RTL CSS equivalent by the running the following in the same directory your original CSS is available in:

`rtlcss input.css output.rtl.css`


And of course you can just require it in your page. More details are available on [github](https://github.com/MohammadYounes/rtlcss).

This project is very popular and is being used by several projects including WordPress.

### Final words

While there is still a lot to cover, this article aims to provide you with enough knowledge to start exploring RTL confidently. In the next article we’ll cover more advanced topics around RTL.

Be sure to ask any questions you may have around RTL in the comments section and we will try to answer them here or in the next post!

## About Ahmed Nefzaoui

RTL (Right-To-Left) connoisseur. Front-End Web Developer. Firefox OS UI hacker and a Mozilla Technical Speaker.

## 10 comments

Pavel IvanovSeptember 24th, 2015 at 13:37Gabriel MičkoSeptember 25th, 2015 at 00:37SteveSeptember 25th, 2015 at 02:05Ahmed NefzaouiSeptember 25th, 2015 at 11:21Steve LeeSeptember 25th, 2015 at 11:34Ahmed NefzaouiSeptember 25th, 2015 at 11:55Patrick BrossetSeptember 25th, 2015 at 07:00Ahmed NefzaouiSeptember 25th, 2015 at 11:27SteveLeeSeptember 25th, 2015 at 11:40Francis KimSeptember 27th, 2015 at 01:46