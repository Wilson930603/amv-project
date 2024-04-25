Yêu cầu:
1. Python >= 3.8 : Cài đặt từ đây: https://www.python.org/downloads/
2. scrapy: pip install scrapy
3. selenium: pip install webdriver-manager
4. Firefox version 105.0
5. openpyxl: pip install openpyxl

Cấu hình:
Thông tin tài khoản glassdoor trong file settings.py (dòng 11, 12):
GLASSDOOR_USER='?????'
GLASSDOOR_PASSWORD='xxxxxx'

Chạy spider:
1. Đặt tất cả các url muốn crawl trong file urls.txt, mỗi url một dòng (không nên để dòng trống)
2. Chuyển đến thư mục hiện hành có chứa file scrapy.cfg
3. Chạy lệnh: scrapy crawl glassdoor_reviews
4. Chờ crawl chạy và nhận kết quả trong thư mục ./Data

Chúc thành công