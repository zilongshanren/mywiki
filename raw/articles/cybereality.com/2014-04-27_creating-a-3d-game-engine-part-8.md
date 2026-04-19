---
title: Creating a 3D Game Engine (Part 8)
url: https://cybereality.com/creating-a-3d-game-engine-part-8/
author: Cybereality
published: '2014-04-27'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

![engine zero triangle](../../assets/5fb6a3e1c742ee6c.jpg)

So I buckled down and spent the better half of the day actually getting something to show on the screen. Yes, it’s still just a triangle, but it feels pretty satisfying after struggling to get it to work all morning. While there are tons of triangle tutorials online, and it would seem like a 20 minute hack, I ended up having some difficulty for a few reasons.

One, I decided last night to upgrade to Visual Studio 2013 so I could take advantage of C++11 and the 64-bit compiler. Right off the bat, this resulted in a bunch of warnings. I eventually found the instructions to clean this up [here](http://msdn.microsoft.com/en-us/library/windows/desktop/ee663275%28v=vs.85%29.aspx), and it ended up not being a big deal.

The second issue was with compiling the HLSL shader (currently, it just passes along the position and color attributes without any fancy math). It turns out the D3DX11CompileFromFile is deprecated as is the whole D3DX library. I guess I could have still used them anyway, but what fun is that? So I decided to remove the D3DX dependency and either move to newer functions, or reimplement certain classes completely.

Luckily there is a function called D3DCompileFromFile, which does the heavy-lifting of compiling a HLSL shader file. However, for some reason shader files from tutorials I was following did not seem to work correctly with the new additions. After tweaking it for a bit, and a lot of trial-and-error, I was able to get something built. I know it seems rather silly to have spent hours on this, but hopefully once I get this foundation built things will become easier. Here is the (dirt simple) shader file if anyone is having similar problems.

struct VS_OUTPUT { float4 pos : SV_POSITION; float4 color : COLOR0; }; VS_OUTPUT VS(float4 pos : POSITION, float4 color : COLOR) { VS_OUTPUT output; output.pos = pos; output.color = color; return output; } float4 PS(VS_OUTPUT input) : SV_Target { return input.color; }

Next up, I want to get in texture mapping, finish the Vector and Matrix classes, and make a spinning cube. Stay tuned.