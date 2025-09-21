#!/usr/bin/env bash
set -euo pipefail

# 检查是否在 git 仓库内
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
	echo "不是一个 git 仓库，退出。" >&2
	exit 1
fi

# 检查是否有变更（包含未跟踪文件）
if [ -z "$(git status --porcelain)" ]; then
	echo "没有新的更改，退出。"
	exit 0
fi

# 暂存所有变更（包含未跟踪文件）
git add -A

# 使用参数作为 commit 信息，否则使用默认带时间戳的信息
if [ $# -ge 1 ]; then
	commit_msg="$*"
else
	commit_msg="Auto commit: $(date +'%Y-%m-%d %H:%M:%S')"
fi

# 提交（如果没有实际变更，git commit 会返回非零）
if git commit -m "$commit_msg"; then
	echo "提交成功：$commit_msg"
else
	echo "提交失败或没有需要提交的变更。" >&2
	exit 1
fi

# 获取当前分支，处理 detached HEAD（此时使用 HEAD 推送）
branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || true)"
if [ -z "$branch" ] || [ "$branch" = "HEAD" ]; then
    echo "处于 detached HEAD 状态，跳过推送。请手动推送。" >&2
    exit 0  # 或改为 exit 1，如果不想跳过
else
	push_target="$branch"
fi

# 检查是否存在 origin 远程
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "没有配置 origin 远程，退出。" >&2
    exit 1
fi

# 推送到 origin（若没有 origin，git 会报错）
if git push origin "$push_target"; then
	echo "推送到 origin/$push_target 成功。"
	exit 0
else
	echo "推送到 origin/$push_target 失败。" >&2
	exit 1
fi
