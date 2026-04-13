---
title: UE4 4.15 to 4.16 ReadOnlyTargetRules Backwards Compatibility
url: https://allarsblog.com/2017/06/29/ue4-4-15-to-4-16-readonlytargetrules-backwards-compatibility/
author: Michael Allar
published: '2017-06-29'
source_blog: Allar's Blog
source_site: https://allarsblog.com/
category: graphics
fetched: '2026-04-13'
---

If you're a marketplace plugin maintainer and would like to maintain backward compatibility between 4.16 and 4.15, you've most likely run into the issue of the change of module target files moving to a ReadOnlyTargetRules constructor.

Epic has provided an undocumented preprocessor to help govern this change.

```
#if WITH_FORWARDED_MODULE_RULES_CTOR
public Linter(ReadOnlyTargetRules Target) : base(Target)
#else
public Linter(TargetInfo Target)
#endif
```


`WITH_FORWARDED_MODULE_RULES_CTOR`

will be defined if on 4.16 or later.