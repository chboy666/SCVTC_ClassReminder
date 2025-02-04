def is_within_week_range(a: str, b: str) -> bool:
    """
    判断给定的周数a是否在任意一个周数范围b内。

    参数：
    a (str): 当前周数，格式为字符串形式的数字，例如'5'。
    b (str): 周数范围或单独的周数，多个范围用';'分隔，例如'1-2;7-9'或者'4;6;8'。

    返回：
    bool: 如果a在任意一个b范围内或等于b，则返回True；否则返回False。
    """
    # 将a转换成整数
    current_week = int(a)

    # 解析所有单独的条件（可能是单个周数或周数范围）
    conditions = b.split(';')

    for condition in conditions:
        if '-' in condition:  # 是范围
            start_week, end_week = map(int, condition.split('-'))
            if start_week <= current_week <= end_week:
                return True
        else:  # 是单独的周数
            if int(condition) == current_week:
                return True

    return False
def int_to_chinese(num):
    if not 0 <= num <= 9:
        raise ValueError("数字必须在0到9之间")
    chinese_numbers = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    return chinese_numbers[num]