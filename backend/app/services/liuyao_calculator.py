"""
六爻起卦计算引擎
模拟铜钱摇卦，计算本卦、变卦、世应、六亲等
"""

import random

# ============================================================
# 基础数据表
# ============================================================

# 八卦 (三爻 → 卦名)
BAGUA = {
    (1, 1, 1): "乾",
    (0, 0, 0): "坤",
    (1, 0, 0): "震",
    (0, 1, 0): "坎",
    (0, 0, 1): "艮",
    (0, 1, 1): "巽",
    (1, 0, 1): "离",
    (1, 1, 0): "兑",
}

# 六十四卦 (上卦, 下卦) → (卦名, 卦辞)
GUA_64 = {
    ("乾", "乾"): ("乾为天", "元亨利贞"),
    ("坤", "坤"): ("坤为地", "元亨，利牝马之贞"),
    ("震", "震"): ("震为雷", "亨。震来虩虩，笑言哑哑"),
    ("坎", "坎"): ("坎为水", "习坎，有孚，维心亨"),
    ("艮", "艮"): ("艮为山", "艮其背，不获其身"),
    ("巽", "巽"): ("巽为风", "小亨，利有攸往"),
    ("离", "离"): ("离为火", "利贞，亨。畜牝牛，吉"),
    ("兑", "兑"): ("兑为泽", "亨，利贞"),
    ("震", "坤"): ("雷地豫", "利建侯行师"),
    ("坤", "震"): ("地雷复", "亨。出入无疾，朋来无咎"),
    ("坎", "震"): ("水雷屯", "元亨利贞，勿用有攸往"),
    ("震", "坎"): ("雷水解", "利西南，无所往"),
    ("艮", "坎"): ("山水蒙", "亨。匪我求童蒙，童蒙求我"),
    ("坎", "艮"): ("水山蹇", "利西南，不利东北"),
    ("乾", "坎"): ("天水讼", "有孚窒惕，中吉"),
    ("坎", "乾"): ("水天需", "有孚，光亨贞吉"),
    ("坤", "坎"): ("地水师", "贞，丈人吉，无咎"),
    ("坎", "坤"): ("水地比", "吉。原筮元永贞，无咎"),
    ("乾", "震"): ("天雷无妄", "元亨利贞"),
    ("震", "乾"): ("雷天大壮", "利贞"),
    ("乾", "艮"): ("天山遁", "亨。小利贞"),
    ("艮", "乾"): ("山天大畜", "利贞，不家食吉"),
    ("乾", "巽"): ("天风姤", "女壮，勿用取女"),
    ("巽", "乾"): ("风天小畜", "亨。密云不雨，自我西郊"),
    ("乾", "兑"): ("天泽履", "履虎尾，不咥人，亨"),
    ("兑", "乾"): ("泽天夬", "扬于王庭，孚号有厉"),
    ("坤", "兑"): ("地泽临", "元亨利贞"),
    ("兑", "坤"): ("泽地萃", "亨。王假有庙"),
    ("坤", "巽"): ("地风升", "元亨。用见大人"),
    ("巽", "坤"): ("风地观", "盥而不荐，有孚颙若"),
    ("坤", "离"): ("地火明夷", "利艰贞"),
    ("离", "坤"): ("火地晋", "康侯用锡马蕃庶"),
    ("坤", "艮"): ("地山谦", "亨，君子有终"),
    ("艮", "坤"): ("山地剥", "不利有攸往"),
    ("震", "巽"): ("雷风恒", "亨，无咎，利贞"),
    ("巽", "震"): ("风雷益", "利有攸往，利涉大川"),
    ("震", "离"): ("雷火丰", "亨。王假之，勿忧"),
    ("离", "震"): ("火雷噬嗑", "亨。利用狱"),
    ("震", "艮"): ("雷山小过", "亨利贞。可小事，不可大事"),
    ("艮", "震"): ("山雷颐", "贞吉。观颐，自求口实"),
    ("震", "兑"): ("雷泽归妹", "征凶，无攸利"),
    ("兑", "震"): ("泽雷随", "元亨利贞，无咎"),
    ("坎", "巽"): ("水风井", "改邑不改井"),
    ("巽", "坎"): ("风水涣", "亨。王假有庙"),
    ("坎", "离"): ("水火既济", "亨小利贞。初吉终乱"),
    ("离", "坎"): ("火水未济", "亨。小狐汔济"),
    ("坎", "兑"): ("水泽节", "亨。苦节不可贞"),
    ("兑", "坎"): ("泽水困", "亨，贞大人吉"),
    ("坎", "巽"): ("水风井", "改邑不改井"),
    ("艮", "巽"): ("山风蛊", "元亨，利涉大川"),
    ("巽", "艮"): ("风山渐", "女归吉，利贞"),
    ("艮", "离"): ("山火贲", "亨。小利有攸往"),
    ("离", "艮"): ("火山旅", "小亨，旅贞吉"),
    ("艮", "兑"): ("山泽损", "有孚，元吉"),
    ("兑", "艮"): ("泽山咸", "亨，利贞"),
    ("巽", "离"): ("风火家人", "利女贞"),
    ("离", "巽"): ("火风鼎", "元吉，亨"),
    ("巽", "兑"): ("风泽中孚", "豚鱼吉"),
    ("兑", "巽"): ("泽风大过", "栋桡，利有攸往"),
    ("离", "兑"): ("火泽睽", "小事吉"),
    ("兑", "离"): ("泽火革", "己日乃孚，元亨利贞"),
    ("离", "离"): ("离为火", "利贞，亨。畜牝牛，吉"),
    ("兑", "兑"): ("兑为泽", "亨，利贞"),
    ("巽", "巽"): ("巽为风", "小亨，利有攸往"),
    ("艮", "艮"): ("艮为山", "艮其背，不获其身"),
}

