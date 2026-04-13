---
title: Requirements and tips for getting your GNOME Shell Extension approved
url: https://blog.mecheye.net/2012/02/requirements-and-tips-for-getting-your-gnome-shell-extension-approved/
author: Jasper St Pierre
published: '2012-02-25'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

If you’ve written and submitted a GNOME Shell Extension, you’ve probably run across a reviewer saying that you shouldn’t do something, not even knowing what you shouldn’t have done beforehand. I’m sorry, the Shell team (including myself) hasn’t really done a good job documenting what a good GNOME Shell Extension should do, and we reviewers constantly run across the same mistakes in review.

I’m going to hopefully change this for the better by documenting most of what us reviewers look for when reviewing code. This isn’t meant to be an exhaustive list – even if you do everything in here, we still may reject your extension for other reasons. If it’s a code reason and it’s a common one, I’ll update the list.

This is mostly about GNOME-specific gotchas. Please attempt to write straightforward and clean code. Unravelling spaghetti is not fun for any of the extension reviewer team.

## Don’t do anything major in `init()`


`init()`

is there to have anything that needs to happen at first-run, like binding text domains. Do **not** make any UI modifications or setup any callbacks or anything in `init()`

. Your extension will break, and I will reject it. Do any and all modifications in `enable()`

.

## Undo all UI modifications in `disable()`


If you make any UI modifications in `enable()`

, you need to undo them in `disable()`

. So, if you add an icon to the top bar when your extension is enabled, you need to remove it. Simple. Failure to do so will be an immediate rejection.

## Remove all possible callback sources

If you’re writing an extension, you **must** disconnect all signals and remove all Mainloop sources. Failure to do so will be an immediate rejection. So, if you connect to a signal using `global.display.connect('window-created', onWindowCreated);`

, you need to disconnect it:

let _windowCreatedId; function enable() { _windowCreatedId = global.display.connect('window-created', onWindowCreated); } function disable() { global.display.disconnect(_windowCreatedId); }

The same goes for any timeouts or intervals added with the Mainloop module. Use `Mainloop.source_remove`

to make sure your source is removed.

## Extensions targeted for GNOME 3.2 cannot use GSettings

It’s unfortuate, but true. Extensions that target GNOME 3.2 cannot use GSettings when uploaded to the repository. It will crash the Shell. There are new APIs in GNOME 3.4 that allow us to work around this. The technique used most often is to have a bunch of `const`

statements at the top of the shell that the user can modify.

## A quick aside, a libsoup gotcha

function buttonPressed() { // This code will crash the Shell, do not use it! let session = new Soup.SessionAsync(); let message = Soup.form_request_new_for_hash('GET', 'http://example.com', {'beans': 'sauce'}); session.queue_message(message, function() { log('soup is so easy!'); }); }

While we really shouldn’t be crashing here, it’s a hard issue to fix. The technical reason is that when the session gets garbage collected, it calls back into all callbacks to let them know that the request is cancelled. Because the session is in destruction, this will crash gjs when it tries to find the object to pass to the callback.

A quick fix is to prevent the session from being garbage collected. Move it outside the function to get the correct behaviour.

const session = new Soup.SessionAsync(); // This makes the session work under a proxy. The funky syntax here // is required because of another libsoup quirk, where there's a gobject // property called 'add-feature', designed as a construct property for // C convenience. Soup.Session.prototype.add_feature.call(session, new Soup.ProxyResolverDefault()); function buttonPressed() { let message = Soup.form_request_new_for_hash('GET', 'http://example.com', {'beans': 'sauce'}); session.queue_message(message, function() { log('soup is so easy!'); }); }

And now, these aren’t required, but it helps me tremendously when reading extensions. Following these tips will likely get your extension approved faster.

## Consistent and appropriate indentation

If you indent your code properly and consistently, I don’t have to figure out which brace corresponds to what. Makes it easier for me to read code. It also helps if you follow the GNOME Shell’s indentation and brace style (4-space indents, braces on the same line), but I don’t want to start a flamewar in the comments section. If you like another indentation and brace style, use it. The important thing is that you are consistent.

## Removing dead and commented out code

If you know that some code you have is dead, remove it. If you’re using a modern VCS like git, you should be able to get it back at any point. Don’t leave a bunch of commented code in there for me to digest through.

Some kind of a markup error ([/js without a closing ]) in this post is making some of the text paragraphs be rendered as preformatted text with no line wrapping, which is very hard to read.

Whoops, fixed. Thanks for notiicing,

Great to see some guidelines on extensions to keep them save for users and helpful for developers!!

Wouldn’t make sense to add them on the upload[1] page itself? So that they can be cross-checked before the developer uploads the extension? It will be also easier to see which expectations are set upfront before submitting the extension.

Great job!!!

[1] https://extensions.gnome.org/upload/

I’ve just pushed a set of changes that did exactly this.

To avoid spamming GNOME mailing list, i may ask my question here : is there something new concerning the license thing ?

http://mail.gnome.org/archives/gnome-shell-list/2012-January/msg00005.html

hi, thanks for this, i second Gil’s sugestion – i am trying to upload extension and getting 500 error that doenst explain reason – i concluded that there must be some automated code checks in place that doenst allow me to upload extension, if this is a case it would be really handy to know the reason extension code was rejected – also do all clutter actors emit ‘destroy’ signal when actor.destroy() is called? will it be enough to call this.actor.destroy() to remove workId added to Main.initializeDeferredWork(this.actor, Lang.bind(this, this._redisplay));

or explicit this.actor.emit(‘destroy’) is needed? thanks for help

It’s not an issue with your extension, I broke the site by accident. It should be fixed now. And yes, all actors emit the destroy signal, an explicit emit is not needed.

hi, could you please expand section ‘Extensions targeted for GNOME 3.2 cannot use GSettings’ – my extension was rejected for this reason but i cannot see how i can use mentioned technique (it looks like i will have to write my own little version of gsettings and that is a lot of overhead) I have extension running on 3.2.2 with no problems – it enables/disables with no issues – so I belive there is issue for web-enabled installs. In this case could you allow manual extension installs by providing download link only and disabling ON/OFF web button for such extensions?

No, the entire point of the repository is to be web-installable. I will not provide a download button, and especially not promote an extension that would require root access to install and use properly.

Simply add some constants to the top of your GNOME Shell Extension. Look at how the dock extension manages settings on 3.2, for instance.

thanks, extension doesnt need root access to use, root access is only needed once to load schema entries into well defined and isolated place since your framework simply doesnt provide so much needed option – i cant be at fault here – example provided hooks into existing schema entry (getAppFavorites()) which was meant for other purposes (probobly overview dash) and in my opinion is all wrong – what if i now hook to the same entry and other extensions will do same? but even if i use it i could only have a copy of dash entries and nothing else – but i dont need a copy i need a seperate set of icons to operate with – providing constants is fine and i do have defaults already, but where to store users data that persists logouts and reboots without having dedicated schema entry?

They can edit the JS file. That’s what other extensions do, that’s what you’ll do… until 3.4, that is.

hi, i uploaded Light Overview extension over the weekend and in a process it was wiped out from my hard drive, wonder how can i get it back? would be ideal to have pending extensions listed in profile so i could grab it without bothering people but for a time being will you mind sending it over to myself? i sort of miss it :) thanks for understanding

