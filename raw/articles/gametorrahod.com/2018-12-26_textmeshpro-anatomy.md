---
title: TextMeshPro Anatomy
url: https://gametorrahod.com/textmeshpro-anatomy/
author: Sirawat Pitaksarit
published: '2018-12-26'
source_blog: Game Torrahod
source_site: https://gametorrahod.com/
category: game programming
fetched: '2026-04-13'
---

Your imported TMP font looks weird, kinda off from the `RectTransform`

you had setup, or broke when using multiple languages that falls back to other TMP asset? Let’s not rely on extracted data and understand it completely in this article.

## Terms

**Font, TextMesh Pro Documentation***The TextMesh Pro font creation window can be opened in the editor via Window / TextMeshPro - Font Asset Creator. The…*digitalnativestudios.com

**Font Anatomy***Font Height ()- Refers to the height of the font from the lowest descender to the highest ascender. riginally Font…*facweb.cs.depaul.edu

## What to adjust

Here’s our workspace. We will start from everything at 0.

![](../../assets/f200f3cc25be9ba4.png)

## Fallback fonts must-know

Before we start.. you maybe thinking of making an uber TMP font asset that you can assign to all your `TMP_Text`

component in your game. And somehow that magically resolves to every possible text you throw at it. **That's not how it works. **As you will learn later that you must use a combination of font asset switching **and **fallback fonts. Anyways, we will look at just how the fallback fonts works first.

Notice the fallback font list in the image. This font does not have Japanese character, so I (naively) think needs to go to an another texture when that happens. Again, this is **not** how localization would work out in the end. Be aware that :

- Fallback fonts must share the
**Line Height**with the root font. Therefore with this approach, a game in Japanese localization will get the same massive line height from Thai language where we need some room for diacritics, etc. - It can have unique everything else,
**Scale**being the most important as you must use it to “reconcile” with main font’s line height when is being fallbacked on.

## Alignment & Baseline relationship

What you see is top, middle, and bottom align with equal RectTransform matching the Unity grid.

![](../../assets/d7521adf779a1a28.png)

The top align isn’t quite the expected result, I expected the top edge of character to be at the top box. But, the meaning of Top alignment is actually : **put** **the baseline **at the top edge of the RectTransform .

So.. top align will not be “in the box” but bottom align is. Also, center align is not so “center” as when you put the baseline at center the font sticks up from it. Let’s fix these.

![](../../assets/49af03f9e556d5c5.gif)

You see

**Baseline**affects all alignment.**Ascender**do not affect bottom align. Only**positive value**is valid.**Descender**do not affect top align. Only**negative value**is valid.

So what I want to do here is the bottom align should have the descender sticking out of the box but the top and center align should be moved down a bit. So I want to adjust **only Ascender.**

Note that definition of TMP’s “Ascender” is not the same with some other source’s “Ascender”. From this two images, TMP’s Ascender is equal to the first image’s cap height.

![](../../assets/dd38795fb94cc9dc.gif)

![](../../assets/7167bb781941c05e.png)

Here’s the result of adjusting just Ascender. Top align is at the top edge, middle aling has the baseline at center of most characters, bottom align untouched.

![](../../assets/f057f77ddac4422c.png)

## Line Height — Alignment — Baseline

![](../../assets/3c209146b9fc157c.gif)

Actually the 3 on the left has 3 more lines in each. **Line Height** affects how **baseline **are spaced out from each other. If there is no line height each line’s baseline would be at the same position.

Remember that all fallback fonts will share Line Height with the root font. We will counter-adjust that later with scaling.

With only Line Height and Ascender, I could achieve this result.

![](../../assets/1f33054074db1791.png)

## Fallback font adjustment

![](../../assets/9a99e0c0568225b0.png)

Fallback font means in the TextMeshProUGUI inspector we are using the same font as previously used, but because the character isn’t there it will load up an additional texture for those fonts.

First adjust the scale to match the first font. Also notice that **Line Height has no effect at all.**

![](../../assets/57e537120e560662.png)

Then you notice **something wrong** where there is only fallback font. The last line certainly does not looks right. If I add an empty line (press enter once) then it would looks right. What’s going on?

## Lowest/Highest common Ascender/Descender

When multiple TMP are mixed via fallback system, it choose the highest or lowest Ascender/Descender **PER LINE** order to support all fonts required. Remember again that **Line Height **are fixed to the root font. Though, not ascender and descender.

What’s happening here is that all lines except the last one need 2 mixed fonts. The last one is pure Japanese. Why? Because all prior line has the **carriage return **which maps to the root font, the CR is one of the character too, and it accidentally fix my 0 ascender settings to use ascender in the fallback English font. (It will eventually fallback to Liberation Sans that is built in)

![](../../assets/bbd1166497968fb4.gif)

That is it is not related to a new line at all. I can just press space bar once instead of enter and it would inherit the highest required ascender.

![](../../assets/9bb0b216b7a2ffc6.gif)

But anyways, the correct setup is to **properly set the ascender **for Japanese font (not 0 like this), so that when there is only Japanese the ascender would be correct. But here’s the problem. Line Height is inherited from the root font regardless of required texture. So we would best set the Ascender/Descender to the same as the root font even if Japanese character does not need any Ascender.

Then the problem will be, the Japanese text will be kinda too spaced out because it is assuming Ascender of other possible languages in the game. Also line height is assumed from the other language too. This is the problem of using** fallback font. **You want to assign only one TMP font to all TextMeshProUGUI and let it handle the texture selection, so life is easy. Too bad it is not the way to go.

## Fallback font is not for localization

