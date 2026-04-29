"""
紫微斗数排盘计算引擎
计算十二宫、星曜分布、四化等
"""

from datetime import datetime

# ============================================================
# 基础数据表
# ============================================================

# 地支（十二宫顺序）
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 十二宫名称
GONG_NAMES = ["命宫", "兄弟宫", "夫妻宫", "子女宫", "财帛宫", "疾厄宫",
              "迁移宫", "奴仆宫", "官禄宫", "田宅宫", "福德宫", "父母宫"]

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 五行局表 (天干 + 地支 → 五行局)
# 命宫天干 + 命宫地支 → 五行局
WUXING_JU = {
    "甲子": 2, "甲丑": 6, "甲寅": 6, "甲卯": 2, "甲辰": 5, "甲巳": 1,
    "甲午": 8, "甲未": 4, "甲申": 9, "甲酉": 3, "甲戌": 7, "甲亥": 5,
    "乙子": 7, "乙丑": 5, "乙寅": 1, "乙卯": 9, "乙辰": 3, "乙巳": 7,
    "乙午": 2, "乙未": 6, "乙申": 4, "乙酉": 8, "乙戌": 5, "乙亥": 1,
    "丙子": 6, "丙丑": 2, "丙寅": 5, "丙卯": 1, "丙辰": 6, "丙巳": 2,
    "丙午": 9, "丙未": 5, "丙申": 1, "丙酉": 6, "丙戌": 2, "丙亥": 9,
    "丁子": 1, "丁丑": 9, "丁寅": 3, "丁卯": 7, "丁辰": 5, "丁巳": 1,
    "丁午": 6, "丁未": 2, "丁申": 5, "丁酉": 1, "丁戌": 9, "丁亥": 3,
    "戊子": 5, "戊丑": 1, "戊寅": 6, "戊卯": 2, "戊辰": 5, "戊巳": 1,
    "戊午": 8, "戊未": 4, "戊申": 9, "戊酉": 3, "戊戌": 7, "戊亥": 5,
    "己子": 9, "己丑": 3, "己寅": 7, "己卯": 5, "己辰": 1, "己巳": 9,
    "己午": 6, "己未": 2, "己申": 5, "己酉": 1, "己戌": 9, "己亥": 3,
    "庚子": 2, "庚丑": 6, "庚寅": 6, "庚卯": 2, "庚辰": 5, "庚巳": 1,
    "庚午": 8, "庚未": 4, "庚申": 9, "庚酉": 3, "庚戌": 7, "庚亥": 5,
    "辛子": 7, "辛丑": 5, "辛寅": 1, "辛卯": 9, "辛辰": 3, "辛巳": 7,
    "辛午": 2, "辛未": 6, "辛申": 4, "辛酉": 8, "辛戌": 5, "辛亥": 1,
    "壬子": 6, "壬丑": 2, "壬寅": 5, "壬卯": 1, "壬辰": 6, "壬巳": 2,
    "壬午": 9, "壬未": 5, "壬申": 1, "壬酉": 6, "壬戌": 2, "壬亥": 9,
    "癸子": 1, "癸丑": 9, "癸寅": 3, "癸卯": 7, "癸辰": 5, "癸巳": 1,
    "癸午": 6, "癸未": 2, "癸申": 5, "癸酉": 1, "癸戌": 9, "癸亥": 3,
}

# 五行局名称
JU_NAMES = {2: "水二局", 3: "木三局", 4: "金四局", 5: "土五局", 6: "水六局",
            7: "火六局", 8: "火八局", 9: "金九局", 1: "水一局"}

