---
title: 'Firefox 4: OpenType font feature support – Mozilla Hacks - the Web developer
  blog'
url: https://hacks.mozilla.org/2010/11/firefox-4-font-feature-support/
author: John Daggett
published: '2010-11-10'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

When [@font-face](https://developer.mozilla.org/en/css/@font-face) support was introduced in Firefox 3.5, web authors were suddenly given a way of dramatically enhancing the typography used on their sites. With all major browsers slated to soon support WOFF fonts offered by many font vendors, the range of fonts available on the web is far wider than it was just two years ago.

The OpenType format has long provided font designers ways of including a rich set of variations in their fonts, from ligatures and swashes to small caps and tabular figures. The OpenType specification describes these features, identifying each with a unique feature tag but they have typically only been available to those using professional publishing applications such as Adobe InDesign. When glyphs are selected for a particular sequence of characters and positioned for rendering, these features affect both glyph selection and positioning. Firefox currently renders using a font’s default feature settings; it would be much more interesting to provide web authors with a way of controlling these font features via CSS.

Included among the many new features in Firefox 4 is the next step, support for controlling OpenType font features directly via CSS. The [-moz-font-feature-settings CSS property](https://developer.mozilla.org/en/CSS/-moz-font-feature-settings) permits control over kerning, ligatures, alternates, real small caps and stylistic sets to name just a few.

The CSS3 Fonts specification contains a number of [new subproperties of font-variant](http://dev.w3.org/csswg/css3-fonts/#font-variant-ligatures-prop). These will eventually provide much better author control over font features but for Firefox 4 only the low-level [-moz-font-feature-settings CSS property](https://developer.mozilla.org/en/CSS/-moz-font-feature-settings) is supported. With this authors can enable and disable OpenType font features directly:

```
.altstyles {
/* format: feature-tag=[0,1] with 0 to disable, 1 to enable */
/* dlig = discretionary ligatures, ss01 = stylistic set 1 */
-moz-font-feature-settings: "dlig=1,ss01=1";
}
```

For reference, a complete list of registered OpenType features can be found [here](http://www.microsoft.com/typography/otspec/featurelist.htm). The folks at FontFont provide a [nice visual guide to OpenType features](http://www.fontfont.com/opentype/FF_OT_UserGuide_v2.pdf).

#### Ligatures and Contextual Alternates

Font designers often include simple ligatures and kerning data in their fonts but some go beyond these and spend a lot of time creating special ligatures and contextual alternate glyphs to enhance a given design. The [Bello Pro script font](http://www.underware.nl/site2/index.php?id1=bello&id2=features) from Underware is a brush-like design that includes many special ligatures (click image to view):

Note the special ligatures for “and” and “by”, the use of all small caps and the use of alternate glyphs to enhance the script connection between the letters in “Smooching”. Only font styling is used here, all the text can be selected and copied, there are no images used on the example page.

#### Number styles

Using [Minion Pro from Adobe](http://typekit.com/fonts/minion-pro), available via Typekit, the example below illustrates the use of tabular, monospaced number forms to display columns of data in a way that’s easy to read and analyze. When proportional numbers are used, the width of large figures with the same number of digits will vary. Normally this would require using a different, monospaced font. But with OpenType fonts that provide number formatting features, authors can use a single font without giving up the readibility of large data sets (click image to view):

Fonts may use either tabular or proportional number forms by default; providing access to these features allows authors to use both proportional figures for inline text and tabular figures for tabular data without the need to switch fonts.

#### Automatic fractions

Recipes for American dishes often use fractional amounts. These can easily be rendered using the automatic fraction feature in OpenType (click image to view):

Each of the fractions above is written in simple text form, (e.g. 2 1/2), no special Unicode codepoints are used. For fonts that support automatic fractions, an OpenType layout engine will automatically generate fractional forms for numbers separated by a slash. These are typically limited to simple fractions, for more complex math expressions markup languages like [MathML](https://developer.mozilla.org/en/Mathml) should be used instead.

#### Language sensitivity

Many languages often use a common script and over time differences in usage naturally arise. Serbian, Macedonian and Bulgarian all use the Cyrillic script but with slightly different glyph forms for some common characters. OpenType fonts support the ability to specify script-specific and language-specific glyph handling so given the correct lang attribute in the markup of a page, Firefox 4 can now render text in a language-specific way (click image to view):

#### Arbitrary features

OpenType defines font feature support using an underlying set of primitives. This allows font designers the ability to create their own features, either for a specialized purpose or as a general feature to be included in a future version of the OpenType specification. Since the syntax of -moz-font-feature-settings allows for the use of arbitrary feature tags, these can be accessed via CSS.

In the example below, font designer Erik van Blokland of [LettError](http://letterror.com/) uses a custom designed set of feature properties to create an interesting animation effect when hovering over text on the page (click image to view):

#### HarfBuzz, an OpenType shaping engine

The process of selecting and positioning glyphs used to display text runs has in the past always been done via platform libraries such as Uniscribe on Windows and CoreText on OSX. To assure more robust and consistent text rendering across platforms, Firefox 4 will use the open source [HarfBuzz OpenType shaping engine](http://www.freedesktop.org/wiki/Software/HarfBuzz) on all platforms. In the future this will allow us to integrate support for complex Indic and Southeast Asian scripts that have often been ignored or supported inconsistently in the past.

#### A Note About Typekit Use

All of the Adobe fonts available via the Typekit webfont service provide access to the full range of OpenType features found in the original fonts. But to access those features you’ll need to explicitly enable “All Characters” under the “Language Support” category in the kit editor dialog before publishing.

#### Other examples

(Updated from a [blog post last year](http://hacks.mozilla.org/2009/10/font-control-for-designers/)):

[Use of contextual alternates and ornaments](http://people.mozilla.com/~jkew/feature-samples/MEgalopolis.html)[Another recipe example](http://people.mozilla.com/~jkew/feature-samples/cooking.html)[Tabular data example](http://people.mozilla.com/~jkew/feature-samples/forex.html)[Language specific rendering of Turkish](http://people.mozilla.com/~jkew/feature-samples/udhr-turkish.html)[Rendering historical text](http://people.mozilla.org/~jdaggett/webfonts/historicaltext.html)

*Update: the content of the examples is now editable! Edit the text of each example to experiment with the different font features.*

## 48 comments

Robert O’CallahanNovember 9th, 2010 at 19:19John DaggettNovember 9th, 2010 at 20:29Brett ZamirNovember 9th, 2010 at 20:31John DaggettNovember 9th, 2010 at 21:13Brett ZamirNovember 10th, 2010 at 07:32arnoNovember 10th, 2010 at 07:38Hans HalperNovember 9th, 2010 at 23:46benoitbNovember 10th, 2010 at 00:00John DaggettNovember 10th, 2010 at 00:56thinsoldierNovember 10th, 2010 at 13:11John DaggettNovember 10th, 2010 at 13:15arnoNovember 10th, 2010 at 01:26John DaggettNovember 10th, 2010 at 04:25yagraphNovember 10th, 2010 at 02:25John DaggettNovember 10th, 2010 at 04:29yagraphNovember 10th, 2010 at 06:49MaaikeNovember 10th, 2010 at 07:15John DaggettNovember 10th, 2010 at 13:21StuartNovember 11th, 2010 at 18:58Dave DawsonNovember 10th, 2010 at 08:06Sean KernerNovember 10th, 2010 at 11:17John DaggettNovember 10th, 2010 at 13:16steveNovember 12th, 2010 at 06:16John DaggettNovember 13th, 2010 at 07:11steveNovember 14th, 2010 at 06:16steveNovember 14th, 2010 at 06:18xxNovember 15th, 2010 at 19:08Matt WilcoxNovember 16th, 2010 at 08:17James John MalcolmNovember 16th, 2010 at 14:34Jason NgNovember 17th, 2010 at 10:55snafuracerNovember 18th, 2010 at 05:45zambDecember 12th, 2010 at 23:02HenryFebruary 13th, 2011 at 03:25KnsiNovember 25th, 2010 at 11:21AndrejDecember 15th, 2010 at 21:31AlexDecember 23rd, 2010 at 02:42Wurdebalg HurrstJanuary 30th, 2011 at 06:20AlexFebruary 4th, 2011 at 06:34NiznaicaDecember 15th, 2010 at 23:25KAMAL.SA88December 16th, 2010 at 14:46KAMAL.SA88December 16th, 2010 at 15:06DianaDecember 20th, 2010 at 19:49Robson SobralJanuary 2nd, 2011 at 17:34Robson SobralJanuary 4th, 2011 at 06:26bryanFebruary 21st, 2012 at 09:45edwinJuly 1st, 2012 at 17:05John DaggettJuly 11th, 2012 at 01:09edwinJuly 11th, 2012 at 07:38