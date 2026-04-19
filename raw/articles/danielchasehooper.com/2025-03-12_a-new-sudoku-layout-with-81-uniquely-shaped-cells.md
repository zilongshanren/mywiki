---
title: A New Sudoku Layout With 81 Uniquely Shaped Cells
url: https://danielchasehooper.com/posts/cracked-sudoku/
published: '2025-03-12'
source_blog: Daniel Hooper
source_site: https://danielchasehooper.com/
category: graphics
fetched: '2026-04-19'
---

March 12, 2025・5 minute read

Something productive finally came from my daily Sudoku habit: I invented a new type of puzzle that I call “Cracked Sudoku”. It’s named after [cracked dirt](https://duckduckgo.com/?t=h_&q=cracked+dirt&iax=images&ia=images):

Even though it looks weird, the rules should feel familiar to Sudoku fans:

Fill the cells with numbers 1-9 without repeating numbers in a dark-outlined group or along a colored run line.


Give it a try:

Those of you with a life may be unaware that the past 10 years have seen an explosion of alternative Sudoku rules:

German Whisper Lines, Dutch flat mates, Killer cages, Yin-yang (My favorite), Fog-of-war, Sum arrows, Even & Odd squares, Thermometers, Black dots, White dots, Jigsaw Sudo, Renban lines, Nabner lines, Star Battle, Masyu loop, Inequality signs, Region sum lines


Whew.

Despite all the innovation in *rules*, there has been comparatively little innovation in *layout*. Pretty much all Sudoku use a 9x9 grid. There are variants using hexagons or triangles, but they’re rare and the solving experience isn’t that different from a grid.

To address this, I realized that it’s possible to tweak Sudoku’s rules to allow for cells of any shape, which produces a different layout on every puzzle:

These layouts are generated from [Voronoi Diagrams](https://en.wikipedia.org/wiki/Voronoi_diagram), but you could design a Cracked Sudoku other ways too.

They still have 81 cells in 9 groups just like classic Sudoku. However instead of “rows” and “columns” Cracked Sudoku have “runs”. Runs are a strip of 2 to 9 cells that can’t contain repeated numbers. Here’s one puzzle with its runs shown:

The randomly assigned line colors exist only to help distinguish separate runs 1.

The puzzle generator I wrote (more on that in a bit) creates runs based on the cell layout: Runs connect all neighboring cells and can continue through the opposite side to form a longer run. “Opposite” for a N-sided polygon means “two sides that are N/2 sides away from each other”. That’s a confusing explanation for something I hope you intuitively understand from the image above. Runs terminate on cells with an odd number of sides because the concept of “opposite sides” doesn’t work with an odd number of sides.

A human constructor could place runs wherever they like.

Runs can form interesting structures. Here, the green and orange runs cross in more than one cell:

Theoretically my generator could produce a run forming a loop, but I didn’t encounter any. If my generator were to produce a loop under its run logic, it would need a layout like this:

Human-designed puzzles are more interesting to solve than computer generated, so ideally I’d have a human designed Cracked Sudoku for you (and me!). Unfortunately I’m not an experienced puzzle constructor, so I wrote a puzzle generator.

It works in 4 phases:

And with that, I could generate Cracked Sudoku. I left it running long enough generate thousands of puzzles – enough for several years of daily puzzles.

A few things I’d do if I kept working on this:

Have you made a Sudoku that was featured by [Cracking the Cryptic](https://www.youtube.com/c/CrackingTheCryptic)? If so, I would love to coauthor a human-made Cracked Sudoku and have Cracking the Cryptic solve it (a nerd dream of mine). I don’t have enough construction experience to make a high quality one by myself. Email “daniel” at this website’s domain if you’re interested. For everyone else, subscribe to my newsletter to be alerted about the first human-made Cracked Sudoku.

You can play Cracked Sudoku [here](https://danielchasehooper.com/projects/cracked-sudoku/). It has a new puzzle every day, just like Wordle.