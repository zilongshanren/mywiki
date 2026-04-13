---
title: Multiple-column Layout and column-span in Firefox 71 – Mozilla Hacks - the
  Web developer blog
url: https://hacks.mozilla.org/2019/11/multiple-column-layout-and-column-span-in-firefox-71/
author: Rachel Andrew
published: '2019-11-20'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Firefox 71 is an exciting release for anyone who cares about CSS Layout. While I am very excited to have [subgrid](https://hacks.mozilla.org/2019/06/css-grid-level-2-subgrid-is-coming-to-firefox/) available in Firefox, there is another property that I’ve been keeping an eye on. Firefox 71 implements `column-span`

from Multiple-column Layout. In this post I’ll explain what it is and a little about the progress of the Multiple-column Layout specification.

[Multiple-column Layout](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Columns), usually referred to as *multicol*, is a layout method that does something quite different to layout methods such as flexbox and grid. If you have some content marked up and displaying in Normal Flow, and turn that into a multicol container using the [ column-width](https://developer.mozilla.org/en-US/docs/Web/CSS/column-width) or

[properties, it will display as a set of columns. Unlike Flexbox or Grid however, the content inside the columns flows just as it did in Normal Flow. The difference is that it now flows into a number of anonymous column boxes, much like content in a newspaper.](https://developer.mozilla.org/en-US/docs/Web/CSS/column-count)

`column-count`

Multicol is described as *fragmenting* the content when it creates these anonymous column boxes to display content. It does not act on the direct children of the multicol container in a flex or grid-like way. In this way it is most similar to the fragmentation that happens when we print a web document, and the content is split between pages. A column-box is essentially the same thing as a page.

## What is column-span?

We can use the [ column-span](https://developer.mozilla.org/en-US/docs/Web/CSS/column-span) property to take an element appearing in a column, and cause it to span across all of the columns. This is a pattern common in print design. In the CodePen below I have two such spanning elements:

- The
`h1`

is inside the article as the first child element and is spanning all of the columns. - The
`h2`

is inside the second section, and also spans all of the columns.

This example highlights a few things about `column-span`

. Firstly, it is only possible to span **all** of the columns, or **no** columns. The allowable values for `column-span`

are all, or none.

Secondly, when a span interrupts the column boxes, we end up with two lines of columns. The columns are created in the inline direction above the spanning element, then they restart below. Content in the columns does not “jump over” the spanning element and continue.

In addition, the `h1`

is a direct child of the multicol container, however the `h2`

is not. The `h2`

is nested inside a `section`

. This demonstrates the fact that items do not need to be a direct child to have `column-span`

applied to them.

Firefox has now joined other browsers in implementing the `column-span`

property. This means that we have good support for the property across all major browsers, as the [Compat data for column-span](https://developer.mozilla.org/en-US/docs/Web/CSS/column-span#Browser_compatibility) shows.

![The compat data for column-span on MDN](../../assets/c2f57163cec97c98.png)


## The multicol specification

My interest in the implementation of `column-span`

is partly because I am one of the editors of the [multicol specification](https://drafts.csswg.org/css-multicol-1/). I volunteered to edit the multicol specification as it had been stalled for some time, with past resolutions by the WG not having been edited into the spec. There were also a number of unresolved issues, many of which were to do with the `column-span`

feature. I started work by digging through the mailing list archives to find these issues and resolutions where we had them. I then began working through them and editing them into the spec.

At the time I started working on the specification it was at Candidate Recommendation (CR) status, which infers that the specification is deemed to be fairly complete. Given the number of issues, the WG decided to return it to Working Draft (WD) status while these issues were resolved.

### CSS development needs teamwork between browsers and spec editors

As a spec editor, it’s exciting when features are being implemented, as it helps to progress the spec. CSS is created via an iterative and collaborative process; the CSS WG do not create a complete specification and fling it over the wall at browser engineers. The process involves working on a feature in the WG, which browser engineers try to implement. Questions and problems discovered during that implementation phase are brought back to the working group. The WG then have to decide what to do about such issues, and the spec editor then gets the job of clarifying the spec based on the resolution. The process repeats — each time we tease out issues. Any lack of clarity could cause an interoperability issue if two browsers interpreted the description of the feature in a different way.

Based on the work that Mozilla have been doing to implement `column-span`

, several issues were brought to the CSS WG and discussed in our calls and face-to-face meetings. We’ve been able to make the specification much clearer on a number of issues with `column-span`

and related issues. Therefore, I’m very happy to have a new property implemented across browsers, and also happy to have a more resilient spec! We recently published an updated WD of multicol, which includes many changes made during the time Mozilla were implementing multicol in Firefox.

## Other multicol related issues

With the implementation of `column-span`

, multicol will work in much the same way across browsers. We do have an outstanding issue with regards to the `column-fill`

property, which controls how the columns are filled. The default way that multicol fills columns is to try to balance the content, so equal amounts of content end up in each column.

By using the `column-fill`

property, you can change this behavior to fill columns sequentially. This would mean that a multicol container with a height could fill columns to the specified height, potentially leaving empty columns if there was not enough content.

Due to specification ambiguity, Firefox and Chrome do different things if the multicol container does not have a height. Chrome ignores the `column-fill`

property and balances, whereas Firefox fills the first column with all of the content. This is the kind of issue that arises when we have a vague or unclear spec. It’s not a case of a browser “getting things wrong”, or trying to make the lives of web developers hard. It’s what happens when specifications aren’t crystal clear! For anyone interested, the somewhat lengthy issue trying to resolve this is [here](https://github.com/w3c/csswg-drafts/issues/4036). Most developers won’t come across this issue in practice. However, if you are seeing differences when using `column-fill`

, it is worth knowing about.

The implementation of `column-span`

is a step towards making multicol robust and useful on the web. To read more about multicol and possible use cases see the [Guides to Multicol](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Columns#Guides) on MDN, and my article [When And How To Use Multiple-column Layout](https://www.smashingmagazine.com/2019/01/css-multiple-column-layout-multicol/).

## About
[
Rachel Andrew ](https://rachelandrew.co.uk)

Rachel Andrew is a front and back-end web developer, one half of the company behind Perch CMS, and Editor in Chief of Smashing Magazine. She is a Google Developer Expert for web technologies and a member of the CSS Working Group representing Fronteers, where she is co-editor of the Multi-column Layout spec. Author of 22 books, and a frequent public speaker at conferences worldwide, you can find out what she is up to at https://rachelandrew.co.uk.

## One comment

Max BattcherNovember 20th, 2019 at 13:51