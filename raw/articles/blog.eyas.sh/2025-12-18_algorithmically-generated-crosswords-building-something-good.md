---
title: 'Algorithmically Generated Crosswords: Building something ''good enough'' for
  an NP-Complete problem'
url: https://blog.eyas.sh/2025/12/algorithmic-crosswords/
author: Eyas Sharaiha
published: '2025-12-18'
source_blog: Eyas's Blog
source_site: https://blog.eyas.sh/
category: game programming
fetched: '2026-04-13'
---

Generating crossword puzzles is NP-Complete. Every cell where two words intersect creates a constraint that both words must satisfy, and those constraints multiply across the grid into a combinatorial explosion. There’s no efficient algorithm that guarantees a solution—but with the right heuristics, you can build something that works surprisingly well.

In late 2021, deep in lockdown, my NYT Crossword obsession turned into a side
project. I wanted to build a crossword app, realized I needed puzzles, tried
making them by hand, found that tedious, and wondered: could I generate them
algorithmically? Earlier this year, I finally shipped
[Crosswarped](https://crosswarped.com/) on iOS and Android — a crossword game
powered by the generator I’ll describe here.

**Figure 1: The Crossword Constraint Problem.**
Where horizontal word “START” crosses vertical word “PLACE”, both must share the letter ‘A’ at that position.
This simple constraint, multiplied across an entire grid, creates an NP-Complete puzzle.

It turns out, around the same time [Otis Peterson](https://otispeterson.com/)
was [working on the same thing](https://crosswordconstruction.com/) at
Swarthmore College, where they presented their findings in 2021. The
[source](https://github.com/MichaelWehar/Automatic-Crossword-Puzzle-Filling) was
published in December 2024. I discovered this while writing, hoping for a neat
proof that crossword generation is NP-Complete.
[Turns out, it is a good one to cite](https://www.crosswordconstruction.com/npcomplete)!

Crossword generation algorithms, including Peterson’s, tend to solve a constrained version of the general problem that is still NP-Complete: Given a pattern of blocks and white squares, fill in the white squares with words from a dictionary such that all across and down words are valid. “Crossword filling” as it is called, is NP-Complete on its own.

I wanted to solve a different problem: **generate both the pattern and the words
simultaneously**. Instead of starting with a fixed grid layout, my algorithm
decides where to place black squares as it goes.

This freedom might seem like it would make things easier: if a word doesn’t fit, just add a black square! But I think it also causes the solution space to explode.

### Huge Solution Spaces for Crosswords

Consider a single row of squares. Let’s call the set of all valid ways to fill that row . This set includes:

**Full-length words:**All words of exactly letters from the dictionary (including phrases like “BADIDEA” which are valid entries in crossword dictionaries)**Shorter words with edge blocks:**Any valid row of length (that’s ) with a black square before or after it**Split words:**Two shorter words separated by a black square—all combinations where the lengths add up to (accounting for the block)

**Figure 2: The Explosion of Row Possibilities.**
A single 7-square row doesn’t just contain 7-letter words—it can hold any valid combination of shorter words separated by blocks.
This combinatorial explosion is why naive approaches fail quickly.

## The Code

If you want to explore the implementation:

**Go version** (recommended): The
[main branch](https://github.com/Eyas/xwgen/tree/main) of
[Eyas/xwgen](https://github.com/Eyas/xwgen) contains a polished implementation.
This powers a GCP Cloud Function I use to generate puzzles from a web-based
admin tool. The code builds standalone, though you’ll need to implement the word
list loader (mine queries a BigQuery table).

**C# version** (historical): The
[ csharp branch](https://github.com/Eyas/xwgen/tree/csharp) has my original
implementation, integrated with a Windows UI editor. I extracted it from a
larger prototyping codebase using

[. It won’t build out of the box (hardcoded paths to word lists that don’t exist), but it shows the evolution of the algorithm.](https://github.com/newren/git-filter-repo)

`git filter-repo`

## Approaching the problem

When tackling an NP-Complete problem, you start with the understanding that the perfect is the enemy of the good. This is freeing; it encourages you to begin with the simplest approach and iterate.

My first attempt was a totally greedy algorithm: pick a random word that fits
*within* the first row, then find a perpendicular word that fits, and so on,
backtracking when stuck.

Then I tried this on a 5x5 grid. Nothing. Just kept looping for minutes. I started visualizing what it’s doing to understand how soon it failed. It fails very soon, it turns out; if we are picking words randomly just because they fit with what exists, 3 or 4 words in, and we exhaust all options for the next word.

### Thinking in Rows

The first insight: instead of picking individual words, think about the **entire
set of valid lines** for each row and column.

I recursively defined my possible rows set and used that to build the grid one row/column at a time.

At , the grid is empty, and each row and column has a *possible lines*
set equal to (where is the side length of the puzzle).

Then, I pick one value for one random row or column and filter each row or column to the compatible set of their possible lines and go from there.

This was really slow, but it sometimes worked for 5x5 grids. It was a memory hog though, and my machine ran out of memory trying to do 7x7 grids.

### Lazy evaluation of possibilities

The set of all possible lines is enormous—but we don’t need to materialize it.
Instead, we can represent it as a **tree of options** that we filter lazily.

In other words, a “possible lines set” is a lazily-filterable *description* of a
huge set. It supports operations like “filter by a letter constraint at position
(i)” and “is this set empty?” without enumerating the entire thing.

For a 5-letter line, the possibilities aren’t stored as a flat list. They’re a
tree: a `Words`

node (5-letter dictionary words) combined with structural
variants (`BlockBefore`

, `BlockAfter`

, etc.).

The recursive grammar is defined by an interface that allows us to treat “a list of words” and “a complex structure of words and blocks” uniformly:

```
type PossibleLines interface {
FilterAny(constraint rune, index int) PossibleLines
}
```


The base case is a simple list of **Words** from our dictionary. From there, we
build complexity recursively:

**BlockBefore**: A line that starts with a black square, followed by a valid line of length .**BlockAfter**: A line that ends with a black square.**BlockBetween**: A line formed by`Line(A) + Block + Line(B)`

, where .

In the Go implementation, `BlockBetween`

is a struct that holds two child
`PossibleLines`

trees. It doesn’t store the resulting words, just the recipe for
combining them:

```
type BlockBetween struct {
first PossibleLines
second PossibleLines
}
```


This structure allows us to represent combinatorial explosions compactly. A
`BlockBetween`

doesn’t store every combination of `first`

and `second`

; it just
holds references to them and can express the cross product of the two sets. In
practice, it never needs to iterate through the entire set.

For a 5-letter line, for example, the set of possible lines looks like:

```
AllPossibleLines[5] =
Compound(
Words(WordsByLength[5]...),
BlockBefore(AllPossibleLines[4]),
BlockAfter(AllPossibleLines[4]),
)
```


Types like `Compound`

, `BlockBefore`

, `BlockAfter`

, and `BlockBetween`

implement
primitives like iterating over all possible answers, computing the (approximate)
size of the set, and filtering the set based on constraints, all without ever
materializing the entire set.

This was already a game changer, and I could now do 10x10 grids with some luck, though that could take hours.

### Constraint Propagation

With lazy data structures in place, we can efficiently propagate constraints
using an [AC-3](https://en.wikipedia.org/wiki/AC-3_algorithm) style algorithm.

When we commit to a word in one row, every intersecting column learns something
new. If Row 3, Column 4 *must* be ‘E’ (because of a vertical word crossing it),
we tell Row 3’s `PossibleLines`

to `Filter('E', 4)`

.

The `Filter`

method trickles down the tree. For example, for a `BlockBetween`

,
it does:

**BlockBetween**: “Hey`first`

part, do you look at index 4? Yes? Okay, filter yourself. No? Okay`second`

part, you filter yourself.”**Words**: “Hey, filter out any word that doesn’t have ‘E’ at this index.”

**Figure 3: Constraint Propagation.**
When we commit to “START” in row 1, each column must now start with that letter.
This single choice filters out ~90% of possibilities in each crossing column.

### Domain Splitting: Binary Search on the Solution Space

Even with lazy evaluation and constraint propagation, I was still making progress too slowly—picking a random word from the possibilities and filtering the grid based on that choice.

The key insight: instead of picking specific words, we can **bisect the
possibility space**. If a row has 10,000 possible lines, we don’t pick one—we
split them in half and ask: “Can the grid be solved if this row uses a word from
the first half of the dictionary (A-M)?”

Here’s the crucial part: **we don’t actually check every word in that half**.
Instead, we simply *decide* to restrict that row to words from A-M, then
propagate the consequences through the grid using constraint propagation. The
row now only accepts words starting with A through M, which constrains the first
column to letters that could start words from the A-M portion of the dictionary,
and so on.

After propagation, one of three things happens:

**Contradiction**: Some row or column ends up with zero valid options. We’ve proven that no word in the A-M range can work here, so we instantly prune 5,000 words and try N-Z instead.**Solution found**: We’ve narrowed everything down to specific words — done!**Still ambiguous**: Multiple options remain. We pick the most constrained row/column and split*its*possibilities in half, recursing deeper.

This way, as long as we represent our “filtered possibilities” efficiently (and
lazily) enough, each step in this splitting is relatively cheap, with the heavy
lifting done by constraint propagation. To keep `PossibleLines`

efficient:

- it needs to be an
*immutable*structure that we don’t have to clone on each split - conceptual lists (e.g. lists of words or compound possibilities) need to
support efficient slicing without copying data (like Go’s slices, a C++
`span`

, etc.)

This way, each split keeps the possibilities that haven’t changed, and very cheaply replaces the ones we are bisecting.

Propagating actual constraints on a line will often result in more allocations, e.g. removing every word that doesn’t match a constraint at some given index. But we typically only do that when we’re about to recurse deeper into that search space.

**Figure 4: Domain Splitting.**
The root represents all possible words for a row. Instead of picking one word,
we split them in half and explore one branch. If it fails, we’ve pruned
half the dictionary in one step.

One thing I was doing that was still quite slow was picking one row or column, and picking a ‘random’ value in its possible lines set and using that to filter the rest of the grid.

Since we now have these lazy sets, can each “choice” we do be a bisection of that set?

We ask the `PossibleLines`

object to `MakeChoice()`

.

- If it’s a list of
`Words`

, it splits them in half - If it’s a
`BlockBetween`

, it splits based on the possibilities of one side

```
// From generator.go
func (g *Generator) PossibleGrids(ctx context.Context) iter.Seq[Grid] {
// ...
// Finds the "least undecided" line
undecidedDown := root.getUndecidedIndexDown()
// Splits the possibilities into two sets
// ...
}
```


This effectively binary searches the solution space. If “Row 1 uses a word from A-M” leads to a contradiction, we’ve pruned half the dictionary for that row instantly.

Our *possible lines* types need to now support new operations: getting the set
of characters they *could* contain at a particular index and filtering out any
options that don’t contain any of a given set of characters at a given index.

With this in place, 10x10 grids became solvable in seconds.

#### Disqualifying choices

Satisfying word constraints isn’t enough—a grid can have all valid words and still be unusable. Invalid grids include:

**Repeated words:**The same word appearing twice in the puzzle**Disconnected regions:**Black squares that split the grid into isolated islands**Too many blocks:**Grids where black squares dominate, leaving too few actual words

(Traditional crosswords also require 180° rotational symmetry, but I intentionally skip that constraint—it’s aesthetic, not structural.)

The naive approach is to check these conditions only when we reach a complete grid (a leaf of the search tree). But by now, you can probably guess: that’s far too slow.

Instead, we check for definite invalidity as early as possible. Since each
`PossibleLines`

tracks not just what characters are *possible* but which are
*certain*, we can detect problems mid-search. If the current state *definitely*
places blocks that would disconnect the grid, we prune that entire subtree
immediately—no need to explore further.

### Fast Character Set Operations

At each position in a line, we need to track which characters are still possible. This gets checked millions of times during search, so it needs to be fast.

My first implementation of this `CharSet`

was a literal set of characters.
Copying this around each time there was a new constraint was very slow.

My second attempt was a tight list of booleans, one per character for my
alphabet and block character. I decided to use `a`

to `z`

and ```

as my
block character, since it was right before `a`

in ASCII, so I could have an
fully-utilized array with no gaps that I could easily test in time.

The final iteration solved these issues: a `uint32`

bitmask. We only need 27
characters (`a`

-`z`

plus the block character ```

, conveniently adjacent in
ASCII), which fits perfectly. Set intersection becomes a single bitwise AND.

```
// CharSet efficiently represents a set of characters using bit manipulation.
// It supports characters from '`' (96) to 'z' (122), total of 27 characters.
// This fits perfectly in a uint32.
type CharSet struct {
bits uint32
}
const (
minChar = '`' // 96
maxChar = 'z' // 122
numChars = maxChar - minChar + 1 // 27 characters
fullBits = 0x7ffffff
)
func (c *CharSet) Add(r rune) error { /*...*/ }
func (c *CharSet) AddAll(other *CharSet) { /*...*/ }
func (c *CharSet) Contains(r rune) bool { /*...*/ }
func (c CharSet) IsFull() bool { /*...*/ }
func (c CharSet) Count() int { /*...*/ }
func (c *CharSet) Clear() { /*...*/ }
func (c *CharSet) Clone() *CharSet { /*...*/ }
func (c *CharSet) ContainsAll(other *CharSet) bool { /*...*/ }
func (c *CharSet) Intersect(other *CharSet) { /*...*/ }
func (c CharSet) Intersects(other CharSet) bool { /*...*/ }
```


Most operations are single bitwise instructions. When filtering, we can instantly tell if a subtree is dead (empty intersection), fully unconstrained (all bits set), or partially constrained (needs further filtering). Dead or unconstrained subtrees can be discarded or reused without copying.

## What About Clues?

When you start generating crosswords like it’s nobody’s business, you realize that clues are a whole other can of worms. When I started this project, clue generation was not conceivably automatable. LLMs change that, but at the risk of turning my app idea into a slop factory.

For my first pass of actually turning the generated grids into puzzles with clues, I wrote my own clues. In another post, maybe, I should share how AI and LLMs inevitably crept into that part of the process as well.

## Closing Thoughts

This journey was less about proving anything and more about finding a pragmatic way through an NP-Complete thicket. Lazy sets, fast bitmask filters, and domain splitting were enough to make small crossword generation feel alive and usable. It is not perfect, but it produces puzzles quickly.

The generated puzzles still feel *artificial*, there is a beauty to
human-crafted crosswords that is hard to replicate algorithmically. But if you
finished all your human-crafted crosswords for the day and want more, these
crosswords fill the gap!