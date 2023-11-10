from datetime import datetime

def convert_datetime(date_string, time_string):
    # 将日期字符串转换为 datetime 对象
    date_time_obj = datetime.strptime(date_string, "%d %B, %Y")

    # 将时间字符串转换为时间对象
    time_obj = datetime.strptime(time_string, "%I:%M %p")

    # 将时间对象的时间部分赋予日期对象
    date_time_obj = date_time_obj.replace(hour=time_obj.hour, minute=time_obj.minute)

    return date_time_obj