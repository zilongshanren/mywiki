---
title: 'Dark Theme Darkening: Better Theming for Firefox Quantum – Mozilla Hacks -
  the Web developer blog'
url: https://hacks.mozilla.org/2018/07/dark-theme-darkening-better-theming-for-firefox-quantum/
author: Dylan Stokes
published: '2018-07-03'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

## The Team

*Project Dark Theme Darkening was part of Michigan State University’s Computer Science capstone experience. Twenty-four groups of five students were each assigned an industry sponsor based on preference and skill set. We had the privilege of working with Mozilla on Firefox Quantum’s Theming API. Our project increases a user’s ability to customize the appearance of the Firefox browser.*

(left to right)

Vivek Dhingra: MSU Student Contributor

Zhengyi Lian: MSU Student Contributor

Connor Masani: MSU Student Contributor

[Dylan Stokes](https://www.linkedin.com/in/stokesdy/): MSU Student Contributor

[Bogdan Pozderca](http://bogdan.pozderca.com): MSU Student Contributor

[Jared Wein](https://mozillians.org/en-US/u/jaws/): Mozilla Staff

[Mike Conley](https://mozillians.org/en-US/u/mconley/): Mozilla Staff

[Tim Nguyen](https://mozillians.org/en-US/u/ntim/): Volunteer Contributor

## The Project

Our goal was to expand upon the existing “lightweight” Theming API in Quantum to allow for more areas of customization. Themes had the ability to alter the appearance of the default toolbars, but did not have the ability to style menus, or customize auto-complete popups. Our team also worked on adding a more fluid transition when dynamic themes changed to allow for a smoother user experience.

### Project Video

This video showcases a majority of the improvements we added to the Theming API and gives a good explanation of what our project was about. Enjoy — and then read on for the rest of the details:

### Experience

Prior to this project, none of us had experience with Firefox development. After downloading the [mozilla-central repository](https://hg.mozilla.org/mozilla-central/) and exploring through the 40+ million lines of source, it was a bit daunting for all of us. Our mentors: Jared, Mike, Tim, and the Mozilla community on IRC all helped us through squashing our first bug.

Through the project, we learned to ask questions sooner rather than later. Being programmers, we were stubborn and wanted to figure out our issues ourselves but could have solved them a lot faster if we just simply asked in the Mozilla IRC. Everyone on there is extremely helpful and friendly!

All code written was in JavaScript and CSS. It was neat to see that the UI of Firefox is made in much the same way as other web pages. We got a great introduction to [Mercurial](https://www.mercurial-scm.org/) by the end of the project and used some sweet tools to help our development process such as [searchfox.org](http://searchfox.org) for indexed searching of mozilla-central, and [janitor](https://janitor.technology/) for web-based development.

### Auto-complete Popups

We added the ability to customize the URL auto-complete popups. With this addition, we had to take in account the text color of the `ac-url`

and `ac-action`

tips associated with each result. For example, if the background of the auto-complete popup was dark, the text color of the tips are set to a light color so they can be seen.

We did this by calculating the [luminance](https://en.wikipedia.org/wiki/Luminance) and comparing it to a threshold. The `lwthemetextcolor`

attribute is set to either dark or bright based on this luminance threshold:

```
["--lwt-text-color", {
lwtProperty: "textcolor",
processColor(rgbaChannels, element) {
if (!rgbaChannels) {
element.removeAttribute("lwthemetextcolor");
element.removeAttribute("lwtheme");
return null;
}
const {r, g, b, a} = rgbaChannels;
const luminance = 0.2125 * r + 0.7154 * g + 0.0721 * b;
element.setAttribute("lwthemetextcolor", luminance <= 110 ? "dark" : "bright");
element.setAttribute("lwtheme", "true");
return `rgba(${r}, ${g}, ${b}, ${a})` || "black";
}
}]
```


The top image shows the auto-complete popup with the native default theme while the bottom image shows the auto-complete popup with the Dark theme enabled. Notice that the `ac-action`

(“Switch To Tab”) text color and `ac-url`

are changed so they can be more easily seen on the Dark background.

### Theme Properties Added

We added many new theme properties that developers like you can use to customize more of the browser. These properties include:

`icons`

– The color of toolbar icons.`icons_attention`

– The color of toolbar icons in attention state such as the starred bookmark icon or finished download icon.`frame_inactive`

– color of the accent color when the window is not in the foreground`tab_loading`

– The color of the tab loading indicator and the tab loading burst.`tab_selected`

– The background color of the selected tab.`popup`

– The background color of popups (such as the url bar dropdown and the arrow panels).`popup_text`

– The text color of popups.`popup_border`

– The border color of popups.`popup_highlight`

– The background color of items highlighted using the keyboard inside popups (such as the selected URL bar dropdown item)`popup_highlight_text`

– The text color of items highlighted using the keyboard inside popups.`toolbar_field_focus`

– The focused background color for fields in the toolbar, such as the URL bar.`toolbar_field_text_focus`

– The color of text in focused fields in the toolbar, such as the URL bar.`toolbar_field_border_focus`

– The focused border color for fields in the toolbar.`button_background_active`

– The color of the background of the pressed toolbar buttons.`button_background_hover`

– The color of the background of the toolbar buttons on hover.

The `toolbar_field`

, and `toolbar_field_border`

properties now apply to the “Find” toolbar.

Additionally, these new properties now apply to the the native Dark theme.

```
colors: {
accentcolor: 'black',
textcolor: 'white',
toolbar: 'rgb(32,11,50)',
toolbar_text: 'white',
popup: "rgb(32,11,50)",
popup_border: "rgb(32,11,50)",
popup_text: "#FFFFFF",
popup_highlight: "rgb(55,36,71)",
icons: "white",
icons_attention: "rgb(255,0,255)",
frame_inactive: "rgb(32,11,50)",
tab_loading: "#0000FF",
tab_selected: "rgb(32,11,50)",
}
```


Above shows an example of some of the added properties being set in a theme manifest file and what it looks like in the browser below:

## Conclusion

Our team learned a lot about web browser development over the semester of our project, and we had the opportunity to write and ship real production-level code. All of the code we wrote shipped with the recent releases of [Firefox Quantum 60](https://hacks.mozilla.org/2018/05/firefox-60-modules-and-more/) and [61](https://hacks.mozilla.org/2018/06/firefox-61-quantum-of-solstice/) and will impact millions of users, which is an awesome feeling. We want to thank everyone at Mozilla and the Mozilla community for giving us this opportunity and mentoring us through the process. We are looking forward to seeing what developers and Firefox enthusiasts create using the improved Theming API!

## 14 comments

dosJuly 3rd, 2018 at 08:17JohanJuly 3rd, 2018 at 08:37qqqqqqJuly 3rd, 2018 at 10:36JPJuly 3rd, 2018 at 11:01Dylan StokesJuly 7th, 2018 at 07:06sergioJuly 3rd, 2018 at 14:42James WalkerJuly 4th, 2018 at 00:42Wallace SilvaJuly 4th, 2018 at 05:40TreckoJuly 4th, 2018 at 12:09Dylan StokesJuly 7th, 2018 at 07:11StiffuxJuly 5th, 2018 at 00:59TimJuly 5th, 2018 at 07:43TimJuly 5th, 2018 at 07:47Bla blaJuly 5th, 2018 at 08:48