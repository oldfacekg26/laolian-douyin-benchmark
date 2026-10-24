# 公开数据契约

输入 UTF-8 JSON 数组，每条记录对应一个作品。

```json
[
  {
    "author_id": "demo-account",
    "author": "示例博主",
    "id": "demo-work-001",
    "url": "https://www.douyin.com/video/作品ID",
    "title": "作品标题",
    "published_at": "2026-10-01T10:00:00+08:00",
    "collected_at": "2026-10-11T10:00:00+08:00",
    "likes_display": "1.2万",
    "likes": 12000,
    "comments": null,
    "favorites": null,
    "shares": null,
    "views": null,
    "pinned": false,
    "selected": true,
    "topic": "业务自动化",
    "format": "口播",
    "evidence": "证据/主页截图.png"
  }
]
```

示例是虚构字段演示，不是真实采集结果。`author_id`、`id` 必填且为字符串，`likes` 为非负数或 null；布尔字段只能为 true/false。相同账号与作品ID只保留输入中最后一条快照，因此采集者应按时间从旧到新排列。原始快照另行保存。

其他字段用于报告追溯；unknown 数值留 null。公开显示取整后的点赞值仅近似，报告不制造小数精度。不同时间快照不得混算成“当时表现”。图文与视频分别标注。

脚本输出：
- baseline_n：排除置顶、目标作品和缺失点赞后的有效基线数。
- baseline_median_likes：基线中位点赞，样本不足5条仍展示描述统计，relative_likes 留空。
- relative_likes：该作品点赞 / 基线中位数；中位数为零、缺失或样本不足时为空。
- 倍数不是爆款因果、曝光率或收益。脚本不自动把5倍等门槛命名为“已证实爆款”。

逐条内容编码建议记录：目标受众、需求、标题公式、前几秒原话及时间点、结构、案例/证明、情绪、CTA、画面核验范围、机器转写纠错、对照作品ID。商业证据记录页面链接、日期、公开价格、产品、自述与核实状态。
