# 🍱 Food Calories Calculator & BMI Recommendation System

Ứng dụng web xây dựng bằng **Python + Streamlit** giúp người dùng:

- Nhập các thành phần món ăn
- Tính tổng lượng calories của bữa ăn
- Tính BMI cá nhân
- Ước lượng nhu cầu calories mỗi ngày
- So sánh calories món ăn với nhu cầu cơ thể
- Đưa ra đánh giá dinh dưỡng phù hợp

---

# Demo chức năng

## 1. Nhập thông tin cá nhân

Người dùng nhập:

- Giới tính
- Tuổi
- Chiều cao (cm)
- Cân nặng (kg)

Hệ thống sẽ tính:

- BMI
- Phân loại thể trạng:
  - Thiếu cân
  - Bình thường
  - Thừa cân
  - Béo phì

---

## 2. Nhập thành phần món ăn

Người dùng có thể:

- chọn tên thực phẩm
- nhập khối lượng (gram)
- thêm nhiều thành phần trong cùng một món ăn

Ví dụ:

- Cơm trắng — 200g
- Thịt bò — 150g
- Trứng — 50g

---

## 3. Tính calories

Hệ thống sử dụng mô hình hồi quy đã huấn luyện từ dữ liệu dinh dưỡng để tính:

```text
Calories = trọng số thực phẩm × khối lượng
```

Sau đó cộng tất cả để ra:

```text
Tổng calories của bữa ăn
```

---

## 4. So sánh với nhu cầu cơ thể

Dựa trên:

- giới tính
- tuổi
- chiều cao
- cân nặng

hệ thống ước tính lượng calories cần thiết trong ngày.

Sau đó so sánh với calories bữa ăn vừa nhập để đánh giá:

- Ăn nhẹ
- Phù hợp
- Hơi cao
- Quá nhiều calories

---

# Công nghệ sử dụng

- Python 3
- Streamlit
- Pandas
- Joblib
- Machine Learning Regression

---

# Cài đặt

## Clone project

```bash
git clone https://github.com/LamDoan1412/KHMT.git
```

---

## Tạo môi trường ảo

```bash
python -m venv .venv
```

---

## Kích hoạt môi trường ảo

### Windows

```bash
.\.venv\Scripts\activate
```

---


# Chạy chương trình

```bash
streamlit run app.py
```

Sau đó mở trình duyệt:

```text
http://localhost:8501
```

---

# Cấu trúc thư mục

```bash
KHMT/
│
├── app.py
├── train.py
├── model_weights.pkl
├── requirements.txt
└── README.md
```

---

# Ý tưởng phát triển thêm

Trong tương lai có thể mở rộng:

- gợi ý thực đơn giảm cân / tăng cân
- lưu lịch sử bữa ăn theo ngày
- biểu đồ calories theo tuần/tháng
- tính protein / carb / fat
- kết nối camera nhận diện món ăn bằng AI
- đề xuất khẩu phần phù hợp theo mục tiêu:
  - giảm cân
  - giữ cân
  - tăng cơ

---

# Tác giả

Sinh viên thực hiện: **Lâm Đoàn**

Môn học: **Khoa học máy tính / Python**