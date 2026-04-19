---
title: Stupid sample generator
url: https://c0de517e.blogspot.com/2010/12/stupid-sample-generator.html
published: '2010-12-15'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

I had to write in a rush some code to generate low-discrepancy samples in a shape (i.e. hemisphere). For those kind of quick hacks I find

[processing](http://processing.org/)to be great, mostly because of its visual nature.The code is really stupid and it requires some manual interaction. With the left mouse button you dump the sample info, with the middle you shrink the sample minimum distance spheres, with the right you add a random shake to the whole thing (yes, it's laughable...).

Anyways. Here it is.






// Generates a packing of points inside a 2d shape // press right/middle mouse buttons a few times until convergence... class pnt { float x; float y; }; pnt points[] = new pnt[16]; float mindist = 60; void setup() { size(512, 512, P3D); fill(204); for(int i=0; i< points.length; i++) { points[i]=new pnt(); points[i].x = random(200)-100; points[i].y = random(200)-100; } } void mousePressed() { if(mouseButton == LEFT) { for(int i=0; i< points.length; i++) { float len = sqrt(points[i].x*points[i].x + points[i].y*points[i].y); println(points[i].x/100.0 + ", " + points[i].y/100.0 + ", " + len/100.0 + ","); } } else if(mouseButton == CENTER) { mindist -= 5; // manual control... } else // RIGHT mouse button { // A LITTLE BIT OF NOISE for(int i=0; i< points.length; i++) { points[i].x += random(mindist/10)-(mindist/20); points[i].y += random(mindist/10)-(mindist/20); } } } void draw() { lights(); background(0); // Change height of the camera with mouseY camera(30.0, mouseY, 400.0, // eyeX, eyeY, eyeZ 0.0, 0.0, 0.0, // centerX, centerY, centerZ 0.0, 1.0, 0.0); // upX, upY, upZ noStroke(); float totaldist = 0; // DISTANCE CONSTRAINT for(int i=0; i< points.length; i++) { for(int k=0; k<50; k++) { int j = (int)random(points.length); if(i!=j) { pnt tmp = new pnt(); tmp.x = points[j].x - points[i].x; tmp.y = points[j].y - points[i].y; float len = sqrt(tmp.x*tmp.x + tmp.y*tmp.y); if(len< mindist) { tmp.x = (tmp.x/len)*mindist; tmp.y = (tmp.y/len)*mindist; points[i].x = points[j].x - tmp.x; points[i].y = points[j].y - tmp.y; totaldist += len; } } } } // DISTANCE FROM ZERO CONSTRAINT for(int i=0; i< points.length; i++) { float len = sqrt(points[i].x*points[i].x + points[i].y*points[i].y); if(len< mindist) { points[i].x /= len/(mindist); points[i].y /= len/(mindist); } } // SHAPE CONSTRAINT for(int i=0; i< points.length; i++) { float len = sqrt(points[i].x*points[i].x + points[i].y*points[i].y); if(len>100) { points[i].x/=len/100.0; points[i].y/=len/100.0; } } // display distance violation totaldist = sqrt(totaldist); fill(15,15,15,255); box(totaldist); for(int i=0; i< points.length; i++) { pushMatrix(); translate(points[i].x,points[i].y,0); if(mindist>0) { fill(255,255,255,64); sphere(mindist); } fill(255,0,0,255); sphere(5); popMatrix(); } }



## No comments:

Post a Comment