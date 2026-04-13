---
title: Games as Applets 3
url: https://blog.gemserk.com/2011/02/10/games-as-applets-3/
published: '2011-02-10'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Following our Games as Applets series, we want to talk about the Wordrpess Page Template we are using in order to deploy our games as Java Applets inside the Blog.

### WordPress Custom Fields

When creating a new blog post or page, the creator can add metadata using [WordPress Custom Fields](http://codex.wordpress.org/Custom_Fields), to be processed later by the PHP templates associated. In our case, we are using the following custom fields:

- applet_height - height of the applet.
- applet_width - width of the applet.
- applet_screenshot - URL to a screenshot of the game
- jnlp_url - URL to the JNLP for launching the game.

### WordPress Page Templates

After adding metadata to our posts or pages, we need to make a [WordPress Page Template](http://codex.wordpress.org/Pages#Page_Templates) in order to process it. In our case, we created a PHP template for our games deployed as Java Applets using the structure explained in our last post about [Games as Applets](https://blog.gemserk.com/2011/01/21/games-as-applets-2/). Our games template looks like this [file](http://www.gemserk.com/things/game_template.php.txt).

Note: I didn’t want to put all the PHP file code directly in the post because it is too large.

This is how we get the post metadata:

<?php $jnlp_href = get_post_meta($post->ID, "jnlp_url", true); $applet_width = get_post_meta($post->ID, "applet_width", true); $applet_height = get_post_meta($post->ID, "applet_height", true); $applet_screenshot = get_post_meta($post->ID, "applet_screenshot", true); ?>

And this is how we pass the values to the javascript:

<?php echo ' ' ?>

Once the page template is created, if we want to add a new page for a game, we only have to select it from the templates list and voilá.

## Conclusion

Using WordPress Page Templates and Custom Fields, we can reduce the information of the game’s page to game’s related information only, and move all common logic and information between game pages to the page template.

This is how it looks to edit a game page:

![Game Page being Edited Game Page being Edited](../../assets/68ca81401de9b921.jpg)


Note: there is no applet tag or javascript in the page.

Also, if we modify the page template, we have all game pages updated, that could be really useful if you need to fix a bug or make an improvement to the page but could be a problem in case we introduce a new bug.

One problem not resolved yet is if you want to change the WordPress Theme, you will have to migrate the page template. I don’t know exactly if you can create a page template theme independent.

## References

- Games as Applets - </2010/12/30/game-as-applets/>
- Games as Applets 2 - </2011/01/21/games-as-applets-2/>
- WordPress Custom Fields -
[http://codex.wordpress.org/Custom_Fields](http://codex.wordpress.org/Custom_Fields) - WordPress Page Templates -
[http://codex.wordpress.org/Pages#Page_Templates](http://codex.wordpress.org/Pages#Page_Templates)