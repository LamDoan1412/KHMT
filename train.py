import streamlit as st
import joblib

# ===============================
# Cấu hình giao diện
# ===============================
st.set_page_config(
    page_title="Tính Calo & BMI",
    layout="centered"
)

# ===============================
# Load model
# ===============================
@st.cache_resource
def load_model():
    return joblib.load("vietnamese_popular_foods.pkl")


try:
    weights = load_model()
    food_options = sorted(list(weights.keys()))
except:
    st.error("Không tìm thấy file model_weights.pkl. Hãy chạy train.py trước.")
    st.stop()


# ===============================
# Hàm tính BMI
# ===============================
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return bmi


# ===============================
# Hàm tính BMR
# ===============================
def calculate_bmr(gender, weight, height_cm, age):
    if gender == "Nam":
        bmr = 10 * weight + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height_cm - 5 * age - 161
    return bmr


# ===============================
# Giao diện
# ===============================
st.title("🍱 Tính toán calo cho bữa ăn")

st.header("Thông tin cơ thể")

gender = st.selectbox(
    "Giới tính",
    ["Nam", "Nữ"]
)

age = st.number_input(
    "Tuổi",
    min_value=1,
    max_value=100,
    value=20
)

height = st.number_input(
    "Chiều cao (cm)",
    min_value=50.0,
    max_value=250.0,
    value=170.0
)

body_weight = st.number_input(
    "Cân nặng (kg)",
    min_value=10.0,
    max_value=300.0,
    value=60.0
)

# ===============================
# Tính BMI + BMR
# ===============================
bmi = calculate_bmi(body_weight, height)
bmr = calculate_bmr(gender, body_weight, height, age)

st.markdown(f"### BMI của bạn: `{bmi:.2f}`")

if bmi < 18.5:
    st.info("Bạn đang thiếu cân.")
elif bmi < 25:
    st.success("BMI bình thường.")
elif bmi < 30:
    st.warning("Bạn đang thừa cân.")
else:
    st.error("Bạn đang béo phì.")

st.markdown(f"### Nhu cầu calo gợi ý mỗi ngày: `{bmr:.0f} kcal`")

st.divider()


# ===============================
# Nhập món ăn
# ===============================
st.header("Nhập món ăn")

if "rows" not in st.session_state:
    st.session_state.rows = 1


current_entries = []

for i in range(st.session_state.rows):
    col1, col2 = st.columns([3, 1])

    with col1:
        food = st.selectbox(
            f"Thành phần {i+1}",
            food_options,
            key=f"food_{i}"
        )

    with col2:
        gram = st.number_input(
            f"Gram {i+1}",
            min_value=0.0,
            step=1.0,
            key=f"gram_{i}"
        )

    current_entries.append((food, gram))


if st.button("➕ Thêm thành phần"):
    st.session_state.rows += 1
    st.rerun()

st.divider()


# ===============================
# Tính calo món ăn
# ===============================
if st.button("TÍNH TOÁN", type="primary"):

    total_calories = 0

    st.subheader("Chi tiết món ăn")

    for food, gram in current_entries:
        if gram > 0:
            cal = weights[food] * gram
            total_calories += cal

            st.write(
                f"• **{food}** ({gram}g): {cal:.1f} kcal"
            )

    st.markdown(
        f"## Tổng calo bữa ăn: `{total_calories:.2f} kcal`"
    )

    st.divider()

    st.subheader("So sánh với nhu cầu cơ thể")

    percent = (total_calories / bmr) * 100

    st.write(
        f"Bữa ăn này tương đương **{percent:.1f}%** nhu cầu calo/ngày của bạn."
    )

    if percent < 20:
        st.info(
            "🟢 Bữa ăn nhẹ, lượng calo thấp."
        )

    elif percent < 35:
        st.success(
            "🔵 Lượng calo phù hợp cho một bữa ăn."
        )

    elif percent < 50:
        st.warning(
            "🟡 Bữa ăn hơi nhiều calo."
        )

    else:
        st.error(
            "🔴 Bữa ăn khá cao calo, nên cân nhắc điều chỉnh khẩu phần."
        )