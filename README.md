# Google Ads Identity Verification Tool

Công cụ tự động hóa quy trình xác minh danh tính cho nhiều tài khoản Google Ads con một cách hiệu quả và an toàn.

## Giới Thiệu

**Google Ads Identity Verification Tool** là một ứng dụng desktop được phát triển bằng Python với giao diện Tkinter, giúp tự động hóa quy trình xác minh danh tính cho hàng loạt tài khoản Google Ads con thông qua tài khoản MCC.

Công cụ được thiết kế để giải quyết vấn đề xác minh danh tính thủ công tốn thời gian và dễ sai sót, đặc biệt hữu ích cho các agency quản lý nhiều tài khoản Google Ads.

## Tính Năng Chính

### Xác Minh Tự Động

-   **Tự động xác minh danh tính** cho nhiều tài khoản Google Ads con
-   **Xử lý 3 loại nhiệm vụ xác minh**:
    -   Task 1: Câu hỏi về quảng cáo chính trị
    -   Task 2: Xác minh thông tin tổ chức
    -   Task 3: Xác minh thông tin người thanh toán

### Hiệu Suất Cao

-   **Chạy đa luồng** - xử lý nhiều tài khoản đồng thời
-   **Tự động điều chỉnh số luồng** dựa trên số tài khoản được chọn
-   **Cơ chế thử lại thông minh** cho các thao tác thất bại

### Quản Lý Dữ Liệu

-   **Import/Export dữ liệu** từ file CSV
-   **Theo dõi tiến độ** xác minh real-time
-   **Lưu trữ trạng thái** tự động, không mất dữ liệu khi tắt ứng dụng
-   **Báo cáo chi tiết** về kết quả xác minh

### Giao Diện Thân Thiện

-   **Giao diện trực quan** với 3 tab chính:
    -   Tab Quản lý MCC: Thêm/xóa tài khoản MCC
    -   Tab Dữ liệu xác minh: Xem và quản lý dữ liệu xác minh
    -   Tab Thực thi: Điều khiển quá trình xác minh
-   **Thu gọn/mở rộng** cửa sổ ứng dụng
-   **Log màu sắc** để dễ theo dõi trạng thái

### Bảo Mật & An Toàn

-   **Không lưu trữ thông tin đăng nhập**
-   **Yêu cầu đăng nhập thủ công** để đảm bảo an toàn
-   **Mỗi luồng sử dụng profile Chrome riêng biệt**
-   **Tự động đóng các Chrome driver** khi khởi động

## Yêu Cầu Hệ Thống

-   **Python 3.8** trở lên
-   **Google Chrome** (phiên bản mới nhất)
-   **Windows 10/11** (được tối ưu hóa cho Windows)
-   **RAM**: Tối thiểu 4GB (khuyến nghị 8GB+)
-   **Ổ cứng**: Tối thiểu 1GB trống

## Cài Đặt

**Liên hệ ở thông tin liên hệ để được hướng dẫn cài đặt chi tiết**

## Hướng Dẫn Sử Dụng

**Liên hệ ở thông tin liên hệ để được hướng dẫn sử dụng chi tiết**

## Cấu Trúc Dự Án

```
Google_Ads_account_identity_verification/
├── main.py                          # Điểm khởi đầu chương trình
├── config.py                        # Cấu hình XPath và các hằng số
├── click.py                         # Tiện ích tự động click
├── requirements.txt                 # Danh sách thư viện Python
├── Account_id.csv                  # Dữ liệu tài khoản MCC
├── bcxm.csv                        # File báo cáo xác minh danh tính
├── app/                            # Module ứng dụng chính
│   ├── google_ads_app.py          # Class ứng dụng chính
│   ├── app_initializer.py         # Khởi tạo ứng dụng
│   └── thread_manager.py           # Quản lý luồng
├── browser/                        # Module xử lý trình duyệt
│   ├── driver_manager.py          # Quản lý Chrome driver
│   ├── verification_processor.py  # Xử lý quy trình xác minh
│   └── task_handlers.py           # Xử lý các nhiệm vụ cụ thể
├── data/                           # Module quản lý dữ liệu
│   ├── account_manager.py         # Quản lý tài khoản MCC
│   ├── file_handler.py            # Xử lý file CSV
│   └── verification_manager.py    # Quản lý dữ liệu xác minh
├── ui/                             # Module giao diện người dùng
│   ├── widget_creator.py          # Tạo các widget
│   ├── tab_setup.py               # Thiết lập các tab
│   ├── table_managers.py          # Quản lý bảng dữ liệu
│   ├── event_handlers.py          # Xử lý sự kiện
│   └── status_updater.py          # Cập nhật trạng thái
└── utils/                          # Module tiện ích
    ├── chrome_manager.py          # Quản lý Chrome
    ├── logging.py                 # Hệ thống log
    └── validation.py              # Xác thực dữ liệu
```

