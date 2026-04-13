---
title: Random Wordpress Notes
url: http://hacksoflife.blogspot.com/2011/02/random-wordpress-notes.html
author: Benjamin Supnik
published: '2011-02-10'
source_blog: The Hacks of Life
source_site: http://hacksoflife.blogspot.com/
category: graphics
fetched: '2026-04-13'
---

If you put your news feed 'on a page' the page template is ignored - index.php is still used. I am sure this is by design, but I discovered it while creating a custom template. The page contents appear to be ignored too.

If you have an existing site and you want to merge in WordPress, you can do this:

- Host your news feed on a specific page, rather than letting it default to 'home'.
- Change the WordPress URL base (not install base) to your site.
- Put a mod_rewrite rule into your site root to rewrite missing files to /wp/index.php (or wherever WP is installed).
- If you want to replace an existing HTML page with a WP page you can use a rewrite rule from the old name to something like /wp/index.php?page_id=20 (or whatever page ID you want).

RewriteEngine Onmod_rewrite is pretty cryptic. Basically what this says is:

RewriteRule news.html /wp/index.php?page_id=5 [L]

RewriteCond %{REQUEST_FILENAME} !-f

RewriteCond %{REQUEST_FILENAME} !-d

RewriteRule . /wp/index.php [L]

- If the user asks for news.html, go to WordPress article 5.
- If the user asks for a missing file, let WordPress sort it out.

## No comments:

## Post a Comment