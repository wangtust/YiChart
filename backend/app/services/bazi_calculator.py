"""
八字排盘计算引擎
计算天干地支、五行、十神、纳音等
"""

from datetime import datetime

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干五行
TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

# 天干阴阳
TIANGAN_YINYANG = {
    "甲": "阳", "乙": "阴",
    "丙": "阳", "丁": "阴",
    "戊": "阳", "己": "阴",
    "庚": "阳", "辛": "阴",
    "壬": "阳", "癸": "阴",
}

# 地支五行
DIZHI_WUXING = {
    "子": "水", "丑": "土",
    "寅": "木", "卯": "木",
    "辰": "土", "巳": "火",
    "午": "火", "未": "土",
    "申": "金", "酉": "金",
    "戌": "土", "亥": "水",
}

# 地支藏干
DIZHI_CANGGAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

# 生肖
SHENGXIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 纳音表 (60甲子纳音)
NAYIN_TABLE = {
    "甲子": "海中金", "乙丑": "海中金",
    "丙寅": "炉中火", "丁卯": "炉中火",
    "戊辰": "大林木", "己巳": "大林木",
    "庚午": "路旁土", "辛未": "路旁土",
    "壬申": "剑锋金", "癸酉": "剑锋金",
    "甲戌": "山头火", "乙亥": "山头火",
    "丙子": "涧下水", "丁丑": "涧下水",
    "戊寅": "城头土", "己卯": "城头土",
    "庚辰": "白蜡金", "辛巳": "白蜡金",
    "壬午": "杨柳木", "癸未": "杨柳木",
    "甲申": "泉中水", "乙酉": "泉中水",
    "丙戌": "屋上土", "丁亥": "屋上土",
    "戊子": "霹雳火", "己丑": "霹雳火",
    "庚寅": "松柏木", "辛卯": "松柏木",
    "壬辰": "长流水", "癸巳": "长流水",
    "甲午": "砂中金", "乙未": "砂中金",
    "丙申": "山下火", "丁酉": "山下火",
    "戊戌": "平地木", "己亥": "平地木",
    "庚子": "壁上土", "辛丑": "壁上土",
    "壬寅": "金箔金", "癸卯": "金箔金",
    "甲辰": "覆灯火", "乙巳": "覆灯火",
    "丙午": "天河水", "丁未": "天河水",
    "戊申": "大驿土", "己酉": "大驿土",
    "庚戌": "钗钏金", "辛亥": "钗钏金",
    "壬子": "桑柘木", "癸丑": "桑柘木",
    "甲寅": "大溪水", "乙卯": "大溪水",
    "丙辰": "沙中土", "丁巳": "沙中土",
    "戊午": "天上火", "己未": "天上火",
    "庚申": "石榴木", "辛酉": "石榴木",
    "壬戌": "大海水", "癸亥": "大海水",
}

# 十神关系 (以日主天干为中心)
SHISHEN_MAP = {
    # 同我者为比劫: 同阴阳=比肩, 异阴阳=劫财
    # 生我者为印枭: 同阴阳=偏印, 异阴阳=正印
    # 我生者为食伤: 同阴阳=食神, 异阴阳=伤官
    # 克我者为官杀: 同阴阳=偏官(七杀), 异阴阳=正官
    # 我克者为财才: 同阴阳=偏财, 异阴阳=正财
}

# 五行相生相克
WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


def get_shishen(day_master: str, other_stem: str) -> str:
    """计算十神关系"""
    dm_wx = TIANGAN_WUXING[day_master]
    dm_yy = TIANGAN_YINYANG[day_master]
    other_wx = TIANGAN_WUXING[other_stem]
    other_yy = TIANGAN_YINYANG[other_stem]
    same_yy = dm_yy == other_yy

    if dm_wx == other_wx:
        return "比肩" if same_yy else "劫财"
    elif WUXING_SHENG[other_wx] == dm_wx:
        return "偏印" if same_yy else "正印"
    elif WUXING_SHENG[dm_wx] == other_wx:
        return "食神" if same_yy else "伤官"
    elif WUXING_KE[other_wx] == dm_wx:
        return "偏官" if same_yy else "正官"
    elif WUXING_KE[dm_wx] == other_wx:
        return "偏财" if same_yy else "正财"
    return "未知"


