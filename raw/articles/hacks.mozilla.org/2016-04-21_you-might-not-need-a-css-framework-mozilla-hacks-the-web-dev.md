---
title: You might not need a CSS framework – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/04/you-might-not-need-a-css-framework/
author: Belén Albeza
published: '2016-04-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

CSS frameworks have been around for a while and they have gotten extremely popular in the front-end development scene. **These frameworks provide snippets of code** you can just copy and paste in your website to craft the whole layout and UI.

You have already probably read a lot of articles about how they might be good for your projects, but here I would like to do the opposite: to **highlight some of the drawbacks** they might bring to your websites or applications, and how you can avoid or mitigate them.

When I ask people why they are using a particular framework, their answer usually falls into one (or more) of these categories:

**Speed:**Most people**believe it will make development faster**. And this*may*be true in the initial stages of a project. But this gain may be followed at the expense of technical debt – we will see how the debt is produced – that will need to be paid later on, with interest.**Best practice:**Some people**believe it is a best practice**to use a framework, especially those just beginning front-end development. This is reinforced by the avalanche of articles and by the inclusion of frameworks in bootcamp curriculums or in job descriptions that mention them.**Design:**A lot of developers just want to release something and they don’t have a designer available for their project. CSS**frameworks provide a basic design**developers can use. While this is useful, the consequence is that your site or app ends up looking like every other recent site on the Internet –but whether that impacts your project is up to you to decide.

## Technical debt

Regardless of the reasons for using a framework, **frameworks might introduce technical debt** in your project. Sometimes it can make sense to have this technical debt, for instance if you need to launch something as soon as possible or if you’re building a prototype whose code will be discarded later.

However, for big projects like an ongoing website or application, this technical debt can potentially become unmanageable and hinder development. Let’s see why this happens.

### Unsemantic HTML code

This is not a problem of frameworks per se, but I have seen it happen a lot in the most popular ones.

For instance, maybe you’re reading documentation for styling buttons: You might find a code snippet that tells you to use a CSS class for *disabled* buttons instead of adding the `disabled`

attribute to the `<button>`

tag itself.

There are abundant examples of `<div>`

or `<span>`

where a more semantic tag would be appropriate. And let’s not talk about the `<div>`

inside a `<div>`

, inside a `<div>`

…

### Over-specific CSS selectors

Again, this is not a problem intrinsic to frameworks, but something we can observe in the most popular ones: there is a tendency to use very specific selectors to create the CSS rules. For instance:

```
.table-responsive > .table-bordered > thead > tr > th:first-child
```


What happens if you need to override some of the properties of your `<th>`

? Then you need to create an even more specific selector! You can’t just get away with creating a generic rule like:

```
th.important-heading { color: #000; }
```


Instead you would need to set up a rule like this:

```
.table-responsive > .table-bordered > thead > tr > th:first-child.important-heading {
color: #000;
}
```


What happens in the wild is that nobody wants to write that kind of code. We soon start to see these kind of rules popping up:

```
th.important-heading { color: #000; !important }
```


…which only makes the problem *worse*!

### Rules you don’t need

If you include a whole framework instead of just the bits you really *need* you will have **CSS rules you are not actually using**.

Of course you can mitigate this with the aid of a post-processing tool to remove unused rules, but the moment you begin to add or remove classes dynamically with JavaScript, you’ll never be 100% sure that you will not need that code.

Unused CSS not only makes your files bigger, which can be a problem for mobile devices that are connected to a cellular network rather than wi-fi, but they make your codebase larger too, and thus harder to maintain.

### Owning your opinions and decisions

All frameworks are opinionated. This is not an issue if you don’t have a strong opinion or if yours is the same as the frameworks.

But sometimes you do have strong opinions. For instance, here’s the HTML one framework proposes to create some coloured text labels:

```
<span class=“label label-warning”>Out of stock</span>
```


I find these classes redundant, since I like to use only the classes I deem necessary. If that were my code, I would probably only have a class `label-warning`

.

