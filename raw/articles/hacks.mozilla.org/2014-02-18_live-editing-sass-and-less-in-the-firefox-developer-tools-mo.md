---
title: Live Editing Sass and Less in the Firefox Developer Tools – Mozilla Hacks -
  the Web developer blog
url: https://hacks.mozilla.org/2014/02/live-editing-sass-and-less-in-the-firefox-developer-tools/
author: Heather Arthur
published: '2014-02-18'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

[Sass](http://sass-lang.com/) and [Less](http://lesscss.org/) are expressive languages that compile into CSS. If you’re using Sass or Less to generate your CSS, you might want to debug the source that you authored and not the generated CSS. Luckily you can now do this in the Firefox 29 developer tools using source maps.

The Firefox developer tools use source maps to show the line number of rules in the original source, and let you edit original sources in the Style Editor. Here’s how to use the feature:

## 1. Generate the source map

When compiling a source to CSS, use the option to generate a sourcemap for each style sheet. To do this you’ll need Sass 3.3+ or Less 1.5+.

### Sass

```
sass index.scss:index.css --sourcemap
```

### Less

```
lessc index.less index.css --source-map
```

This will create a `.css.map`

source map file for each CSS file, and add a comment to the end of your CSS file with the location of the sourcemap: `/*# sourceMappingURL=index.css.map */`

. The devtools will use this source map to map locations in the CSS style sheet to locations in the original source.

## 2. Enable source maps in developer tools

Right-click anywhere on the inspector’s rule view or in the Style Editor to get a context menu. Check off the `Show original sources`

option:

Now CSS rule links will show the location in the original file, and clicking these links will take you to the source in the Style Editor:

## 3. Set up file watching

You can edit original source files in Style Editor tool, but order to see the changes apply to the page, you’ll have to watch for changes to your preprocessed source and regenerate the CSS file each time it changes. To set watching up:

### Sass

```
sass index.scss:index.css --sourcemap --watch
```

### Less

For Less, you’ll have to set up another service to do the watching, like [grunt](https://github.com/gruntjs/grunt-contrib-watch).

## 4. Save the original source

Save the original source to your local file system by hitting the `Save`

link or `Cmd/Ctrl-S`

:

The devtools will infer the location of the generated CSS file locally and watch that file for changes to update the live style sheet on the page.

Now when you edit an original source and save it, the page’s style will update and you’ll get immediate feedback on your Sass or Less changes.

**The source has to be saved to disk and file watching set up in order for style changes to take effect**.

## About Heather Arthur

Firefox developer tools developer at Mozilla, working mainly on the style tools.

Technical Evangelist & Editor of Mozilla Hacks. Gives talks & blogs about HTML5, JavaScript & the Open Web. Robert is a strong believer in HTML5 and the Open Web and has been working since 1999 with Front End development for the web - in Sweden and in New York City.
He regularly also blogs at [http://robertnyman.com](http://robertnyman.com) and loves to travel and meet people.

## 32 comments

Mihai CherejiFebruary 18th, 2014 at 10:18Jonas KFebruary 18th, 2014 at 11:45HaiFebruary 18th, 2014 at 12:04Brian GrinsteadFebruary 18th, 2014 at 13:51HaiFebruary 18th, 2014 at 14:39Brian GrinsteadFebruary 18th, 2014 at 15:03BenFebruary 18th, 2014 at 15:08Heather ArthurFebruary 18th, 2014 at 15:27Matthew BalaamFebruary 19th, 2014 at 02:51Heather ArthurFebruary 19th, 2014 at 11:37Matthew BalaamFebruary 20th, 2014 at 02:02Heather ArthurFebruary 20th, 2014 at 18:44Matthew BalaamMarch 6th, 2014 at 01:48Camille BissuelFebruary 19th, 2014 at 09:21Heather ArthurFebruary 19th, 2014 at 11:10Camille BissuelFebruary 20th, 2014 at 05:39Alex BellFebruary 19th, 2014 at 18:19Brian GrinsteadFebruary 20th, 2014 at 08:46Scott GilbertsonFebruary 19th, 2014 at 18:35Ronan JouchetFebruary 19th, 2014 at 19:07Heather ArthurFebruary 20th, 2014 at 18:51LukeFebruary 19th, 2014 at 22:22Nick FitzgeraldFebruary 20th, 2014 at 18:58Heather ArthurFebruary 20th, 2014 at 19:04LukeFebruary 20th, 2014 at 23:32JayFebruary 23rd, 2014 at 07:33Heather ArthurMarch 12th, 2014 at 01:21JamesMarch 10th, 2014 at 17:24LukeMarch 11th, 2014 at 21:53JamesMarch 12th, 2014 at 05:49Chris EppsteinMarch 11th, 2014 at 11:51Heather ArthurMarch 11th, 2014 at 23:24