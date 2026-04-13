---
title: 'An Emacs Tutorial: Beginner''s Guide to Emacs'
url: https://www.masteringemacs.org/article/beginners-guide-to-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

Emacs is a complex beast with tens of thousands of commands and even more settings that you can customize. No wonder so many people find it difficult to get their footing and opt for simpler editors.

But learning Emacs is more than just memorizing key bindings and commands. That’s just one part of it. You’ll also have to contend with a radically different way of thinking about how you interact with text. But more on that later.

Emacs is more than forty years old. It predates graphical user interfaces and almost all common computing standards we now take for granted. Emacs is also built around the idea that your freedom to edit or change anything is sacrosanct: at no point will Emacs attempt to hide any part of its inner workings from you. That may seem like a weird flex, but it matters.

Emacs is the editor of tinkerers and artisans; those who are eternally dissatisfied with all other tools because of their adamantine rigidity. Crafting, or shaping, your tools to meet your exacting needs is what Emacs excels at. Because of that, Emacs is – much to the chagrin of everyone who picks it up for the first time – squarely aimed at people who already know Emacs.

That’s right. Emacs is notionally built for people who have already learned Emacs. That’s not to say Emacs is hostile to new users: quite the contrary. Emacs has meticulous documentation: it has a 350,000 word manual and it is self-documenting. Every key and command – and everything in-between – is cross-referenced and easily looked up.

So, overcoming the initial hurdle of understanding Emacs is not an insurmountable task. But you will need to learn some terminology, as Emacs has its own naming conventions; basic movement and editing, so you can get around and benefit from Emacs’s superb text editing capabilities; a touch of philosophy, so you know why Emacs behaves the way it does; and enough knowledge to ask Emacs the right questions.

The latter is *especially* important. The difference between someone who *knows* Emacs and someone who does not comes down to that. Not how long they’ve been using Emacs, and not how snazzy or personalized their Emacs is.

When you can ask Emacs the right questions then – and *only* then – do you know Emacs.

## Philosophy

Emacs is the extensible, customizable, self-documenting real-time display editor.


What you just read is Emacs’s tagline and a one-line summary of everything Emacs stands for:

- Emacs is Extensible
-
Emacs is a tiny C core that forms the foundation of how it interacts with your operating system. The core is several hundred thousand lines of C code.

The rest is written in Emacs Lisp – that’s what you’re likely to interface with directly as a user and developer – and is more than a million. Community packages add up to millions of lines of code also.

Although you can easily recompile Emacs from source, the guiding philosophy is that anything that a user would reasonably want to modify belongs in the Lisp layer.

Extending Emacs is as simple as writing a little bit of Lisp and evaluating it from inside your running Emacs instance.

- Customizable
-
Like all sufficiently complex programs, Emacs has switches you can tweak — tens of thousands of them, in actual fact.

You can customize – either using some of Emacs’s many formal customizable options, or with a sprinkling of Emacs Lisp – nearly everything.

And I don’t mean it like the incredulous claims people made about Linux in the 1990s that “anybody can, you know, just download the Linux kernel and hack on it.” Sure, you can; but how many improvements can you make to the kernel’s USB driver or memory manager?

Emacs is designed with customization in mind. And there’s a low skill barrier: even users with little or no Emacs knowledge can come away and feel like they’ve personalized their Emacs. In fact, you don’t even need to write code to change many aspects of it.

Combine that ease of use with Emacs’s inherent extensibility, and it’s easy to conjure up a set of changes that enable you and perhaps your coworkers to accomplish something that you couldn’t easily do before.

- Self-documenting
-
Emacs is self-documenting. When you write code or extend Emacs, it’s customary to summarize what your code does as a

*documentation string*. Emacs pioneered*docstrings*in the 70s, and today it’s supported by most modern programming languages.My point is that you can always ask Emacs for help: from the mundane to the esoteric. Emacs is built around the idea that it’s

*introspectable*.Emacs’s answer is always correct because it’s querying its internal state. So if you rebind keys or customize a variable, Emacs knows about the changes.

Almost all variables and commands are not only documented, but cross-referenced with Emacs’s manual.

- Real-Time Display
-
Although this part may not be a distinction worth talking about today, editors in the 70s operated on lines instead of the whole screen. As a user, you’d edit only one line of text at a time — and even then, the act of editing, displaying, and typing were separate tasks!