Then I realized that fallback font is probably for missing characters, like emoji or some weird marks. For localization the best way is to manually change the font asset field on the TextMeshProUGUI according to the language. And so you have a separated line height now. Then in those asset, you can utilize fallback font inside.

Here's how to think about it. You will need a TMP asset of equal amont of available languages. TMP asset need SDF texture generation from an actual font files and can have fallback to other TMP asset. Say I need English, Thai, and Japanese in my game. I need 3 TMP assets `X`

`Y`

`Z`

for each languages. But I only have 2 fonts I like `A`

and `B`

, the one with BOTH English and Thai glyphs (it is common to find Thai fonts that has A-Z in it) and another with **just **Japanese glyphs. How to make 3 TMP asset from this 2?

- TMP Asset
`X`

: Using font`A`

, choose only English character in SDF texture. Baseline/ascender/descender for English to look good, no fallback. - TMP Asset
`Y`

: Using font`A`

, only Thai character even though English glyphs are also available in this font file. Baseline/ascender/descender for Thai so wider than English, then set fallback to TMP Asset`X`

. When a line with mixed Thai/English came when the game’s language is Thai (the asset switched to`Y`

), we would get a spaced out mixed English sentence with room for Thai’s ascender/descender. (Expecting the sentence to be Thai-dominant, so it doesn't look like a weirdly spaced English sentence.) When the game is English, it would use just the TMP Asset`X`

with tighter line height. - TMP Asset
`Z`

: Using font`B`

, Baseline/ascender/descender for Japanese. Fallback to TMP Asset`X`

for occasional English and numbers. You see why I don't just include English and Thai in`X`

and use it for both languages, it make fallback more flexible and Japanese player will not have to use memory for Thai glyphs.

The appropriate use of fallback font is, you want consistency of number or English fonts. Numbers are universal and English is usually mixed in other languages, and in Japanese fonts you intentionally exclude the number or English glyphs in your SDF texture so it fallback to English one.

Though, in a game like Overwatch where it's main marketing font obviously don't have Japanese or Korean where Blizzard also sell the game, Blizzard choose to change them all including numbers in Japanese version. Though use mixed approach for Korean version. Anyways this also means you must be able to swap font asset file with different attributes, not by solving everything with just one uber font file with intricate fallback network.

Also by using a separated TMP asset for each language, in Japanese it uses Line Height from Japanese font because numbers are compact and not requiring ascender/descender space.

![](../../assets/68f07e2f770b9f13.png)

In this image, Japanese font grabs number texture from English font while still using **Japanese Line Height**.

### Material problems

Notice that also the **material** that it uses the one of the main font. The red outline is also from the material, and this effect depends on pixel size of SDF texture of each character.

Because I tuned the dilate and outlines according to Japanese font’s texture size (much smaller than English, since there are a lot of characters to pack) the outline on those number (where those glyphs were yanked from an another SDF texture) looks a little bit **thinner **because the Japanese material settings is being applied to English’s bigger texture.

You can fix this by telling TMP to pack the font **at fixed size for all languages** rather than trying to do the biggest that fits the texture.

The strategy is to start at language with massive character count. Make your English/Thai/whatever low character count language to the same size with Chinese/Japanese/Korean/whatever high character count language’s size that fits in a reasonable texture size. (Like 1024x1024)

For example, I required 1000 Kanji characters. I could afford up to 1024x1024, and turns out each character is at size 16 to fit the texture. Then I go to English and set the size as 16 **even if** English have very low character count and could benefit from larger SDF texture. That way when “material fallback” happen, it can looks similar. (I also think lower size's smearing effect of SDF looks kinda "artistic")

### Then how to automatically switch font assets, finally?

Then use a tool like **I2Localization **to change the assigned TMP asset based on your game’s current language. I think that’s the way to go. [Unity is making its own](https://forum.unity.com/forums/localisation-tools-previews.205/) asset swapping package, but not ready to go yet. (in 2019)

![](../../assets/b77664b08d9e5720.png)

After reconciling all languages and all mix-up cases, we can get consistent and expected behaviour in the TMP box.

![](../../assets/fadaa90fd84ab33f.png)

## Make ALL your text linked from the same prefab!!

Realizing that font asset switching is the proper way, we face a much bigger problem that is, it means, these font assets must be serialized in the scene on **each **`Localize`

component. Look at this image again. This `Localize`

component is on the scene. That 5 fonts **reference **is also serialized right in this component, and therefore bound to the `GameObject`

and the scene. There is no link to any other `Localize`

component at all even though that is what you probably want.

![](../../assets/b77664b08d9e5720.png)

It means you must re-assign **all **possible fonts for all languages again and again everywhere, without mistake, or else the fallback will not work as it only know to look on what references were serialized on **this** **component. **There is no "global" language switching set of fonts.

Therefore the strategy is for each "kind of text" (for my game, "normal" with white/black and "header" with different font and white/red material), you should make a little prefab of **just** `TMP_Text`

and compose anything else from there by instantiating this prefab everywhere.

It means a dialog of just a text, or that text on your button, or text in your option screen, anything, must be instantiated from this prefab thanks to the new nested prefab possible since 2018.3. Yes, a prefab of just a text. But the point is to go into this prefab and assign your font references and have them appear everywhere in the game automatically.

If you are too far in and just realize this, then feel a moment of silence, then prepare the next 2-3 days to replace text in an entire game to came from a single source. It will greatly reduce error and provide you more business opportunity to add a new language easily. Just add one more text asset and see it propagate to everywhere in the game. As a bonus, some settings like receive raycast which you may forgot to turn off can be propagated throughout the game.