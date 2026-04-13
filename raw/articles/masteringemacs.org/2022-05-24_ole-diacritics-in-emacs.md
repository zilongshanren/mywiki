---
title: Olé! Diacritics in Emacs
url: https://www.masteringemacs.org/article/diacritics-in-emacs
author: Mickey Petersen
published: '2022-05-24'
source_blog: Mastering Emacs
source_site: https://www.masteringemacs.org/feed
category: game programming
fetched: '2026-04-13'
---

If you’ve ever had to write the word *résumé* or *über* or *smörgåsbord* and, like me, lacked the keyboard character set to do it, you’ve probably reached for an external program to type those characters. That’s completely unnecessary though, as Emacs has complete support for Unicode and has several input methods that makes Emacs act like a bilingual keyboard but without the hassle of having to change your keyboard character set.

Emacs has three modes for inserting symbols and diacritical marks: *Unicode Code Points*, *Character Composition* and *Multilingual Text Input*.

## Unicode Code Points

Because Emacs’s internal display and text engine supports Unicode you can make Emacs insert any character you like. Emacs will also, for some sets of fonts, substitute one for another if the code point is not supported by your default font.

To insert a code point type *C-x 8 RET* and enter the Unicode name (type `TAB`

twice to get a complete list).

Here’s *SNOWMAN* and *SNOWFLAKE*:

`☃❄`


### Emoji

If you want to insert Emoji – and you want colorful ones – you should read some of my other articles on that subject: [Inserting Emoji with Input Methods](https://www.masteringemacs.org/article/inserting-emoji-input-methods) and [Unicode, Ligatures and Color Emoji](https://www.masteringemacs.org/article/unicode-ligatures-color-emoji)

## Character Composition

This is a simpler way of entering ANSI symbols. To write *Olé* You’d type: `O l C-x 8 ' e`

.

To get a list of all available character compositions type `C-x 8 C-h`

. And to get a list of all accented characters you can type `C-x 8 ' C-h`

, and so on.

## Multilingual Text Input

The Multilingual Text Input hooks into all typeable symbols and augment them so they act like a *dead key*. If you don’t know what that is, you’ve never used a type writer or a keyboard character set with accented characters.

A dead key is a key like the acute accent(`´`

) that attaches itself to character typed immediately after the dead key. So to write *Olé* on a Spanish keyboard you’d type `O l ´ e`

.

Emacs’s Multilingual Text Input mode does exactly the same. To enable it, type `C-\`

or `M-x toggle-input-method`

select an input method (I picked `latin-1`

). If the input method is toggled on, you should see an abbreviation of the method you picked appear in the left-hand corner of your modeline.

Now type a symbol like an apostrophe(`'`

) and Emacs will ask for a symbol to attach the character to, and you’re done.

To change the input method again, type `C-x RET C-\`

or `M-x set-input-method`

.

Although I used `latin-1`

you can use any number of input methods, even ones that aren’t tied to a language *per se*, like `sgml`

or `TeX`

.

The TeX input method in particular deserves a mention, because it lets you insert symbols the same way you would in a TeX document: by requiring the escape character `\`

*first* you can use the other symbols on your keyboard with impunity.

The “utility” input methods are useful indeed, and they show you just how powerful Emacs truly is: it even supports the International Phonetic Alphabet (IPA).