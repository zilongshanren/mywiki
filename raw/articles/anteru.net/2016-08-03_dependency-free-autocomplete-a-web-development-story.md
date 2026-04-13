---
title: Dependency-free autocomplete - a web development story
url: https://anteru.net/blog/2016/dependency-free-autocomplete-a-web-development-story
published: '2016-08-03'
source_blog: Anteru's blog
source_site: https://anteru.net
category: graphics
fetched: '2026-04-13'
---

This week I’ve updated the search box on my GPU database. Previously, there were two search boxes – one for ASICs, one for cards – and the autocompletion was done using jQuery UI. For that, I had a simple REST API hooked up was easy to reach from jQuery UI, and you’d get the results instantly while typing. Selecting one result and hitting enter would get you to the page, so everything was fine. Well, mostly. Turns out, the front page of the GPU database is really tiny in terms of HTML and script code. Pulling in jQuery, jQuery UI, and the jQuery UI CSS is pretty huge compared to the rest of the page. Even a minimized jQuery UI with only the autocomplete ticked is around 45 KiB for the CSS and JS alone, and jQuery adds another 32 KiB on top. For comparison, the GPU database landing page is 0.94 KiB, the CSS is 1.15 KiB, and the (new script with autocomplete) is 12.41 KiB (and that is not minified). That’s less than 15 total - compared to 77 for jQuery and its dependencies. Moreover, there’s no access to external web pages to fetch jQuery from a CDN, which increases loading time even more.

The requirement list was pretty simple:

Must work with keyboard (i.e. cursor up/down, enter)

Must also work with mouse (and only one thing must be highlighted)

Must be able to carry some additional data for each option (so I can
actually use it instead of going to a generic search page)

Notice that 3. isn’t a super-hard requirement – it does simplify life however a bit.

And here’s how the final solution looks like, before we go onto a detour on our way towards it!

The final product -- user types into the input field, autocomplete shows up, can be navigated using the cursor keys, etc.

The <datalist> fail

Technically, <datalist> is exactly what I should need. It’s the HTML5 way of providing autocomplete hints to the user. The way it works is you provide a <input> element, set the list attribute on it and make it point to a <datalist>. Inside the <datalist>, you provide the options. The list itself can get populated using AJAX, so everything seems easy enough.

And in fact, I got that one working pretty quickly. But it turns out there’s a few ugly things about <datalist>. To start with, it’s designed for completion only – that is, expanding text. It’s not designed to provide additional data. The way I solved this is to add an event handler to select on the input, and once that happened, I’d go through the list of items and search for a matching entry, and if I found one, I assumed that’s the selected one and would pull the data from there.

Well, all good, except select doesn’t trigger on Chrome, only Firefox. Wrap a form around it, handle submit, and there you go. Except that Chrome (as of today) has a quite … erm, unhelpful implementation of the completion.

Let’s assume for a moment I have something like this:

If I type Fury into the input field, what would you expect? If you want to give it a shot on your browser, try this Plunker demo. Turns out, on Firefox, it does autocomplete no matter where the string appears in an option, but Chrome only autocompletes if the option starts with the string. Which makes it pretty much useless, as graphics card names tend to have a boring prefix …

Ok, so let’s roll it on our own – how hard can it be, after all?

100% custom

Given the fail with <datalist>, we’re going to do it “old-school”. Below the input field, a <div> is placed, matching the size exactly. We hook input on the input field (as well as focus) and run the autocomplete core loop there. Which is pretty simple:

Send a XMLHttpRequest to get suggestions

Build a list

Clear the <div> and put the freshly built list into it

That gives us a basic autocomplete. Well, not so fast. It only solves 2. – selecting by mouse. Selecting by cursor keys doesn’t work, the list is very long, it does not disappear when the user clicks elsewhere … let’s get on those problems.

Focus & blur

On blur, we just hide the input list. Done. Except for one small thing – this does break on Chrome when you click on a link inside the autocomplete suggestions. What happens is that mousedown triggers, then blur triggers – hiding the list – and then mouseup and click follow. By the time you get to click, which would follow the link, there’s nothing left to click. Of course, it works in Firefox … the solution is pretty simple though, add a new event listener on the element for mousedown and just call preventDefault on the event. That fixes it for Chrome, and we got this part working!

Keyboard handling

While we’re on the list, we want to navigate through it using the keyboard. This means we need to hook up the cursor keys and enter. It’s pretty straightforward, just hook up to keydown event and then we’re going to store currently selected item somewhere and add/remove classes as needed.

inputBox.addEventListener('keydown',function(ev){switch(ev.key){case'ArrowDown':{ev.preventDefault();// Update indexreturn;}// Similar for up}},true);

And indeed, this would work, if not for Edge, who decided that ArrowDown (as the spec hints at) is not the string that should be used for the arrow down, but instead, Down. Of course the answer is to use the keyCode or just add another case. I used another case, to improve maintainability (if you want to look how different browsers interpret key codes, check out this huge table of which code maps to which key on which browser).

So this is solved now. We can navigate using the keyboard. Let’s hook up the mouse next.

Mouse handling

Handling the mouse might seem easy to do by hooking up mouseenter but that’s not going to fly. If the list scrolls due to keyboard events, then the mouse event will fire, and suddenly you’ll have two items selected. This is not an uncommen problem: As of today, the Angular autocomplete has this issue. Select an entry using the keyboard, mouse over another, and you have two selected, and god knows where you’ll go if you press enter.

The solution I use is to handle mousemove on my element, and also checking for the mouse move delta. Only if the cursor was actually moved, the selection changes, so basically whatever was used last (mouse or keyboard) decides what’s selected.

Scrolling

Wait a moment, I just said when an entry scrolls under the mouse. That’s another missing bit. So far, the autocomplete <div> was basically the size of the autocomplete list, but what if we add a max-height on the <div> to ensure it doesn’t go crazy long?

Now we need to make sure that if we navigate using the keyboard, the entry is actually visible. Thank god there’s scrollIntoView which is all we need. Except it’s not quite what we want. The problem with scrollIntoView is that it’s not 100% standardized and at least the Firefox implementation scrolls the container down until the item you called scrollIntoView is at the top of the container (or the container is already scrolled to bottom). This is pretty bad for two reasons. First of all, if you have 5 items in view, and your selection moves from the first to the second one, it will scroll even though no scrolling is needed (so you loose context). Second, if you mouse over, and it scrolls to the item selected by the mouse, hilarity ensues … so you’d have to special case it for selections triggered by mouse and those by keyboard.

The way I solved it is to scroll “on-demand”, that is, only if the item would go out of scope, and only from keyboard. The assumption is that you can always see the item you want to work on, so scrolling one item up or down is safe.

Wrapping up

Whew, that was a lot of stuff for a seemingly simple feature. The lesson here is that a lot of the user experience things are not obvious right away. On the desktop, we’re used to good user experience because it’s all taken care of by the OS or GUI toolkit. On the web, we only got a few basic things to work with and building a more complex user experience requires quite some work and attention to detail. Even then, my solution as presented here has some accessibility shortcomings which I hope to fix at some point. For instance, a user with a screen reader will probably fail to use the up/down keys to select an item. This means I should probably have a fallback path – for example, a form submit handler which goes to a separate page which then redirects if the entry did match directly, instead of relying on the fact that the user selected the item from the list in one way or another.

Interestingly, the complete solution so far clocks in at roughly 150 lines of TypeScript. This seems quite reasonable for being able to get rid of jQuery and improve the loading times significantly. It also resolves all three requirements that I have, which the previous solution didn’t, so there’s that that :)