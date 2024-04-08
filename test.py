

import datetime

def convert_nanoseconds_to_time(nanoseconds):
    # Tính số giây, phút, giờ, vv từ số nano giây
    total_seconds = nanoseconds / 1e9  # Chuyển đổi nano giây thành giây
    total_minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(total_minutes, 60)
    days, hours = divmod(hours, 24)

    # Tạo một đối tượng datetime từ số giây tính được
    start_date = datetime.datetime(1601, 1, 1)
    delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    result_date = start_date + delta

    return result_date

# Số nano giây cách ngày 1/1/1601
nano_seconds = 13355596338628280500

# Chuyển đổi thành thời gian
result_time = convert_nanoseconds_to_time(nano_seconds)

# Trích xuất các thành phần thời gian cụ thể
year = result_time.year
month = result_time.month
day = result_time.day
hour = result_time.hour
minute = result_time.minute
second = result_time.second

