"""
八字解读 Prompt 模板
"""

BAZI_ANALYSIS_PROMPT = """你是一位精通中国传统命理学的大师，擅长八字命理分析，拥有数十年的命理研究经验。
请根据以下八字信息进行详细、专业且通俗易懂的分析。

## 命主信息
- 性别: {gender}
- 生肖: {shengxiao}
- 纳音: {nayin}

## 四柱排盘
| 柱 | 天干 | 地支 | 藏干 | 五行 |
|---|---|---|---|---|
| 年柱 | {year_stem} | {year_branch} | {year_hidden} | {year_wuxing} |
| 月柱 | {month_stem} | {month_branch} | {month_hidden} | {month_wuxing} |
| 日柱 | {day_stem} | {day_branch} | {day_hidden} | {day_wuxing} |
| 时柱 | {hour_stem} | {hour_branch} | {hour_hidden} | {hour_wuxing} |

## 五行分布
金: {jin}  木: {mu}  水: {shui}  火: {huo}  土: {tu}

## 日主
日主为 {day_master}，五行属 {day_master_wuxing}

## 十神
{shishen_info}

---

请从以下维度进行详细分析:

### 1. 命格总评
简要概括此命格的特点和格局。

### 2. 性格特征
根据日主五行、十神组合分析命主的性格特点。

### 3. 事业运势
分析适合的行业方向、事业发展特点和注意事项。

### 4. 感情婚姻
分析感情运势、婚姻特点和相处之道。

### 5. 健康提醒
根据五行偏旺偏弱，提示需要关注的健康方面。

### 6. 开运建议
- 有利方位
- 有利颜色
- 有利数字
- 适合佩戴的饰物
- 日常注意事项

请用温暖积极的语气，既要指出命理特点，也要给出建设性的建议。
分析要结合传统命理知识，但用通俗易懂的语言表达，让普通人也能理解。
每个维度至少写 3-5 句话，整体分析不少于 500 字。
"""


def format_bazi_prompt(bazi_result: dict, gender: str) -> str:
    """格式化八字分析 prompt"""
    gender_cn = "男" if gender == "male" else "女"

    pillars = {
        "year": bazi_result["year_pillar"],
        "month": bazi_result["month_pillar"],
        "day": bazi_result["day_pillar"],
        "hour": bazi_result["hour_pillar"],
    }

    def fmt_hidden(stems):
        return " ".join(stems) if stems else "无"

    shishen_info = "\n".join([f"- {k}: {v}" for k, v in bazi_result["shishen"].items()])

    return BAZI_ANALYSIS_PROMPT.format(
        gender=gender_cn,
        shengxiao=bazi_result["shengxiao"],
        nayin=bazi_result["nayin"],
        year_stem=pillars["year"]["heavenly_stem"],
        year_branch=pillars["year"]["earthly_branch"],
        year_hidden=fmt_hidden(pillars["year"].get("hidden_stems", [])),
        year_wuxing=pillars["year"].get("wuxing", ""),
        month_stem=pillars["month"]["heavenly_stem"],
        month_branch=pillars["month"]["earthly_branch"],
        month_hidden=fmt_hidden(pillars["month"].get("hidden_stems", [])),
        month_wuxing=pillars["month"].get("wuxing", ""),
        day_stem=pillars["day"]["heavenly_stem"],
        day_branch=pillars["day"]["earthly_branch"],
        day_hidden=fmt_hidden(pillars["day"].get("hidden_stems", [])),
        day_wuxing=pillars["day"].get("wuxing", ""),
        hour_stem=pillars["hour"]["heavenly_stem"],
        hour_branch=pillars["hour"]["earthly_branch"],
        hour_hidden=fmt_hidden(pillars["hour"].get("hidden_stems", [])),
        hour_wuxing=pillars["hour"].get("wuxing", ""),
        jin=bazi_result["wuxing"].get("金", 0),
        mu=bazi_result["wuxing"].get("木", 0),
        shui=bazi_result["wuxing"].get("水", 0),
        huo=bazi_result["wuxing"].get("火", 0),
        tu=bazi_result["wuxing"].get("土", 0),
        day_master=bazi_result["day_master"],
        day_master_wuxing=bazi_result["day_master_wuxing"],
        shishen_info=shishen_info,
    )
