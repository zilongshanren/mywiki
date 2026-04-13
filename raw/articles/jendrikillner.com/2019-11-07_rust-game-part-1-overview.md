---
title: Rust Game - Part 1 - Overview
url: https://www.jendrikillner.com/post/rust-game-part-1/
author: Jendrik Illner
published: '2019-11-07'
source_blog: Weekly on Jendrik Illner - 3D Programmer
source_site: https://www.jendrikillner.com/tags/weekly/
category: graphics
fetched: '2026-04-13'
---

This is the start of a series of small posts about my game development endeavors using Rust. I have been using Rust more and more in my free time projects but never used it in a larger project.

This will be my first larger project using Rust, and I will talk about my learnings here. So what I am making?

![Expected Visual Result alt text](../../assets/4d0f57cf5d48aba9.png)


Going to make a simple “Match 3” game from scratch.

My goals for the final project result are

- Implement full game-flow (Menus, Options, Loading, Gameplay, Pause screen, etc.)
- Multiple levels
- Save game system
- Audio (Music and Sound Effects)

Constraints

- Windows only
- fixed resolution
- D3D11 renderer
- using no external crates at runtime, besides
[winapi](https://crates.io/crates/winapi)

Tools might be using some crates, but I want to keep the game itself free from external dependencies as much as possible.