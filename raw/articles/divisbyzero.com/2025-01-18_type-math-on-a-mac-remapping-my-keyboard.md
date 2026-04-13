---
title: Type Math on a Mac—Remapping My Keyboard
url: https://divisbyzero.com/2025/01/18/type-math-on-a-mac-remapping-my-keyboard/
author: Dave Richeson
published: '2025-01-18'
source_blog: 'David Richeson: Division by Zero'
source_site: https://divisbyzero.com
category: game programming
fetched: '2026-04-13'
---

I use LaTeX to type mathematical documents. However, I often want to type mathematics when LaTeX is unavailable—for instance, in an email to a student, in a social media post, etc. To do so, I typically go to one of the many websites that offer “copy-and-paste” mathematical symbols, Greek letters, or subscript/superscripts. It is do-able but annoying.

For Christmas, my son made me a mechanical keyboard. It was so thoughtful—a solid keyboard base with high-quality switches and elegant keycaps. There are many ways to customize the keyboard. I asked him if it was possible to enable it to type Greek letters and other mathematical notation using various key combinations. He looked into it and found a fantastic method that should work for any keyboard (on a Mac).

Basically, you create a text file called DefaultKeyBinding.dict and put it in a folder called Keybindings in your Library. (In the Finder, select the “Go” menu while pressing the option key. You’ll see you can open your Library. In it, create the Keybindings folder and put your text file in there.) For it to take effect in an app you’re using, you need to restart the app after modifying the dict file.

The text file could look something like this:

```
{
// double slashes indicate comments
"~#2" = (insertText:, "\U2082"); // option-2 on the number pad will produce the subscript 2
"~$#2" = (insertText:, "\U00B2"); // option-shift-2 on the nubmer pad will produce superscript 2
"~t" = (insertText:, "\U03B8"); // option-t produces a theta
"~$D" = (insertText:, "\U0394"); // option-shift-D will produce a capital delta
"~$E" = (insertText:, "\U2203"); // option-shift-E will produce the "there exists" symbol
}
```


As you should be able to tell, the first part of each line tells what modifier keys you need to press along with the key on the keyboard. They are

~ : option

$ : shift

^ : control

@ : command

# : numpad

