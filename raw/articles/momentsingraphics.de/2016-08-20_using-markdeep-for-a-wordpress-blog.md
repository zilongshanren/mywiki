---
title: Using Markdeep for a WordPress blog
url: http://momentsingraphics.de/MetaPost.html
published: '2016-08-20'
source_blog: Moments in Graphics
source_site: http://momentsingraphics.de/
category: graphics
fetched: '2026-04-13'
---

# Using Markdeep for a WordPress blog

**Update 2016-12-23:** [Morgan McGuire](http://casual-effects.com/) has kindly fixed an issue in Markdeep pertaining to HTML mode. In an earlier version of this blog post I suggested a workaround, which has been removed now. Besides [the utility](http://momentsingraphics.de/Media/MetaPost/MarkdeepUtility.zip) has been extended to make it easier to update to new Markdeep versions.

In response to [Morgan McGuire's request](https://twitter.com/CasualEffects/status/765239091986333696) this post will explain how I set up this blog using his handy [Markdeep](https://casual-effects.com/markdeep/), [MathJax](http://mathjax.org/) and [Wordpress](http://wordpress.org/). The blog is hosted on my rented server and when you request a page it usually won't make connections to any other hosts to keep you from being tracked. Most of this post is specific to Markdeep, so you may also find it useful if you have no plans to use Wordpress.

I am not a web developer by any means. I never used Javascript before, I know but [loathe PHP](https://eev.ee/blog/2012/04/09/php-a-fractal-of-bad-design/) and my HTML and CSS are quite rusty. On top of that I did not want to invest too much time into the setup. Therefore, you should be prepared to find some bad advice in this post. If you have suggestions how to do it better, please leave a comment.

## Design goals

I set up the blog with very specific goals in mind. If you value the same aspects, this post may be for you:

- Convenient offline content creation
- My time for blogging is limited. If the creation of new posts and pages takes too long, I would end up not doing it. Therefore, I wanted a system that allows me to write posts offline with rapid iteration and convenient editing.
- Comments
- Given my
[attitude towards PHP](https://eev.ee/blog/2012/04/09/php-a-fractal-of-bad-design/), I would have preferred a blog with completely static HTML pages. However, one feature that I care about requires some amount of server-side processing and that's comments. Receiving feedback and getting discussions going is one of the key motivations for this blog, so I cannot do without comments. - Privacy
- I'm allergic to trackers. It is my belief that Google, Facebook and the other big players should not know everyone's browser history. To avoid tracking on my page, I wanted to make sure that no connections to external hosts are made unless external contents are embedded into a post. Furthermore, I respect when people disable Javascript for security or privacy reasons and I wanted the page to function reasonably well without it.
- Available server
- I already had
[rented a server](https://hosteurope.de/)with support for PHP and SQL. - New domain
- To make sure that I do not bind myself to the owner of some domain, I registered a new one.
[Wordpress](http://wordpress.org/)- Comments are built-in, the system is not too cluttered but just flexible enough and good themes are available. To avoid opening up security holes, I try to stay away from plugins.
[Markdeep](https://casual-effects.com/markdeep/)- This system has all the features I care about, such as convenient offline editing, powerful formatting features, cross-references, citations, floating figures, videos and a MathJax integration. Also, I figured that I cannot really go wrong using something developed by a graphics researcher for a graphics blog. Though, I wanted the HTML-code-generation to happen on my local system because I do not want to make excessive use of Javascript on the client side.
[MathJax](http://mathjax.org/)- My work tends to be heavy on the math, so I care about pretty typesetting of formulas. The MathJax output looks great and it has extensive support for TeX, including macros. Besides, it is already integrated into Markdeep by default. Hosting it locally is possible. It does require client-side Javascript but as long as the remainder of the page looks fine without it, that's acceptable. Here's an example of MathJax output where \(f: \mathbb{C}\rightarrow\mathbb{C}\) is holomorphic:

## Markdeep in a Wordpress framework

Setting up Wordpress is easy enough and most of the default settings work for me. It took a little bit more tinkering to use preprocessed Markdeep output as content of blog posts and pages without hurting the rapid iteration.

Markdeep is implemented in Javascript and enabled by adding one script invocation to a file with Markdeep code. By default Markdeep takes the whole content of this intentionally misformated HTML file and interprets it as Markdeep code. It then replaces it by nicely formatted HTML code. In the end, I want to be able to conveniently post this HTML code on Wordpress.

My first attempt was to use [Node.js](https://nodejs.org/en/) as suggested on the [Markdeep webpage](https://casual-effects.com/markdeep/) but that did not work because Markdeep does in fact require a DOM to function properly, i.e. there has to be an HTML-document in a browser window to work with.

Thus, I'm now using [Firefox](https://www.mozilla.org/en-US/firefox/new/) for all of my Javascript processing. The Markdeep script is embedded into an [automatically generated larger Javascript file](http://momentsingraphics.de/Media/MetaPost/MarkdeepUtility.zip). This file executes the following operations in sequence:

- It surrounds the Markdeep code in the body by actual HTML code. In my case this HTML code defines the layout of my Wordpress blog to get a preview that is as close as possible to the final result. The inner-most element is a
`<pre class="markdeep">`

tag surrounding the Markdeep code, - It sets
`window.markdeepOptions.mode="html"`

, i.e. Markdeep does not generate the whole page but only processes the part in the`<pre class="markdeep">`

tag, - It invokes Markdeep to turn the Markdeep code into HTML,
- It extracts the generated HTML and displays it in a text box,
- It adds an invocation of MathJax to the end of the head.

The use of this extended script is the same as that of Markdeep itself. You add an invocation of it to the end of a text file with file-format extension *.md.html containing Markdeep code. On opening this file in a browser you see the Markdeep output within the surrounding webpage followed by a text box with the code for the body. This code can then be copied easily to post it online.

There was one issue when using the unmodified code for the head. By default Markdeep uses a section numbering for all headings. However, in a Wordpress environment there are many headings (e.g. in the sidebar) which you really do not want to be numbered. Eventually I decided that the section numbering is fairly pointless for blog posts anyway. Its main purpose would be cross references but you can do those via hyperlinks. Thus, I removed the section numbering altogether. The remainder of the code for the head was then added to the header.php in my Wordpress theme.

## Eliminating connections to third-party hosts

To figure out which other hosts my page references, I used the network traffic inspector in Firefox.

Of course Google was in there. By default my theme of choice used fonts retrieved from a Google server. This leads to [the one plugin that I am using](https://wordpress.org/plugins/disable-google-fonts/). It disables use of these fonts. The code looked clean enough.

Next I had to upload MathJax to my server and reference that in the head rather than using their content distribution network. Uploading the 32k files via FTP was slightly painful but worked eventually.

Finally, I tried to find some page impression counter that would not phone home but I could not find anything decent and resorted to using the analytics provided by my server. If someone has a recommendation, that would be appreciated.

## Publishing

The procedure for publishing a new post is not quite as automated as I would want it to be but that's largely owed to the restrictions of my server. The first step is to upload all files (images, videos, downloads, etc.) referenced by the article via FTP. It is easiest to keep the paths consistent if you enable permalinks based on the page ID in the Wordpress settings (e.g. [http://momentsingraphics.de/?p=24](http://momentsingraphics.de/?p=24) ). Then in the second step you create the post (or page) through the Wordpress admin panel and paste the body HTML produced by Markdeep.

## Updating Markdeep

Markdeep is being improved continuously. I will not update the [Markdeep utility](http://momentsingraphics.de/Media/MetaPost/MarkdeepUtility.zip) provided here with each new version of Markdeep. However, you can easily update it yourself. Just download the [latest markdeep.min.js](https://casual-effects.com/markdeep/latest/markdeep.min.js), replace the version that comes as part of the [Markdeep utility](http://momentsingraphics.de/Media/MetaPost/MarkdeepUtility.zip) and run the Python script `BuildMarkdeepUtility.py`

. If the new version of Markdeep makes changes to the header code, you should also open `ShowHeadAdditions.html`

to grab the new code.

## Summary

Here's a summary of how to set up your blog the way I did:

- Perform a standard installation of
[Wordpress](http://wordpress.org/)on your server, - Choose your theme. You will need to change its code a little, so if you change the theme later, you have to start over,
- Add the following code to the <head> of your theme. It should be located in header.php. If you have installed MathJax on your server, you have to change the path accordingly. If you have updated Markdeep, just open
`ShowHeadAdditions.html`

in the utility package to get the new code to add.

```
<!-- Markdeep styles -->
<style>body{counter-reset: h1 h2 h3 h4 h5 h6}.md code,pre{font-family:Menlo,Consolas,monospace;font-size:15.018802542857143px;line-height:140%}.md div.title{font-size:26px;font-weight:800;line-height:120%;text-align:center}.md div.afterTitles{height:10px}.md div.subtitle{text-align:center}.md .image{display:inline-block}.md div.imagecaption,.md div.tablecaption,.md div.listingcaption{margin:0.2em 5px 10px 5px;text-align: justify;font-style:italic}.md div.imagecaption{margin-bottom:0}.md img{max-width:100%;page-break-inside:avoid}li{text-align:left};.md div.tilde{margin:20px 0 -10px;text-align:center}.md blockquote.fancyquote{margin:25px 0 25px;text-align:left;line-height:160%}.md blockquote.fancyquote::before{content:"“";color:#DDD;font-family:Times New Roman;font-size:45px;line-height:0;margin-right:6px;vertical-align:-0.3em}.md span.fancyquote{font-size:118%;color:#777;font-style:italic}.md span.fancyquote::after{content:"”";font-style:normal;color:#DDD;font-family:Times New Roman;font-size:45px;line-height:0;margin-left:6px;vertical-align:-0.3em}.md blockquote.fancyquote .author{width:100%;margin-top:10px;display:inline-block;text-align:right}.md small{font-size:60%}.md div.title,contents,.md .tocHeader,h1,h2,h3,h4,h5,h6,.md .shortTOC,.md .mediumTOC,.nonumberh1,.nonumberh2,.nonumberh3,.nonumberh4,.nonumberh5,.nonumberh6{font-family:Verdana,Helvetica,Arial,sans-serif;margin:13.4px 0 13.4px;padding:15px 0 3px;border-top:none;clear:both}.md svg.diagram{display:block;font-family:Menlo,Consolas,monospace;font-size:15.018802542857143px;text-align:center;stroke-linecap:round;stroke-width:2px;page-break-inside:avoid;stroke:#000;fill:#000}.md svg.diagram .opendot{fill:#FFF}.md svg.diagram text{stroke:none}.md h1,.tocHeader,.nonumberh1{border-bottom:3px solid;font-size:20px;font-weight:bold;}h1,.nonumberh1{counter-reset: h2 h3 h4 h5 h6}h2,.nonumberh2{counter-reset: h3 h4 h5 h6;border-bottom:2px solid #999;color:#555;font-size:18px;}h3,h4,h5,h6,.nonumberh3,.nonumberh4,.nonumberh5,.nonumberh6{font-family:Helvetica,Arial,sans-serif;color:#555;font-size:16px;}h3{counter-reset:h4 h5 h6}h4{counter-reset:h5 h6}h5{counter-reset:h6}.md table{border-collapse:collapse;line-height:140%;page-break-inside:avoid}.md table.table{margin:auto}.md table.calendar{width:100%;margin:auto;font-size:11px;font-family:Helvetica,Arial,sans-serif}.md table.calendar th{font-size:16px}.md .today{background:#ECF8FA}.md .calendar .parenthesized{color:#999;font-style:italic}.md div.tablecaption{text-align:center}.md table.table th{color:#FFF;background-color:#AAA;border:1px solid #888;padding:8px 15px 8px 15px}.md table.table td{padding:5px 15px 5px 15px;border:1px solid #888}.md table.table tr:nth-child(even){background:#EEE}.md pre.tilde{border-top: 1px solid #CCC;border-bottom: 1px solid #CCC;padding: 5px 0 5px 20px;margin:0 0 30px 0;background:#FCFCFC;page-break-inside:avoid}.md a:link, .md a:visited{color:#38A;text-decoration:none}.md a:link:hover{text-decoration:underline}.md dt{font-weight:700}dl>.md dd{padding:0 0 18px}.md dl>table{margin:35px 0 30px}.md code{white-space:pre;page-break-inside:avoid}.md .endnote{font-size:13px;line-height:15px;padding-left:10px;text-indent:-10px}.md .bib{padding-left:80px;text-indent:-80px;text-align:left}.markdeepFooter{font-size:9px;text-align:right;padding-top:80px;color:#999}.md .mediumTOC{float:right;font-size:12px;line-height:15px;border-left:1px solid #CCC;padding-left:15px;margin:15px 0px 15px 25px}.md .mediumTOC .level1{font-weight:600}.md .longTOC .level1{font-weight:600;display:block;padding-top:12px;margin:0 0 -20px}.md .shortTOC{text-align:center;font-weight:bold;margin-top:15px;font-size:14px}</style>
<!-- hljs styles -->
<style>.hljs{display:block;overflow-x:auto;padding:0.5em;background:#fff;color:#000;-webkit-text-size-adjust:none}.hljs-comment{color:#006a00}.hljs-keyword{color:#02E}.hljs-literal,.nginx .hljs-title{color:#aa0d91}.method,.hljs-list .hljs-title,.hljs-tag .hljs-title,.setting .hljs-value,.hljs-winutils,.tex .hljs-command,.http .hljs-title,.hljs-request,.hljs-status,.hljs-name{color:#008}.hljs-envvar,.tex .hljs-special{color:#660}.hljs-string{color:#c41a16}.hljs-tag .hljs-value,.hljs-cdata,.hljs-filter .hljs-argument,.hljs-attr_selector,.apache .hljs-cbracket,.hljs-date,.hljs-regexp{color:#080}.hljs-sub .hljs-identifier,.hljs-pi,.hljs-tag,.hljs-tag .hljs-keyword,.hljs-decorator,.ini .hljs-title,.hljs-shebang,.hljs-prompt,.hljs-hexcolor,.hljs-rule .hljs-value,.hljs-symbol,.hljs-symbol .hljs-string,.hljs-number,.css .hljs-function,.hljs-function .hljs-title,.coffeescript .hljs-attribute{color:#A0C}.hljs-function .hljs-title{font-weight:bold;color:#000}.hljs-class .hljs-title,.smalltalk .hljs-class,.hljs-type,.hljs-typename,.hljs-tag .hljs-attribute,.hljs-doctype,.hljs-class .hljs-id,.hljs-built_in,.setting,.hljs-params,.clojure .hljs-attribute{color:#5c2699}.hljs-variable{color:#3f6e74}.css .hljs-tag,.hljs-rule .hljs-property,.hljs-pseudo,.hljs-subst{color:#000}.css .hljs-class,.css .hljs-id{color:#9b703f}.hljs-value .hljs-important{color:#ff7700;font-weight:bold}.hljs-rule .hljs-keyword{color:#c5af75}.hljs-annotation,.apache .hljs-sqbracket,.nginx .hljs-built_in{color:#9b859d}.hljs-preprocessor,.hljs-preprocessor *,.hljs-pragma{color:#643820}.tex .hljs-formula{background-color:#eee;font-style:italic}.diff .hljs-header,.hljs-chunk{color:#808080;font-weight:bold}.diff .hljs-change{background-color:#bccff9}.hljs-addition{background-color:#baeeba}.hljs-deletion{background-color:#ffc8bd}.hljs-comment .hljs-doctag{font-weight:bold}.method .hljs-id{color:#000}</style>
<!-- MathJax invocation -->
<script type="text/javascript" async src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
```


- Change the structure of permalinks to plain links such as
`http://momentsingraphics.de/?p=24`

in the Wordpress settings (optional, but makes it easier to reference files uploaded via FTP), - Optionally install a
[plugin to disable Google fonts](https://wordpress.org/plugins/disable-google-fonts/).

Then to create a post and publish it, you proceed as follows:

- Download my
[Markdeep utility](http://momentsingraphics.de/Media/MetaPost/MarkdeepUtility.zip). If it suits your needs out of the box, you only need MarkdeepUtility.js. Otherwise you should edit the other files (especially PreviewBlogPage.htm) and run`python BuildMarkdeepUtility.py`

with[Python 3.x](https://www.python.org/downloads/)to rebuild MarkdeepUtility.js, - Create a new file (named e.g. Article.md.html) next to MarkdeepUtility.js and paste the following code into it with the text editor of your choice (I use
[Notepad++](http://notepad-plus-plus.org/)),

```
<meta charset="utf-8" lang="en">
<!-- Markdeep code goes here -->
<script src="MarkdeepUtility.js"></script>
```


- Open the file in a browser next to your text editor. If you are using Firefox, you can use the plugin
[Auto Reload](https://addons.mozilla.org/en-US/firefox/addon/auto-reload/)to ensure that your article updates in the browser whenever you save your local file. It should look roughly like this:

- Write your article using standard
[Markdeep notation](https://casual-effects.com/markdeep/features.md.html), then copy the body HTML from the text box at the bottom, - Upload files referenced by your post (if any) to the appropriate path on your server via FTP,
- Create a new page or post in the Wordpress administration panel and fill in Wordpress meta data such as title, tags, categories, discussion settings, etc.,
- Go to text-edit mode and paste the body HTML,
- Optionally preview the article,
- Click Publish.

## Downloads

## Comments

**gellenburg**

2017-02-12, 15:05

WordPress has built-in support for MarkDown. Seems like a lot of extra work to accomplish something that’s built-in? Including LaTeX math (with JetPack). Or am I missing something?

**Christoph**

2017-02-12, 15:26

This feature does not really fit my needs for several reasons:

- I want to be able to write posts offline with an immediate preview of what they look like in the blog layout. Achieving this with the native Markdown support of WordPress would have taken at least as long as what I did here.
- Markdown is not the same as Markdeep. Markdeep is an extension with various features that really come in handy for me.
- I respect that some users like to have JavaScript disabled by default when browsing the web (for security and privacy reasons). Therefore, I would not want to run the formatting scripts on the client-side. Admittedly, formulas still require JavaScript but having broken formulas without JavaScript clearly seems more acceptable than completely broken posts and pages.
- I've had a look at JetPack and did not like how it sends data about my visitors to a centralized server.

This is not to say that the built-in Markdown support is bad or should not be used. It just did not match my design goals.

Comments are closed.