Emacs broke the mold a bit here by being a

*screen-based editor*instead of a*line-based editor*.Line editors still exist today: the tool

`ed(1)`

is one such example. I would heartily encourage you to try out`ed`

on the command line and marvel at how far we’ve come! - Editor
-
Emacs is a fantastically advanced text editor, capable of both basic and advanced movement and editing.


## Terminology

You’re going to come across a handful of words that mean something other than what it does in other tools.

### What is a Buffer?

A buffer is where you read or write text. It need not be a file; it could be a temporary buffer that you created just to store snippets of text that you want to modify. In Emacs a buffer is also the medium you use when you communicate with external processes, like a Python shell, or maybe the bash shell.

When Emacs has to communicate via the network or a background process – common if you regularly use tools like LSP, bash or write email in Emacs – then Emacs will also use a buffer. Those buffers are all visible and accessible to you, the user.

If you are a computer programmer (or a floor cleaner, I guess) you may already believe you know what a *buffer* is, but in Emacs the technical concept that programmers call *buffers* is an unimportant detail, and you should instead think of a *buffer* in Emacs as a vessel into which you or Emacs itself pours text and images for later consumption by you *or* Emacs.

A buffer, then, is a Swiss army knife, and it’s so much more than just a “file”. It is used for all forms of communication in Emacs; it is also the primary way you programmatically edit text, by issuing commands directly to a buffer instead of editing *strings* like you would in most other programming languages. So when you edit text as a human, you’re often using the same commands that an Emacs Lisp programmer would use to do the same thing with code. [Why Emacs has buffers](https://www.masteringemacs.org/article/why-emacs-has-buffers) explains in great detail why Emacs’s buffers are the way they are and why it’s such an awesome concept.

### Frames and Windows

In Emacs, the definition of frames and windows are reversed. What you would normally open and close; minimize and maximize; and drag around on your screen is a *frame* in Emacs parlance. And in Emacs, a *window* is the bit of the *frame* that displays a buffer. In Emacs, you can have as many windows in a frame as you like.

Emacs is a tiling window manager onto itself. When you split a window in Emacs – like with `C-x 2`

and `C-x 3`

, or at Emacs’s insistence if you run certain commands – you’re creating *windows* inside an Emacs *frame*.

You don’t have to use frames if you don’t want to. Emacs’s own window management is good enough for most. Of course, if you *also* use a tiling window manager, you could use Emacs’s frames as you already have a tool that can handily manage them.

### Modeline, Echo Area and Minibuffer

The echo area is the void at the bottom of your Emacs. There’s only ever one, no matter how often you split your windows. The echo area is where Emacs displays messages that it thinks you should know about. Larger messages, or if there is a sudden rush of incoming messages, also end up in `C-h e`

.

Contrast that with the mode line: each window gets its own mode line. The mode line contains information about the buffer currently shown in that window.

The minibuffer and echo area share space. When you’re prompted for action by Emacs, you’ll typically be asked to answer in the minibuffer. The minibuffer, as its name alludes to, is… a miniature buffer. So, it behaves like most other buffers in most respects.

### Command vs Function

A command is a *interactive function*, but not all functions are commands. A command is something you can interact with in `M-x`

. Functions are not executable from `M-x`

.

A command is sometimes bound to one or more key bindings. You cannot bind a function to a key; only interactive functions – commands – can.

### Major and Minor Modes

A major mode imbues a buffer with the capabilities it needs to do a particular job. When you open a `.c`

file, Emacs activates the C major mode. When you open a `.org`

file, it activates the Org major mode.

Major modes govern how a buffer behaves. You can only have one major mode active in a buffer at a time. Minor modes, by contrast, bear no such limitation. You can have as many minor modes active as you like. Minor modes usually enrich your Emacs experience in some way. Some are specific to one buffer, and others are effectively global and always on.

### Point and Mark

The point is your cursor caret. Simple as that. The mark is a transient beacon that Emacs sets when you activate the region (selection rectangle) and is always on the other side of the region to your point. Together they form the beginning and end of the region.

Marks are also placed when you invoke certain commands in Emacs, and using `C-u SPC`

cycles through the marks in the reverse order they were placed, with the first being the most recent.

### Killing and Yanking

Emacs’s clipboard – the *kill ring* – does not work the way it works in other editors. Killing (cutting) text appends to the same clipboard entry if you successively kill text; the chain – and the clipboard entry the text goes into – is only broken when you ‘break’ the chain of kill commands. You can break the chain by invoking a key binding or command that does not kill text.

Thus, calling `M-d`

(delete forward word) three times in a row creates a single kill ring entry containing the three words.

Yanking – pasting – text is also unique in Emacs. Emacs does not ‘forget’ kill ring entries. They are instead added to the end of a ‘ring’ of other killed entries. You can recall previously killed items with `C-y`

followed by `M-y`

to cycle through your kill ring.

It’s worth noting that, although a bit hard to get used to, this approach makes it all but impossible to lose information! Emacs will never knowingly junk a clipboard entry. Only when you exceed the very generous (and configurable!) limit on the number of kill ring entries will Emacs discard items.

### Undoing Information

Like the kill ring, Emacs’s undo ring works in much the same way, but with an important and critical distinction: the act of undoing something is *itself* an action that you can undo! So if you undo three times in a row with `C-_`

or `C-/`

then Emacs will add three undo entries to – in effect redo – the previously undone actions.

Like the kill ring, it’s almost impossible to lose information in your undo ring, no matter how convoluted your undoing and redoing is. By all means undo 15 times; write more text; undo *that* text and the 15 undone steps and you’ll wind up where you started.

It’s an unfathomably powerful feature.

## Movement and Editing

If you’re new to Emacs, by all means use the arrow keys if that is what you are used to. You can slowly shift to Emacs’s way of navigating once you’re comfortable.

I’ve written a separate article about [Effective Movement](https://www.masteringemacs.org/article/effective-editing-movement) with a good overview of how you can improve your Emacs movement skills.

## Asking Emacs for Help

Asking Emacs questions is how we all – regardless of skill level – discover new features or learn how to operate or interact with the ones we already know about.

Here are the most important things to remember when you need help:

Memorize

`C-h r`

, which is also bound to`M-x info`

or`Help -> Read the Emacs Manual`

in the menu bar. This is Emacs’s manual and it is*very*detailed.It’s organized by subject area, so you can find what you are looking for.

You can also go to

`Help -> Search Documentation`

and search, not only the manual, but also Emacs in a variety of ways.If you know a key, and you want to know what it does, type

`C-h k`

(or`Help -> Describe -> Describe Key or Mouse Operation`

) and then the key you want*describe*. Emacs then tells you what it does.Note that it’s contextual: make sure you run it in the buffer you intend to run the command! It may not execute the same command in other buffers!

If you know the name of a function or a command, and you want to know what it does, then

`C-h f`

(or`Help -> Describe -> Describe Function`

) works well. You’re then treated to a*documentation string*of the function along with any keys it’s bound to.You can press

`i`

(Emacs 28+) to open the corresponding manual page, if any, for that function.The manual is often more detailed and will usually feature other, similar, functions on the same page.

You can ask for help about the active modes in your current buffer by typing

`C-h m`

(or`Help -> Describe -> Describe Buffer Modes`

)The information shown is a list of active minor modes along with (possibly many) tables of major and minor modes commands and their key bindings. It is a useful source of information, particularly when you are exploring.

On your journey to mastering Emacs, the first hillock you’ll have to climb is memorizing some of the fundamental key bindings used in Emacs. The

`M-x help-quick`

command (bound to`C-h C-q`

) pops up a little window with a bunch of the most common key bindings you should learn.

## Customizing Emacs

You can customize Emacs with elisp or with the builtin *Customize* interface. I recommend you use the builtin interface unless you’re keen on learning Emacs *and* Lisp at the same time!

You can invoke the Customize interface by typing `M-x customize`

. Try it. Browse and go ahead and change things — you’re at no risk of breaking things, as it’s easy to revert or discard changes you don’t like.

If you have a vague notion of the group you want to customize, you can also use `M-x customize-group`

and TAB completion. If you prefer a tree-like structure, you can give `M-x customize-browse`

a try. Personally, I like the detailed descriptions found in `M-x customize`

.

There are tens of thousands of customizable options. Might I recommend that you tweak as you go along? By all means start changing things left and right, but without a solid idea of what you’re looking for, you are – trust me here – drinking from the fire hose.

I recommend you familiarize yourself with the UI. It’s not the prettiest, but it’s solid, and it supports a dizzying array of different configurations. And don’t forget, applying an option is not the same as saving it!

If you’re experimenting, I recommend you don’t save until you’re sure it’s a change you like.

When you are ready to save to your changes, type `M-x customize-save-customized`

and Emacs saves all your changes. `M-x customize-save`

and `M-x customize-unsaved`

show a list of changed and *saved* and changed and *unsaved* customizations, respectively.

So if you screw up or you don’t how know you got Emacs into a state you don’t like, just revert the changes. Simple as that.

If you know the exact name of a variable you want to change, you can use `M-x customize-option`

to edit just that option. This is perhaps the most common way to apply changes you find elsewhere on the internet, other than inserting Lisp snippets into your `init.el`

file (and more on that below.)

#### Searching for Options to Change

There’s several *apropos* commands that search the entire space of customizable options. `M-x customize-apropos-options`

is one of them. If you want to find stuff related to indentation, then searching for `indentation`

is one way to uncover options related to that.

Another is `M-x customize-apropos-groups`

which does the same, but only for group names.

#### Applying One-off Changes

Here and in my other articles I’ll occasionally throw out a suggestion for a command you want to change, or how you enable a mode.

One example is `M-x fido-mode`

, an intelligent search-as-you-type framework. If you were to just type it into `M-x`

then it’ll work great until you exit Emacs. At that point it, or indeed any other change you’ve made but haven’t explicitly saved, is lost.

How do you fix that? You can add it to your `init.el`

file in `~/.emacs.d/init.el`

*or* you can check and see if it’s supported by the customize interface: `M-x customize-option RET fido-mode RET`

.

And sure enough it is — try it!

Not every option is customizable. It’s down to the author of the library to decide if it is or not. If it’s missing from the customize interface, then it’s possible Emacs does not know how to customize it. In that case you have to write Lisp instead, or possibly load the library or module explicitly first, as Emacs only loads modules that it needs.

#### Personalizing Emacs’s Colors

To do this effectively, I recommend you put the point (cursor) over the color you want to change and type `M-x customize-face`

. You may find that some colors inherit from others; that’s normal.

You can place your point over the name of the *face* it inherits from and type `M-x customize-face`

(or just type it in manually – up to you).

#### Changing Emacs’s Font

The simplest, no-effort way to tweak Emacs’s default font(s) is with `M-x customize-group RET basic-faces RET`

. The one named `Basic default face`

is the garden-variety font Emacs should use for most things. That’s a good place to start.

You can also pick `M-x customize-group RET faces RET`

and you’ll see the full list of *all* faces in use. It’s organized by group, so you can also click the `faces`

hyperlink from within `M-x customize`

.

#### Changing the Color Theme

If you dislike Emacs’s default color theme, and you don’t want to personalize it yourself, you can change it with `M-x customize-themes`

. There are thousands of themes around the web; so feel free to have a look around.

## Avoiding Bad Habits

There is a tiny minority in Emacs that dispense [bad advice](https://www.masteringemacs.org/article/bad-emacs-advice). Their advice is well-intentioned, and I firmly believe they think they’re being helpful, but it’s partisan and damaging to new users’ learning.

Here’s a brief list of bad advice and habits you should avoid doing:

- Disabling the menu, tool and scroll bars
-
There’s a lot of good advice out there. And then people round off an otherwise fine article or suggestion with “oh yeah turn off the menu bar!”

Don’t turn off the menu bar until you’re 100% confident that you know how to do most of the things in it! The menu bar is contextual, and will update depending on the major and minor modes of the buffer you’re editing.

- If you’re stuck and need help, then check out the
`Help`

menu entry. - If you forgot how to save a buffer, then look in the
`File`

menu entry. - Can’t remember how to switch buffers? The
`Buffer`

menu entry is there to help. - Curious about all the different things Emacs can do? Have a look in
`Edit`

or`Tools`

. - Not sure what you can do when you’re editing an Org Mode file, or a Python file? Well, guess what. There are
`Python`

and`Org`

entries to help you get started.

If you’re starved for space, you can disable the tool bar. But it’s also contextual; so keep that in mind.

The scroll bar is often used as more than just a navigation aid: it’s a visual aid also, that shows how far down a buffer you are.

Once you’re comfortable and familiar with Emacs’s basics, by all mean disable it and selectively enable it by pressing

`F10`

. - If you’re stuck and need help, then check out the
- Avoiding the mouse
-
Yes, the mouse is a great way to slow everything down, and it also contributes to RSI, tennis elbows and whatnot. The keyboard is naturally better at text editing than a mouse.

But it’s not

*useless*in Emacs; in fact, most things have useful keyboard*and*mouse shortcuts. And if you’re the type that likes to lean back in your chair when you’re reading text, then it’s nice to know that your scroll wheel works fine, right?Although I would encourage you to learn how to use Emacs without reaching for the mouse, it

*does*have a place. Navigating the info browser (`M-x info`

) is one such example where a mouse is handy if you’re still finding your footing with Emacs’s key bindings. You can jump between the hyperlinks with`TAB`

– or just click them.You can also click on stuff in the mode line (the bar at the bottom) and customize things that way also.

Emacs 28 adds

`M-x context-menu-mode`

that adds contextual menus to your right mouse button, but it is not enabled by default. (To do so, type`M-x customize-option RET context-menu-mode RET`

.)The context menu is another way to learn more about Emacs: through contextual suggestions.

- Ditching all of Emacs’s key bindings
-
There is nothing wrong with Emacs’s default key bindings. They have been around for decades, they work well, and it is what 98% of all Emacs users continue to use all day, every day.

By all means change the ones you dislike to something else! But I would discourage you from buying into the dismissive and loud vociferations of, particularly a small subset of eager Vim users, who think Emacs’s approach to text movement and editing are slow, ineffectual, or both. They’re of course entitled to their opinions, but many of them have adopted Emacs and use Vim key bindings inside of it and have never actually made an effort to learn how Emacs works.

Expert Emacs users move around with dizzying alacrity. The only thing stopping me – as a veteran user of 20-odd years – from going any faster is literally the speed with which my brain can synthesize instructions to give my hands and fingers. I already type at 100 words per minute — I’ve enough finger dexterity, but I wouldn’t turn down a faster brain!

Emacs is a superb text editor, capable of both scalpel-like precision editing all the way up to sweeping bulk edits spanning hundreds of files. And with Emacs’s hyper-advanced keyboard macro recorder, you can trivially automate frequent actions – no Lisp skills required.

I recommend you also read my article on why

[keyboard macros are misunderstood](https://www.masteringemacs.org/article/keyboard-macros-are-misunderstood)to firmly grasp just how crazy powerful Emacs’s keyboard macros are. - Not using the Customize Interface
-
Ask Emacs propeller heads about the

*Customize*Interface and many of them sneer at it. Their arguments distill down to a dislike of the “interface” part of*Customize*; that it generates hard-to-read elisp (not true!); or that it’s confusing or doesn’t teach users Lisp. Pah!Yes, the UI is baroque, but it has to work with a dizzying array of configurable options – and some of those options are structurally complex that it’s small miracle that it even works as well it currently does.

The Customize interface works just fine, and it’s got a large array of helper commands: like applying but not saving changes, so you can try them out; or showing all the customizations you’ve made so you can easily tweak or undo them. It also comes with excellent search functions, and you can easily tweak individual options using

`M-x customize-option`

and friends.For a beginner it’s an invaluable tool. But it’s not a

*requirement*: you can write Lisp instead! And if you prefer doing that, then by all means go ahead.But please consider whether the people dispensing this advice (it’s sadly far too common) have

*your*best interests at heart as a novice Emacs user. - Adopting a Kitchen Sink Starter Kit
-
There’s a large body of

*starter kits*– collections of packages and tweaks to Emacs – that you can try out.They have their place. They’re a great way to explore Emacs through the tasteful (or not so tasteful) choices made by other people.

You should definitely check out these ones:

They add, without taking away, from Emacs. They’re built around the idea that, although it’s a kit authored by someone else, the kit should remain easy to modify and understand by you, when you’re ready to take that next step.

- Running Emacs in a Terminal
-
To be clear: there’s

*nothing wrong*with Emacs in a Terminal. It works really well. But there are certain key combinations that you cannot enter in a terminal due to historical limitations*in the terminals*and not in Emacs.You’ll also lose out on Emacs’s native support for PDF, Word Document and Image support. And you won’t benefit from fancier things like text ligatures, icons or contextual fonts and variable font sizes.

If you regularly edit things on remote servers, you should instead look at

[Tramp](https://www.gnu.org/software/tramp/). Emacs has remote editing capabilities built in.

## Emacs’s Package Repositories

I would encourage you to explore Emacs’s package repositories. There is one third-party repository called [MELPA](https://melpa.org/) and two builtin repositories. The default repositories are much smaller; you should enable MELPA.

You can browse the package repositories by typing `M-x list-packages`

or selecting it from `Options -> Manage Emacs Packages`

.

Note that, if you install packages, that they may not activate nor give any indication as to how to run them. Some require configuration before they’ll work. I heartily encourage you to visit the associated `Website`

when you browse the package description!

## CUA Mode: Emulating a Regular Clipboard

Emacs reserves `C-x`

, `C-c`

and `C-v`

for its own operations. But they conflict with the clipboard shortcuts you may know and use in other programs. You can use Emacs’s emulation layer, CUA Mode, to recover some of the features of the common clipboard system. To enable it, type `M-x cua-mode`

(and customize it to save it) or select `Options -> Cut Paste ... (CUA Mode)`

.

By all means enable it if it helps with the adoption of Emacs. But I think Emacs’s system is better in the long haul. Emacs merges the notion of deleting text with your kill ring: most activities in Emacs that purport to delete text in actual fact *kills* it and sends it to your kill ring. That means you can chain any number of commands that delete text and insert it again somewhere else. It’s a different paradigm, but a much more powerful one.

But it’s ultimately your decision. Emacs still expects you to use the aforementioned shortcuts for regular Emacs activities. CUA mode merely overlays clipboard keys on top them.

## Next Steps

Here’s where I think you should go from here:

Read the builtin tutorial (

`C-h t`

) if you haven’t. It’s important – it’ll take you 20 minutes, and you’ll come away knowing more about how Emacs’s fundamentals work.Browse the builtin manual (

`C-h r`

) as it’s packed full of information.Decide on a goal. “Using Emacs” is not, though, a

*goal*.A goal is authoring papers with LaTeX; configuring Emacs for C programming; system administration with Tramp and

`M-x dired`

; or organizing your life with Org mode. Those are*goals*.A goal is easier to manage: you have a singular mission to fulfill, and it’ll give purpose and urgency to your use of Emacs. If you just dabble, a bit here and there, you won’t ever commit, and you’ll forget things quicker than you learn new things.

Most people who tried and failed to learn Emacs did so because they never found the time to get good at doing just one thing. Don’t sweat the fancy text editing just yet. Let that come naturally once you’re comfortable with Emacs basics.

Practice! Get into the habit of asking Emacs questions instead of Google or an addled AI that can’t tell truth from fiction. Yes, searching the internet will probably get you the answer quicker in the beginning, but over time that balance will shift.

If you don’t learn how to ask Emacs questions, then you’ll never learn Emacs!

Optional, but if you want a curated learning experience, then I highly recommend you read my book

[Mastering Emacs](https://www.masteringemacs.org/book). It’s 314 pages long and it will quite literally**teach you Emacs**.I’ve written about Emacs on this site since 2010, and I’ve been using Emacs for 20-some years. Everything I know, and everything I

*wish*I knew when I was learning Emacs, I’ve put into that book.Read my

[Reading Guide](https://www.masteringemacs.org/reading-guide). I’ve packed it full of all manner of things you might find useful to know about. And it’s just a small selection of a much larger corpus of text I’ve written about Emacs.There’s a lot of workflow concepts, so even if a certain area of Emacs won’t hold your interest, you’re likely to come away with a greater appreciation for what is possible.


## Summary

Emacs is not an inscrutable, black box that defies understanding. Nor is it an editor that requires an advanced degree to master. A large swathe of experienced Emacs users are knowledge workers and not techies. Emacs is a broad church, and if you put in the time to read and learn about it, you’ll quickly reach a point where it just ‘clicks’.

I had that very experience once and it took *much* longer then that it would take someone today. (The internet was severely lacking in learning material back then!) That’s partly why I started Mastering Emacs: to share the things I knew so others could hopefully benefit from the hard work I’d put in to learn that stuff myself. But I’ll say this: once it did ‘click’ for me, back in the day, it was because I finally grokked the significance of being able to ask Emacs questions. Who cares if you don’t remember a key or a command if you can look it up?

Emacs is as relevant today as it’s ever been. And it has a much larger, and growing, community than it has ever had before. Your time investment will pay dividends in the coming years and decades. Emacs has been around in some form since the late 70s — and it’ll be here in 40 years. Happy learning!