---
title: Replace Bootstrap Layouts with CSS Grid – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2017/04/replace-bootstrap-layouts-with-css-grid/
author: Dan Brown
published: '2017-04-13'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

In March, [Mozilla released Firefox 52](https://hacks.mozilla.org/2017/03/firefox-52-introducing-web-assembly-css-grid-and-the-grid-inspector/), which added support for CSS Grid Layout. If you aren’t familiar with CSS Grid, it is a two-dimensional layout system for the web that allows us to create layout patterns natively in the browser. This means we can easily recreate familiar grids using just a few lines of CSS. It also means we can do a whole lot with CSS and layouts that wasn’t possible before… but more on that in a bit.

A quick note: This post isn’t meant to be a comprehensive primer for CSS Grid, and assumes a basic familiarity with CSS Grid. If you haven’t already, I’d recommend checking out the fantastic [CSS Grid Layout page](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout) on MDN.

Layouts on the web have always been tricky. When the web was first introduced, there was no method for layouts. Then came tables (in tables, in tables, in tables). It was hackish and weird, but it worked. When CSS was introduced in the late 90s, developers were able to start using divs and floats for their designs and layouts. This eventually led to frameworks and grid systems that helped make sense of all of the “gotchas” like clearing floats, negative margins, responsive design and more. And that’s how things have been for years now. There are [thousands](https://github.com/search?utf8=%E2%9C%93&q=css+grid&type=) of grid systems, but they are all, more or less, the same.

Now that CSS Grid Layout is a reality, I wanted to see what it would take to replace an existing grid framework with CSS Grid. For this experiment, I chose the popular Bootstrap framework.

I started by creating a basic site using the Bootstrap grid:

So let’s break this down and convert it to use CSS Grid.

In Bootstrap, the `.container`

class wraps everything and sets the width constraints. It also adds a padding to the left and right edges and centers everything. There isn’t much to change here. Just like with Bootstrap, the container class can be handy to use with CSS Grid. I recreated it like so:

```
.container {
margin-left: auto;
margin-right: auto;
padding-left: 15px;
padding-right: 15px;
}
```


We can also add responsive breakpoints by adding the following:

```
@media (min-width: 992px) {
.container {
width: 970px;
}
}<code>
```


Bootstrap uses the `.row`

class to wrap columns and provide a negative margin on the left and right to negate the padding added by individual columns. Hacks like negative margins are no longer needed with CSS Grid, but if you’ve read [the documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout), you’ll know that CSS Grid requires a grid container. The `.row`

class is the perfect place to do this. Let me show you what I did, and then we’ll break it down.

```
.row {
display: grid;
grid-template-columns: repeat(12, 1fr);
grid-gap: 20px;
}
```


`display: grid`

creates the grid container.

The `grid-template-columns`

property defines the columns for the grid. You can use spaces to define each column individually, but here we utilize the repeat notation to define 12 equal-sized columns. `1fr`

refers to the width of the individual column. MDN defines the *fr unit* as a new unit which *“represents a fraction of the available space in the grid container.”* You can read more about [fr units](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout#The_fr_Unit) on MDN. You can also read more about [the grid-template-columns property](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-template-columns).

Finally, the `grid-gap`

property is a shorthand property that defines both the amount of space between the columns and between rows of columns. Think of it as our gutter. You can read more about [grid-gap](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-gap) here.

Now, all that’s left are the column classes. Bootstrap uses column classes such as `.col-md-6`

or `.col-lg-8`

to determine the number of columns a div should span. It also floats the div and adds padding to the left and right to create gutters between the columns. Recreating these classes is *incredibly* easy thanks to the `.grid-column`

shorthand property. For example, if we wanted to recreate the `.col-md-6`

class, we can use the following:

```
@media (min-width: 992px) {
.col-md-6 {
grid-column: span 6;
}
}
```


Simple, right? No floats. No padding. It just works. The `grid-column`

shorthand specifies an item’s size and location. We can use `span`

to indicate that this particular item should span six columns. The gutter is automatically taken care of because of the wrapper’s `grid-gap`

property. You can learn more about [the grid-column property](https://developer.mozilla.org/en-US/docs/Web/CSS/grid-column) here.

So what happens when you put it all together? Well, the website looks exactly the same, but we are able to completely remove the Bootstrap dependency and use native CSS Grids.

This type of experiment is a fun learning exercise, but it can also be dangerous. To borrow a line from wise [philosopher Jeff Goldblum](https://en.wikiquote.org/wiki/Jurassic_Park_(film)):


“You … were so preoccupied with whether or not you could, you didn’t stop to think if you should.”

We don’t want to limit CSS Grid by shoehorning it into a syntax that will limit its potential. We were able to easily recreate the Bootstrap grid, but CSS Grid is so much more powerful than any grid system that came before it. That’s because it is a web-native solution built from the ground up.

We are no longer locked into 12 column grids that float from left to right. Do you want to place elements in precise locations on the grid, independent of their HTML source order? Go for it. Do you want to create items that span multiple columns and rows? Not a problem. Check out [this demo](https://www.mozilla.org/en-US/developer/css-grid/) that Mozilla’s [Craig Cook](https://github.com/craigcook/) created to showcase various layout patterns. Try recreating some of those layouts using Bootstrap (hint: not possible). We are just scratching the surface of what CSS Grids can do.

If you want to learn more about CSS Grid, check out the following resources:

[Mozilla CSS Grid Demo](https://www.mozilla.org/en-US/developer/css-grid/)

[CSS Grid documentation on MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)

## About Dan Brown

Creator, developer, strategist, homebrewer, runner, sock enthusiast, beard evangelist, writer, drummer, adventurer, Oxford comma advocate, and human Swiss Army Knife.

## 8 comments

MarkusApril 13th, 2017 at 10:38Havi Hoffman [Editor]April 13th, 2017 at 13:14voracityApril 13th, 2017 at 20:45Dan BrownApril 17th, 2017 at 14:59MikeApril 14th, 2017 at 00:31Havi Hoffman [Editor]April 14th, 2017 at 09:22Tomer CohenApril 16th, 2017 at 00:03Dan BrownApril 17th, 2017 at 14:55