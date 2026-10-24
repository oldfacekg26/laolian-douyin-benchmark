# 老脸 · 抖音博主对标分析

分析公开作品与互动数据，比较突出作品和日常作品，提炼内容机制与公开商业路径。

## 能做什么

- 单博主研究、低粉爆款研究、多博主比较。
- 核实账号与作品范围，按作品 ID 去重，保留缺失数据。
- 计算同账号非置顶、非目标作品的中位点赞，筛选相对表现突出的作品。
- 对照选题、标题、开头、结构、证明、评论需求与行动引导。
- 分析公开产品、价格入口和获客路径，交付报告与复用建议。

## 安装与使用

通过 Code → Download ZIP 下载，解压后将文件夹重命名为 `laolian-douyin-benchmark`，放入 Codex 的 `~/.codex/skills/`。确认 `SKILL.md` 位于该文件夹第一层，在新会话中使用：

> 使用 $laolian-douyin-benchmark 分析这个抖音博主最近100条可见作品，找出相对日常表现突出的作品，对比普通作品，并分析产品与获客路径。主页：【填写链接】。

其他支持 SKILL.md 的智能体按各自的安装说明操作。

## 工具与输出

统计脚本仅使用 Python 标准库：

```bash
python scripts/analyze_public.py --input works.json --out output
```

输入格式见 [公开数据契约](references/data-contract.md)。输出账号汇总 CSV、作品相对表现 CSV 和分析汇总 JSON；网页采集、内容判断与报告由宿主智能体完成。完整流程见 [SKILL.md](SKILL.md)，验证记录见 [TESTING.md](TESTING.md)。

## 能力边界

浏览器由宿主提供，平台登录和验证由使用者本人处理。公开点赞不等于播放或成交；相对倍数不能证明爆款因果。没有实际检查内容时，不能只凭标题解释整条视频。

需要批量下载、全文转写和方法模板时，使用独立的 [抖音博主蒸馏 Skill](https://github.com/oldfacekg26/laolian-douyin-distill)，其转写使用 Qwen3-ASR 1.7B。两套 Skill 可分别安装。
