---
title: 'Kuma: The updated editor experience – Mozilla Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2012/07/kuma-the-updated-editor-experience/
author: Eric Shepherd
published: '2012-07-01'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

The editing experience on the new Kuma wiki that we’ll be deploying starting on July 5th is not enormously different from what you’re used to, but there are some key differences I’d like to call out.

**Getting into the editor**

Let’s take a look, first, at differences in how you get into the editor. Once you’ve logged in using BrowserID, you’ll still see your old friend, the “Edit” button, at the top right corner as usual:

You can simply click that big blue “Edit” button to begin editing the entire page. Easy! But if you want, you can edit just a single section. Each header line has its own edit button off to the right, like this:![Primary edit button Screenshot of primary edit button](https://www.bitstampede.com/wp-content/uploads/2012/07/main-edit-button.png)


Clicking that pretty blue “Edit” button to the right of the section heading will open an editor just for that section.

**Changing page information**

Once you’re in the editor, you can edit both content and page information. At the top left you see the title of the page:

Clicking on the “i” icon gives you access to edit page metadata:

You can then edit the page’s title (that is, the text displayed as the title of the individual page, and the slug, which is the URL component below the parent page (which you can’t edit; there’s a separate move feature for that).

The “TOC” checkbox lets you toggle whether or not the page displays its table of contents of its headers.

**Saving and previewing**

Then, at the top right of the editor screen, you’ll see these buttons:

These are pretty self-explanatory. The first gives you the option to save your changes without leaving the editor; this is a feature we’ve wanted for ages, but finally have. The second button saves your changes and closes the editor.

The “Preview Changes” button actually opens a new tab showing a preview of the page. We finally, **finally**, have the ability to double-check our use of scripted templates before saving your edits. This is a huge deal for us!

Finally, the “Discard Changes” button lets you throw away your edits. Hopefully that’s pretty obvious.

**Editing**

The editor is essentially the same CKEditor we’ve always used on MDN, although it’s a newer version. Most of our keyboard shortcuts are the same as they were before. The most notable difference is that Ctrl-S no longer toggles source mode; instead, it does a “Save Changes.”

One thing we’ve done is revamp the toolbar to be more useful for the types of work we do:

This is very reorganized from what we had before, with fewer unneeded buttons. Immediately below the toolbar is a block hierarchy bar; this shows you the hierarchy of elements that leads to your current cursor position. This is helpful, for example, to know what heading level you’re on, or how deeply nested your list is, and so forth.

We also now have handy buttons for the heading levels, and a button for preformatted text. To the right of the <pre> button is a menu that, when opened while your cursor is in a <pre> block, presents a list of syntax highlighting language options:

This list is much simpler than the old one, and is certainly easier to read!

The style drop-down menu is pretty similar to the old one, with an assortment of styles we use regularly:

Currently, the only way to tag articles is from within the editor screen. This will be changed at some point, but for now, you will find the tag editor at the bottom of the edit page:

You can delete tags by clicking the “X” in each tag’s box, or add new ones by simply clicking to the right of the tag list and starting to type.

*There’s currently a bug that makes it impossible to enter tag names with spaces in their names. This will hopefully be fixed before we deploy Kuma.*

**Requesting reviews**

We’re in the process of building a new, formal review system. While not all of the support for tracking reviews is in place yet, you can establish review requests using the checkboxes at the bottom of the editor page:

For new articles, both the technical and editorial review requests are enabled by default. You can set or clear these as appropriate based on the type and number of changes you’ve made (and, of course, your confidence in your work!).

The “Template” review request is used to indicate that a template has been changed and needs a code review. This won’t affect very many people, because template editing is now under a tighter set of permissions than most editing, for security reasons.

**Onward and upward**


Sometime in the next couple of days, I’ll share a look at the new localization tools we provide in Kuma. They’re not finished, but they’re already much, much better than what we had with our old system (which is to say: none at all).

## About
[
Eric Shepherd ](http://www.bitstampede.com/)

Back in the early days of my career, I was a coder for computer games; if you search little-known Mac titles published by companies including Interplay/MacPlay, MGM Interactive, and Logicware, you'll see my name. Eventually, that work got old and I became a technical writer. Now I'm the developer documentation team lead at Mozilla.

## 4 comments

ziyunfeiJuly 2nd, 2012 at 07:30Dmitry PashkevichJuly 3rd, 2012 at 06:15John KarahalisJuly 3rd, 2012 at 10:37Dmitry PashkevichJuly 4th, 2012 at 04:13