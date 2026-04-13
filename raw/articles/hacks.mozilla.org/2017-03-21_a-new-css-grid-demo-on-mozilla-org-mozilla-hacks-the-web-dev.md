---
title: A new CSS Grid demo on mozilla.org – Mozilla Hacks - the Web developer blog
url: https://hacks.mozilla.org/2017/03/a-new-css-grid-demo-on-mozilla-org/
author: Ali Spivak
published: '2017-03-21'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

With [CSS Grid](https://www.w3.org/TR/css3-grid-layout/) shipping across browsers this spring (already in Firefox 52, Chrome 57, and Safari 10.1. UPDATED: Safari 10.1 shipped in March with the release of iOS 10.3 and macOS Sierra 10.12.4) the team here at Mozilla wanted to show off some of the key features and also let our in-house designers and developers experiment with the technology on [mozilla.org](https://www.mozilla.org/en-US/). The result is a [live demo site](http://mozilla.org/developer/css-grid) that shows CSS Grid features and provides links to our favorite resources. The bonus is the mozilla.org web developers got hands-on, real world experience by working up a site from scratch with Grid.

It turned out that the resources available on the web, including tons of examples and instruction, do such a great job of clearly explaining the basics that they were able to dive in and build the site without any handholding. [Jen Simmons](http://labs.jensimmons.com/) and [Rachel Andrew](http://gridbyexample.com/examples/) both provide excellent examples and tutorials on how to start working with grids. In addition, [MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout) contains several detailed guides on using CSS Grids.

When designing this project we had the following goals in mind:

- Demonstrate the potential of CSS Grid to developers and designers.
- Introduce Firefox Developer Tools Grid Inspector, which is currently the only in-browser developer tool for Grid.
- Build a page on mozilla.org that uses Grid Layout.
- Prove CSS Grid makes it easy for anyone who knows CSS to grasp the fundamentals and create a functional page. (Bonus: the Mozilla webdev team had fun doing it!)

Grid provides powerful layout capabilities, and on the demo site we wanted to illustrate some of the key features. This list is not exhaustive, but does show some really interesting capabilities that are now available.

- Fixed or Flexible Grids: You can create a grid either with fixed
[track](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout#Grid_Tracks)sizes or with flexible sizes using percentages or the[new fr fractional unit](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout#The_fr_Unit). - Place & Align Items: You can place items at precise locations on the grid using standard
[grid properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout#Positioning_items_against_lines)or by using[grid template areas](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Grid_Template_Areas). Items can be placed independent of their HTML source order.[Alignment](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Box_Alignment_in_CSS_Grid_Layout#Aligning_items_on_the_block_or_column_Axis)features control how items align when placed into a grid area, and also how the whole grid is aligned. - Control Overlap: Grid cells can contain more than one item, and can
[span](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Layout_using_Named_Grid_Lines)multiple rows and columns. You can also control[layering with z-index](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout/Basic_Concepts_of_Grid_Layout#Layering_items_with_z-index).

Additionally, we wanted to show off Firefox’s [Grid Inspector Tool](https://developer.mozilla.org/en-US/docs/Tools/Page_Inspector/How_to/Examine_grid_layouts), which lets you see the grid lines in the browser while you’re creating a layout or studying other examples of CSS Grid in action.

Please check out the demo site and let us know what you think. We hope it will help you to learn and inspire you to start using CSS Grid. And stay tuned for more coverage of CSS Grid and how to use it, here and [on MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout).


## About Ali Spivak

[@alispivak](https://twitter.com/alispivak). Ali is the head of Developer Ecosystem at Mozilla, and has been developing and managing web sites for longer than she cares to admit. She's passionate about keeping the web open and working on things developers love (like MDN).

## 12 comments

RalfMarch 22nd, 2017 at 23:09Ali SpivakMarch 23rd, 2017 at 13:35Jos SparreboomMarch 23rd, 2017 at 08:30Ali SpivakMarch 23rd, 2017 at 13:30Johaven KaindoaMarch 24th, 2017 at 06:30voracityMarch 25th, 2017 at 20:37DavidMarch 26th, 2017 at 14:02Craig CookMarch 27th, 2017 at 13:09MasonMarch 30th, 2017 at 12:42Ali SpivakApril 7th, 2017 at 12:55ffgfgfApril 19th, 2017 at 23:51georgeApril 20th, 2017 at 08:05