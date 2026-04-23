---
tags: [source, java, webstart, applet, maven, deployment, gemserk]
date: 2026-04-19
sources: 1
---

# Signing JARs for Applet and Webstart（Gemserk）

[[gemserk]] 于 2010 年 2 月的博客，记录了这家乌拉圭独立工作室用 Java + LWJGL 做桌面游戏、再以 Applet / Java Web Start 方式一键网页开玩时，如何解决 JVM 沙盒对 JAR 签名的硬性要求。

## 摘要

Java Web Start 与 Applet 默认把应用关在受限沙盒里，LWJGL、JInput 和自定义 ClassLoader 都需要完整权限，因此所有 jar 必须被签名。一次性用临时证书签会让用户每次升级都重新点一次"信任"；合理做法是保留一把长期 keystore，签出来的版本能被用户"永久信任"一次到底。Gemserk 的落地方案是用 `maven-webstart-plugin`，把 keystore 路径、alias、密码全部写成 `${gemserk.*}` property，默认值指向 `/tmp/...` 并打开 delete + gen（开发模式每次重建临时 keystore），在 `settings.xml` 里另配一个 `useDeploymentCertificate` profile 覆盖这些 property，指向 `/opt/gemserk-keystore`、关闭 delete/gen。日常 `mvn package` 走开发证书，发布版本 `mvn package -PuseDeploymentCertificate` 走正式证书。

## 关键要点

- Applet / Web Start 默认受限沙盒，用 LWJGL / JInput / 自定义 ClassLoader 必须签名后 JVM 才放权
- 临时证书 vs 长期证书的取舍是"每次发版用户都要点一次信任" vs "点一次永久接受"
- 实现靠 Maven property + profile 分层：`pom.xml` 定义 property 默认值（开发用临时 keystore，跑完即删），`settings.xml` 的 profile 覆盖为正式 keystore
- 命令行激活：`mvn package -PuseDeploymentCertificate`
- 密钥 / 密码不进仓库，正式 keystore 放在构建机固定路径（文中是 `/opt/gemserk-keystore`）

## 链接到的概念

- [[java-webstart-jar-signing]]

## 原文

- 链接：https://blog.gemserk.com/2010/02/07/signing-jars-for-applet-and-webstart/
- 本地：`raw/articles/blog.gemserk.com/2010-02-07_signing-jars-for-applet-and-webstart.md`
