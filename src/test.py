import pandas as pd

df = pd.read_csv('Báo cáo xác minh danh tính.csv', skiprows=2)
ma_khach_hang_list = df['Mã khách hàng'].tolist()
name_customer_list = df['Tài khoản'].tolist()

df = pd.read_csv('Báo cáo xác minh danh tính (1).csv', skiprows=2)
ma_khach_hang_list += df['Mã khách hàng'].tolist()
name_customer_list += df['Tài khoản'].tolist()

print(ma_khach_hang_list)
print(len(ma_khach_hang_list))
# print(name_customer_list)
