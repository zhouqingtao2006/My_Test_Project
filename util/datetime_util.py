import time


# 返回中文格式的日期：xxxx年xx月xx日
def get_chinese_date():
    set1 = time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday
    res = ""
    for idx, s in enumerate(set1):
        if len(str(s)) == 1:
            if idx == 0:
                res += "0" + str(s) + "年"
            elif idx == 1:
                res += "0" + str(s) + "月"
            else:
                res += "0" + str(s) + "日"
        else:
            if idx == 0:
                res += str(s) + "年"
            elif idx == 1:
                res += str(s) + "月"
            else:
                res += str(s) + "日"
    return "{}".format(res)


# 返回英文格式的日期：xxxx/xx/xx
def get_english_date():
    year, month, day = time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday
    if len(str(year)) == 1:
        year = "0" + str(year)
    if len(str(month)) == 1:
        month = "0" + str(month)
    if len(str(day)) == 1:
        day = "0" + str(day)
    return "{}/{}/{}".format(year, month, day)


# 返回中文格式的时间：xx时xx分xx秒
def get_chinese_time():
    hour, minute, second = time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
    if len(str(hour)) == 1:
        hour = "0" + str(hour)
    if len(str(minute)) == 1:
        minute = "0" + str(minute)
    if len(str(second)) == 1:
        second = "0" + str(second)
    return "{}时{}分{}秒".format(hour, minute, second)


# 返回英文格式的时间：xx:xx:xx
def get_english_time():
    hour, minute, second = time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
    if len(str(hour)) == 1:
        hour = "0" + str(hour)
    if len(str(minute)) == 1:
        minute = "0" + str(minute)
    if len(str(second)) == 1:
        second = "0" + str(second)
    return "{}:{}:{}".format(hour, minute, second)


# 返回中文格式的日期时间
def get_chinese_datetime():
    return get_chinese_date() + " " + get_chinese_time()


# 返回英文格式的日期时间
def get_english_datetime():
    return get_english_date() + " " + get_english_time()


# 返回时间戳
def get_timestamp():
    year, month, day = time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday
    hour, minute, second = time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
    if len(str(year)) == 1:
        year = "0" + str(year)
    if len(str(month)) == 1:
        month = "0" + str(month)
    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(hour)) == 1:
        hour = "0" + str(hour)
    if len(str(minute)) == 1:
        minute = "0" + str(minute)
    if len(str(second)) == 1:
        second = "0" + str(second)
    return "{}{}{}_{}{}{}".format(year, month, day, hour, minute, second)


if __name__ == "__main__":
    print(get_chinese_date())

    print(get_chinese_datetime())
    print(get_english_datetime())
    print(get_timestamp())
