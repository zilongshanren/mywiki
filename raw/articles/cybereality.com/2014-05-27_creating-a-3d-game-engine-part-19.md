---
title: Creating a 3D Game Engine (Part 19)
url: https://cybereality.com/creating-a-3d-game-engine-part-19/
author: Cybereality
published: '2014-05-27'
source_blog: cybereality » the matrix was a documentary
source_site: https://cybereality.com/
category: graphics
fetched: '2026-04-19'
---

While getting models loaded was pretty exciting, I ended up dealing with major load times on the demo. Granted, my XML parsing code is probably slow as all hell, but I don’t think COLLADA is really designed for real-time engine use. With simple plane and cube shapes the loading wasn’t that bad, but with my soda can model (around 600 triangles) the loading was nearing 10 seconds (totally unacceptable). I can only imagine what would happen with a really complex model. Something had to be done.

So I decided to switch to a binary format with basically only exactly what I needed to pump into DirectX (the vertices, normals, uvs, and indices). I created a separate console application that would covert *.DAE files into my new binary format. Then I added engine support for loading the binary file instead of COLLADA. The gain was HUGE. Now when running the exe, there was no noticeable lag time at all. I guess I kind of knew I needed to do this at some point, but the wait times were too much to bear any longer. Glad to find a good solution.

Here are some snippets of code to show how to save variables as binary data:

float someValue= 0.12345f; ofstream outputFile; outputFile.open(L"output.bin", ios::out | ios::binary); outputFile.write((char*)&someValue, sizeof(float)); outputFile.close();

And then you can read this value later by doing:

float someValue; ifstream inputFile; inputFile.open(L"output.bin", ios::in | ios::binary); inputFile.read((char*)&someValue, sizeof(float)); inputFile.close();

Actually not that difficult at all. The benefits are decreased loading time and also smaller file sizes. The cons are that you now have another step in the asset pipeline, and that the files are no longer human-readable. A fair trade I would say.