# ============================================================
# 万年历数据 (1900-2100 年的年柱和月柱)
# ============================================================

# 年柱天干地支索引 (以1900年庚子年为基准)
# 1900年 = 庚子年, 庚=6, 子=0
YEAR_BASE = 1900
YEAR_STEM_OFFSET = 6  # 1900年天干索引
YEAR_BRANCH_OFFSET = 0  # 1900年地支索引


def get_year_pillar(year: int) -> tuple[str, str]:
    """计算年柱天干地支"""
    # 立春分界 (简化: 以2月4日为界)
    stem_idx = (year - YEAR_BASE + YEAR_STEM_OFFSET) % 10
    branch_idx = (year - YEAR_BASE + YEAR_BRANCH_OFFSET) % 12
    return TIANGAN[stem_idx], DIZHI[branch_idx]


def get_month_pillar(year: int, month: int, day: int) -> tuple[str, str]:
    """
    计算月柱天干地支
    月柱以节气为分界:
    立春(寅月)、惊蛰(卯月)、清明(辰月)、立夏(巳月)、
    芒种(午月)、小暑(未月)、立秋(申月)、白露(酉月)、
    寒露(戌月)、立冬(亥月)、大雪(子月)、小寒(丑月)
    """
    # 简化节气分界 (日)
    jieqi = {
        1: 6, 2: 4, 3: 6, 4: 5, 5: 6, 6: 6,
        7: 7, 8: 8, 9: 8, 10: 8, 11: 7, 12: 7,
    }

    # 判断是否已过本月节气
    lunar_month = month
    if day < jieqi[month]:
        lunar_month = month - 1
    if lunar_month == 0:
        lunar_month = 12

    # 地支: 寅月(1月)起
    branch_idx = (lunar_month + 1) % 12  # 寅=2, 所以 month+1

    # 天干: 五虎遁月 (年干决定月干起点)
    year_stem, _ = get_year_pillar(year)
    year_stem_idx = TIANGAN.index(year_stem)
    # 甲己之年丙作首, 乙庚之年戊为头, 丙辛之岁寻庚上, 丁壬壬寅顺水流, 戊癸之年甲寅起
    month_stem_start = [2, 4, 6, 8, 0]  # 丙(2), 戊(4), 庚(6), 壬(8), 甲(0)
    base = month_stem_start[year_stem_idx % 5]
    month_stem_idx = (base + lunar_month - 1) % 10

    return TIANGAN[month_stem_idx], DIZHI[branch_idx]


def get_day_pillar(year: int, month: int, day: int) -> tuple[str, str]:
    """
    计算日柱天干地支
    使用基姆拉尔森公式的变体计算日干支
    """
    # 基准日: 1900年1月1日 = 甲戌日 (甲=0, 戌=10)
    # 使用儒略日数计算
    if month <= 2:
        year -= 1
        month += 12

    # 儒略日数
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day - 1524.5

    # 已知: 1900年1月1日儒略日 = 2415021, 当天为甲戌日
    # 甲=0, 戌=10 => 干支序号 = (0, 10)
    base_jd = 2415021
    offset = int(jd - base_jd)

    stem_idx = offset % 10
    branch_idx = offset % 12

    return TIANGAN[stem_idx], DIZHI[branch_idx]