# 紫微星系 (按五行局和农历日安紫微，然后排其他星)
# 紫微星在十二宫的位置 (五行局, 农历日) → 紫微所在宫位索引
ZIWEI_POS_TABLE = {
    # 水二局
    (2, 1): 2, (2, 2): 1, (2, 3): 1, (2, 4): 0, (2, 5): 0,
    (2, 6): 11, (2, 7): 11, (2, 8): 10, (2, 9): 10, (2, 10): 9,
    (2, 11): 9, (2, 12): 8, (2, 13): 8, (2, 14): 7, (2, 15): 7,
    (2, 16): 6, (2, 17): 6, (2, 18): 5, (2, 19): 5, (2, 20): 4,
    (2, 21): 4, (2, 22): 3, (2, 23): 3, (2, 24): 2, (2, 25): 2,
    (2, 26): 1, (2, 27): 1, (2, 28): 0, (2, 29): 0, (2, 30): 11,
    # 木三局
    (3, 1): 3, (3, 2): 2, (3, 3): 1, (3, 4): 1, (3, 5): 0,
    (3, 6): 0, (3, 7): 11, (3, 8): 11, (3, 9): 10, (3, 10): 9,
    (3, 11): 9, (3, 12): 8, (3, 13): 8, (3, 14): 7, (3, 15): 6,
    (3, 16): 6, (3, 17): 5, (3, 18): 5, (3, 19): 4, (3, 20): 4,
    (3, 21): 3, (3, 22): 2, (3, 23): 2, (3, 24): 1, (3, 25): 1,
    (3, 26): 0, (3, 27): 0, (3, 28): 11, (3, 29): 11, (3, 30): 10,
    # 金四局
    (4, 1): 4, (4, 2): 3, (4, 3): 2, (4, 4): 1, (4, 5): 1,
    (4, 6): 0, (4, 7): 0, (4, 8): 11, (4, 9): 10, (4, 10): 10,
    (4, 11): 9, (4, 12): 8, (4, 13): 8, (4, 14): 7, (4, 15): 6,
    (4, 16): 6, (4, 17): 5, (4, 18): 4, (4, 19): 4, (4, 20): 3,
    (4, 21): 3, (4, 22): 2, (4, 23): 1, (4, 24): 1, (4, 25): 0,
    (4, 26): 0, (4, 27): 11, (4, 28): 10, (4, 29): 10, (4, 30): 9,
    # 土五局
    (5, 1): 5, (5, 2): 4, (5, 3): 3, (5, 4): 2, (5, 5): 1,
    (5, 6): 1, (5, 7): 0, (5, 8): 0, (5, 9): 11, (5, 10): 10,
    (5, 11): 10, (5, 12): 9, (5, 13): 8, (5, 14): 8, (5, 15): 7,
    (5, 16): 6, (5, 17): 6, (5, 18): 5, (5, 19): 4, (5, 20): 4,
    (5, 21): 3, (5, 22): 2, (5, 23): 2, (5, 24): 1, (5, 25): 0,
    (5, 26): 0, (5, 27): 11, (5, 28): 10, (5, 29): 9, (5, 30): 9,
    # 水六局
    (6, 1): 6, (6, 2): 5, (6, 3): 4, (6, 4): 3, (6, 5): 2,
    (6, 6): 1, (6, 7): 1, (6, 8): 0, (6, 9): 0, (6, 10): 11,
    (6, 11): 10, (6, 12): 10, (6, 13): 9, (6, 14): 8, (6, 15): 8,
    (6, 16): 7, (6, 17): 6, (6, 18): 6, (6, 19): 5, (6, 20): 4,
    (6, 21): 4, (6, 22): 3, (6, 23): 2, (6, 24): 2, (6, 25): 1,
    (6, 26): 0, (6, 27): 0, (6, 28): 11, (6, 29): 10, (6, 30): 10,
    # 火六局
    (7, 1): 7, (7, 2): 6, (7, 3): 5, (7, 4): 4, (7, 5): 3,
    (7, 6): 2, (7, 7): 1, (7, 8): 1, (7, 9): 0, (7, 10): 0,
    (7, 11): 11, (7, 12): 10, (7, 13): 10, (7, 14): 9, (7, 15): 8,
    (7, 16): 8, (7, 17): 7, (7, 18): 6, (7, 19): 6, (7, 20): 5,
    (7, 21): 4, (7, 22): 4, (7, 23): 3, (7, 24): 2, (7, 25): 2,
    (7, 26): 1, (7, 27): 0, (7, 28): 0, (7, 29): 11, (7, 30): 10,
    # 火八局
    (8, 1): 8, (8, 2): 7, (8, 3): 6, (8, 4): 5, (8, 5): 4,
    (8, 6): 3, (8, 7): 2, (8, 8): 1, (8, 9): 1, (8, 10): 0,
    (8, 11): 0, (8, 12): 11, (8, 13): 10, (8, 14): 10, (8, 15): 9,
    (8, 16): 8, (8, 17): 8, (8, 18): 7, (8, 19): 6, (8, 20): 6,
    (8, 21): 5, (8, 22): 4, (8, 23): 4, (8, 24): 3, (8, 25): 2,
    (8, 26): 2, (8, 27): 1, (8, 28): 0, (8, 29): 0, (8, 30): 11,
    # 金九局
    (9, 1): 9, (9, 2): 8, (9, 3): 7, (9, 4): 6, (9, 5): 5,
    (9, 6): 4, (9, 7): 3, (9, 8): 2, (9, 9): 1, (9, 10): 1,
    (9, 11): 0, (9, 12): 0, (9, 13): 11, (9, 14): 10, (9, 15): 10,
    (9, 16): 9, (9, 17): 8, (9, 18): 8, (9, 19): 7, (9, 20): 6,
    (9, 21): 6, (9, 22): 5, (9, 23): 4, (9, 24): 4, (9, 25): 3,
    (9, 26): 2, (9, 27): 2, (9, 28): 1, (9, 29): 0, (9, 30): 0,
    # 水一局
    (1, 1): 1, (1, 2): 0, (1, 3): 11, (1, 4): 10, (1, 5): 9,
    (1, 6): 9, (1, 7): 8, (1, 8): 7, (1, 9): 7, (1, 10): 6,
    (1, 11): 5, (1, 12): 5, (1, 13): 4, (1, 14): 3, (1, 15): 3,
    (1, 16): 2, (1, 17): 1, (1, 18): 1, (1, 19): 0, (1, 20): 11,
    (1, 21): 11, (1, 22): 10, (1, 23): 9, (1, 24): 9, (1, 25): 8,
    (1, 26): 7, (1, 27): 7, (1, 28): 6, (1, 29): 5, (1, 30): 5,
}

