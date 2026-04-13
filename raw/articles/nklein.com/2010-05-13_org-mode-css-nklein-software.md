---
title: 'Org-Mode CSS :: nklein software'
url: http://nklein.com/2010/05/org-mode-css/
author: Pat
published: '2010-05-13'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

The color scheme here is a bit me-centric, but I am mostly posting it because I find the typography pleasing…. In my *.emacs* file, I have set up the `org-export-headline-levels`

to two and the `org-export-html-style`

to the following:

(setq org-export-html-style

"<style type="text/css">#<:use "style.css"></style>")

<<basic body style>>

<<header style>>

<<content style>>

The basic body has no margin and a pleasing (to me) khaki color.

body {

background-color: #999966;

margin: 0em;

}

The headers are carefully sized to try to take up a multiple of 1.4em with a consistent bottom margin.

h1 {

font-size: 2.0em;

margin-top: 1.9em;

margin-bottom: 0.3em;

}

h2 {

font-size: 1.5em;

margin-top: 2.4em;

margin-bottom: 0.3em;

}

h3 {

font-size: 1.25em;

margin-top: 1.25em;

margin-bottom: 0.3em;

}

The main body is a pale yellow color with vertical borders. It’s got a decent font (the one that I have by default for my browser) with a slight tweak to the letter spacing and a big tweak to the leading. It keeps from getting too wide and stays centered. Oh, and I don’t skip space before lists.

div#content {

background-color: #ffffcc;

border-left: double #333300 3mm;

border-right: double #333300 3mm;

font-family: Times, serif;

letter-spacing: 0.075em;

line-height: 1.4;

margin: 0em auto;

padding: 2em;

width: 45em;

}

ul {

margin: 0;

}

Here is some [sample output](http://nklein.com/wp-content/uploads/2010/05/construction-loan.html).

Great example, thanks for posting! I used the #+STYLE method instead of modifying my .emacs file since i may want different styles for different docs, but your method allows the CSS to be embedded in the HTML, which is also nice.

I definitely used your CSS as a starting point for creating my own look and feel – again, thanks!