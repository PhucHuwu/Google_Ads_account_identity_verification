# Công Cụ Xác Minh Danh Tính Google Ads

Công cụ tự động hóa quy trình xác minh danh tính cho nhiều tài khoản con Google Ads.

## Tính Năng

- Xác minh danh tính tự động cho nhiều tài khoản con Google Ads
- Hỗ trợ chạy đa luồng
- Giao diện người dùng thân thiện

## Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- Trình duyệt Google Chrome
- Các gói Python cần thiết (xem requirements.txt)

## Cài Đặt

1. Tải về hoặc clone repository này
2. Cài đặt các gói cần thiết:

```bash
pip install -r requirements.txt
```

## Hướng Dẫn Sử Dụng

**Vui lòng liên hệ trong thông tin liên hệ**

## Cấu Trúc Thư Mục

- `main.py`: File chương trình chính
- `config.py`: File cấu hình và XPath
- `click.py`: Tiện ích tự động click
- `requirements.txt`: Danh sách gói Python cần thiết
- `Account_id.csv`: Dữ liệu tài khoản MCC
- `bcxm.csv`: File báo cáo xác minh danh tính

## Lưu Ý

- Đảm bảo MCC có quyền truy cập vào các tài khoản Google Ads con
- Cập nhật Chrome thường xuyên
- Với danh sách nhiều tài khoản, nên sử dụng nhiều luồng

## Xử Lý Lỗi

- Công cụ có cơ chế thử lại cho các thao tác thông thường
- Các xác minh thất bại được ghi lại và có thể thử lại
- Tiến độ được tự động lưu

## Bảo Mật

- Không lưu trữ thông tin đăng nhập
- Yêu cầu đăng nhập thủ công để đảm bảo an toàn
- Mỗi luồng sử dụng một profile Chrome riêng biệt

## Tác Giả

- Phuc TranHuwu
