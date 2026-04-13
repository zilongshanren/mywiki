---
title: CSS coding techniques – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2016/05/css-coding-techniques/
author: Belén Albeza
published: '2016-05-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Lately, we have seen a lot of people struggling with CSS, from beginners to seasoned developers. Some of them don’t like the way it works, and wonder if replacing CSS with a different language would be better—CSS processors emerged from this thinking. Some use CSS frameworks in the hopes that they will have to write less code (we have seen [in a previous article](https://hacks.mozilla.org/2016/04/you-might-not-need-a-css-framework/) why this is usually not the case). Some are starting to ditch CSS altogether and use JavaScript to apply styles.

But you don’t always need to include a CSS processor in your work pipeline. You don’t need to include a bloated framework as the default starting point for any project. And using JavaScript to do the things CSS is meant for is just a terrible idea.

In this article we will see some tips and recommendation to write better, **easier-to-maintain CSS** code, so your stylesheets are shorter and have fewer rules. CSS can feel like a handy tool instead of a burden.

## The “minimum viable selector”

CSS is a declarative language, in which you specify rules that will style elements in the DOM. In this language, **some rules take precedence** over others in the order they are applied, like inline styles overriding some previous rules.

For instance, if we have this HTML and CSS code:

`<button class="button-warning">`


```
.button-warning {
background: red;
}
button, input[type=submit] {
background: gray;
}
```


Despite `.button-warning`

being defined before the `button, input[type=submit]`

rule, it will override the latter `background`

property. Why? What is the criteria to decide which rule will override the styles of another one?

**Specificity**.

Some selectors are considered to be more specific than others: for instance an `#id`

selector will override a `.class`

selector.

What happens if we use a selector that is more specific than it really needs to be? If we later want to override those styles, we need an even more specific selector. And if we later need to override this more specific selector, we will need… yes, it’s a snowball growing larger and larger and will eventually become very difficult to maintain.

So, whenever you are writing your selectors, ask yourself: **is this the least specific selector that can do the job here?**

