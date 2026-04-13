---
title: JNLP Downloader Tool
url: https://blog.gemserk.com/2011/03/09/jnlp-downloader-tool/
published: '2011-03-09'
source_blog: Gemserk
source_site: https://blog.gemserk.com/
category: game programming
fetched: '2026-04-13'
---

Some time ago, Rubén wrote a Java based tool to download all JNLP resources and prepare executable files to run it based on the JNLP file values.

It downloads all the resources specified by the [JNLP file](http://download.oracle.com/javase/1.5.0/docs/guide/javaws/developersguide/syntax.html) and save them into `/libs`

and `/natives`

for jar `resources`

and `nativelib`

resources respectively, in the second case it creates sub folders for each platform (Windows, Mac and Linux). After that, it creates one executable script file to run the application for each platform, configuring `classpath`

and `java.library.path`

inside it.

For example, running the tool:

java -jar jnlpdownloader.jar example http://www.example.com/application.jnlp

where the JNLP contents are:

<?xml version="1.0" encoding="utf-8"?> <jnlp spec="1.0+" codebase="http://www.example.com/" href="application.jnlp"> <information> <title>Some Title</title> <vendor>Some Vendor</vendor> <description>Some Description</description> </information> <resources> <jar href="slf4j-api-1.5.8.jar" /> <jar href="google-collections-1.0.jar" /> <jar href="lwjgl-2.4.2.jar" /> </resources> <resources os="Windows"> <nativelib href="lwjgl-2.4.2-natives-win.jar" /> </resources> <resources os="Linux"> <nativelib href="lwjgl-2.4.2-natives-linux.jar" /> </resources> <resources os="Mac"> <nativelib href="lwjgl-2.4.2-natives-mac.jar" /> </resources> <application-desc main-class="Main" /> </jnlp>

will create the next file structure:

./example ./example/natives ./example/natives/Linux ./example/natives/Linux/liblwjgl.so ./example/natives/Windows ./example/natives/Windows/lwjgl.dll ./example/natives/Mac ./example/natives/Mac/liblwjgl.jnilib ./example/libs ./example/libs/google-collections-1.0.jar ./example/libs/slf4j-api-1.5.8.jar ./example/libs/lwjgl-2.4.2.jar ./example/run-windows.bat ./example/run-macosx.sh ./example/run-linux.sh

More info at the [project’s home page](https://code.google.com/p/jnlpdownloader/).

We used this tool mainly to take a snapshot of a deployed Java Web Start application to make it run offline, for demo purposes.