---
title: Blur Shaders Pro
url: https://danielilett.com/blur-shaders-pro/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

*Blur Shaders Pro* is a bundle of blur shaders from the *Snapshot Shaders Pro* package. These blur shaders are designed to be efficient and flexible.

Use the menu button on the left to navigate through each effect in the pack.

# ✨ Features

*Blur Shaders Pro* gives you a handful of blurring algorithms with configurable kernel size and some optimizations.

## 📦 Works out of the box with volumes

Each blur effect in the pack can be attached to a volume profile and added to any volume in your scene. The effects start off in a neutral state, so just override the effect parameters and see the shaders come to life!

## 📚 Stackable effects

These effects stack with any other effect you would normally add as a Renderer Feature to URP. Mix and match with Unity’s built-in post processing effects or other shader packs! Note: I can’t guarantee compatability with any given asset pack.

## 🛠️ Fast and efficient blur

The **Gaussian** and **Box Blur** effects are implemented with an efficient two-pass solution on all render pipelines, and all blur effects have a **Step Size** option which can make the blurring kernel more sparse, so you still get a large blur, with a trade-off between efficiency and fidelity. In my own testing, you can drastically reduce the number of texture samples with a nearly indistinguishable quality level in some cases.