# 紫微星系各星相对于紫微星的偏移
ZIWEI_SYSTEM = {
    "紫微": 0,
    "天机": -1,
    "太阳": -3,
    "武曲": -4,
    "天同": -5,
    "廉贞": -8,
}

# 天府星系各星相对于天府星的偏移
TIANFU_SYSTEM = {
    "天府": 0,
    "太阴": 1,
    "贪狼": 2,
    "巨门": 3,
    "天相": 4,
    "天梁": 5,
    "七杀": 6,
    "破军": 10,
}

# 天府星位置 (紫微在某宫时，天府在对应宫)
# 紫微宫位索引 → 天府宫位索引
TIANFU_FROM_ZIWEI = {
    0: 4, 1: 3, 2: 2, 3: 1, 4: 0, 5: 11,
    6: 10, 7: 9, 8: 8, 9: 7, 10: 6, 11: 5,
}

# 四化表 (天干 → 化禄、化权、化科、化忌)
SIHUA_TABLE = {
    "甲": ["廉贞", "破军", "武曲", "太阳"],
    "乙": ["天机", "天梁", "紫微", "太阴"],
    "丙": ["天同", "天机", "文昌", "廉贞"],
    "丁": ["太阴", "天同", "天机", "巨门"],
    "戊": ["贪狼", "太阴", "右弼", "天机"],
    "己": ["武曲", "贪狼", "天梁", "文曲"],
    "庚": ["太阳", "武曲", "太阴", "天同"],
    "辛": ["巨门", "太阳", "文曲", "文昌"],
    "壬": ["天梁", "紫微", "左辅", "武曲"],
    "癸": ["破军", "巨门", "太阴", "贪狼"],
}

# 辅星
# 文昌星位置 (出生时辰 → 文昌所在宫)
WENCHANG_POS = {
    "子": 4, "丑": 3, "寅": 2, "卯": 1, "辰": 0, "巳": 11,
    "午": 10, "未": 9, "申": 8, "酉": 7, "戌": 6, "亥": 5,
}

# 文曲星位置 (出生时辰 → 文曲所在宫)
WENQU_POS = {
    "子": 10, "丑": 11, "寅": 0, "卯": 1, "辰": 2, "巳": 3,
    "午": 4, "未": 5, "申": 6, "酉": 7, "戌": 8, "亥": 9,
}

# 左辅星位置 (出生月 → 左辅所在宫)
ZUOFU_POS = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 0, 12: 1}

# 右弼星位置 (出生月 → 右弼所在宫)
YOUBI_POS = {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3, 9: 2, 10: 1, 11: 0, 12: 11}