def get_hour_pillar(day_stem: str, hour: int) -> tuple[str, str]:
    """
    计算时柱天干地支
    时辰: 子(23-1), 丑(1-3), 寅(3-5), 卯(5-7), 辰(7-9), 巳(9-11),
          午(11-13), 未(13-15), 申(15-17), 酉(17-19), 戌(19-21), 亥(21-23)
    """
    # 时辰地支索引
    hour_idx = ((hour + 1) % 24) // 2
    branch = DIZHI[hour_idx]

    # 五鼠遁时 (日干决定时干起点)
    day_stem_idx = TIANGAN.index(day_stem)
    # 甲己还加甲, 乙庚丙作初, 丙辛从戊起, 丁壬庚子居, 戊癸何方发, 壬子是真途
    hour_stem_start = [0, 2, 4, 6, 8]  # 甲(0), 丙(2), 戊(4), 庚(6), 壬(8)
    base = hour_stem_start[day_stem_idx % 5]
    hour_stem_idx = (base + hour_idx) % 10

    return TIANGAN[hour_stem_idx], branch


def calculate_wuxing(pillars: dict) -> dict[str, int]:
    """计算五行统计"""
    wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}

    for pillar_name in ["year", "month", "day", "hour"]:
        pillar = pillars[pillar_name]
        wuxing_count[TIANGAN_WUXING[pillar["heavenly_stem"]]] += 1
        wuxing_count[DIZHI_WUXING[pillar["earthly_branch"]]] += 1

    return wuxing_count


def calculate_bazi(birth_date: str, birth_time: str, gender: str) -> dict:
    """
    完整八字排盘计算

    Args:
        birth_date: 出生日期 YYYY-MM-DD
        birth_time: 出生时间 HH:MM
        gender: 性别 male/female

    Returns:
        完整八字排盘结果
    """
    dt = datetime.strptime(birth_date, "%Y-%m-%d")
    year, month, day = dt.year, dt.month, dt.day
    hour, minute = map(int, birth_time.split(":"))

    # 计算四柱
    year_tg, year_dz = get_year_pillar(year)
    month_tg, month_dz = get_month_pillar(year, month, day)
    day_tg, day_dz = get_day_pillar(year, month, day)
    hour_tg, hour_dz = get_hour_pillar(day_tg, hour)

    pillars = {
        "year": {"heavenly_stem": year_tg, "earthly_branch": year_dz},
        "month": {"heavenly_stem": month_tg, "earthly_branch": month_dz},
        "day": {"heavenly_stem": day_tg, "earthly_branch": day_dz},
        "hour": {"heavenly_stem": hour_tg, "earthly_branch": hour_dz},
    }

    # 添加藏干
    for key in pillars:
        pillars[key]["hidden_stems"] = DIZHI_CANGGAN[pillars[key]["earthly_branch"]]
        pillars[key]["wuxing"] = TIANGAN_WUXING[pillars[key]["heavenly_stem"]]

    # 五行统计
    wuxing = calculate_wuxing(pillars)

    # 生肖 (以年支定)
    year_dz_idx = DIZHI.index(year_dz)
    shengxiao = SHENGXIAO[year_dz_idx]

    # 纳音 (以年柱定)
    nayin_key = year_tg + year_dz
    nayin = NAYIN_TABLE.get(nayin_key, "未知")

    # 日主
    day_master = day_tg
    day_master_wuxing = TIANGAN_WUXING[day_master]

    # 十神
    shishen = {}
    all_stems = [year_tg, month_tg, day_tg, hour_tg]
    pillar_names = ["年干", "月干", "日干", "时干"]
    for name, stem in zip(pillar_names, all_stems):
        if stem == day_master:
            shishen[name] = "日主"
        else:
            shishen[name] = get_shishen(day_master, stem)

    return {
        "year_pillar": pillars["year"],
        "month_pillar": pillars["month"],
        "day_pillar": pillars["day"],
        "hour_pillar": pillars["hour"],
        "wuxing": wuxing,
        "shengxiao": shengxiao,
        "nayin": nayin,
        "day_master": day_master,
        "day_master_wuxing": day_master_wuxing,
        "shishen": shishen,
    }
