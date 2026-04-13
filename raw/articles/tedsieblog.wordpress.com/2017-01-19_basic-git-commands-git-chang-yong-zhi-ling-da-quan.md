---
title: Basic Git Commands – Git 常用指令大全
url: https://tedsieblog.wordpress.com/2017/01/19/basic-git-commands/
author: Ted Sie
published: '2017-01-19'
source_blog: 阿祥的開發日常
source_site: https://tedsieblog.wordpress.com
category: graphics
fetched: '2026-04-13'
---

Git 是現今在軟體業中被廣泛使用的一套分散式版本控制軟體，與集中式最大的不同在於，分散式不需要伺服器就可以運行版本控制，使得軟體開發的交流變得更為簡單快速。

本篇記錄了在使用 Git 時，所常用的的各種相關指令。



### 用戶配置

//顯示用戶名 git config user.name //顯示用戶信箱位址 git config user.email //設定本地用戶名 git config user.name "your_name" //設定本地用戶信箱位址 git config user.email "your_name@example.com" //設定全域用戶名 git config --global user.name "your_name" //設定全域用戶信箱位址 git config --global user.email "your_name@example.com"


### 初始化與複製專案

//初始化儲存庫 git init //在當前目錄下複製現有儲存庫 git clone <url>


### 新增與移除

//新增檔案至暫存區域 git add <file> //新增所有副檔名為 extension 的檔案至暫存區域 git add *.extension //新增所有更改過的檔案至暫存區域 git add . //將檔案從暫存區域中移除 git reset <file> //將所有副檔名為 extension 的檔案從暫存區域中移除 git reset *.extension //將所有檔案從暫存區域中移除 git reset . //將所有已追蹤檔案還原 git reset --hard //將所有已追蹤檔案還原 git reset --hard //將未追蹤檔案捨棄 git clean -f -d //提交並附上提交訊息 git commit -m "commit message" //修改提交訊息 git commit --amend //取消追蹤並刪除檔案 git rm <file> //取消追蹤檔案 git rm --cached <file> //取得提交內容並提交到當前分支 git cherry-pick <sha> //取得合併內容並提交到當前分支 git cherry-pick -m 1 <sha> //還原提交內容 git revert <sha>


### 檢查與比較

//查看當前檔案狀態 git status //比對工作目錄及暫存區域的差異 git diff //顯示提交歷史紀錄 git log //顯示 n 個提交歷史紀錄 git log -n //顯示提交內容 git show <sha>


### 遠端和更新

//顯示所有遠端儲存庫 git remote //顯示所有遠端儲存庫及 URL git remote -v //新增遠端儲存庫並命名為 short_name git remote add <short_name> <url> //更名遠端儲存庫 git remote rename <short_name> <new_name> //移除遠端儲存庫 git remote rm <short_name> //擷取所有遠端儲存庫 git fetch //擷取遠端儲存庫的 branch_name 分支 git fetch <branch_name> //擷取並合併遠端儲存庫 git pull //將當前分支上傳到遠端儲存庫 git push <remote_name> <branch_name>


### 分支與合併

//顯示本地所有分支 git branch //顯示儲存庫所有分支 git branch -a //新增分支 git branch <branch_name> //刪除分支 git branch -d <branch_name> //強制刪除分支 git branch -D <branch_name> //更名分支 git branch -m <old_branch_name> <new_branch_name> //切換分支 git checkout <branch_name> //新增並切換至分支 git checkout -b <branch_name> //將 branch_name 合併到當前分支 git merge <branch_name> //以 branch_name 為基底衍合當前分支 git rebase <branch_name> //新增暫存 git stash //顯示查看所有暫存 git stash list //提取暫存 git stash apply //提取特定暫存 git stash apply <stash_name> //刪除特定暫存 git stash drop <stash_name>


### 子模組

//新增子模組 git submodule add <url> //初始化子模組 git submodule init //更新子模組 git submodule update


參考資料

Git – [https://git-scm.com/](https://git-scm.com/)

一直想學好Git，但是很抗拒用指令…

想Github +Github Desktop 學好，

寫篇超簡單教學文。

LikeLike