The output is the Unicode for the desired symbol. I found [this Wikipedia page helpful](https://en.wikipedia.org/wiki/Apple_Symbols) in finding the Unicode for my desired characters.

I created key combinations that type many of the Greek letters in lower case, some of them capitalized, basic set notation (intersection, union, subset, element of, etc.), the “blackboard bold” notation for sets of numbers (like the real numbers and the integers), and so on. I created a way to get superscripts and subscripts by using the option key or shift-option and typing on the number pad.

Finally, I made a cheat sheet to help me remember what’s where on my keyboard.

![](../../assets/46693119cf9c1910.png)


![](../../assets/46693119cf9c1910.png)

In case you are interested, here’s the file I created. (I tried to upload the file so it could be downloaded, but this blogging platform did not allow me to do so. You’ll have to copy and paste this into your own text file.) There were a few that didn’t work for me—like remapping option-shift-#—I suspect that there is some escape code that would make it work, but I didn’t look into it.

```
{
// Save as ~/Library/KeyBindings/DefaultKeyBinding.dict
// ~ : option
// $ : shift
// # : numpad
// ^ : control
// @ : command
// helpful website: https://en.wikipedia.org/wiki/Apple_Symbols
// subscript (option + numpad 0-9)
"~#0" = (insertText:, "\U2080"); // subscript 0 ₀
"~#1" = (insertText:, "\U2081"); // subscript 1 ₁
"~#2" = (insertText:, "\U2082"); // subscript 2 ₂
"~#3" = (insertText:, "\U2083"); // subscript 3 ₃
"~#4" = (insertText:, "\U2084"); // subscript 4 ₄
"~#5" = (insertText:, "\U2085"); // subscript 5 ₅
"~#6" = (insertText:, "\U2086"); // subscript 6 ₆
"~#7" = (insertText:, "\U2087"); // subscript 7 ₇
"~#8" = (insertText:, "\U2088"); // subscript 8 ₈
"~#9" = (insertText:, "\U2089"); // subscript 9 ₉
// superscript (option + shift + numpad 0-9)
"~$#0" = (insertText:, "\U2070"); // superscript 0 ⁰
"~$#1" = (insertText:, "\U00B9"); // superscript 1 ¹
"~$#2" = (insertText:, "\U00B2"); // superscript 2 ²
"~$#3" = (insertText:, "\U00B3"); // superscript 3 ³
"~$#4" = (insertText:, "\U2074"); // superscript 4 ⁴
"~$#5" = (insertText:, "\U2075"); // superscript 5 ⁵
"~$#6" = (insertText:, "\U2076"); // superscript 6 ⁶
"~$#7" = (insertText:, "\U2077"); // superscript 7 ⁷
"~$#8" = (insertText:, "\U2078"); // superscript 8 ⁸
"~$#9" = (insertText:, "\U2079"); // superscript 9 ⁹
// option + letter
// "~1" = (insertText:, ""); //
// "~2" = (insertText:, ""); //
// "~3" = (insertText:, ""); //
// "~4" = (insertText:, ""); //
// "~5" = (insertText:, ""); // Leave alone---infinity ∞
// "~6" = (insertText:, ""); //
// "~7" = (insertText:, ""); //
// "~8" = (insertText:, ""); // Leave alone---bullet symbol •
// "~9" = (insertText:, ""); //
// "~0" = (insertText:, ""); //
// "~-" = (insertText:, ""); // Leave alone---en-dash –
// "~=" = (insertText:, ""); // Leave alone---not equal ≠
"~a" = (insertText:, "\U03B1"); // α
"~b" = (insertText:, "\U03B2"); // β
"~c" = (insertText:, "\U03B5"); // ε
"~d" = (insertText:, "\U03B4"); // δ
// "~e" = (insertText:, ""); // Leave alone---produces the acute accent
"~f" = (insertText:, "\U03C6"); // φ
"~g" = (insertText:, "\U03B3"); // γ
"~h" = (insertText:, "\U03B7"); // η
// "~i" = (insertText:, ""); // Leave alone---produces an accent
"~j" = (insertText:, "\U03C4"); // τ
"~k" = (insertText:, "\U03BA"); // κ
"~l" = (insertText:, "\U03BB"); // λ
"~m" = (insertText:, "\U03BC"); // μ
// "~n" = (insertText:, ""); // Leave alone---produces an accent
// "~o" = (insertText:, ""); //
"~p" = (insertText:, "\U03C0"); // π
"~q" = (insertText:, "\U03BE"); // ξ
"~r" = (insertText:, "\U03C1"); // ρ
"~s" = (insertText:, "\U03C3"); // σ
"~t" = (insertText:, "\U03B8"); // θ
// "~u" = (insertText:, ""); // Leave alone---produces the umlaut
"~v" = (insertText:,"\U03BD"); // ν
"~w" = (insertText:, "\U03C9"); // ω
"~x" = (insertText:, "\U03C7"); // χ
"~y" = (insertText:, "\U03C8"); // ψ
"~z" = (insertText:, "\U03B6"); // ζ
// "~`" = (insertText:, ""); // Leave alone---produces an accent
"~[" = (insertText:, "\U2229"); // intersection ∩
"~]" = (insertText:, "\U222A"); // union ∪
// "~\" = (insertText:, ""); //
// "~;" = (insertText:, ""); //
// "~'" = (insertText:, ""); //
// "~," = (insertText:, ""); // Leave alone---produces less than or equal to ≤
// "~." = (insertText:, ""); // Leave alone---produces greater than or equal to ≥
// "~/" = (insertText:, ""); // Leave alone---produces the division symbol ÷
// option + shift + letter
// "~$~" = (insertText:, ""); // leave alone---causes an error
"~$!" = (insertText:, "\U2248"); // ≈
// "~$@" = (insertText:, ""); // leave alone---causes an error
// "~$#" = (insertText:, ""); // leave alone---causes an error
// "~$$" = (insertText:, ""); // leave alone---causes an error
"~$%" = (insertText:, "\U222B"); // ∫
// "~$^" = (insertText:, ""); // leave alone---causes an error
"~$&" = (insertText:, "\U221A"); // √
// "~$*" = (insertText:, ""); // Leave alone---degree symbol °
"~$(" = (insertText:, "\U27E8"); // left angle bracket ⟨
"~$)" = (insertText:, "\U27E9"); // right angle bracket ⟩
// "~$_" = (insertText:, ""); // Leave alone---em-dash —
// "~$+" = (insertText:, ""); // Leave alone---plus-minus ±
"~$A" = (insertText:, "\U2200"); // for all ∀
"~$B" = (insertText:, "\U2135"); // Alef ℵ
"~$C" = (insertText:, "\U2102"); // Complex numbers ℂ
"~$D" = (insertText:, "\U0394"); // Delta Δ
"~$E" = (insertText:, "\U2203"); // there exists ∃
"~$F" = (insertText:, "\U220A"); // element of ∊
"~$G" = (insertText:, "\U0393"); // Gamma Γ
"~$H" = (insertText:, "\U2190"); // left arrow ←
"~$I" = (insertText:, "\U2194"); // double arrow ↔
"~$J" = (insertText:, "\U21D0"); // double left arrow ⇐
"~$K" = (insertText:, "\U21D2"); // doubleright arrow ⇒
"~$L" = (insertText:, "\U2192"); // right arrow →
"~$M" = (insertText:, "\U2193"); // down arrow ↓
"~$N" = (insertText:, "\U2115"); // Natural numbers ℕ
"~$O" = (insertText:, "\U2207"); // nabla (gradient) ∇
"~$P" = (insertText:, "\U2119"); // Projective plane ℙ
"~$Q" = (insertText:, "\U211A"); // Rational numbers ℚ
"~$R" = (insertText:, "\U211D"); // Real numbers ℝ
"~$S" = (insertText:, "\U03A3"); // Σ
// "~$T" = (insertText:, ""); //
"~$U" = (insertText:, "\U2191"); // up arrow ↑
"~$V" = (insertText:, "\U2209"); // not an element of ∉
// "~$W" = (insertText:, ""); //
"~$X" = (insertText:, "\U2A2F"); // times/cross product ⨯
// "~$Y" = (insertText:, ""); //
"~$Z" = (insertText:, "\U2124"); // Integers ℤ
"~${" = (insertText:, "\U2227"); // and ∧
"~$}" = (insertText:, "\U2228"); // or ∨
// "~$|" = (insertText:, ""); //
"~$:" = (insertText:, "\U039B"); // Gamma Λ
// "~$"" = (insertText:, ""); //
// "~$:" = (insertText:, ""); //
// "~$"" = (insertText:, "\U2228"); // Leave alone---causes an error
"~$<" = (insertText:, "\U2286"); // subset ⊆
"~$>" = (insertText:, "\U2287"); // supset ⊇
// "~$?" = (insertText:, ""); //
}
```


The article is a practical and concise guide. It offers clear steps for customizing keys, making it easier to type notation like ∀, ∃, or ∑. A great resource for improving workflow efficiency—thank you for the useful tips!