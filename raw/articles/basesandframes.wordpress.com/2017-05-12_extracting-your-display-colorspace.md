---
title: Extracting your display Colorspace
url: https://basesandframes.wordpress.com/2017/05/12/extracting-your-display-colorspace/
author: Robingreen
published: '2017-05-12'
source_blog: Bases and Frames
source_site: https://basesandframes.wordpress.com
category: graphics
fetched: '2026-04-13'
---

![edid-extract](../../assets/93350f6252ed8513.png)


If you’re using Windows and have access to Powershell, there is an interesting set of APIs called [Windows Management Instrumentation (WMI)](https://msdn.microsoft.com/en-us/library/aa394572(v=vs.85).aspx) that allow you to extract a lot of information about the computer. One of the pieces of information it can extract are the Display [EDID Records](https://en.wikipedia.org/wiki/Extended_Display_Identification_Data).

EDID (Enxtended Display Identification Data) started life as a digital serial interface embedded in your VGA cable – when you attached a display to the computer it would set up a two-wire SPI interface that allowed for bidirectional communication between the computer and the display. A set of [standards for the EDID data block](http://blog.chinaunix.net/attachment/attach/10/05/06/5110050651fcae644afa632e740b608f15ad5af3cc.pdf) were thrashed out and this allowed the computer to know the refresh rates your CRT was capable of, allowing it to avoid blowing up your display.

Part of this data block are the chromaticities of the Red, Green and Blue elements used in the display. Now, there are differing views on the reliability of this data but as a first-order test of whether a display might be interesting to test for wide gamut colors, it’s something.

You can get at the WMI interfaces through Powershell, which allows us to write a script to inspect all the displays attached to a machine. If you have admin rights, you can extend this script to visit every machine in your domain which would allow you to extract a spreadsheet of chromaticity information for every machine in your building from the comfort of your desk.

function get-monitorChromaticies { $monitors = Get-WmiObject -Namespace root\wmi -Class WmiMonitorColorCharacteristics $monitors | ForEach-Object { $colours = New-Object -TypeName PSObject -Property @{ Monitor = $_.InstanceName Active = $_.Active } $colours | Add-Member -MemberType NoteProperty -Name "Red" ` -Value @(([double]$_.Red.X / 1024.0), ` ([double]$_.Red.Y / 1024.0)) $colours | Add-Member -MemberType NoteProperty -Name "Green" ` -Value @(([double]$_.Green.X / 1024.0), ` ([double]$_.Green.Y / 1024.0)) $colours | Add-Member -MemberType NoteProperty -Name "Blue" ` -Value @(([double]$_.Blue.X / 1024.0), ` ([double]$_.Blue.Y / 1024.0)) $colours | Add-Member -MemberType NoteProperty -Name "White" ` -Value @(([double]$_.DefaultWhite.X / 1024.0), ` ([double]$_.DefaultWhite.Y / 1024.0)) Write-Output $colours } }