# 八卦五行
BAGUA_WUXING = {
    "乾": "金", "兑": "金",
    "震": "木", "巽": "木",
    "坎": "水",
    "离": "火",
    "坤": "土", "艮": "土",
}

# 纳甲表 (八卦 → 天干地支，从初爻到上爻)
NAJIA_TABLE = {
    "乾": ["甲子", "甲寅", "甲辰", "壬午", "壬申", "壬戌"],
    "坤": ["乙未", "乙巳", "乙卯", "癸丑", "癸亥", "癸酉"],
    "震": ["庚子", "庚寅", "庚辰", "庚午", "庚申", "庚戌"],
    "巽": ["辛丑", "辛亥", "辛酉", "辛未", "辛巳", "辛卯"],
    "坎": ["戊寅", "戊辰", "戊午", "戊申", "戊戌", "戊子"],
    "离": ["己卯", "己丑", "己亥", "己酉", "己未", "己巳"],
    "艮": ["丙辰", "丙午", "丙申", "丙戌", "丙子", "丙寅"],
    "兑": ["丁巳", "丁卯", "丁丑", "丁亥", "丁酉", "丁未"],
}

# 六亲关系
LIUQIN_MAP = {
    "金": {"金": "兄弟", "木": "妻财", "水": "子孙", "火": "官鬼", "土": "父母"},
    "木": {"金": "官鬼", "木": "兄弟", "水": "父母", "火": "子孙", "土": "妻财"},
    "水": {"金": "父母", "木": "子孙", "水": "兄弟", "火": "妻财", "土": "官鬼"},
    "火": {"金": "妻财", "木": "父母", "水": "官鬼", "火": "兄弟", "土": "子孙"},
    "土": {"金": "子孙", "木": "官鬼", "水": "妻财", "火": "父母", "土": "兄弟"},
}

