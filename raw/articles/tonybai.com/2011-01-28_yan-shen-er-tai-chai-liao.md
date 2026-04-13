---
title: 眼神儿太差了
url: https://tonybai.com/2011/01/28/terrible-eyes/
published: '2011-01-28'
source_blog: Tony Bai
source_site: https://tonybai.com
category: game programming
fetched: '2026-04-13'
---

# 眼神儿太差了

昨天晚饭后，打开本子继续工作，却发现无法连上[无线路由器](http://tonybai.com/2008/03/08/configure-wireless-router/)。最初以为路由器忘记打开了，可拿起路由器看了下，不是那么回事儿，路由器工作一切正常。我这才看到发现本子的无线网卡的指示灯不亮了，以前在这台x60本子上还从未出现此类情况，于是开始查找故障原因。

故障查找过程是痛苦的，一次次燃起希望，又一次次被冷水破灭：

* 最初怀疑是我误点击了Fn + F5而把无线网卡关了，于是我又无数次的点击Fn + F5，居然一点反应都没有；

* 我的[T400](http://tonybai.com/2010/01/10/thinkpad-t400-is-available/)上有无线网卡的硬件开关，我将x60翻转了几周，也没找到无线开关位置；

* [Ubuntu](http://tonybai.com/2010/08/25/move-to-ubuntu-thoroughly/)上Network Manager面板中，无线网络显示已停用，且菜单项为灰色，无法选择，无法启用；

* N次重启机器，无果；

* 切换到Win7下，Win7设备管理器显示无线网卡设备正常，驱动正常；反复停用、启用无线，都无法使指示灯亮起；

* 重启机器，F1进入BIOS，查看网络设备也是Enabled，遂将BIOS恢复成默认出厂设置；

* 再尝试进入Win7，蓝屏，提示修复，修复若干次依旧无法进入Win7，无线指示灯依旧处于熄灭状态;

* 继续回到Ubuntu下折腾，卸载Network Manager，更换网络管理软件，用T400下载[WCID](http://wicd.sourceforge.net)，并用U盘COPY到x60里安装(家里没有备网线)，WCID也没比自带的Network Manager好哪里去，依旧无法找到无线网卡；

* 恢复Network Manager；

* 用系统->系统管理->系统日志查看器查看系统日志，看到如下错误日志：

dhclient: receive_packet failed on wlan0: Network is down

wpa_supplicant[824]: Failed to initiate AP scan.

NetworkManager: WiFi now disabled by radio killswitch

NetworkManager: (wlan0): device state change: 8 -> 2 (reason 0)

NetworkManager: (wlan0): deactivating device (reason: 0).

NetworkManager: (wlan0): canceled DHCP transaction, dhcp client pid 2816

* 根据网上资料，按如下操作：

– sudo -i

– echo 1 > /sys/class/rfkill/rfkill0/state

– 重启机器

问题依旧。

* 安装[rfkill](http://wireless.kernel.org/en/users/Documentation/rfkill)，rfkill list看到：

0: phy0: Wireless LAN

Soft blocked: yes

Hard blocked: yes

执行rfkill unblock all，得到：

0: phy0: Wireless LAN

Soft blocked: no

Hard blocked: yes

依旧无法打开无线网卡

* 被折腾近四个小时后上床睡觉！

* 上班后联系设备维修部门；

* 带着本子到维修部门查找故障原因，说明情况后，维修人员操作我的本子；

* 重启机器，进入BIOS，将Config -> Serial ATA -> SATA Controller的MODE OPTION改为COMPATIBILITY，保存退出；

* 选择Win7，居然不再蓝屏，正常进入Win7；

* 在Win7加载进度条还在闪烁的时候，这位维修人员托起本子看了看，指着本子某个部位对我说：这是不是无线开关？

* 他拨动无线开关，无线信号指示灯亮起；

* 我无语！

不得不承认：我的眼神儿太差了！

© 2011, [bigwhite](https://tonybai.com). 版权所有.

Related posts:

嘿嘿，昨儿你继续找那个开关嘛 ^_^

我的X61是在掌托方向边缘下面有这个开关。

重启机器，进入BIOS，将Config -> Serial ATA -> SATA Controller的MODE OPTION改为COMPATIBILITY，保存退出；为什么会影响win7启动