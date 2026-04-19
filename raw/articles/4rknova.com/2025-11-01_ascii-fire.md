---
title: ASCII Fire
url: https://www.4rknova.com/blog/2025/11/01/ascii-fire
author: Nikolaos Papadopoulos
published: '2025-11-01'
source_blog: Nikos Papadopoulos - Portfolio
source_site: https://www.4rknova.com/
category: graphics
fetched: '2026-04-19'
---

The fire effect is one of the most iconic demos from the demoscene era. It first appeared in the late 1980s and became a rite of passage for demo programmers. Despite its simplicity, the effect creates surprisingly convincing animated flames using nothing but basic arithmetic.

In this post, I will break down how the effect works.

# The Algorithm

The fire effect is elegantly simple. It operates on a 2D grid of “heat” values, where each cell contains an integer representing how hot that position is. The algorithm runs in three phases each frame:

**Seeding**: Random heat values are placed along the bottom row**Cooling**: Random cold spots are added to create gaps**Propagation**: Heat flows upward through neighbor averaging

The key insight is that heat naturally dissipates as it rises. By averaging each cell with its neighbors and using floor truncation, we get gradual cooling without any explicit decay factor.

## The Heat Buffer

The simulation uses a 1D array to represent a 2D grid of heat values:

```
// The heat buffer: a 1D array representing a 2D grid.
// Layout: buffer[y * width + x] gives the heat at position (x, y).
let buffer = [];
// Initialize with zeros (cold)
for (let i = 0; i < width * height + 1; i++) {
buffer[i] = 0;
}
```


Each cell contains an integer from 0 (cold) to `palSize`

(maximum heat). These values map directly to characters in the palette and colors in the color scheme.

## Phase 1: Seeding the Fire

The bottom row acts as the heat source. Each frame, we place random hot spots along this row:

```
// Seed bottom row with random hot spots.
// The number of spots is proportional to width * intensity.
for (let i = 0; i < Math.floor(width * intensity); i++) {
// Pick a random column
const x = Math.floor(Math.random() * width);
// Calculate index in the 1D buffer (bottom row)
const bottomRowIndex = x + width * (height - 1);
// Assign a random heat value from 0 to palSize
buffer[bottomRowIndex] = Math.floor(Math.random() * palSize);
}
```


The `intensity`

parameter controls how many hot spots are created. Higher values produce more hot spots, while lower values create sparse, flickering flames.

## Phase 2: Cooling

To prevent the fire from becoming a solid wall, we add random cold spots to the bottom row:

```
// Add cooling spots to create gaps in the fire.
// More cooling spots = shorter, more separated flames.
for (let i = 0; i < Math.floor(width * cooling); i++) {
// Pick a random column
const x = Math.floor(Math.random() * width);
// Calculate index in the 1D buffer (bottom row)
const bottomRowIndex = x + width * (height - 1);
// Set to zero (cold) to create a gap
buffer[bottomRowIndex] = 0;
}
```


The `cooling`

parameter determines how many gaps appear. More cooling creates shorter, more separated flames.

## Phase 3: Propagation

This is where the magic happens. Each cell’s new value is calculated as the average of itself and three neighbors below it:

```
// Process all rows except the bottom (which is the heat source).
// We iterate top-to-bottom, left-to-right.
for (let i = 0; i < width * (height - 1); i++) {
// Average this cell with its neighbors below.
// This creates upward heat flow with natural diffusion.
const average = (
buffer[i] + // Current cell
buffer[i + 1] + // Cell to the right
buffer[i + width] + // Cell directly below
buffer[i + width + 1] // Cell below-right
) / 4;
// Floor truncates fractional values, providing natural cooling.
// Heat is gradually lost as it rises through the grid.
buffer[i] = Math.floor(average);
}
```


The averaging creates smooth heat diffusion, while `Math.floor()`

ensures that heat gradually decreases as it rises. This is the secret to the effect: no explicit decay factor is needed because floor truncation naturally loses fractional heat.

# Character Palettes

The heat values are mapped to ASCII characters, creating the visual fire. Characters are ordered from “cold” (empty or dim) to “hot” (dense or bright):

