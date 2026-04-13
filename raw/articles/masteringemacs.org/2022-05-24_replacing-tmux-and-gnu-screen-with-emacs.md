---
title: Replacing tmux and GNU screen with Emacs
url: https://www.masteringemacs.org/article/replacing-tmux-gnu-screen-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If you’re a command line hacker – and I know you are – then I am sure you are familiar with, and possibly use, GNU `screen`

or its contemporary replacement, `tmux`

. If you are in the process of [switching from Vim to Emacs](https://www.masteringemacs.org/article/switching-from-vim-to-emacs), then `tmux`

is no doubt a large part of your workflow.

But here’s the thing: you do not need a terminal multiplexer if you are already using Emacs. Emacs can accomplish nearly everything your terminal multiplexer can do. If you’re not a serious user of `screen`

or `tmux`

, but you’re still addicted to the command line, then I’m sure this article will convince you of the merits of multiplexers, and how Emacs can slot right in. If you’re still unconvinced after having read this article, then my parting advice is to read about the [keyboard shortcuts in GNU readline](https://www.masteringemacs.org/article/keyboard-shortcuts-every-command-line-hacker-should-know-about-gnu-readline) as that’ll at least bring more of Emacs to your command line life.

Before I get into the weeds of why, let me just quickly state that, sure, `tmux`

and friends will always have their uses: on remote servers for people who insist on running their daemons inside a `screen`

session like it’s 1997 (bonus points if it’s an IRC client); and of course for actual terminal use on machines where Emacs is not available, or where you have to work with others who may not know Emacs.

Caveats aside, let me share why I think you should consider using Emacs for some or all of your multiplexing needs, as it can do everything from detaching and re-attaching sessions; to windowing; to terminal emulation and running shells; and even the odd bit of text editing…

## The Perils of Terminal Programs

Naturally, terminal multiplexers are meant for terminals, and as such, I’ll talk exclusively about running Emacs in a terminal from now on, although nearly all the advice I write applies equally to GUI Emacs. My thoughts on terminal Emacs are well known if you’re a frequent reader, but I will restate them again by saying that running GUI Emacs is a far better proposition than running Emacs in a terminal (multiplexer or not) for the following simple reasons:

- Key Bindings often clash with your terminal
-
It’s such a common problem for beginners: they fire up Emacs in a terminal, and wonder why some keys don’t work at all. The answer is usually the terminal tool itself. You’ll have to disable their invasive overreach of your key bindings so they pass through to the terminal, but now you lose said key bindings as you may want to use them elsewhere.

- Not all key bindings work in a terminal
-
Despite a lot of bolted-on protocols, additions and extensions made over the years, the fact of the matter is that some keys are simply not possible to represent and transmit to a terminal and the underlying program. This is another common newbie trap.

- Lack of fidelity
-
You cannot view PDFs, use images, or rice your Emacs with fancy SVG icons; some terminal emulators have limited color bit depth. The value of this is debatable, but I find the ability to view PDFs and images useful.

- Flow Control Chaos
-
And the ultimate trap of them all: the ossified flow control feature that some terminals still enable by default. Type

`Control+s`

in some terminal setups, and your terminal freezes, so as to give you enough time to read the text before it can scroll by.`Control+q`

thaws your terminal. A fantastic feature when you’re downloading Dr. Who fan scripts from a dusty newsgroup back in the 1980s. Today… not so much. You can permanently disable flow control with`stty -ixon`

, but it’s just one more thing to think about.

There’s one more reason not to run terminal Emacs inside a *terminal multiplexer* and that is… well, everything, actually. The multiplexer gets first dips on the ANSI escape codes terminals use to move the cursor and draw stuff to the screen, and it’s oh-so-easy to break or gum things up. Mismatched colors; loss of color bit-depth; keys not getting translated properly; keys intercepted and repurposed by the multiplexer; weird scrollback and buffering issues; the list goes on and on.

Terminal multiplexers are awesome, but they’re also faced with a tricky problem: they *must* work with nearly everything in a way that is sensible and consistent and often across a wide range of terminal capabilities and platforms. Sure, you can tweak this stuff: do you really want to, though?

So those are the downsides of terminal Emacs with or without the lather of a multiplexer messing with your escape codes. But as annoying as these issues are, terminal Emacs is a full-fledged Emacs experience otherwise.

Now let’s replicate the multiplexing experience inside Emacs.

## Emacs’s Client-Server Architecture

Of course Emacs has a client-server architecture. It’s a *text editor!*

Run `M-x server-start`

in an active Emacs instance and your current Emacs becomes the server host. Note that there are multiple ways of running Emacs in server mode. If you use `emacs --daemon`

to start the daemon, you’ll get a persistent daemon that does not spawn a frame; you must then type `emacsclient -c`

to connect to your Emacs. A third way is `systemctl --user enable emacs`

and you can let systemd run Emacs as a daemon.

Either way, from that moment on, if you call `emacsclient`

, Emacs will talk to your Emacs server. This is how experienced hackers prefer to use Emacs, but you do not have to, of course. If you run `emacs`

it will launch a standalone instance. You can even mix and match.

Now you can set `emacsclient`

to your `$EDITOR`

and everything Just Works.


NOTE: Emacs’s client-server architecture is not intended to straddle multiple computers; both should be run on the same machine, lest you run into weird, hard-to-debug problems. If you want to use Emacs ‘remotely’, you can use[Tramp]or`ssh`

to your target machine and run Emacs as a client-server architecture there.

## Running Programs from Emacs

Obviously this is the main purpose of a multiplexer, and Emacs is more than capable of doing this. Running instances of your favorite shell is the most common, so let’s start with that.

### Shells and Terminal Emulators

Command |
Description |
`M-x shell` |
Runs your preferred shell via a pseudo-terminal or pipe. Uses Emacs keys, Emacs for scrollback, its own history, better search and a plain Emacs buffer. Limited emulation; cannot handle curses apps without third-party packages like |
`M-x term` |
Emacs’s builtin terminal emulator. Can switch between traditional terminal mode and a mode that makes it temporarily behave like an Emacs buffer. Can be quite slow. |
`M-x vterm` |
Uses
|
`M-x eat` |
EAT is another terminal emulator that plugs into Eshell and also has its own terminal mode. Very fast.
|
`M-x eshell` |
Not a terminal emulator, but instead a replacement for your preferred shell. It’s loosely inspired by
|

My article on [Running Shells and Terminal Emulators in Emacs](https://www.masteringemacs.org/article/running-shells-in-emacs-overview) is a more in-depth look at these options. If you want a near-terminal-like experience, then `vterm`

is a great package. If you want to lean into the Emacs way of doing things, then `M-x shell`

is a good choice, and that is what I mostly use, unless I absolutely have to run a curses app (then I use `M-x vterm`

.) If you are unsure, then I recommend you install `vterm`

and start with that.

Another way – the more Emacsy way – is to instead consider that most things may not require a shell (and a terminal) at all for common tasks. If you just want to compile stuff (or run your development server, test harness, etc. etc.), then [compiling and running scripts in Emacs](https://www.masteringemacs.org/article/compiling-running-scripts-emacs) is the way to go. You gain the added benefit of error highlighting (with hyperlinks to the erroneous file) that works with darn near every structured error output you can throw at it.

But wait, there’s more: you can run a range of [command line network utilities](https://www.masteringemacs.org/article/network-utilities-emacs); [use M-x proced, Emacs’s replacement for top](https://www.masteringemacs.org/article/displaying-interacting-processes-proced); and use dired, Emacs’s [directory editor](https://www.masteringemacs.org/article/dired-shell-commands-find-xargs-replacement) to do all sorts of cool stuff.

For simple things? You can [execute shell commands](https://www.masteringemacs.org/article/executing-shell-commands-emacs) directly, or even feed buffer text to the standard input of a command line program and get the output piped back. That solves a whole swathe of problems also.

#### Interacting with `fzf`


Not really multiplexer related per se, so I’m going to point out that you can use [Emacs for fuzzy finding](https://www.masteringemacs.org/article/fuzzy-finding-emacs-instead-of-fzf) instead of `fzf`

using a fistful of shell script code. Kinda cool.

### Starting programs from outside or inside Emacs

Another common thing to do with a multiplexer is to quickly open a program inside a running tmux instance; perhaps from a shell pane *inside* your `tmux`

instance, or perhaps outside it.

You can do this with Emacs also (with `M-x vterm`

if it’s installed, otherwise `M-x term`

) with the provided bash script. Let’s call it `emux.sh`

:

Here I temporarily bind the Emacs variable `vterm-shell`

to the command to run (it defaults to your shell). Then I invoke `vterm`

(if it’s installed, otherwise I use `term`

) and start a new instance.

To use it is simple:

`./emux.sh top`

runs`top`

inside your active Emacs instance.`./emus.sh watch free -hg`

calls`watch`

and tells it to run`free -hg`

.`./emux.sh`

on its own will call your`$SHELL`

instead.

All from the comfort of your Emacs. You don’t have to run this from inside an Emacs instance, either. Provided you’ve got the client-server feature enabled, it’ll work anywhere.

### Detaching and Attaching & Long-running programs

By running programs in an Emacs server instance, you can leave them running even if you hang up your remote connection (such as when you disconnect from `ssh`

) but that does depend a bit on the method you used to start your server. I recommend you daemonize it with `emacs --daemon`

, or run it through systemd, to ensure this works.

Your Emacs server remembers everything: processes, sockets, buffers — you name it. You can even have multiple daemons if you really, really want to.

So if your workflow depends heavily on the ability to engage and disengage from a ‘running’ session of work, then Emacs can definitely do this.

If you regularly work on remote servers, a lot of your work could be done from your local Emacs by talking to the remote server directly with Emacs’s [Tramp](https://www.gnu.org/software/tramp/).

## Panes, Windows, Buffers, Frames

Emacs’s windowing technology is so far ahead of every other terminal or GUI application that I’d struggle to even begin to cover all the things you can do with it. Emacs is a tiling window manager onto itself (and some do indeed use it as their tiling window manager!), with hundreds of commands and variables that govern how it works. It also has *frames* (Emacs’s name for what most people call *windows*), if you prefer a non-tiling approach.

I’ve made a handy table of the window-related nomenclature used in `screen`

and `tmux`

and of course Emacs. They do differ, so let’s just quickly cover that.

Term |
Emacs |
tmux |
GNU Screen |
Frame |
The entire Emacs instance visible on screen, can contain multiple windows | The entire terminal instance running tmux, equivalent to the terminal window | The entire terminal instance running Screen, equivalent to the terminal window |
Window |
A subdivision within a frame that displays one buffer | A full-screen view within a session that can be divided into panes (similar to tabs) | A full-screen virtual terminal identified by a number or name |
Buffer |
Container for text being edited, displayed within windows | No direct equivalent (closest is the content displayed in a pane) | No direct equivalent (closest is the content displayed in a window) |
Pane |
No direct equivalent (similar to windows) | Subdivision of a window that contains a separate terminal instance | Called “regions” — subdivisions of the display when split screen is used |
Session |
Another term for an Emacs server instance | A collection of windows under a single server instance that can be detached/reattached | A detachable collection of windows running as a single process |

Of note is that in Emacs, a *frame* is of course what most people would call a *window*, but there’s another dimension to it: frames behave differently in a terminal Emacs session.

In terminal Emacs, a frame is really more like *window* in `tmux`

or `screen`

. Only one is ever visible at a time; in GUI Emacs, you can have many visible at the same time, subject to the whims of your window manager (tiling vs stacking for example) and Emacs has another set of complex commands for interacting with frames specifically. Emacs does its level best to provide parity between the GUI and terminal versions, but this is one area where there is some difference in appearance and behavior.

Now let’s talk about – let’s call it “windowing features” for want of a better phrase – across the multiplexers and Emacs. There’s an awful lot of asterisks attached to some of these, but more on that below.

tmux Feature |
screen Key Binding |
tmux Key Binding |
Emacs Key Binding |
| Create new window | `C-a c` |
`C-b c` |
`C-x 2` , `C-x 3` (splits instead) |
| Close current window | `C-a K` |
`C-b &` |
`C-x 0` (close window), `C-x k` (kill buffer) |
| Rename current window | `C-a A` |
`C-b ,` |
`M-x rename-buffer` or `C-x x r` |
| List all windows | `C-a "` |
`C-b w` |
`C-x b` (switch to) or `C-x C-b` |
| Next window | `C-a n` |
`C-b n` |
`C-x o` (other window) |
| Previous window | `C-a p` |
`C-b p` |
N/A but you can fiddle with numeric arguments to `C-x o` to simulate it, or use windmove. |
| Go to window by number | `C-a [0-9]` |
`C-b [0-9]` |
Registers can sort of stand in for this, but there is no simple equivalent. |
| Go to last active window | `C-a C-a` |
`C-b l` |
Maybe `M-x mode-line-other-buffer` |
| Split window horizontally | `C-a S` (added later) |
`C-b "` |
`C-x 2` |
| Split window vertically | `C-a |` (added later) |
`C-b %` |
`C-x 3` |
| Move to next pane | `C-a tab` |
`C-b o` |
`C-x o` |
| Convert pane to window | N/A | `C-b !` |
N/A |
| Show pane numbers | N/A | `C-b q` |
N/A |
| Toggle between pane layouts | N/A | `C-b space` |
Window Configurations; `M-x tab-bar-mode` |
| Resize pane | N/A (not as intuitive) | `C-b C-[arrow keys]` |
`C-x {` / `C-x }` |
| Break pane into window | N/A | `C-b !` |
N/A |
| Join pane from window | N/A | `C-b :join-pane -s [window]` |
N/A |
| Enter copy mode | `C-a [` |
`C-b [` |
N/A |
| Search in copy mode | `/` (forward), `?` (backward) |
`/` (forward), `?` (backward) |
`C-s` (forward), `C-r` (backward) |
| Swap window positions | `C-a :number [n]` |
`C-b .` (prompt for new number) |
Use Windmove |
| Detach from session | `C-a d` |
`C-b d` |
`C-x #` (if in an emacs client) |
| Choose a session | N/A (via command line) | `C-b s` |
Technically a thing, but multiple daemons is a rarely used feature. |
| Zoom pane (toggle full-screen) | N/A | `C-b z` |
`C-x 1` |
| Rotate panes | N/A | `C-b C-o` |
N/A |
| Display clock | `C-a t` |
`C-b t` |
`M-x display-time` |
| Command prompt | `C-a :` |
`C-b :` |
`M-x` |

`tmux`

and `screen`

are not trying to be Emacs, and Emacs did not set out to replace either of these tools — it’s just that it is so advanced that it can step into the role of multiplexer with relative ease.

Windows in Emacs are *transient* and considered disposable, and the commands are sort of built around that idea. That is a stark difference to other IDEs and editors, but consider that this is a complex topic with a lot of opinions. Luckily, Emacs can accommodate most of people’s complex windowing requirements, if you’re willing to [learn how Emacs’s Window Manager works](https://www.masteringemacs.org/article/demystifying-emacs-window-manager). As such swapping windows or referencing them by number is not really an Emacsy thing to do, though you can with a little bit of code (or using a third-party package like `avy`

), or perhaps by bending registers to your will.

In Emacs you have to contend with buffers first and foremost, as that is the [currency of Emacs](https://www.masteringemacs.org/article/why-emacs-has-buffers). Buffers, though, have no real equivalents in the multiplexers, as you can preserve the window layout in Emacs but change their buffers to show something else (though you technically *can* do this in `tmux`

, it’s clearly not a well-trodden path) so in Emacs I’ve crammed both buffer and window switching commands into the mix. I would be remiss if I did not also mention both `M-x global-tab-line-mode`

, for browser-style tabs; and `M-x tab-bar-mode`

to set up and switch between window configurations (“pane layouts” in `tmux`

), but more on that below.

The builtin package *windmove* adds ortographic movement from the current active window (for example, `C-x <up>`

to pick the window above the current one) as opposed to layout-driven keys like `C-x o`

that cycle through the windows on your screen. It’s a useful package, and one a lot of people use to make movement between windows more intuitive and faster.

Detaching / attaching to a session is best done by explicitly launching a server daemon (as I mentioned before) with `emacs --daemon`

and then connecting and disconnecting (`C-x #`

) at will with `emacsclient`

.

Because GUI frames and terminal frames behave differently, I have opted to use a mix of buffer and window commands to represent the pane/window commands as that is ultimately what you are going to use in Emacs. But that’s obviously not the only way of looking at this: if you want to mirror the behavior of `screen`

or `tmux`

you can use Emacs’s frames for some of this:

Operation |
Terminal Emacs Frame |
tmux |
GNU Screen |
| Create new frame | `C-x 5 2` |
`C-b c` (new window) |
`C-a c` (new window) |
| Switch to next frame | `C-x 5 o` |
`C-b n` (next window) |
`C-a n` (next window) |
| Previous frame | N/A | `C-b p` (previous window) |
`C-a p` (previous window) |
| Close current frame | `C-x 5 0` |
`C-b &` (kill window) |
`C-a K` (kill window) |
| Open file in new frame | `C-x 5 f` |
`C-b c` |
`C-a c` |
| Open buffer in new frame | `C-x 5 b` |
`C-b c` |
`C-a c` |
| List all frames | `M-x select-frame-by-name` |
`C-b w` (list windows) |
`C-a "` (list windows) |
| Rename current frame | `M-x set-frame-name` |
`C-b ,` (rename window) |
`C-a A` (rename window) |

Personally, I think the frame approach is an average facsimile, and that it’s better to just embrace Emacs’s way of doing things, instead of shoehorning frames into the multiplexers’ notion of “windows”.

For that, I recommend you just use `M-x tab-bar-mode`

. Each tab is its own window configuration, and you can interact with tabs in many ways. Note again that tab *bars* are not like tab *lines*, the latter being more like a browser’s open tabs.

Operation |
Emacs tab-bar-mode Key Binding |
| Enable tab-bar-mode | `M-x tab-bar-mode` |
| Create new tab | `C-x t 2` or `C-x t n` |
| Close current tab | `C-x t 0` or `C-x t k` |
| Rename current tab | `C-x t r` |
| Switch to next tab | `C-x t o` or `C-TAB` |
| Switch to previous tab | `C-S-TAB` |
| Switch to tab by name | `C-x t RET` |
| Duplicate current tab | `C-x t n` |
| List all tabs | `M-x tab-switcher` or `M-x tab-list` |
| Open file in new tab | `C-x t f` |

So that’s yet another way to do it. This is my preferred approach: it’s consistent across GUI and terminal Emacs, and it’s a more ergonomic way of interacting with window setups in Emacs. It is also a close approximation of how your terminal multiplexer treats distinct “windows”.

## Prefix Keys

The problem with `screen`

and `tmux`

is that their default prefix keys override two rather useful Emacs key bindings that [also work everywhere GNU Readline](https://www.masteringemacs.org/article/keyboard-shortcuts-every-command-line-hacker-should-know-about-gnu-readline) is used: `C-a`

, to move to the beginning of a line; and `C-b`

to move backward a character.

In Emacs, that obviously isn’t a problem, as the key bindings you’ll need are scattered across a range of keys, and in any event, you’ll have full control over the keys available to you inside Emacs and which ones are sent to the underlying process, should you choose to use Emacs as your terminal emulator.

## Scrollback, Copying and Searching

Emacs is a full-fledged text editor, and it has scrollback everywhere, so there’s not much more to say about that. Selecting (marking) and copying is available everywhere, and Emacs’s terminal emulators can switch from “terminal mode” to “cooked” (meaning it behaves like a regular Emacs buffer with freeform navigation) so you can copy and search as you please. Now is the time mention occur mode, one of many ways of sifting through text. It lets you [regexp search in Buffers](https://www.masteringemacs.org/article/searching-buffers-occur-mode) with a handy popup window of the matches. Terminal multiplexers can’t do that without plugins.

## My Workflow

Workflow are personal things, but I’ll quickly talk about how I use Emacs in lieu of a multiplexer.

I prefer to do everything local to my machine, where feasible.

For remote sessions, I will use

`ssh`

in a`M-x shell`

instance (unless I have to interface with curses apps, then I use`M-x vterm`

) and combine it with[Tramp](https://www.gnu.org/software/tramp/)for file editing.I avoid running Emacs on a remote machine directly because I will always opt for local, as I mentioned in #1. But when I

*have*to, I will run emacs in a client-server architecture. Having said that, it is very rare that I cannot do 90% of my work from my local machine.For things like docker containers or even talking to kubernetes pods, I can do this with Tramp also. I can also ssh to a bastion host and then onwards to root with

`sudo`

and then perhaps into a container with`docker`

. I can bookmark these things in Emacs so I can return to them with the snap of a finger.Emacs’s Tramp can execute command line programs remotely for you. If you’re editing a remote file in a buffer, then

`M-x dired`

(`C-x d`

) and tools like`M-x compile`

,`M-x grep`

, etc. automatically call out to their remote counterpart and return the results back to your local Emacs instance. Very powerful.`M-x shell`

is the right tool for me. It’s a ‘dumb terminal’ in the sense that everything is fed into an Emacs buffer which is then enriched with features such as history, prompt detection, and more. Works great, except when it does not. However, I can live with the tradeoffs. I prefer a free-flowing buffer with all the advantages and disadvantages that brings. For example, I can type`M-s h p`

(`M-x highlight-phrase`

) and highlight stuff in the buffer by regexp. Emacs will highlight current and future instances.I’m sure you’re thinking of all the many, many instances in your career where you wished you could do such a simple, simple thing like highlight stuff.

Watching logs and other changing files. Again with Tramp: open the file then

`M-x auto-revert-mode`

or`M-x auto-revert-tail-mode`

and Emacs will revert the file when it changes. Simple.

And that’s just *some* of the things I do. The main thing to take away from my workflow – and this article – is that things orbit around Emacs, because I am proficient at using Emacs, and it is capable of a great many things.

Honestly? Thrashing around on the command line – no matter your shell, even with nice ones like fish – feels like an enormous step back in productivity compared to using Emacs and regular old bash.

But that’s me. You’ll build your own workflow that meets your needs.

## Conclusion

If you’re familiar with Emacs then most of my advice should not come as a surprise to you. If you’re new or still learning, then I hope this will give you some food for thought.

You can pare back your use of your if it makes sense to do so: but most of the day-to-day grind I see `tmux`

users do can easily be done from within Emacs, but with a real gain to your productivity. Switching to Emacs *just* to replace your terminal multiplexer is perhaps a harder sell, but if you can learn and memorize your multiplexer’s commands, then you’ll do just fine learning Emacs also.

Let me know in the comments if ditching a multiplexer helps (or hinders!) your workflow!