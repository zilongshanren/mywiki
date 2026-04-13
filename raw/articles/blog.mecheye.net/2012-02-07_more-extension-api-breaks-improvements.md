---
title: More Extension API breaks/improvements
url: https://blog.mecheye.net/2012/02/more-extension-api-breaks/
author: Jasper St Pierre
published: '2012-02-07'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

Since [GNOME Shell Extensions](https://extensions.gnome.org/) launched, we’ve been overwhelmed at the response from the community. You guys are awesome, and I’m constantly impressed at what things you guys are doing with the Shell. I’ve been a bit behind on reviewing extensions and adding requested features to the website (I still need to get started on search and investigating some pretty big bugs), and I apologize. I recently landed a bunch of features to the review system to make it easier for me to review your extensions, such as rewriting the diff system. Hopefully things will go a lot faster now.

When [Owen Taylor](https://blog.mecheye.net/http;/www.fishsoup.net) first suggested the project, we worked out some basic sketches and built an overview for the site, but we didn’t want to change the extension API until we knew what extensions were going to need or want to do. As I’ve said before, I felt that we needed a co-operative live enable/disable system for asthetic reasons: the Shell isn’t the fastest thing at restarting, and a user having to spend ten or fifteen seconds to revert your system to the previous state after deciding that an extension sucks makes for a pretty poor experience. That was the only API break that I inserted into the extension system for 3.2, and it was purely to make sure that your extensions were presented in the best way possible.

## Multi-file extensions

The extension system in the shell really wasn’t designed for extensions that had multiple files. The many people that built the system had no idea that this clever hack would be commonplace. While I hate to break API, I’d say it’s for the better. Introducing the “`extension`

object”. Previous to now, we would construct a `meta`

object from your `metadata.json`

, install some random things into it and pass it to you, the extension, through the init method. Over time, we inserted more and more on the metadata object where it was this jumbled bag of things that the extension system added, and things that were in the metadata.json file. While adding a few more keys for the prefs tool below, I finally decided it was worth a redesign.

Here’s an example of the new system in action:

const Gio = imports.gi.Gio; let extension = imports.misc.extensionUtils.getCurrentExtension(); let convenience = extension.imports.convenience; Gio.app_info_launch_default_for_uri(extension.dir.get_uri(), global.create_app_launch_context()); let metadata = extension.metadata; Gio.app_info_launch_default_for_uri(metadata.url, global.create_app_launch_context()); function init() {} function enable() {} function disable() {}

Of course, you shouldn’t do these things outside of any user interaction, but a concise, imperfect example is better than one that misses the point by building an `StButton`

, sticking it somewhere on `enable()`

, and then removing it on `disable()`

.

You might notice that **you don’t get the extension object passed to you – you go out and grab it**. If you’re curious as to how we know what extension you are, [there’s some clever trickery involved](http://git.gnome.org/browse/gnome-shell/tree/js/misc/extensionUtils.js#n23).

What’s on this object? A bunch of stuff that used to be on the metadata object: `state`

, `type`

, `dir`

, `path`

, etc. When we introduce new APIs specifically designed for the ease of extension, this is that place we will put them. `metadata`

is now a pristine and untampered representation of your `metadata.json`

file, and we’re going to keep it that way.

## Preferences

One thing that we don’t really have an area for in the current 3.2 API is preferences. Unfortunately, GSettings was incompatible with extensions installed into your home directory (like extensions installed from GNOME Shell Extensions do). We couldn’t get this fixed in time for 3.2, but [Ryan Lortie](http://blogs.gnome.org/desrt/) spent a lot of his personal time fixing this, and I thank him graciously. **We now have a usable API for settings from extensions**. It requires a bit more code, as you can see in [gnome-shell-extensions’s convenience.js](http://git.gnome.org/browse/gnome-shell-extensions/tree/lib/convenience.js).

I spend a lot of my time looking at the code for extensions. Extensions have been shipping their own Python or gjs scripts that stick up a GTK+ dialog. Someitimes they built a configuration UI inside the extension with St. Sometimes they installed a .desktop file so that they would show up in the Applications section of the Shell. Sometimes they would insert a button to launch the script, or maybe they made users right-click on their item in the toolbar.

When Owen and I sat down to discuss this, we both decided **we need some consistent way for extensions to be configured**. Introducing the “GNOME Shell Extension Preferences” tool. It’s a new entry point to your extension – `prefs.js`

. [Here’s a simple prefs.js file adding support to the Alternate Tab extension](http://magcius.mecheye.net/shell/prefs.js).

I didn’t make it too fancy, and it’s entirely possible that Giovanni may want to make a better UI.

Your entry point is a function labeled `buildPrefsWidget()`

, and it should return some sort of GTK+ widget. Whatever you return from there will get inserted into preferences widget.

The combobox is for switching between extensions, and it’s ours. Otherwise, go crazy… the world below is your canvas. As usual, try to make it useful and pretty, but the reviewers on the extensions repo can’t and won’t discriminate against ugly UIs. **There is still a policy for this**, though: the widgets that you put in the preferences UI have to be related to preferences (I think I’ll allow version strings and other things though), and you should not walk up the GTK+ widget tree beyond your preferences widget (to adjust the combobox or manipulate any UI that is not yours). I’m looking forward to the neat things that you guys do with this!

“But how do I launch it?”

Oh, right. The tool is marked NoDisplay, so it won’t show up in the Applications menu. This is intentional. I’m currently working on a patch to SweetTooth so you can launch it directly from the website, provided the browser-plugin is installed correctly.

“Something broke, and I don’t think it’s my fault!”

I’m human. I make mistakes. You can let me know I was or am being a moron by [filing a bug for GNOME Shell](https://bugzilla.gnome.org/enter_bug.cgi?product=gnome-shell&component=extensions), or [filing a bug for SweetTooth](https://bugzilla.gnome.org/enter_bug.cgi?product=website&component=extensions.gnome.org). While I try to respond to everyone’s mail and read all blog comments, I regularly check my task list on these two things, so this is a better system for me.

“How do I try it out?”

Providing everything goes well, GNOME Shell 3.3.5 should be released tonight, which should have all this new awesomeness. If you want to test with the new browser-plugin stuff, you’ll need to copy the browser plugin from `gnome-shell/browser-plugin/.libs/libgnome-shell-browser-plugin.so`

to `~/.mozilla/plugins`

, and then restart your browser.

Is there a way to upload multiple versions of the same extension to extensions.gnome.org, so that an extension can be offered for multiple Gnome Shell versions (e.g. 3.2 and 3.4) at the same time?

Yep, just upload two files. Down at the bottom of your extensions page, you should see a thing that says “Shell Versions” – that maps a shell version to an extension version. You can manipulate the table with the “Activate” and “Inactivate” buttons above.

I would prefer user can install multiple version of extension for different version of shell, since upgrade gnome-shell is always need a re-login, and user might suddenly found all of his necessary extension not work. This is really even worse than firefox upgrade.

Or you guys should break API less, or provide backward compatible, but as far as gnome-shell is under active development this might be not quite possible.

This should be take into account before extension upgrade becomes a hell.

Yeah, I’ve been thinking about how I would make it so users can install multiple extension versions so they don’t have to swap directories, etc.

A way to provide preferences to extensions, finally!

Can you remind me again why it is that we have a nice, modern extension/plugin system called libpeas available for all gnome applications, but that shell feels it needs to reinvent, so that now we have two separate plugin systems…

The majority of the Shell is built with JS, and extensions need to be able to monkey-patch and manipulate that JS. libpeas, as far as I know, can’t do that.

I don’t know what that means, monkey patch.

Wikipedia has a decent article on the subject.

That’s just what extensions do anyway, and you can write them in js no problem. I don’t really see the argument.

I just checked. libpeas’s gjs loader creates a new GJS context, which means it won’t be able to interact with any objects created by the Shell’s JavaScript (Main.panel.statusArea is a popular example). So no, we can’t use libpeas.

Please not a combobox. Give it a treeview on the left, the one that has the inline [ + | – ] in other places at the bottom.

Maybe in the future. For now, a combobox was easy to hook up, so that’s what I did. Extension names are also quite long, so I’m not sure a horizontal layout would work well (or you would see “Alternate Sta…” all the time). And what’s the [ + | – ] for?

That’s great work, thanks for your efforts!

Why won’t this be available as a System Settings tool?

Because extensions are tweaks and are not considered configuration.

But who decided that they are tweaks. I (and I believe many others) believe that the extensions are 100% necessary for us to productively use Gnome 3.

If there were no extensions, I would not use Gnome 3.

Perhaps the users could be considered in that matter. Using Gnome 3 for the first time, it is hard to determine how to get started with these tweaks… and I’m sure many throw up their hands in frustration and decide to use something else.

I tried to start a discussion about putting this configuration in gnome-tweak-tool.

The discussion went nowhere. Not my problem I guess – see here if interested.

https://bugzilla.gnome.org/show_bug.cgi?id=668429

I’m unsure what you wanted from a discussion. I thought Owen described it pretty well – we don’t require gnome-tweak-tool to be installed to use the website, so any preferences tool launched from the website should be separate from g-t-t. If extension authors want their own logic, they should be able to write it in JS, not Python, so we’d need a separate tool anyway.

You’re certainly allowed to launch the preferences tool from g-t-t.

“they should be able to write it in JS, not Python, so we’d need a separate tool anyway.”

Yeah, that wasnt what I was close to suggesting. You two must have misread.

I was proposing giving extension authors an autogenerated configuration UI if they followed gsettings key naming conventions or shipped a whitelist of keys they wanted me to show.

Oh, that. Yeah, Owen and I decided early on that an autogenerated UI would be annoying at worst and mediocre at best.

I might as well be screaming into the wind. People want configurability. They want it easy.

Jasper, please please: Please tell me what is logic in not having something like extensions in the setting user interface? Is it just Gnome 3 developers being obstinate?

Awesome work… this is the killer feature of gnome3

Good news! next step : make this works with epiphany

Epiphany?

A bit off topic: i meant make https://extensions.gnome.org/ work with Epiphany web browser. When it will work we’ll be able to use the “save as a web app” Epiphany feature to make this site the best control center ever!

It should work with Epiphany. Make sure you have GNOME Shell 3.2.2.1

My mistake, excellent! actually the update just hit fedora!

Pingback: Liberados los nuevos GNOME Shell 3.3.5 y Mutter 3.3.5 | emsLinux

Pingback: Liberados los nuevos GNOME Shell 3.3.5 y Mutter 3.3.5 | El Blog de Rigo

Pingback: some useful links for gnome-shell-extension

Thanks for this post. It made me stumble upon https://extensions.gnome.org/ and I was amazed how easy it is to install an extension! Felt nice to see such an integration between a website and the desktop environment.

The extensions I liked instantly were the advanced volume controler and maximus. Felt nice to activate them :-)

But the on/off button in the nativ config gui is missing. I needed to go to the website to deactivate an extension. I consider this a bug (not filed yet, if someone will do it before me: thanks a lot, hero!) cause you need to be online to do something which could be done offline.