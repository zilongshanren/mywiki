---
title: Using Unity’s TextGenerator.verts
url: https://www.boristhebrave.com/2021/06/20/using-unitys-textgenerator-verts/
author: Boris
published: '2021-06-20'
source_blog: BorisTheBrave.Com
source_site: https://www.boristhebrave.com/
category: graphics
fetched: '2026-04-19'
---

`TextGenerator.verts`

is *meant* to give the position information of every character in a given string. This is useful in Unity if you need to align something with exactly where some particular text is occuring, if for some reason you are not already using TextMeshPro.

Older Unity versions created 4 verts for every character, which made life easy. But now many non-rendering characters don’t have verts generated for them, and the relationship between verts and characters is undocumented. I’ve reverse engineered it, as best as I can tell:

```
int? GetVertForPosition(int position, string text, TextGenerator textGenerator)
{
var c = 0;
var vert = 0;
for (var i = 0; i < position; i++)
{
if (textGenerator.characters.Count <= c)
return null;
if (!char.IsWhiteSpace(text[i]) && textGenerator.characters[c].charWidth > 0)
vert += 4;
if (text[i] != '\n')
c++;
}
return vert;
}
```