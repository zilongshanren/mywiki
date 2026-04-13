---
title: UX Opinions
url: https://benui.ca/blog/ux-opinions/
published: '2026-01-01'
source_blog: ben🌱ui
source_site: https://benui.ca/
category: unreal engine
fetched: '2026-04-13'
---

Every so often I get full of myself and come up with a UX Opinion. Despite not being a UI or UX expert. I like to write them down.

I've tried to write a short version of the idea, and then some more verbose explanation why. Each is a separate heading so it's linkable, in the likely event that someone wants to link to it point out how wrong I am.

Also I'm trying to use the [RFC 2119: Key words for use in RFCs to Indicate Requirement Levels](https://www.rfc-editor.org/rfc/rfc2119) usage of 'must', 'should' and 'may'.

Also most of these are just like, stolen from existing UX best-practices.

# On-screen Buttons

## Cursor Change

If a UI element is interactive, the

cursor must changewhen it moves over the element.

This is a [huge personal gripe of mine](https://doesthecursorchange.com/), but anybody who uses a mouse probably uses the web for the vast majority of that time. They will be so used to interactive things making the cursor change, every time you break that in your game, you're making the player have to *think*.

Ideally interactive elements should be marked by the cursor changing to some sort of pointing hand 👆 to match web browser behaviour.

But it doesn't have to be a pointing hand. It should just change to something **visually different** to the default pointer.

- Can you click on it? Change it to a 👆 pointer hand.
- Can you drag it? Change it to a 🖐️ grabby hand.
- Can you click and change text? Change it to an I-shaped text-input cursor.

## Appearance Change on Hover

If a UI element is interactive, its appearance must change on hover.


I feel this is pretty self-explanatory but a lot of games don't even do this. If the player moves their cursor over a button, and the button doesn't visually change, how do they know that the have their cursor in the right place?

Similarly, if the change in the button state is not significant enough, they will still be confused. Changing from 80% opacity to 90% is not enough.

## Visually Distinct States

Any clickable UI element must have

visually distinct statesfor: normal, hover, mousedown, mouseup (confirm), disabled.

## Button is a Verb

Text on buttons must be a

verb. So don't use "Yes" and "No", use "Save" and "Cancel".

Users should be able to choose what to do just by reading the text on buttons, they shouldn't have to read surrounding text to understand it.

## Explanation when Disabled

If a button is disabled, a tooltip or clicking it should explain

why it is disabledand what the user can do to fix it.

This is more unusual, but I think it really helps with user experience. If you can't do a thing, explain to the user why not. That explanation can come in the form of a tooltip-on-hover, or showing a message when clicking.

# Shortcuts

## Show Shortcuts In-place

If a button has a keyboard shortcut, that shortcut must be displayed inside the button or in a tooltip.


It's the best way to get users to learn shortcuts.

## All Buttons can have Shortcuts

It must be possible to set a keyboard shortcut to all on-screen buttons.


Not all buttons need a shortcut by default, but designers cannot know which functions will be used by players, and cannot know if accessibility issues make it a requirement for a particular user.

## Default Shortcuts for Common Actions

Any action that is performed in over 50% of interactions should have a keyboard shortcut by default.


50% is arbitrary here, but the idea is if the player is doing something *most* of the time, they should be able to do it without clicking.

## Show Button Activation on Shortcut

Pressing a keyboard shortcut must trigger a "confirm" reaction in the corresponding button.


This might mean that there is a short delay between pressing a shortcut and the action taking place.

## Shortcut to Binding Configuration

Pressing a shortcut when hovering over a button should

take the user to a binding screenwhere they can set or change the shortcut for the action associated with the button.

This is maybe a bit wacky, but hear me out. If you want to change the shortcut to an action, there are a few ways that the user could do it:

- a) Open up settings, try to remember the name for the button or action, search for it in bindings, maybe forget, search around more. Give up. Feel disempowered, don't learn to love the software, don't learn to make it their own.
- b) Press shortcut while hovering button, input new shortcut, done.

The way to do b) is up to you, but the idea is that changing shortcuts should be as effortless as using them.

# Input

## Synonymity of D-Pad, Left Analogue Stick, WASD and Arrow Keys

In menus, unless there is a very good reason, the following should

allwork for primary navigation: d-pad and left analogue stick on controller, WASD and arrow keys on keyboard.

## Modifier Keys should be modifier-like actions

Modifier keys (control, shift, alt) should not be used for single-press actions, but for long-press modifier-like actions.


Using shift for sprint is OK, using it for toggling weapons feels weird as a PC user.

# Text

## Markdown Everywhere

All text formatting should be done using Markdown or similar minimal-markup language.


I just feel that Markdown is the simplest and most flexible approach to formatting.

## Write for your Audience

All text should be written for the

target audience. For example if your game is aimed at kids, don't say"modified"say"changed".

I've seen so many games aimed at younger kids that use unnecessarily long words.

## Keep Lines Short

All text must be displayed with less than 80 characters on a line.


There is an optimal number of characters on a line in English of around 50-70. Above that it starts tiring out users.

## Understandable at a Glance

All functional text must be understandable at a glance.


Use **bold**, *emphasis*, different colours, 🪙 Icons, to **highlight key points**.

Note that this only need be applied to functional text. For flavour text go wild.

# Desktop

## Many Instances

It must always be possible to run multiple instances of the same application.


There are *always* situations in which your users will want to run multiple instances of your application. There is no reason to not let them do it.

GitHub's desktop app for example will not let you. Instead of having a separate window for each repo, the user is forced to swap between repos within the same window, losing their context and making it impossible to compare changes.

# Misc

## Make Everything Linkable

Files, menu options, screens, etc. should have a copy-pastable

link. Clicking the link should open the item.

Use cases:

- Sharing a link to a screen or menu when developing the game or software. For example
[Hermes](https://github.com/jorgenpt/Hermes)adds clickable URLs to Unreal Engine assets. - Support can share a link to customers that takes them to the correct part of the software.

## Comments Everywhere

It should be possible to add shared comments

anywherein a piece of shared work.

Adding comments in code, on shared Figma documents is standard within the industry, but I think this mindset should be brought to other creative work:

[Breath of the Wild](https://www.4gamer.net/games/341/G034168/20170901120/)allowed developers to add notes and tasks in the game world itself.- When adding custom data structs to Unreal Engine, each item should have a comment field that can be used to describe its purpose, caveats.

## Search When More than 20

If there are greater than 20 somethings, the user must be able to search through them. Search should include plain text.


This applies to:

- Options menus in games.
- Drop-down File/Edit/Window menus in desktop software.

## Jump to File Location

Any screen that or window that has

corresponding files on-disk, must have a shortcut toopen the locationof those files.

This applies to logs, settings, saves, screenshots, anything. The software will always know where those files are located, don't make the user go through the hassle of finding out where they are.

Clicking on a button near the file should open that file location in Windows Explorer. If it makes more sense, opening the file itself and opening focusing on the correct line is also valid.