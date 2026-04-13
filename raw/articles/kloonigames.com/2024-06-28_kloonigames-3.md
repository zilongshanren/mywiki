---
title: Kloonigames
url: https://www.kloonigames.com/blog/games/wordpyramid
published: '2024-06-28'
source_blog: Kloonigames
source_site: https://www.kloonigames.com/blog
category: game programming
fetched: '2026-04-13'
---

![Word Pyramid - Another solitaire word game.](../../assets/56ff9303b5dff065.gif)


![Word Pyramid - Another solitaire word game.](../../assets/879a7e93f194a332.gif)

Another word solitaire game appears. After

[Word Solitaire](http://kloonigames.com/blog/games/wordsolitaire)I was kinda curious as to how the game would play with an inverted setup, so I implemented a small prototype. It’s a little easier and thus might be a good “tutorial” game for

[Word Solitaire](http://kloonigames.com/blog/games/wordsolitaire).

The real reason for working on this game was not the game (although I feel the game is just *fine*), but I was more curious about working on the tech. I got a little curious as to what could be done with [Emscripten](https://emscripten.org/), which allows for C++ to be compiled into WebAssembly. This involved porting a bunch of old code to use [SDL2](https://www.libsdl.org/) and Emscripten. The process was fairly straight forward. I’ll probably end up using this tech to make some new games. So you can try [playing the game in your browser here](https://kloonigames.com/wordpyramid/).

### Word Pyramid – Release 1

### Download

Windows: [WordPyramid.zip (4.3 Mb)](https://www.kloonigames.com/download.php?file=wordpyramid.zip) (Release 1)

**Instructions**

Word game + Solitaire. You need to clear the board by doing 5 letter words.

- A-Z = To form words
- CTRL+Z = UNDO
- CTRL+Y = REDO
- RETURN = Input word
- BACKSPACE = Erase letter

**Credits**

Game Design & Code: Petri Purho ( petri.purho (at) gmail.com )