```
const palettes = {
// Classic ASCII progression
classic: " ......::::::------======++++++******######%%%%%%@@@@@@",
// Extended character set with varied density
extended: " ,;+ltgti!lI?/\\|)(1}{][rcvzjftJUOQocxfXhqwWB8&%$#@",
// Unicode block characters for a pixelated look
blocks: " ░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▓▓████████████",
// Dot-based progression using Unicode bullets
dots: " ··················••••••••••••••••●●●●●●●●●●●●●●●●"
};
```


The palette length affects flame height. Longer palettes allow more gradual cooling and taller flames. All palettes in this implementation are normalized to approximately 50 characters for consistent behavior.

# Color Mapping

Each heat value is also mapped to a color from a gradient. The color schemes define an array of hex colors from cold to hot:

```
const colorSchemes = {
// Classic fire: dark red -> orange -> yellow -> white
fire: [
'#1a0000', '#3d0000', '#6b0000', '#a30000', '#d40000',
'#ff3300', '#ff6600', '#ff9900', '#ffcc00', '#ffff00', '#ffffff'
],
// Green fire variant
green: [
'#001a00', '#003d00', '#006b00', '#00a300', '#00d400',
'#33ff00', '#66ff00', '#99ff00', '#ccff00', '#ffff00', '#ffffff'
]
};
```


The mapping function normalizes the heat value to the color array:

```
function getColorForIndex(index) {
// Get the active color scheme array
const scheme = colorSchemes[params.colorScheme];
// Normalize heat index to [0, 1] range
const ratio = index / palSize;
// Map to color scheme index, clamped to valid range
const colorIndex = Math.min(
Math.floor(ratio * (scheme.length - 1)),
scheme.length - 1
);
// Return the hex color string
return scheme[colorIndex];
}
```


This creates a smooth color gradient that matches the character gradient, producing the characteristic fire colors.

# Rendering

The final step is rendering the buffer to the screen. Each cell is converted to a colored character:

```
// Build HTML string for the entire fire grid
let screenHtml = "";
for (let i = 0; i < width * (height - 1); i++) {
// Clamp heat value to valid palette range
const charIndex = buffer[i] > palSize ? palSize : buffer[i];
// Look up character and color for this heat value
const char = palette[charIndex];
const color = getColorForIndex(charIndex);
// Render the cell
if (char === ' ') {
// Spaces need no styling
screenHtml += ' ';
} else {
// Wrap non-space characters in colored span
screenHtml += `<span style="color:${color}">${char}</span>`;
}
// Add newline at end of each row
if ((i + 1) % width === 0) {
screenHtml += "\n";
}
}
// Update the DOM with the rendered fire
fireEl.innerHTML = screenHtml;
```


The HTML is built as a string and injected into a `<pre>`

element. While not the most efficient approach for large grids, it allows per-character coloring and works well for moderate sizes.

# Parameter Controls

The demo exposes several parameters through the GUI:

| Parameter | Effect |
|---|---|
| Width | Number of columns in the fire grid |
| Height | Number of rows in the fire grid |
| Palette | Character set used for rendering |
| Color Scheme | Color gradient from cold to hot |
| Reversed | Flip the palette (inverts visual density) |
| Font Size | Size of the monospace characters |
| Speed | Frame delay in milliseconds (higher = slower) |
| Intensity | How much fire to seed each frame |
| Cooling | How many cold spots to add (more = shorter fire) |

Try adjusting the intensity and cooling together. High intensity with low cooling produces tall, dense flames. Low intensity with high cooling creates sparse, flickering embers. Try different palettes and color schemes to see how the visual character of the fire changes while the underlying simulation remains the same.

# Conclusion

The fire effect originated in the demoscene, a subculture focused on creating impressive audiovisual demonstrations. The algorithm was popularized in the early 1990s on platforms like the Amiga and DOS PCs.

The beauty of the effect lies in its efficiency. The original versions ran on hardware with just a few MHz of processing power, using clever tricks to achieve real-time animation. The basic algorithm has remained unchanged because it simply works. This implementation adds modern touches like color schemes and Unicode character support, but the core algorithm is identical to what demos used decades ago.

This effect demonstrates how simple rules can create complex, organic-looking behavior. Three basic operations, seeding, cooling, and averaging, combine to produce convincing animated flames. The algorithm is a good example of emergence: the fire behavior is not explicitly programmed but arises naturally from the interaction of simple rules. This principle appears throughout computer graphics, from cellular automata to particle systems.