# 世应表 (八宫六十四卦 → 世爻位置、应爻位置)
# 位置从1开始(初爻=1, 上爻=6)
SHIYAO_TABLE = {
    # 乾宫
    "乾为天": (6, 3), "天风姤": (1, 4), "天山遁": (2, 5), "天地否": (3, 6),
    "风地观": (4, 1), "山地剥": (5, 2), "火地晋": (4, 1), "火天大有": (5, 2),
    # 坤宫
    "坤为地": (6, 3), "地雷复": (1, 4), "地泽临": (2, 5), "地天泰": (3, 6),
    "雷天大壮": (4, 1), "泽天夬": (5, 2), "水天需": (4, 1), "水地比": (5, 2),
    # 震宫
    "震为雷": (6, 3), "雷地豫": (1, 4), "雷水解": (2, 5), "雷风恒": (3, 6),
    "地风升": (4, 1), "水风井": (5, 2), "泽风大过": (4, 1), "泽雷随": (5, 2),
    # 巽宫
    "巽为风": (6, 3), "风天小畜": (1, 4), "风火家人": (2, 5), "风雷益": (3, 6),
    "天雷无妄": (4, 1), "火雷噬嗑": (5, 2), "山雷颐": (4, 1), "山风蛊": (5, 2),
    # 坎宫
    "坎为水": (6, 3), "水泽节": (1, 4), "水雷屯": (2, 5), "水火既济": (3, 6),
    "泽火革": (4, 1), "雷火丰": (5, 2), "地火明夷": (4, 1), "地水师": (5, 2),
    # 离宫
    "离为火": (6, 3), "火山旅": (1, 4), "火风鼎": (2, 5), "火水未济": (3, 6),
    "山水蒙": (4, 1), "风水涣": (5, 2), "天水讼": (4, 1), "天火同人": (5, 2),
    # 艮宫
    "艮为山": (6, 3), "山火贲": (1, 4), "山天大畜": (2, 5), "山泽损": (3, 6),
    "火泽睽": (4, 1), "天泽履": (5, 2), "风泽中孚": (4, 1), "风山渐": (5, 2),
    # 兑宫
    "兑为泽": (6, 3), "泽水困": (1, 4), "泽地萃": (2, 5), "泽山咸": (3, 6),
    "水山蹇": (4, 1), "地山谦": (5, 2), "雷山小过": (4, 1), "雷泽归妹": (5, 2),
}


# ============================================================
# 核心计算函数
# ============================================================

def toss_coins() -> int:
    """
    模拟三枚铜钱投掷一次
    正面=3, 反面=2
    三个正面(9) = 老阳 (阳变爻)
    两正一反(7) = 少阳 (阳不变)
    一正两反(8) = 少阴 (阴不变)
    三个反面(6) = 老阴 (阴变爻)
    """
    coins = [random.choice([2, 3]) for _ in range(3)]
    return sum(coins)


def generate_yao_lines(method: str = "random", manual_yao: list[int] = None) -> list[dict]:
    """
    生成六爻 (从初爻到上爻)

    Returns:
        list of dict: [{"value": 7/8/9/6, "yinyang": 1/0, "changing": True/False}, ...]
    """
    if method == "manual" and manual_yao and len(manual_yao) == 6:
        values = manual_yao
    else:
        values = [toss_coins() for _ in range(6)]

    lines = []
    for v in values:
        if v == 9:  # 老阳
            lines.append({"value": v, "yinyang": 1, "changing": True})
        elif v == 7:  # 少阳
            lines.append({"value": v, "yinyang": 1, "changing": False})
        elif v == 8:  # 少阴
            lines.append({"value": v, "yinyang": 0, "changing": False})
        elif v == 6:  # 老阴
            lines.append({"value": v, "yinyang": 0, "changing": True})

    return lines


def get_bagua_from_yao(yao1: int, yao2: int, yao3: int) -> str:
    """三爻取卦"""
    key = (yao1, yao2, yao3)
    return BAGUA.get(key, "乾")


def get_gua_name(upper: str, lower: str) -> str:
    """获取六十四卦名"""
    key = (upper, lower)
    gua_info = GUA_64.get(key)
    if gua_info:
        return gua_info[0]
    return f"{upper}{lower}卦"


