---
title: 'Gameboy Development, Part 1: Hello World!'
url: https://www.4rknova.com/blog/2023/08/06/gb-dev-pt-1
author: Nikolaos Papadopoulos
published: '2023-08-06'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

# Introduction

The original Nintendo Gameboy was released in 1989 and is one of the most recognisable game consoles from the 90s era. I’ve always wanted to write a game for it, but sadly this was a project that I kept postponing, mainly due to the associated complexity and dedication required when working with assembly code.

This series of blog posts aim to serve as a collection of notes for myself, but I am also taking this opportunity to share my findings in the hope that they may be useful for your own projects.

My objective is to create a simple, yet fully functional game, written entirely in assembly. I will begin this journey with the simplest possible program that runs on the Gameboy and build upon it iteratively. In each iteration, I will go through the code, line by line, and explain what each instruction does. I will also try to give further context around some subtle details that might not be obvious at first glance.

In this post, I introduce the development tools and then write a simple program that prints “hello world!” on the screen.

# The tools of the trade

My development platform is Debian Linux, however you should be able to follow the same process under any OS. I use the RGBDS toolchain, with Vim serving as my IDE, and BGB for debugging.

![A screenshot of BGB's interface](../../assets/e1b5bdd69f2a018e.png)


You can download the toolchain and the debugger using the links below:

The toolchain is fairly simple to follow.