All of the specificity rules are officially [defined in the W3C CSS Selectors specification](https://www.w3.org/TR/selectors/#specificity), which is *the* way to find out every single detail about CSS Selectors. For something easier to understand, read [this article on CSS specificity](https://www.smashingmagazine.com/2007/07/css-specificity-things-you-should-know/).

## Don’t throw new rules at bugs

Let’s imagine this typical situation: there is a bug in your CSS and you locate which DOM element has the wrong style. And you realise it’s somehow inheriting a property that it shouldn’t have.

*Don’t just throw more CSS at it. *If you do, your code base will grow a bit larger, and locating future bugs will be a bit harder.

Instead, stop, step back, and use the developer tools in your browser to inspect the element and see the whole cascade. Identify exactly which rule is applying the style you don’t want. And modify that existing rule so that it doesn’t have the unintended consequence.

In Firefox you can debug the cascade by right-clicking on a element in a page and selecting `Inspect element`

.

![image00](../../assets/a63014c536dac2a6.png)


Look at that cascade in all its glory. Here you can see all the rules applied to an element, in the order in which they are applied. The top entries are the ones with more specificity and can override previous styles. You can see that some rules have some properties struck out: that means that a more specific rule is overriding that property.

And you can not only see the rules, but you can actually switch them on and off, or change them on the fly and observe the results. It’s very useful for bug fixing!

The needed fix may be a rule change or it may be a rule change at a different point in the cascade. The fix may require a new rule. At least you will know it was the right call and something that your code base needed.

This is also a good time to look for **refactoring opportunities**. Although CSS is not a programming language, *it is source code *and you should give it the same consideration that you give to your JavaScript or Python: it should be clean, readable and be refactored when needed.

## Don’t !important things

This is implied in the previous recommendations, but since it’s crucial I want to stress it: **Don’t use !important in your code**.

`!important`

is a feature in CSS that allows you to break the cascade. CSS stands for “Cascading Style Sheets,” this is a hint.

`!important`

is often used when you are rushing to fix a bug and you don’t have the time or the will to fix your cascade. It is also used a lot when you are including [a CSS framework with very specific rules](https://hacks.mozilla.org/2016/04/you-might-not-need-a-css-framework/) and it’s just too hard to override them.

When you add `!important`

to a property, the browser will ignore other rules with higher specificity. You know you are really in trouble when you `!important`

a rule to override another rule that was marked as `!important`

as well.

There is one legitimate use of `!important`

—and it’s while using the developer tools to debug something. Sometimes you need to find which values for a property will fix your bug. Using `!important`

in the developer tools and modifying a CSS rule on the fly lets you find these values while you ignore the cascade.

Once you know which bits of CSS will work, you can go back to your code, and look at which point of the cascade you want to include those bits of CSS.

## There’s life beyond `px`

and `%`


Working with `px`

(pixels) and `%`

(percentages) units is quite intuitive, so we will focus here on less-known or less intuitive units.

`Em`

and `rem`


The most well-known relative unit is em. 1em is equivalent to the font size of that element.

Let’s imagine the following HTML bit:

```
<article>
<h1>Title</h1>
<p>One Ring to bring them all and in the darkness bind the.</p>
</article>
```


And a stylesheet with just this rule:

```
article {
font-size: 1.25em;
}
```


Most browsers apply a base font size of 16 pixels to the root element by default (by the way, this is overridable—and a nice accessibility feature—by the user). So the paragraph text of that article element will probably get rendered with a `font-size`

of 20 pixels (`16 * 1.25`

).

What about the `h1`

? To understand better what will happen, let’s add this other CSS rule to the stylesheet:

```
h1 {
font-size: 1.25em;
}
```


Even though it’s also `1.25em`

, the same as `article`

, we have to take into account that `em`

units compound. Meaning, that an `h1`

being a direct child of a body, for instance, would have a `font-size`

of 20 pixels (16 * 1.25). However, our `h1`

is inside an element that has a `font-size`

that is different than the root (our `article`

). In this case, the `1.25`

refers to the `font-size`

we are given by the cascade, so the `h1`

will be rendered with a `font-size`

of 25 pixels (16 * 1.25 * 1.25).

By the way, instead of doing all of these multiplication chains in your head, you can just use the `Computed`

tab in the `Inspector`

, which displays the actual, final value in pixels:

![image01](../../assets/ad8639929b1f6191.png)


`em`

units are really versatile and make it really easy to change—even dynamically—all the sizes of a page (not just `font-size`

, but other properties like `line-height`

, or `width`

).

If you like the “relative to base size” part of `em`

but don’t like the compounding part, you can use ** rem units**.

`rem`

units are like `em`

‘s that **ignore compounding**and just take the root element size.

So if we take our previous CSS and change `em`

units for `rem`

in the `h1`

:

```
article { font-size: 1.25em; }
h1 { font-size: 1.25rem; }
```


All h1 elements would have a computed `font-size`

of 20 pixels (assuming a `16px`

base size), regardless of them being inside an article or not.

### vw and vh

`vw`

and `vh`

are viewport units.`1vw`

is 1% of the viewport width, whereas `1vh`

is 1% of the viewport height.

They’re incredibly useful if you need a UI element that needs to occupy the whole screen (like the typical semi-transparent dark background of a modal), which is not always related to the actual body size.

### Other units

There are other units that might be not as common or versatile, but you will inevitably stumble upon them. You can learn more about them [at the MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/length).

## Use flexbox

We have talked about this in a [previous article about CSS frameworks](https://hacks.mozilla.org/2016/04/you-might-not-need-a-css-framework/), but the flexbox module simplifies the task of crafting layouts and/or aligning things. If you are new to flexbox, check out [this introductory guide](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Flexible_Box_Layout/Using_CSS_flexible_boxes).

And *yes*, you can use flexbox *today*. Unless you really need to support ancient browsers for business reasons. The current [support for flexbox in browsers is above 94%](http://caniuse.com/#search=flexbox). So you can stop writing all of those floating `div`

‘s which are hard to debug and maintain.

Also, keep an eye open for the upcoming [Grid module](https://hacks.mozilla.org/2015/09/the-future-of-layout-with-css-grid-layouts/), which will make implementing layouts a breeze.

## When using a CSS processor…

CSS compilers like Sass or Less are very popular in the front-end development world. They are powerful tools, and—when put in good use—can allow us to work more efficiently with CSS.

### Don’t abuse selector nesting

A common feature in these processors or “compilers” is selector nesting. So, for instance, this Less code:

```
a {
text-decoration: none;
color: blue;
&.important {
font-weight: bold;
}
}
```


Would get translated to the following CSS rules:

```
a {
text-decoration: none;
color: blue;
}
a.important {
font-weight: bold;
}
```


This feature allows us to write less code and to group rules that affect elements which are usually together in the DOM tree. This is handy for debugging.

However, it is also common to abuse this feature and end up replicating the whole DOM in the CSS selectors. So, if we have the following HTML:

```
<article class="post">
<header>
<!-- … -->
<p>Tags: <a href="..." class="tag">irrelevant</a></p>
</header>
<!-- … -->
</article>
```


We might find this in the CSS stylesheet:

```
article.post {
// ... other styling here
header {
// ...
p {
// ...
a.tag {
background: #ff0;
}
}
}
}
```


The main drawback is that these CSS rules have **extremely specific selectors**. We have already seen that this is something we should avoid. There are other disadvantages as well to over-nesting, which I have talked about [in another article](http://belenalbeza.com/the-dangers-of-nesting-abuse-in-css-compilers/).

In short: **do not let nesting generate CSS rules you wouldn’t type yourself.**

### Include vs extend

Another useful feature of CSS processors is **mixins**, which are re-usable chunks of CSS. For instance, let’s say that we want to style buttons, and most of them have some basic CSS properties. We could create a mixin like this one in Less:

```
.button-base() {
padding: 1em;
border: 0;
}
```


And then create a rule like this:

```
.button-primary {
.button-base();
background: blue;
}
```


This would generate the following CSS:

```
.button-primary {
padding: 1em;
border: 0;
background: blue;
}
```


As you can see, very handy to refactor common code!

Besides “including” a mixin, there is also the option of “**extending**” or “inheriting” it (the exact terminology differs from tool to tool). What this does is to combine multiple selectors in the same rule.

Let’s see an example using the previous `.button-base`

mixin:

```
.button-primary {
&:extend(.button-base)
background: blue;
}
.button-danger {
&:extend(.button-base)
background: red;
}
```


That would be translated to:

```
.button-primary, .button-danger {
padding: 1em;
border: 0;
}
.button-primary { background: blue; }
.button-danger { background: red; }
```


Some articles online tell us to only use “include”, whereas some tell us to only use “extend”. The fact is that they produce *different* CSS, **none of them is inherently wrong**, and depending on your actual scenario it would be better to use one or the other.

How to choose between them? Again, the “would I write this by hand?” rule of thumb applies.

I hope this can help you to reflect on your CSS code and write better rules. Remember what we said before: CSS *is* code, and as such, worthy of the same level of attention and care as the rest of your code base. If you give it some love, you will reap the rewards.

## About
[
Belén Albeza ](http://www.belenalbeza.com)

Belén is an engineer and game developer working at Mozilla Developer Relations. She cares about web standards, high-quality code, accesibility and game development.

## 25 comments

awalMay 18th, 2016 at 10:05Belén AlbezaMay 19th, 2016 at 02:02JonMay 20th, 2016 at 05:24awalMay 21st, 2016 at 08:32AnonJune 7th, 2016 at 06:20SamJune 9th, 2016 at 08:58NilsMay 19th, 2016 at 06:20KonstantinJune 6th, 2016 at 02:06PeterJune 8th, 2016 at 03:10Gerd NeumannMay 20th, 2016 at 01:33Belén AlbezaMay 20th, 2016 at 06:21Gerd NeumannMay 20th, 2016 at 06:37Janne ClarsonMay 23rd, 2016 at 04:22Ryan JohnsonMay 20th, 2016 at 11:45Gerd NeumannMay 20th, 2016 at 01:51George StephanisMay 20th, 2016 at 02:53peterMay 20th, 2016 at 08:50JensMay 21st, 2016 at 01:57Greg BellMay 25th, 2016 at 04:29JohntrepreneurMay 20th, 2016 at 13:08Jaydev GajeraMay 22nd, 2016 at 22:10Alex WalgreenMay 24th, 2016 at 05:55Adrian Bettridge-WieseMay 24th, 2016 at 10:18AlanMay 28th, 2016 at 08:29feibinyangMay 26th, 2016 at 20:22