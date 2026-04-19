---
title: runevision blog
url: https://blog.runevision.com/2014/07/
published: '2014-07-17'
source_blog: Blog - runevision
source_site: https://blog.runevision.com/
category: graphics
fetched: '2026-04-19'
---

In the past few weeks I've been implementing incremental changes to the design of my website. Generally I still like the overall aesthetic and layout of the design made in 2008, but I wanted to tweak it to bring it more in line with modern web design ideals.

Here's the new design next to the old:

![](../../assets/5ed690a9b67b2eda.png)

![](../../assets/d83ff635b80a6607.png)

The goal has been to move the design more in the direction of minimalism (not that I've striving for absolute minimalism) and to make the layout responsive so it works better on mobile devices and can take better advantage of wider screens.

### Minimalism

There has long been a trend in web design, and in recent years in application design too, towards minimalism in UI aesthetics. The reasoning goes that the content should be the primary focus with little else to distract from it. This has often been implemented in the form of flat designs. Though ubiquitous today, flat redesigns have sometimes been controversial, especially when used in applications, and when taken to an extreme. I have certain reservations myself, but that's a discussion for another time.

In any case, minimalism certainly have some merit to it. Since all the texture and shading in my old web design was purely cosmetic and wasn't used for aiding usability, I could see the point in getting rid of some of that to produce a cleaner design.

I've worked with a process of implementing the low hanging fruit first. Just removing the background pattern and the background spark image already made the design feel a bit more clean, but it left an awkward empty gap to the left of the title. I didn't want to move the menu sidebar upwards, but placing the menu sidebars at the right side instead of left fixed the problem, and has been a general trend for a long time anyway.

![](../../assets/9f2e95c2b49e67a0.png)

Next step was trying out getting rid of the shading. To begin with I simply replaced the shaded graphics files with flat versions to be able to test it without touching the HTML and CSS - well, except for changing the colors of the box headers and timestamps.

For a long time I had disliked the headers being confined to thin colored bars, so I wanted to get rid of that at the same time.

![](../../assets/a789843853c31845.png)

This change basically took the graphical look 90% of the way, but as everyone knows, the devil is in the details, and there was still many small tweaks needed.

What came next though were not more visual design changes but rather technical changes to the implementation.

### Modern styling and responsiveness

Now that the general flat look was validated, I could proceed to implement it in a smarter way. Modern CSS can draw rounded borders fine without any image files needed. This required quite some changes to the HTML and CSS. Most of it was removing a lot of cruft of nested divs that used to control the image-based borders, but some rethinking of the margin and padding values was also required.

Before I could begin implementing responsiveness, I also needed the header to be horizontally resizable. The header was one big image, which made resizing tricky. In order to make it resizable, I split it up into multiple parts: One background image for the box itself, one semi-transparent image with the portrait and left side text, and one semi-transparent image with the site name. Now I could make a resizable box in CSS with the new background image as background, rounded corners handled by the browser, and additional image elements layered on top.

With all boxes now being resizable, I could implement media queries to support multiple layouts of the site suited for different screen resolutions. The original design was designed for a minimum browser width of 800 pixels. I kept that one since it's still good for old monitors, browsers that are not full-screen, and now also for tablets. I added a wider but otherwise identical version for wider screens. Finally, I added a narrower version suitable for mobile browsing.

![](../../assets/11558aed5ec2c82e.png)

![](../../assets/3d64d6b53bcf6676.png)

![](../../assets/9a1c097a2d3496fe.png)

The mobile layout is significantly different from the others. The menu sidebars are absent since there's no room, and the header doesn't have links for each main section in the orange bar. All the text is also larger.

### Text scaling in CSS

For a long time I was seriously confused at the results I got when trying to scale all the text up or down, especially in how it interacted with line height. The best practices I arrived at is:

**Use rem unit for font sizes**

Use not *%*, *pt*, *px*, or *em* for specifying text sizes, but rather the new unit *rem* (root em). Probably obviously, *px* and *pt* are not suitable for scaling at all since they're absolute units. What's more tricky is that *%* and *em* are not easy to use for specifying sizes either. Since they specify sizes relative to the parent element, font sizes can end up being affected in non-trivial ways by the amount of nested elements the text is inside. By contract, the *rem* unit is not relative to the parent, but to the root element (the html tag), so nested elements have no effect on font sizes. Still, the overall scaling of all text can be controlled by setting a *%* font size in the style for the html element. My mobile layout has font-size: 140% for the html element.

**Use unit-less numbers for line height**

Line height should be specified using numbers with no units, except for exotic use cases where you want the same distance between lines regardless of font size. For a long time I assumed line height should be specified in either *%* or *em*, but that will calculate the physical line height in the context of the element it's specified for, and nested elements will then inherit that *physical* line height regardless of whether they use a smaller or larger font. Specifying the line height as a number with no unit prevents that.

I still have some confusion left over how some mobile browsers (such as iOS Safari) scales text up in ways that are inconsistent or ill-explained, but it's not a big issue.

### Mobile menu

There's no room for the sidebar menus in the mobile layout, so I opted for a drop-down menu instead. The menu is expanded and collapsed using jQuery (no surprises there).

![](../../assets/aeba323b98ae7445.png)

### Viewport logic

Modern browsers can scale pages arbitrarily, and mobile browsers scale them all the time by default. When a page can be scaled arbitrarily up or down, the question is how much room it should have available. Mobile browsers let pages decide that using the *viewport* meta information, where the width and height of the viewport can be specified.

The viewport width and height can be set to either constant values, or set to certain variables such as the device-width. The problem is that this doesn't always provide enough control.

In my responsive design, the minimum (mobile) width layout fits 600 pixels and the narrow layout fits 800 pixels. There is no reason a mobile or tablet browser should use a viewport of a different width than either 600 or 800 - it would just be wasted space.

To use the space optimally, I used JavaScript to query the device width, and set it to either 600 or 800 depending on the current screen width. You'd think it should choose the 800 width version only if the screen is at least 800 pixels wide, but that's not actually the intended behavior. Instead it chooses the 800 version of the screen is at least 480 pixels wide, otherwise the 600 version. You see, even for a screen with only 480 pixels width, it works better to use the 800 version scaled down than using the 600 version (scaled down less). Like I said, pages can be scaled arbitrarily, and there's no reason that a 1:1 scale is necessarily the optimum to strive for.

Why use exactly 480 to determine whether to use the 600 or 800 version? Well, supposedly that's about the size that divides the phones from the tablets (in most cases), and I want the 600 mobile-optimized version to be used for phones only; not tablets.

I'm sure this simple logic doesn't cover all cases, but it "works for me" (tested on iPhone 5, iPad retina and Nexus 7) and should be good enough for my personal site.

### Going forward

So far I'm happy with the revised design, though I'm sure there's still many things that could be improved. For example, I didn't look into using more modern fonts at all; it's still using "good old" Verdana/Arial. I also haven't gone through *all* the old content on my site and made sure everything looks good and isn't broken. Let me know if you spot any issues.

Generally my experience getting re-acquainted with HTML / CSS is that it's become a lot nicer to use in the past half decade since I did the original design. Fewer hacks are needed and stuff feels more consistent.

That said, I still find many things in the layout model annoying, and by fewer hacks I definitely didn't mean no hacks at all. I keep Googling for solutions to simple problems and find only partial, yet overly complicated solutions. One issue I didn't solve yet is that boxes with no multi-line paragraphs don't expand to the full available width (like on [this](http://runevision.com/multimedia/mazeraiders/) or [this](http://runevision.com/about/map/) page). Don't think it's simply a matter of setting width: 100%, oh no, that will expand it *beyond* the available width (because of the silly CSS box model where box sizes excludes padding and borders)...

Beyond that, is there any low-hanging fruit I've missed? Some further big improvements I could implement with little effort? If you have any tips, let me know.