---
title: Stupid sample generator - 3d version
url: https://c0de517e.blogspot.com/2010/12/stupid-sample-generator-3d-version.html
published: '2010-12-15'
source_blog: C0DE517E
source_site: https://c0de517e.blogspot.com/
category: graphics
fetched: '2026-04-19'
---

// press right/middle mouse buttons a few times until convergence...class pnt{float x; float y; float z;float len(){return sqrt(x*x + y*y + z*z);}};pnt points[] = new pnt[32];float scalefact = 100;float mindist = scalefact * 0.5;void setup() {size(512, 512, P3D);fill(204);for(int i=0; i< points.length; i++){points[i]=new pnt();points[i].x = random(scalefact*2)-scalefact;points[i].y = random(scalefact*2)-scalefact;points[i].z = random(scalefact*2)-scalefact;}}float getImportance(pnt a){return 1.3 - (((a.z/scalefact) + (a.z/a.len()))/2);}void mousePressed(){if(mouseButton == LEFT) // dump points, report{final float UNIT_HEMISPHERE_VOL = (4.0/3.0) * 3.141592 * 0.5;float totalVol = 0;for(int i=0; i< points.length; i++){float normRadius = mindist * getImportance(points[i]) / scalefact;float vol = (4.0/3.0) * 3.141592 * normRadius * normRadius * normRadius;totalVol+=vol;}println("vol ratio" + UNIT_HEMISPHERE_VOL/totalVol);for(int i=0; i< points.length; i++){//println(points[i].x/scalefact+", "+points[i].y/scalefact+", "+points[i].z/scalefact+", "+points[i].len()/scalefact+",");float normRadius = mindist * getImportance(points[i]) / scalefact;float vol = (4.0/3.0) * 3.141592 * normRadius * normRadius * normRadius;float weight = vol / totalVol;println(points[i].x/scalefact+", "+points[i].y/scalefact+", "+points[i].z/scalefact+", "+weight+",");}println("vol ratio: " + UNIT_HEMISPHERE_VOL/totalVol);}else if(mouseButton == CENTER){mindist -= 5; // manual control...}else // RIGHT mouse button{// A LITTLE BIT OF NOISEfor(int i=0; i< points.length; i++){points[i].x += random(mindist/(scalefact/10))-(mindist/(scalefact/5));points[i].y += random(mindist/(scalefact/10))-(mindist/(scalefact/5));points[i].z += random(mindist/(scalefact/10))-(mindist/(scalefact/5));}}}void draw() {lights();background(0);// Change height of the camera with mouseYcamera(sin(mouseX/512.0 * 6.0)*300, cos(mouseX/512.0 * 6.0)*300, mouseY, // eyeX, eyeY, eyeZ0.0, 0.0, 0.0, // centerX, centerY, centerZ0.0, 0.0, -1.0); // upX, upY, upZnoStroke();// SHAPE CONSTRAINTfor(int i=0; i< points.length; i++){float len = points[i].len();float radius = getImportance(points[i])*mindist;len+=radius;if(len > scalefact) // inside the sphere{points[i].x /= len / scalefact;points[i].y /= len / scalefact;points[i].z /= len / scalefact;}// hemisphereif(points[i].z-radius< 0) points[i].z=radius;}float totaldist = 0;// DISTANCE CONSTRAINTfor(int i=0; i< points.length; i++){float radius = getImportance(points[i])*mindist;for(int k=0; k< 50; k++){int j = (int)random(points.length);if(i!=j){pnt tmp = new pnt();tmp.x = points[j].x - points[i].x;tmp.y = points[j].y - points[i].y;tmp.z = points[j].z - points[i].z;float len = tmp.len();if( len < radius ){tmp.x = (tmp.x/len) * radius;tmp.y = (tmp.y/len) * radius;tmp.z = (tmp.z/len) * radius;points[i].x = points[j].x - tmp.x;points[i].y = points[j].y - tmp.y;points[i].z = points[j].z - tmp.z;totaldist += len;}}}}// display distance violationfill(15,15,15,255);box(scalefact,scalefact,1);totaldist = sqrt(totaldist);fill(128,0,128,128);box(totaldist,totaldist,5);for(int i=0; i< points.length; i++){pushMatrix();translate(points[i].x,points[i].y,points[i].z);if(mindist>0){fill(255,255,255,64);sphere(mindist * getImportance(points[i]) );}fill(255,0,0,255);sphere(5 * getImportance(points[i]) );popMatrix();stroke(255,0,0,255);line(0,0,0,points[i].x,points[i].y,points[i].z);noStroke();}}

## Search this blog

## 15 December, 2010


## No comments:

Post a Comment