# 天魁、天钺位置 (出生年天干 → 宫位)
TIANKUI_POS = {"甲": 1, "乙": 0, "丙": 11, "丁": 11, "戊": 1, "己": 0, "庚": 7, "辛": 6, "壬": 3, "癸": 2}
TIANYUE_POS = {"甲": 7, "乙": 6, "丙": 3, "丁": 5, "戊": 7, "己": 6, "庚": 1, "辛": 0, "壬": 9, "癸": 8}

# 禄存位置 (出生年天干 → 宫位)
LUCUN_POS = {"甲": 2, "乙": 3, "丙": 5, "丁": 6, "戊": 5, "己": 6, "庚": 8, "辛": 9, "癸": 11}

# 地支对应生肖
SHENGXIAO = {
    "子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔", "辰": "龙", "巳": "蛇",
    "午": "马", "未": "羊", "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪",
}


# ============================================================
# 核心计算函数
# ============================================================

def get_ming_gong(month: int, hour_zhi_idx: int) -> int:
    """
    计算命宫位置
    命宫 = 寅宫 + (月数 - 1) - 时辰地支索引
    """
    # 寅宫索引 = 2
    ming_idx = (2 + (month - 1) - hour_zhi_idx) % 12
    return ming_idx


def get_shen_gong(ming_idx: int, month: int, hour_zhi_idx: int) -> int:
    """
    计算身宫位置
    身宫 = 寅宫 + (月数 - 1) + 时辰地支索引
    """
    shen_idx = (2 + (month - 1) + hour_zhi_idx) % 12
    return shen_idx


def get_gong_names(ming_idx: int) -> dict[int, str]:
    """根据命宫位置，确定十二宫名称"""
    gongs = {}
    for i, name in enumerate(GONG_NAMES):
        gongs[(ming_idx + i) % 12] = name
    return gongs


def get_wuxing_ju(ming_gan: str, ming_zhi: str) -> int:
    """获取五行局"""
    key = ming_gan + ming_zhi
    return WUXING_JU.get(key, 2)


def get_ziwei_pos(ju: int, lunar_day: int) -> int:
    """获取紫微星位置"""
    key = (ju, lunar_day)
    return ZIWEI_POS_TABLE.get(key, 0)


def get_tianfu_pos(ziwei_pos: int) -> int:
    """获取天府星位置"""
    return TIANFU_FROM_ZIWEI.get(ziwei_pos, 4)


def place_ziwei_system(ziwei_pos: int) -> dict[int, list[str]]:
    """安紫微星系"""
    stars = {}
    for star, offset in ZIWEI_SYSTEM.items():
        pos = (ziwei_pos + offset) % 12
        if pos not in stars:
            stars[pos] = []
        stars[pos].append(star)
    return stars


def place_tianfu_system(tianfu_pos: int) -> dict[int, list[str]]:
    """安天府星系"""
    stars = {}
    for star, offset in TIANFU_SYSTEM.items():
        pos = (tianfu_pos + offset) % 12
        if pos not in stars:
            stars[pos] = []
        stars[pos].append(star)
    return stars


def place_aux_stars(birth_month: int, birth_hour_zhi: str, year_gan: str) -> dict[int, list[str]]:
    """安辅星"""
    stars = {}

    def add_star(pos, name):
        if pos not in stars:
            stars[pos] = []
        stars[pos].append(name)

    # 文昌、文曲
    if birth_hour_zhi in WENCHANG_POS:
        add_star(WENCHANG_POS[birth_hour_zhi], "文昌")
    if birth_hour_zhi in WENQU_POS:
        add_star(WENQU_POS[birth_hour_zhi], "文曲")

    # 左辅、右弼
    if birth_month in ZUOFU_POS:
        add_star(ZUOFU_POS[birth_month], "左辅")
    if birth_month in YOUBI_POS:
        add_star(YOUBI_POS[birth_month], "右弼")

    # 天魁、天钺
    if year_gan in TIANKUI_POS:
        add_star(TIANKUI_POS[year_gan], "天魁")
    if year_gan in TIANYUE_POS:
        add_star(TIANYUE_POS[year_gan], "天钺")

    # 禄存
    if year_gan in LUCUN_POS:
        add_star(LUCUN_POS[year_gan], "禄存")

    return stars


def get_sihua(year_gan: str) -> dict[str, str]:
    """获取四化"""
    if year_gan in SIHUA_TABLE:
        lu, quan, ke, ji = SIHUA_TABLE[year_gan]
        return {"化禄": lu, "化权": quan, "化科": ke, "化忌": ji}
    return {}


