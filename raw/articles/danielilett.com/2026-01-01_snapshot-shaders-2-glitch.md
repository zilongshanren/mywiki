---
title: Snapshot Shaders 2 - Glitch
url: https://danielilett.com/snapshot-shaders-2/glitch/
author: Daniel Ilett
published: '2026-01-01'
source_blog: Daniel Ilett
source_site: https://danielilett.com/
category: graphics
fetched: '2026-04-13'
---

Distorts the UVs of the image in several ways, such as small offsets along scanlines, large offsets produced by a scrolling shutter effect, and blocky chunks of the image sampling from the wrong place.

# Parameters

## Offset Glitches

**Offset Strength**- How strongly to offset parts of the image based on the**Offset Texture**, as a proportion of the total screen width.**Offset Texture**- A texture encoding how far to offset each line of the screen. This should be a vertical texture, where each pixel represents the distance each line of the image gets shifted. Black pixels move the image fully left, white pixels fully right, and grey pixels keep the image where it is.**Use Point Filter**- If ticked, the**Offset Texture**will be sampled with nearest-neighbor sampling. Otherwise, it will use bilinear filtering.**Offset Speed**- How quickly the shader scrolls down the**Offset Texture**.**Offset Tiling**- How many times the **Offset Texture is tiled across the screen vertically.

## Slice Band Glitches

The slice band is a thick scrolling band of configurable width and speed which travels over the screen periodically and offsets the entire band of pixels. It randomly comes on and off.

**Use Slice Band Glitches**- Choose whether the slice band is visible.**Slice Band Strength**- How strongly to offset pixels, as a proportion of screen width. Values below 0 will move slices to the left, and values above 0 move them to the right.**Slice Band Speed**- How quickly the band travels across the screen.**Slice Band Jitter**- How much the band wobbles up and down randomly as it moves.**Slice Band Width**- How thick the band is, as a proportion of screen height.**Slice Band Min Duration**- The minimum amount of time that a given band is visible for.**Slice Band Max Duration**- The maximum amount of time that a given band is visible for.**Slice Band Frequency**- The number of times per second that a slice band begins (this happens at regular intervals).

## Block Artifact Glitches

Block artifacts are areas of the screen, divided into blocks based on UVs, which randomly sample from an incorrect part of the texture.

**Use Block Artifacts**- Choose whether block artifacts are used.**Block Artifact Tiling**- How many blocks the screen is divided into along each axis.**Block Artifact Chance**- Roughly what proportion of the blocks will be randomly offset at a given time.**Block Artifact Strength Min**- How strongly the block is offset along the x-axis. Values below 1 move the blocks to the right, and values above 1 move them to the left (this directionality may be counter-intuitive). Offsets are random for each block - this is the minimum possible offset.**Block Artifact Strength Max**- This is the maximum possible offset.**Block Artifact Speed**- How quickly blocks cycle through random values. Quicker speeds mean each block is offset for less time.