And what if you are a fan of a specific CSS methodology (like “Block, Element, Modifier”) your framework doesn’t use?

## Alternatives to frameworks

**Write your own HTML and CSS.** If you don’t like the markup a framework produces, you should write your own. If the CSS rules a framework provides makes you work inefficiently, you should craft your own rules.

**If you need a grid**, you can use Flexbox today, which makes crafting a layout much less painful than using floating divs. If you are not familiar with Flexbox, take a look at this [MDN guide](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Using_CSS_flexible_boxes). If you are curious about how the code might look, here’s an [implementation of the Holy Grail layout](https://jsfiddle.net/n7nk0hac/1/) I did using Flexbox.

In the future we will have [Grid](https://hacks.mozilla.org/2015/09/the-future-of-layout-with-css-grid-layouts/)! This will make creating layouts a breeze, and you won’t feel the urge to use an existing grid framework ever again. Here’s [another implementation of the Holy Grail layout](https://jsfiddle.net/6hfw1z23/), this time using Grid.

(Note: To see the actual result [running in your browser](http://gridbyexample.com/browsers/), try [Firefox Nightly](https://nightly.mozilla.org/) or the latest [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) browser —it just works. To view these examples in any other Firefox release, you’ll need to *flip the flag*. Go to `about:config`

in the browser to enable `layout.css.grid.enabled`

functionality.)

**If you just need a UI widget**, like a custom dropdown menu, and you don’t want to code it from scratch, you can always grab that bit—instead of the whole framework—or use a 3rd-party component that has no external dependencies.

**If you need a design** you can use, one reasonable way to use these frameworks would be to grab the [Sass](http://sass-lang.com/) or [Less](http://lesscss.org/) sources instead of the generated CSS files. If you do this, you can grab the mixins and create your own selectors, which will allow you to have your own markup. But keep in mind that your site will look exactly like loads of other sites as well!

If you need **a way to standardise the UI creation** in your project, so people know which code to use and how to add new interface elements, what you are looking for is [a style guide](https://24ways.org/2011/front-end-style-guides/) (in short, your very own custom framework). You should have one for big projects!

## In summary

CSS frameworks may have advantages, but they also have drawbacks that are often overlooked. Be aware of those and also know the tools and APIs you have at your disposal for creating the CSS and markup of your sites and apps.


## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.

## 32 comments

Brandon ZellApril 21st, 2016 at 12:07Belén AlbezaApril 21st, 2016 at 12:17Brandon ZellApril 21st, 2016 at 13:12Philippe LhosteApril 22nd, 2016 at 04:09Alex MandlApril 23rd, 2016 at 06:21ChrisApril 22nd, 2016 at 12:23JAson WittApril 23rd, 2016 at 07:04changkeApril 23rd, 2016 at 13:36John BilickiApril 21st, 2016 at 14:59Dave WoodallApril 27th, 2016 at 13:41Jesús PeralesApril 21st, 2016 at 17:09Jason KnightApril 21st, 2016 at 18:19DavidApril 30th, 2016 at 22:56StefanApril 22nd, 2016 at 00:51Álvaro GonzálezApril 22nd, 2016 at 02:20Jason KnightApril 22nd, 2016 at 16:25JulienApril 27th, 2016 at 11:35NigeApril 29th, 2016 at 08:04Thierry KoblentzApril 23rd, 2016 at 09:13Benjamin Gandhi-ShepardApril 24th, 2016 at 10:32David MurcofApril 25th, 2016 at 02:39Nico BurnsApril 25th, 2016 at 02:53GaryApril 25th, 2016 at 03:00DaneApril 26th, 2016 at 09:16Phil MApril 26th, 2016 at 15:39JulienApril 27th, 2016 at 11:39Barbara SykesApril 26th, 2016 at 23:28JAson WittApril 27th, 2016 at 09:17Álvaro GonzálezApril 28th, 2016 at 01:45SPApril 28th, 2016 at 07:32RajApril 29th, 2016 at 14:52Matthew TROWMay 4th, 2016 at 02:00