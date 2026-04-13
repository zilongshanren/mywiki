---
title: 'Introduction to Kuma: Templates and scripts – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2012/08/introduction-to-kuma-templates-and-scripts/
author: Eric Shepherd
published: '2012-08-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

At just after 10 AM today, we switched over from our MindTouch based wiki to our new, Mozilla-built Kuma wiki platform for the [Mozilla Developer Network](https://developer.mozilla.org/), as I announced yesterday that we’d be doing. So far, all’s well!

Over the next week or two, I will be sharing a few suggestions, tips, and bits of advice about the new platform. This is the first of those posts. Today, I’ll be talking about the new template system.

**A little bit of history**

When we switched to MindTouch a few years ago, one of the key appeals was their incredibly powerful template system. This system made it possible to write complex scripts to automatically generate content. It could be used for everything from simply styling text to looking up information and generating complicated chunks of material. And over the years we used MindTouch, we grew to rely heavily on it.

A key requirement we had from the beginning was that Kuma support similar capabilities, and as a result, Les Orchard and the rest of our development team built [KumaScript](https://developer.mozilla.org/en-US/docs/Project:Introduction_to_KumaScript), an engine for building exactly this sort of scripting. KumaScript is, in essence, server-side JavaScript implemented using [Node.js](http://nodejs.org/), with provided additional routines to make it possible to access wiki data and inject material into page content at load time. It has powerful caching in place that make it work incredibly fast, and has proven to be an incredibly useful tool for us.

**Introduction to KumaScript**

If you’ve done any scripting on MDN in the past, you’ll have to adapt a little bit. Les wrote an excellent [guide introducing KumaScript](https://developer.mozilla.org/en-US/docs/Project:Introduction_to_KumaScript), and I can’t recommend it enough. If you plan to do any scripting, or are curious about the system’s capabilities, read that over.

The truly brilliant thing about KumaScript is that it’s fast and is all JavaScript syntax, so it’s incredibly easy to pick up. If you’ve done any web development, you can script on MDN. The only “trick” is that because it’s so powerful, we do require that you get special privileges to edit or create templates on MDN. You can [contact me](mailto:eshepherd@mozilla.com) to get those permissions.

If you’d like to take a look at existing templates to see how they work, there’s a page that [lists every template](https://developer.mozilla.org/en-US/docs/templates). Look them over and get a feel for things!

**About templates that are unconverted**

[#devmo](http://irc.mozilla.org/devmo) about this, or fix it yourself if you have the privileges and the time.

If you’d like to see a list of the templates that are known not to have been updated, [there is one](https://developer-new.mozilla.org/en-US/docs/needs-review/template)! If you update one, please toggle off the “Template review” checkbox at the bottom of the page and add the tag “ks-fixed” to it.

We have spent much of the last few months converting templates, and you shouldn’t run into pages with broken ones very often, but it absolutely can happen.

**Key differences you should know about**


- There’s no longer a weird syntax you have to use for templates with a dash (“-“) in their names. You can use them just like any other template: {{foo-bar(“some parameter”)}}.
- You can’t run KumaScript outside a template like you could with DekiScript. All KumaScript code must be in a template; MindTouch would let you run arbitrary script on any page. For security reasons, we no longer allow this. This does have the side effect of making it no longer possible to nest template calls; you can’t do {{foo(bar())}} like you could in MindTouch.
- You can use
[JSON as the only parameter to a template](https://developer.mozilla.org/en-US/docs/Project:Introduction_to_KumaScript#Using_JSON_as_a_macro_parameter). This gives you a way to create templates that accept, in essence, named parameters. - Although we’ve implemented
[clones of a number of MindTouch APIs](https://developer.mozilla.org/en-US/docs/Project:Introduction_to_KumaScript#Auto-loaded_modules)as a short-term solution so that we could get online, they should typically not be used by new templates. In addition, only APIs we actually needed have been implemented. From here on out, we will add new Kuma-specific APIs. - Templates are heavily cached. The output from a template is saved for every set of inputs it receives. If you change a template, it doesn’t get re-interpreted for a given set of inputs unless someone forces it to be by shift-reloading a page that uses it with those inputs; however, doing this does affect all users, not just you. This vastly improves performance but does mean you have the chance of template changes not being seen by everyone right away.
- Some locales’
[identifier codes have changed](https://developer.mozilla.org/en-US/docs/Project:Introduction_to_KumaScript#Changing_Locale_Identifiers). - URL paths have changed: instead of /en/JavaScript, for example, it’s now “/en-US/docs/JavaScript”. Server rewrite rules are in place to automatically redirect existing links, but new templates should do it the new way.
- You can’t apply a “nowiki” or “plain” class to text to keep it from being interpreted as a template anymore. Instead, add a backslash in front of the first “{” in the template invocation. This is useful when editing
[docs about templates](https://developer.mozilla.org/Project:en/Custom_Templates), for instance.

**Give it a try!**

That’s a quick overview of what KumaScript is and what’s different about it. There’s certainly a lot more to discover, so be sure to read the I[ntroduction to KumaScript](https://developer.mozilla.org/en-US/docs/Project:Introduction_to_KumaScript) and feel free to ask for help on IRC if you need it!

## 2 comments

Natalie GrossmanAugust 4th, 2012 at 00:40Jonathan KamensAugust 6th, 2012 at 16:45