## Tính Năng Kỹ Thuật

### Xử Lý Đa Luồng

-   Sử dụng `threading` để chạy song song nhiều tài khoản
-   Thread-safe với `threading.Lock()` cho việc truy cập dữ liệu
-   Tự động điều chỉnh số luồng dựa trên số tài khoản

### Tự Động Hóa Trình Duyệt

-   Sử dụng `undetected-chromedriver` để tránh phát hiện bot
-   Tự động tìm và click các element bằng XPath
-   Cơ chế retry thông minh với timeout linh hoạt

### Quản Lý Dữ Liệu

-   Sử dụng `pandas` để xử lý dữ liệu CSV
-   Tự động backup và khôi phục dữ liệu
-   Validation dữ liệu đầu vào

## Lưu Ý Quan Trọng

### Trước Khi Sử Dụng

-   **Đảm bảo MCC có quyền truy cập** vào tất cả tài khoản Google Ads con
-   **Cập nhật Chrome** lên phiên bản mới nhất
-   **Kiểm tra kết nối internet** ổn định
-   **Đóng các ứng dụng khác** sử dụng Chrome để tránh xung đột

### Trong Quá Trình Sử Dụng

-   **Không tắt ứng dụng** khi đang chạy xác minh
-   **Theo dõi log** để phát hiện lỗi sớm
-   **Đăng nhập thủ công** khi được yêu cầu
-   **Không sử dụng máy tính** cho các tác vụ khác khi đang chạy

### Sau Khi Hoàn Thành

-   **Kiểm tra kết quả** trong file bcxm.csv
-   **Backup dữ liệu** quan trọng
-   **Đóng ứng dụng** đúng cách

## Xử Lý Lỗi Thường Gặp

### Lỗi Khởi Động Chrome

-   Kiểm tra Chrome đã được cài đặt
-   Cập nhật Chrome lên phiên bản mới nhất
-   Đóng tất cả Chrome đang chạy

### Lỗi Không Tìm Thấy Element

-   Kiểm tra kết nối internet
-   Đảm bảo đã đăng nhập Google Ads
-   Thử lại với timeout dài hơn

### Lỗi Xác Minh Thất Bại

-   Kiểm tra quyền truy cập MCC
-   Xác minh thông tin tài khoản
-   Thử lại với số luồng ít hơn

## Bảo Mật

-   **Không lưu trữ mật khẩu** hoặc thông tin nhạy cảm
-   **Yêu cầu đăng nhập thủ công** cho mỗi session
-   **Sử dụng profile Chrome riêng** cho mỗi luồng
-   **Tự động dọn dẹp** các file tạm thời

## Hiệu Suất

-   **Xử lý đồng thời** tối đa 10 tài khoản
-   **Thời gian xác minh** trung bình 2-3 phút/tài khoản
-   **Tỷ lệ thành công** >95% với cấu hình đúng
-   **Tự động retry** các thao tác thất bại

## Hỗ Trợ

**Liên hệ ở thông tin liên hệ để được hỗ trợ kỹ thuật**

## Tác Giả

**Phuc TranHuwu** - Developer & Maintainer

---

_Công cụ này được phát triển để hỗ trợ các agency và marketer trong việc quản lý nhiều tài khoản Google Ads một cách hiệu quả.
