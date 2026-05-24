import streamlit as st
import joblib
import pandas as pd

# Cấu hình giao diện
st.set_page_config(page_title="Dự đoán Calo Đa Thành Phần", layout="centered")


# Tải mô hình (hệ số hồi quy)
@st.cache_resource
def load_model():
    return joblib.load('model_weights.pkl')


try:
    weights = load_model()
    food_options = sorted(list(weights.keys()))
except:
    st.error("Chưa tìm thấy file 'model_weights.pkl'. Hãy chạy file train.py trước!")
    st.stop()

st.title("Tính toán calo cho bữa ăn của bạn")
st.write("Chọn các thành phần trong món ăn của bạn và nhập định lượng tương ứng.")

# Quản lý số lượng hàng nhập liệu bằng Session State
if 'rows' not in st.session_state:
    st.session_state.rows = 1

# Tạo các hàng nhập liệu
current_entries = []
for i in range(st.session_state.rows):
    col1, col2 = st.columns([3, 1])
    with col1:
        food = st.selectbox(f"Thành phần {i + 1}", food_options, key=f"food_{i}")
    with col2:
        weight = st.number_input(f"Lượng (gram)", min_value=0.0, step=1.0, key=f"weight_{i}")
    current_entries.append((food, weight))

# Nút thêm hàng (+)
if st.button("➕ Thêm thành phần"):
    st.session_state.rows += 1
    st.rerun()

st.divider()

# Nút tính toán
if st.button("TÍNH TOÁN CALO", type="primary"):
    total_calories = 0
    st.subheader("Chi tiết năng lượng:")

    for food, w in current_entries:
        if w > 0:
            # Áp dụng công thức hồi quy: Calo = Trọng số * Khối lượng
            cal = weights[food] * w
            total_calories += cal
            st.write(f"• **{food}** ({w}g): {cal:.1f} kcal")

    st.markdown(f"## Tổng cộng: `{total_calories:.2f}` kcal")

    # Đánh giá dinh dưỡng chuyên sâu
    st.subheader("Đánh giá từ hệ thống:")
    if total_calories == 0:
        st.info("Vui lòng nhập định lượng để xem đánh giá.")
    elif total_calories < 250:
        st.success("🟢 Đây là một khẩu phần ăn nhẹ hoặc ăn kiêng rất tốt.")
    elif 250 <= total_calories <= 600:
        st.success("🔵 Lượng calo tiêu chuẩn cho một bữa ăn chính cân bằng.")
    elif 600 < total_calories <= 900:
        st.warning("🟡 Lượng calo hơi cao. Phù hợp cho người vận động mạnh.")
    else:
        st.error("🔴 Lượng calo rất cao. Hãy cân nhắc điều chỉnh định lượng nếu bạn đang giảm cân.")