def calculate_ziwei(birth_date: str, birth_time: str, gender: str) -> dict:
    """
    紫微斗数完整排盘

    Args:
        birth_date: 出生日期 YYYY-MM-DD
        birth_time: 出生时间 HH:MM
        gender: 性别 male/female

    Returns:
        完整紫微命盘数据
    """
    from datetime import datetime

    dt = datetime.strptime(birth_date, "%Y-%m-%d")
    year, month, day = dt.year, dt.month, dt.day
    hour, minute = map(int, birth_time.split(":"))

    # 计时辰地支索引
    hour_zhi_idx = ((hour + 1) % 24) // 2
    hour_zhi = DIZHI[hour_zhi_idx]

    # 年干支 (简化计算)
    year_gan_idx = (year - 4) % 10
    year_zhi_idx = (year - 4) % 12
    year_gan = TIANGAN[year_gan_idx]
    year_zhi = DIZHI[year_zhi_idx]

    # 命宫、身宫
    ming_gong_idx = get_ming_gong(month, hour_zhi_idx)
    shen_gong_idx = get_shen_gong(ming_gong_idx, month, hour_zhi_idx)

    # 命宫天干 (用年干遁月干的方法推算)
    # 甲己之年丙作首, 乙庚之年戊为头, 丙辛之岁寻庚上, 丁壬壬寅顺水流, 戊癸之年甲寅起
    month_gan_start = [2, 4, 6, 8, 0]
    base = month_gan_start[year_gan_idx % 5]
    ming_gan_idx_calc = (base + month - 1) % 10
    # 命宫天干 = 从寅宫开始，按命宫位置推算
    ming_gan_idx_calc = (base + ming_gong_idx - 2) % 10
    ming_gan = TIANGAN[ming_gan_idx_calc]
    ming_zhi = DIZHI[ming_gong_idx]

    # 五行局
    wuxing_ju = get_wuxing_ju(ming_gan, ming_zhi)
    ju_name = JU_NAMES.get(wuxing_ju, f"局数{wuxing_ju}")

    # 农历日 (简化: 用公历日近似)
    lunar_day = day

    # 紫微星位置
    ziwei_pos = get_ziwei_pos(wuxing_ju, lunar_day)

    # 天府星位置
    tianfu_pos = get_tianfu_pos(ziwei_pos)

    # 安紫微星系
    ziwei_stars = place_ziwei_system(ziwei_pos)

    # 安天府星系
    tianfu_stars = place_tianfu_system(tianfu_pos)

    # 安辅星
    aux_stars = place_aux_stars(month, hour_zhi, year_gan)

    # 合并所有星曜
    all_stars = {}
    for pos_stars in [ziwei_stars, tianfu_stars, aux_stars]:
        for pos, stars in pos_stars.items():
            if pos not in all_stars:
                all_stars[pos] = []
            all_stars[pos].extend(stars)

    # 四化
    sihua = get_sihua(year_gan)

    # 标记四化星
    sihua_marks = {}
    for hua_name, star_name in sihua.items():
        for pos, stars in all_stars.items():
            if star_name in stars:
                sihua_marks[star_name] = hua_name

    # 十二宫数据
    gong_names = get_gong_names(ming_gong_idx)
    palaces = {}
    for idx in range(12):
        gong_name = gong_names[idx]
        stars_in_gong = all_stars.get(idx, [])
        # 添加四化标记
        stars_with_hua = []
        for star in stars_in_gong:
            if star in sihua_marks:
                stars_with_hua.append(f"{star}({sihua_marks[star]})")
            else:
                stars_with_hua.append(star)

        palaces[gong_name] = {
            "地支": DIZHI[idx],
            "星曜": stars_with_hua,
            "原始星曜": stars_in_gong,
            "是命宫": idx == ming_gong_idx,
            "是身宫": idx == shen_gong_idx,
        }

    return {
        "palaces": palaces,
        "sihua": sihua,
        "ming_gong": DIZHI[ming_gong_idx],
        "shen_gong": DIZHI[shen_gong_idx],
        "五行局": ju_name,
        "紫微位置": DIZHI[ziwei_pos],
        "天府位置": DIZHI[tianfu_pos],
        "年干": year_gan,
        "年支": year_zhi,
        "生肖": SHENGXIAO.get(year_zhi, ""),
        "命宫天干": ming_gan,
        "命宫地支": ming_zhi,
    }
