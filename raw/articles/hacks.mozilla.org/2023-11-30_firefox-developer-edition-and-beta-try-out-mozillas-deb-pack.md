---
title: 'Firefox Developer Edition and Beta: Try out Mozilla’s .deb package! – Mozilla
  Hacks - the Web developer blog'
url: https://hacks.mozilla.org/2023/11/firefox-developer-edition-and-beta-try-out-mozillas-deb-package/
author: Johan Lorenzo
published: '2023-11-30'
source_blog: Mozilla Hacks – the Web developer blog
source_site: https://hacks.mozilla.org/
category: graphics
fetched: '2026-04-13'
---

A month ago, [we introduced our Nightly package](https://blog.nightly.mozilla.org/2023/10/30/introducing-mozillas-firefox-nightly-deb-packages-for-debian-based-linux-distributions/) for Debian-based Linux distributions. Today, we are proud to announce we made our `.deb`

package available for Developer Edition and Beta!

We’ve set up a new APT repository for you to install Firefox as a `.deb`

package. [These packages are compatible with the same Debian and Ubuntu versions as our traditional binaries.](https://www.mozilla.org/firefox/system-requirements)

Your feedback is invaluable, so don’t hesitate to [report any issues](https://bugzilla.mozilla.org/enter_bug.cgi?format=__default__&blocked=1799516&product=Release%20Engineering&component=General) you encounter to help us improve the overall experience.

Adopting Mozilla’s Firefox `.deb`

package offers multiple benefits:

- you will get better performance thanks to our advanced compiler-based optimizations,
- you will receive the latest updates as fast as possible because the
`.deb`

is integrated into Firefox’s release process, - you will get hardened binaries with all security flags enabled during compilation,
- you can continue browsing after upgrading the package, meaning you can restart Firefox at your convenience to get the latest version.

`.deb`

package, simply follow these steps:```
<code># Create a directory to store APT repository keys if it doesn't exist:
sudo install -d -m 0755 /etc/apt/keyrings
# Import the Mozilla APT repository signing key:
wget -q <a class="c-link" href="https://packages.mozilla.org/apt/repo-signing-key.gpg" target="_blank" rel="noopener noreferrer" data-stringify-link="https://packages.mozilla.org/apt/repo-signing-key.gpg" data-sk="tooltip_parent">https://packages.mozilla.org/apt/repo-signing-key.gpg</a> -O- | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
# The fingerprint should be 35BAA0B33E9EB396F59CA838C0BA5CE6DC6315A3
gpg -n -q --import --import-options import-show /etc/apt/keyrings/packages.mozilla.org.asc | awk '/pub/{getline; gsub(/^ +| +$/,""); print "\n"$0"\n"}'
# Next, add the Mozilla APT repository to your sources list:
echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] <a class="c-link" href="https://packages.mozilla.org/apt" target="_blank" rel="noopener noreferrer" data-stringify-link="https://packages.mozilla.org/apt" data-sk="tooltip_parent">https://packages.mozilla.org/apt</a> mozilla main" | sudo tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
# Update your package list and install the Firefox .deb package:
sudo apt-get update && sudo apt-get install firefox-beta # Replace "beta" by "devedition" for Developer Edition
```


`fr`

in the example below with the desired language code:`sudo apt-get install firefox-beta-l10n-fr`


*after*adding the Mozilla APT repository and running

`sudo apt-get update`

:apt-cache search firefox-beta-l10n