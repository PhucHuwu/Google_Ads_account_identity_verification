"""
Google Ads Verification Tool - Main Entry Point
Refactored version with modular structure
"""

import tkinter as tk
from app import GoogleAdsVerificationApp


def main():
    """
    Điểm bắt đầu chương trình, khởi tạo và chạy ứng dụng Tkinter.
    """
    # Khởi tạo root window
    root = tk.Tk()

    # Tạo instance ứng dụng
    app = GoogleAdsVerificationApp(root)

    # Chạy main loop
    root.mainloop()


if __name__ == "__main__":
    main()
