---
title: How to compress and decompress binary streams in Unity - Seba's Lab
url: https://www.sebaslab.com/how-to-compress-and-decompress-binary-stream-in-unity/
author: Sebastiano Mandalà
published: '2013-02-06'
source_blog: Seba's Lab
source_site: https://www.sebaslab.com/
category: game programming
fetched: '2026-04-13'
---

recently I needed to compress a binary stream that was getting to big to be serialized over internet. I could not find any way to compress files easily, so eventually I used a 3rd party library that works very well in Unity3D (web player included): [SharpZipLib](http://www.icsharpcode.net/opensource/sharpziplib/)

I suppose the following code could be handy for someone:

using ICSharpCode.SharpZipLib.BZip2; using System.Runtime.Serialization.Formatters.Binary; using System.IO; static void Compress (string nameOfTheFileToSave, ISerializable objectToSerialize) { using (FileStream fs = new FileStream(nameOfTheFileToSave, FileMode.Create)) { using (MemoryStream objectSerialization = new MemoryStream()) { BinaryFormatter bformatter = new BinaryFormatter(); bformatter.Serialize(objectSerialization, objectToSerialize); using (BinaryWriter binaryWriter = new BinaryWriter(fs)) { binaryWriter.Write(objectSerialization.GetBuffer().Length); //write the length first using (BZip2OutputStream osBZip2 = new BZip2OutputStream(fs)) { osBZip2.Write(objectSerialization.GetBuffer(), 0, objectSerialization.GetBuffer().Length); //write the compressed file } } } } } static void Decompress(string nameOfTheFileToLoad) { using (FileStream fs = new FileStream(nameOfTheFileToLoad, FileMode.Open)) { using (BinaryReader binaryReader = new BinaryReader(fs)) { int length = binaryReader.ReadInt32(); //read the length first byte[] bytesUncompressed = new byte[length]; //you can convert this back to the object using a MemoryStream ;) using (BZip2InputStream osBZip2 = new BZip2InputStream(fs)) { osBZip2.Read(bytesUncompressed, 0, length); //read the decompressed file } } } }




Nice! this helped us a lot.