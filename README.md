# Music Record

一个记录网易云音乐歌单变化、评论歌单音乐的工具

## 功能

- 使用 git 记录多个指定歌单的歌曲变化（新增/删除）
- 可自动化更新文档
- 支持对每首歌添加 markdown 音乐评论

## 使用

1. 克隆仓库，并创建一个分支以记录你自己的歌单变化，并设置你的远程仓库

    ```bash
    git clone --single-branch --branch main https://github.com/cheanus/MusicRecord.git
    cd MusicRecord
    git switch -c mine
    git remote set-url origin <你的远程仓库地址>
    ```

2. 安装依赖

    ```bash
    pip install requests
    ```

3. 安装[NeteaseCloudMusicApiEnhanced](https://github.com/neteasecloudmusicapienhanced/api-enhanced)
4. 修改 `config.py` 文件，添加你想要跟踪的歌单 ID
5. 运行 `update.py` 脚本以生成文档，运行 `git_push.sh` 以推送可能存在的更改（可设置为定时运行）

    ```bash
    python update.py
    bash ./git_push.sh
    ```