def calculate_bian_gua(yao_lines: list[dict]) -> list[dict]:
    """计算变卦 (变爻反转)"""
    bian_lines = []
    for line in yao_lines:
        if line["changing"]:
            bian_lines.append({
                "value": 8 if line["yinyang"] == 1 else 9,
                "yinyang": 1 - line["yinyang"],
                "changing": False,
            })
        else:
            bian_lines.append(line.copy())
    return bian_lines


def get_najia(gua_name: str) -> list[str]:
    """获取纳甲"""
    return NAJIA_TABLE.get(gua_name, [""] * 6)


def get_liuqin(bagua_wuxing: str, najia_list: list[str]) -> list[str]:
    """计算六亲"""
    result = []
    for najia in najia_list:
        if not najia:
            result.append("")
            continue
        yao_wuxing = najia[0]  # 天干
        # 天干五行
        tg_wx = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
                 "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
        wx = tg_wx.get(yao_wuxing, "")
        qin = LIUQIN_MAP.get(bagua_wuxing, {}).get(wx, "")
        result.append(qin)
    return result


def calculate_liuyao(question: str, method: str = "random", manual_yao: list[int] = None) -> dict:
    """
    六爻完整起卦

    Args:
        question: 占卜问题
        method: 起卦方式 (random/manual)
        manual_yao: 手动输入六爻

    Returns:
        完整六爻卦象数据
    """
    # 生成六爻
    yao_lines = generate_yao_lines(method, manual_yao)

    # 本卦上下卦
    lower_gua = get_bagua_from_yao(yao_lines[0]["yinyang"], yao_lines[1]["yinyang"], yao_lines[2]["yinyang"])
    upper_gua = get_bagua_from_yao(yao_lines[3]["yinyang"], yao_lines[4]["yinyang"], yao_lines[5]["yinyang"])

    # 本卦名
    gua_name = get_gua_name(upper_gua, lower_gua)

    # 变卦
    bian_lines = calculate_bian_gua(yao_lines)
    bian_lower = get_bagua_from_yao(bian_lines[0]["yinyang"], bian_lines[1]["yinyang"], bian_lines[2]["yinyang"])
    bian_upper = get_bagua_from_yao(bian_lines[3]["yinyang"], bian_lines[4]["yinyang"], bian_lines[5]["yinyang"])
    bian_gua_name = get_gua_name(bian_upper, bian_lower)

    # 世应
    shi_yao, ying_yao = SHIYAO_TABLE.get(gua_name, (6, 3))

    # 纳甲 (本卦下卦和上卦)
    lower_najia = get_najia(lower_gua)
    upper_najia = get_najia(upper_gua)
    najia = lower_najia[:3] + upper_najia[3:]

    # 六亲 (以下卦五行为我)
    lower_wuxing = BAGUA_WUXING.get(lower_gua, "土")
    liu_qin = get_liuqin(lower_wuxing, najia)

    # 格式化本卦和变卦
    ben_gua = {
        "上卦": upper_gua,
        "下卦": lower_gua,
        "卦名": gua_name,
        "卦辞": GUA_64.get((upper_gua, lower_gua), ("", ""))[1],
    }

    bian_gua = {
        "上卦": bian_upper,
        "下卦": bian_lower,
        "卦名": bian_gua_name,
        "卦辞": GUA_64.get((bian_upper, bian_lower), ("", ""))[1],
    }

    # 格式化六爻数据
    yao_data = []
    for i in range(6):
        yao = yao_lines[i]
        yao_data.append({
            "爻位": i + 1,
            "阴阳": "阳" if yao["yinyang"] == 1 else "阴",
            "动变": yao["changing"],
            "数值": yao["value"],
            "纳甲": najia[i],
            "六亲": liu_qin[i],
            "是世爻": (i + 1) == shi_yao,
            "是应爻": (i + 1) == ying_yao,
        })

    return {
        "question": question,
        "yao_lines": yao_data,
        "ben_gua": ben_gua,
        "bian_gua": bian_gua,
        "gua_name": gua_name,
        "bian_gua_name": bian_gua_name,
        "shi_yao": shi_yao,
        "ying_yao": ying_yao,
        "liu_qin": liu_qin,
    }
