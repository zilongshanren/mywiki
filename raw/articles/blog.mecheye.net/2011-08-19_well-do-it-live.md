---
title: We’ll do it live!
url: https://blog.mecheye.net/2011/08/shell-extensions-live-enable-disable/
author: Jasper St Pierre
published: '2011-08-19'
source_blog: Clean Rinse
source_site: https://blog.mecheye.net
category: graphics
fetched: '2026-04-13'
---

Live extension enabling and disabling has landed! This allows users to do this!

I could do that all day. It’s quite fun.

But there’s one little problem. Extension developers? We need to talk.

“What did I do?”

Nothing bad, I promise. You just have a new responsibility: in case the user doesn’t like the extension, you need to undo all the changes that you ever made to the shell. Make it look like your code never touched the place. Otherwise: that video above? The giant illusion will drop to the ground and crack into a thousand pieces. Like that China I broke last weekend.

“Uh, OK. How?”

If your extension [looked like this before](http://magcius.mecheye.net/shell/SweetTooth/Code/HelloWorld-Old/extension.js), you need to make it look like either [this](http://magcius.mecheye.net/shell/SweetTooth/Code/HelloWorld-Stateless/extension.js), or [this](http://magcius.mecheye.net/shell/SweetTooth/Code/HelloWorld-Stateful/extension.js).

Put simply: `main()`

, uh, how do I say this? `main()`

has been, uh, let go. Sure. Don’t worry though, he’s been replaced with `init()`

, `enable()`

and `disable()`

. They’re just as cool. I promise. The in-depth obitua — uh, termination notice [can be read here](https://mail.gnome.org/archives/gnome-shell-list/2011-June/msg00283.html). `init()`

‘s best friend, the “helper” object couldn’t make it for this trip. He’ll be here next year.

There’s three simple rules to take into account:

- There used to be one required method:
`main()`

. This has been removed. It has been replaced with a new hook,`init()`

. You should use`init()`

to initialize any state. Do not modify the Shell inside of this function. - The
`init()`

may return an object, called the “state object”. If you do not return an object, the module is considered the state object. This object is supposed to have two new methods:`enable()`

and`disable()`

. These should modify Shell in the appropriate way. For lack of better vocabulary, extensions which use the module (return nothing from`init()`

) as their state object are called “stateless” objects, and those which don’t are “stateful”. `init()`

is guaranteed to be called at most once per shell session.`enable()`

and`disable()`

may be called at any time. If your extension is enabled at the start of the session,`enable()`

will be called. If your extension is disabled at the start of the session,`disable()`

will not be called, and there is no guarantee that`init()`

will be called.

Additionally, keep in mind that Shell extensions are versioned, so only extensions that are targeted for 3.2 should port to the new API. Some extensions that want to support both 3.0 and 3.2. Fortunately there is an easy way to do *exactly* that. Just run `init()`

, and then `enable()`

:

` function main() { init(); enable(); } `


… Stateful extensions just need to run `enable()`

on their state object.

` function main() { init().enable(); } `


Oh, and one last thing. Thank you. You don’t have to believe it, but I’m doing this for you. I’m trying to make it easier for users to safely try out your awesome work. There’s more awesome stuff for you guys on the way. I promise.

Hello,

What about metada that was passed to the main() function ? Will it be the same with init() ?

I’ve currently delegated that to be the “helper object”, but right now it’s just the metadata — the same that was passed to main().

Hey Jasper ;) Looks like you are the only one on the planet who has any useful info about the new gs ext api :D

Many extensions are now broken with the 3.2 update – as you obviously know. Could you provide some links to the updated api (in full) so the rest of us can get in on the action and move things forward… ie unbreak stuff :)

cheers,

tAz

I’m unsure what you want me to link to. We currently aren’t publishing any API because, as you’ve found, it’s unstable. If there’s anything specific that you want, please hop on #gnome-shell on irc.gnome.org and I’ll do my best to answer you,

Thanks, your post helped me a lot! I heard about it, but couldn’t make the script work.

Despite unstable, I guess https://live.gnome.org/GnomeShell/Extensions should be updated : “The extension.js file is simply a JavaScript file; it must however have a function called main”

Thanks for the info! I updated the page.