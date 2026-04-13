---
title: Tricksy closures
url: https://etodd.io/2010/08/15/tricksy-closures/
published: '2010-08-15'
source_blog: Evan Todd
source_site: https://etodd.io/
category: game programming
fetched: '2026-04-13'
---

# Tricksy closures

Do not be fooled by the elegant simplicity of the mighty closure! Behind its shiny dynamic veneer lies a powerful machine capable of destroying your immortal soul. Behold:

```
function GetOutputFunctions()
{
var outputFunctions = new Array();
for(var i = 0; i < 4; i++)
{
var x = i * 2;
outputFunctions.push(function() { alert(x); });
}
return outputFunctions;
}
var functions = GetOutputFunctions();
for (var i = 0; i < functions.length; i++)
functions[i]();
```


This will not output the first three multiples of two, as presumably expected. Instead it will output "6" three times, because the variable "x" is only allocated once.

This has been a public service announcement. Beware!