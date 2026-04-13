---
title: PardallMarkdown
url: https://alfredbaudisch.com/projects/open-source/pardallmarkdown/
published: '2021-09-17'
source_blog: Alfred Reinold Baudisch
source_site: https://alfredbaudisch.com
category: game programming
fetched: '2026-04-13'
---

**P ardallMarkdown** is a reactive publishing framework and engine written in Elixir. Instant websites and documentation websites.

**As opposed to static website generators** (such as Hugo, Docusaurs and others), with PardallMarkdown, **you don't need to recompile and republish your application every time you write or modify new content**. The application can be kept running indefinitely in production, while it **watches a content folder for changes** and **the new content re-actively gets available for consumption** by your application.

## Features

- Filesystem-based, with
**Markdown**and static files support.- Markdown files are parsed as HTML.

- FileWatcher, that
**detects new content and modification of existing content**, which then**automatically re-parses and rebuilds the content**.- There is
**no need to recompile**and redeploy the application nor the website, the**new content is available immediately**(depends on the interval set via`:recheck_pending_file_events_interval`

, see below). - Created with
[Phoenix LiveView](https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html)and Phoenix Channels in mind:**create or modify a post**or a whole new**set of posts**and they are**immediately published in a website**. Check out[the demo](https://github.com/alfredbaudisch/pardall-markdown-phoenix-demo)repository.

- There is
- Support for the content folders outside of the application, this way,
**new content files can be synced immediately from a source location**(for example, your computer), and then picked up by the FileWatcher. - Automatic creation of
**table of contents**from Markdown headers. **Infinite content hierarchies**(categories and sub-categories, sections and sub-sections).- Different
**sets of custom hierarchies**and post sets. For example, a website with*Documentation*,*Blog*,*News*and a*Wiki*, which in turn, have their own sub-hierarchies. **Custom sorting rules**per hierarchy set. For example, posts in the*Documentation*hierarchy can be sorted by priority,*Blog*posts by date and*Wiki*posts by title.

- Different
- Automatic creation of
**taxonomy trees and content tress**.- Separate content trees, per root hierarchy are also created. For example, a content tree for the
*Documentation*hierarchy, which contains links to all sub-hierarchies and posts.

- Separate content trees, per root hierarchy are also created. For example, a content tree for the
- Automatic creation of
**post navigation links**(next and previous posts). - Freely embeddable
**metadata into posts**as Elixir maps. - Hierarchy
**archive lists**. - All the content and indexes are kept in an
**in-memory cache (Elixir's ETS)**.

- Blogs
- Documentation websites
- Wikis
- FAQs
- Any kind of website actually? Even e-commerce websites, where you can use PardallMarkdown's parsed content as product pages, and more.
- Any application that needs content?