---
title: Ruby support in Firefox Developer Edition 38 – Mozilla Hacks - the Web developer
  blog
url: https://hacks.mozilla.org/2015/03/ruby-support-in-firefox-developer-edition-38/
author: Xidorn Quan
published: '2015-03-05'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

It was a long-time request from East Asian users, especially Japanese users, to have ruby support in the browser.

Formerly, because of the lack of native ruby support in Firefox, users had to install add-ons like [HTML Ruby](https://addons.mozilla.org/firefox/addon/html-ruby/) to make ruby work. However, in Firefox Developer Edition 38, [CSS Ruby](http://dev.w3.org/csswg/css-ruby-1/) has been enabled by default, which also brings the support of HTML5 ruby tags.

## Introduction

What is ruby? In short, ruby is an extra text, which is usually small, attached to the main text for indicating the pronunciation or meaning of the corresponding characters. This kind of annotation is widely used in Japanese publications. It is also common in Chinese for books for children, educational publications, and dictionaries.

![Ruby Annotation](../../assets/a3e121b9b27b0f4c.png)


## Basic Usage

Basically, the ruby support consists of four main tags: `<ruby>`

, `<rb>`

, `<rt>`

, and `<rp>`

. `<ruby>`

is the tag that wraps the whole ruby structure, `<rb>`

is used to mark the text in the normal line, `<rt>`

is for the annotation, and `<rp>`

is a tag which is hidden by default. With the four tags, the result above can be achieved from the following code:

```
```とある科学の超電磁砲

Since `<rb>`

and `<rt>`

can be auto-closed by themselves, we don’t bother to add code to close those tags manually.

As shown in the image, the duplicate parts as well as `<rp>`

s are hidden automatically. But why should we add content which is hidden by default?

The answer is: it is more natural in semantics, and it helps conversion to the inline form, which is a more general form accepted by more software. For example, this allows the page to have a decent effect on a browser with no ruby support. It also enables the user agent to generate well-formed plain text when you want to copy text with ruby (though this feature hasn’t yet been landed on Firefox).

In addition, the extra content makes it possible to provide inline style of the annotation without changing the document. You would only need to add a rule to your stylesheet:

```
ruby, rb, rt, rp {
display: inline;
font-size: inherit;
}
```

Actually, if you don’t have those requirements, only `<ruby>`

and `<rt>`

are necessary. For simplest cases, e.g. a single ideographic character, you can use code like:

`咲`Saki

## Advanced Support

Aside from the basic usage of ruby, Firefox now provides support for more advanced cases.

By default, if the width of an annotation does not match its base text, the shorter text will be justified as shown in the example above. However, this behavior can be controlled via the [ruby-align](https://developer.mozilla.org/en-US/docs/Web/CSS/ruby-align) property. Aside from the default value (`space-around`

), it can also make the content align to both sides (`space-between`

), centered (`center`

), or aligned to the start side (`start`

).

Multiple levels of annotations are also supported via tag `<rtc>`

which is the container of `<rt>`

s. Every `<rtc>`

represents one level of annotation, but if you leave out the `<rtc>`

, the browser will do some cleanup to wrap consecutive `<rt>`

s in a single anonymous `<rtc>`

, forming one level.

For example, we can extend the example above to:

```
```とある科学の超電磁砲
とあるかがくのレールガン

If you do not put any `<rt>`

inside a `<rtc>`

, this annotation will become a span across the whole base:

```
```とある科学の超電磁砲
とあるかがくのレールガン

You can use [ruby-position](https://developer.mozilla.org/en-US/docs/Web/CSS/ruby-position) to place the given level of annotation on the side you want. For the examples above, if you want to put the second level under the main line, you can apply `ruby-position: under;`

to the `<rtc>`

tag. Currently, only `under`

and the default value `over`

is supported.

(Note: The CSS Working Group is considering a change to the default value of `ruby-position`

, so that annotations become double-sided by default. This change is likely to happen in a future version of Firefox.)

In the end, an advanced example of ruby combining everything introduced above:

![Advanced Example for Ruby](../../assets/bb900c4c6285aaed.png)


```
rtc:lang(en) {
ruby-position: under;
ruby-align: center;
font-size: 75%;
}
```

```
```とある科学の超電磁砲
とあるかがくのレールガン

Got questions, comments, feedback on the implementation? Don’t hesitate to share your thoughts or issues here or via [bugzilla](https://bugzilla.mozilla.org/).

## 6 comments

ChrisMarch 5th, 2015 at 08:17HoroMarch 8th, 2015 at 21:41HexclesMarch 19th, 2015 at 17:25Ruben SchadeMarch 31st, 2015 at 17:40Vannak EngApril 1st, 2015 at 04:39Xidorn QuanApril 1st, 2015 at 04:48