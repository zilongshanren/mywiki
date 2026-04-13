---
title: A simple image gallery using only CSS and the :target selector – Mozilla Hacks
  - the Web developer blog
url: https://hacks.mozilla.org/2012/02/a-simple-image-gallery-using-only-css-and-the-target-selector/
author: Chris Heilmann
published: '2012-02-22'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

Back in the old days of web development and when CSS2 got support I always cringed at “CSS only” demos as a lot of them were hacky to say the least. With CSS growing up and having real interaction features it seems to me though that it is time to reconsider as – when you think about it – visual effects and interactivity should be maintained in the CSS rather than in JavaScript and CSS.

With the support we have in new browsers it would be a waste not to use what has been put in. If you have to give all the visual candy to IE6, OK, then you’d have to use a library like jQuery for your effects. But you can have your cake and eat it if you don’t give the shiny to the old browsers out there, but give them a simpler interface and make sure they don’t get what they don’t understand.

Without any CSS this would just show all the kitten images in a vertical row and the links would point to them. This works, and should be more than enough for the IE6 users out there.

For browsers that support newer CSS, however, we can turn this into our gallery in a few easy steps:

Step 1: Position the articles

To make sure we don’t give IE older than 9 any CSS it chokes on, we can wrap all the selectors in a simple media query (in this case checking that the window is at least 400 pixels wide):

@media screen and (min-width: 400px) {
... all the good stuff ...
}

We then can give the gallery dimensions and an overflow of hidden to make sure that elements positioned outside of it will not be shown. We also position it relative so that every positioned child element will be positioned relatively to it:

Now in order to show the image when the link to it was clicked we use the :target selector. This one assigns the CSS to the element when it was targeted – either by activating a link to it in the document or from the URL when the page loaded. With this pseudo selector, we override the left setting and move it to 20 pixels, thus showing the image.

To make this smoother, all we need to do is to add a CSS transition to the target styles. Now all the changes to the styles will happen smoothly during a second rather than immediately.

That is all there is to it – the rest of the effects are just different variations of the same trick – animating opacity from 0 to 1 or CSS transitions.

Target selectors can be a very powerful trick. The main issue they have though is that the page scrolls to the target, so if there is a big distance between the link and the target you’ll get unsightly jumps.

Thanks! Please check your inbox to confirm your subscription.

If you haven’t previously confirmed a subscription to a Mozilla-related newsletter you may have to do so. Please check your inbox or your spam filter for an email from us.

But don’t forget that Firefox does decode and keep in memory all images on the page even those that aren’t visible. Keep this in mind before stuffing 100 large images in this gallery. Other browsers do this better. There is a bug on bugzilla for this if you are interested.

(P.S. please fix the captcha text below, it does not have the character encoding specified properly so it shows diacritical characters wrongly (it seems the captcha instructions are localized for each visitor). I get “Mus�me sa uisti?, ?e ste ?lovek. Vyrie?te zadanie ni??ie a kliknite na tla?idlo Som ?lovek. Z�skate tak k�d potvrdenia. Ak chcete tento proces v bud�cnosti zjednodu?i?, odpor�?ame v�m povoli? jazyk JavaScript.”).

Positioning the hidden images JUST off-screen will still make them available to assistive technologies (ie screen readers) while not visually displayed.

Consider toggling between display: none & display: block

Yet this means that if you look through an image gallery and would like to return to the place before, you will need to either click back (or hit backslash) several times or click it for a long time, waiting for the dropdown, instead of clicking back once to return.

## 9 comments

VenomVendorFebruary 21st, 2012 at 17:43iamvdoFebruary 22nd, 2012 at 00:38BartFebruary 22nd, 2012 at 04:33acemanFebruary 22nd, 2012 at 04:54Beben KobenFebruary 22nd, 2012 at 08:29George ZamfirFebruary 22nd, 2012 at 09:10sometwothingsFebruary 22nd, 2012 at 15:39dianneFebruary 23rd, 2012 at 06:36JakobMarch 8th, 2012 at 08:39