---
tags: [java, webstart, applet, distribution, deployment, maven, signing]
date: 2026-04-19
sources: 1
---

# Java Applet / Web Start 的 JAR 签名

在 Java Web Start 与浏览器 Applet 时代，JVM 默认把应用关在一个受限沙盒里：不能访问本机 OpenGL、原生输入库或自定义 ClassLoader。Gemserk 这种用 [LWJGL](http://lwjgl.org/) + JInput 做桌面游戏、同时希望能在网页点一下就玩的独立团队，必须给每个 jar 打上数字签名，用户才会被 JVM 提示"是否信任此发布者"，点通过之后才能获得完整权限。

签名策略有两种，差别在于"用户要被弹几次窗"：

- **每次打包都重新生成证书**——部署脚本每次跑都 `keytool -genkey` 一个新 keystore，再用它签 jar。结果是每次发新版本用户都会看到全新指纹，即便之前点了"永久信任"也要重新点一次。开发迭代阶段可以接受，但不能拿出去发给玩家。
- **维护一个长期证书**——一次性生成 keystore，保存在构建机固定路径，之后所有发布版本都用同一把证书签。只要用户勾了"永久信任"，后续版本静默通过。这是面向玩家的正式构建唯一能用的方式。

Gemserk 用 Maven + `maven-webstart-plugin` 把两种策略写进同一个 `pom.xml`，靠 Maven **profile** 在两者之间切换。关键技巧是把 keystore 路径、alias、密码全部写成 `${gemserk.keystore}` 形式的 property，默认值指向 `/tmp/keystore-gemserk` 并把 `delete=true`、`gen=true` 开起来（开发模式：每次打包都把临时 keystore 删掉重建）；另外在 `~/.m2/settings.xml` 里定义一个 `useDeploymentCertificate` profile，把同名 property 覆盖成 `/opt/gemserk-keystore`、关闭 delete/gen。发布时只要 `mvn package -PuseDeploymentCertificate` 就用正式证书签，本地开发保持零配置。

这种用 profile 覆盖同名 property 的模式是 Maven 构建分层配置的标准解法，今天放到 Gradle 的 flavor / productFlavors、或者 Unreal 的 `Target.cs` 配置里依然成立：**敏感秘钥不进仓库，靠构建机本地文件 + 只在命令行激活的 profile 暴露**。Java Web Start 本身在 JDK 11 之后已被移除，现代 Java 游戏分发主要靠 jpackage / Steam / 纯 launcher，但"给产物签名以跨越 OS 的信任边界"这个问题没消失：macOS 的 codesign + notarization、Windows 的 Authenticode 走的是同一套思路。

## 相关

- [[gemserk]]

## Sources

- [[sources/gemserk-signing-jars-applet-webstart]]
