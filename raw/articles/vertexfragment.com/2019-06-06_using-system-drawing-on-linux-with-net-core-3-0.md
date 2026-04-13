---
title: Using System.Drawing on Linux with .NET Core 3.0
url: https://www.vertexfragment.com/ramblings/system-drawing-net-core-linux/
author: Steven Sell
published: '2019-06-06'
source_blog: Vertex Fragment
source_site: https://www.vertexfragment.com/
category: graphics
fetched: '2026-04-13'
---

This guide covers how to get a sample .NET Core 3.0 application building and running on Linux, specifically Ubuntu 16.04.

These steps should be transferrable to other Ubuntu versions and/or Linux distributions but it has not been tested. A list of supported distributions and versions can be [found here](https://github.com/dotnet/core/blob/master/release-notes/3.0/3.0-supported-os.md).

First install any required external dependencies, which in this case means [ libgdiplus](https://www.mono-project.com/docs/gui/libgdiplus/). This is required as the Linux implementation of

`System.Drawing.Common`

[sits on top of it](https://github.com/dotnet/corefx/issues/20325).

```
sudo apt-get -f install libgdiplus
```


Next, [retrieve the latest .NET Core 3.0 release for your system](https://dotnet.microsoft.com/download/dotnet-core/3.0) and place it under `~/dotnet-sdk`

. Once there, perform the following steps:

```
cd ~/dotnet-sdk
sudo mkdir -p /usr/share/dotnet
sudo tar -zxf dotnet-sdk-3.0.100-preview5-011568-linux-x64.tar.gz -C /usr/share/dotnet
sudo ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet
```


Confirm the above worked by checking the installed .NET version,

```
dotnet --version
```


which should output something similar to:

```
3.0.100-preview5-011568
```


Now to create a simple test application that will use `System.Drawing.Common`

to create a bitmap image and save it to disk.

```
dotnet new console -o test-app
cd test-app
dotnet add package System.Drawing.Common
```


Then replace the contents of `Program.cs`

with:

|
|

Finally, build and run it:

```
dotnet build
cd bin/Debug/netcoreapp3.0/
./test-app
```


Assuming it was successful there should now be a `test.bmp`

next to your test application.