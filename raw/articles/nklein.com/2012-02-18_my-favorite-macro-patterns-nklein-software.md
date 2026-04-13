---
title: 'My Favorite Macro Patterns :: nklein software'
url: http://nklein.com/2012/02/my-favorite-macro-patterns
author: Pat
published: '2012-02-18'
source_blog: nklein software
source_site: http://nklein.com
category: game programming
fetched: '2026-04-13'
---

I read [Jorge Tavares’s article on Macro Patterns](http://jorgetavares.com/2012/02/13/macros-design-patterns/) a few days ago.Â I was thinking about replying to mention a few of my favorites:

- The
`with-`

pattern which makes sure a special variable is bound for the body and makes sure the tied resources are released at the end of the block. - Macros which collect content (usually into a special variable) so they can do something with the content at the end of the close of the macro.

Then, I was working on something tonight when I re-discovered a favorite pattern that I’d forgotten about: Putting multiple wrappers on the same body.

I am working on an HTML+JavaScript+CSS project. In the end, I need static files. But, I thought I would use the opportunity to really experience [CL-Who](http://weitz.de/cl-who/), [Parenscript](http://common-lisp.net/project/parenscript/), and [CSS-Lite](https://github.com/paddymul/css-lite).

I have now made a macro called `define-web-file`

which takes a CL-Who or Parenscript body and wraps it up as both a [Hunchentoot](http://weitz.de/hunchentoot/) handler and a `write-to-file`

wrapper. Now, I can test interactively with Hunchentoot and generate the whole web application when I’m ready.