hello, i am not sure about disconnecting from menu (submenu) items, let say in PopupMenu, menu item PopupSwitchMenuItem (psmi) is created and connect(‘activate’, …) attached to psmi – now if I delete psmi will framework automatically disconnect from ‘activate’ signal or do i have to handle disconnection myself? (some of the menus are dynamic, meaning their items are constantly rebuilt, in such a case manual coding to handle disconnections before item(s) are deleted is a bit troublesome (and in my opinion may be error-prone) – wonder if framework handles disconnections from menu items upon deletion or there are some plans to implement auto disconnections in a future? thanks

What about testing extensions ? As in, TDD.

What about it?

Is there any tool/library/framework to help doing unit testing targeting Mozilla’s JS-1.7/JS-1.8?

There’s JSUnit, of which gjs includes an internal copy of.

imports.jsUnit

Nice!

I have this situation. I created an extension. Uploaded it on https://extensions.gnome.org/upload/ . Now I wait for reviewing. Can I upload (upgrade) this extension before it changes status (because I found a bug in code, and added some improvement).

Sure, go ahead.

Hi. when i upload the new version of my extension throught the “Add Yours” [1] page (I didn’t find another way to upload the new version) it just reloads the page, and I don’t understand whether it’s the normal behaviour of the upload page or not. I don’t see a single “done” message or something like that, so I can’t know if the new version of my extension was been uploaded or not.

Can you help me please?

Thank you in advance

[1] https://extensions.gnome.org/upload/

No, that shouldn’t be happening. That is the correct place to upload a new version of your extension.

Well, the extensions works without problems on my 3.4 shell, and the metadata.json file seems to be ok and valid. I can’t get what’s wrong with my extension… any ideas?

How can I track my extension’s status which I uploaded?

Like rejected/pending/approved?

You couldn’t, until now! Check your profile. I added a few new sections for that.

I believe I’m seeing a strange behavior.

After submitting, I’m just being returned to https://extensions.gnome.org/upload/. No error messages, no changes in the list of pending extensions, no nothing.

Hm, that shouldn’t be happening… Can you email the extension so I can test with it?

I’d be glad to. But, if you can send me a first email (using the address that I’ve entered when posting here), it would help me quite a bit.

I’ve just wrote an extensions which realizes PanelMenu.Button as lgLoaderButton, just as DateMenuButton does. My question is, will connections to signals build in lgLoaderButton be destroyed when destroying the object, or I should destroy all the connections in disable function? Looking forward to your reply. Thank you for reading my post.

Regarding Code Review: I’m just getting started with GNOME Shell Extension development but would like to use GJS-CoffeeScript – is that ok or may it present a problem at some point?