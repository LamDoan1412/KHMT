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
    return joblib.load("model_weights.pkl")


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

# ===============================
# TƯ VẤN DINH DƯỠNG CÁ NHÂN
# ===============================
st.divider()
st.subheader("💡 Tư vấn dinh dưỡng cá nhân")

# calories còn lại
remaining = bmr - total_calories

# lời khuyên theo giới tính + tuổi
if gender == "Nam":
    if age < 18:
        age_advice = "Nam dưới 18 tuổi đang trong giai đoạn phát triển nên cần bổ sung đủ đạm, canxi và năng lượng."
    elif age <= 30:
        age_advice = "Nam từ 18–30 tuổi thường có nhu cầu năng lượng khá cao, nên duy trì chế độ ăn cân bằng và vận động thường xuyên."
    elif age <= 50:
        age_advice = "Nam trưởng thành nên cân đối giữa lượng calories nạp vào và vận động để giữ thể trạng ổn định."
    else:
        age_advice = "Nam trên 50 tuổi nên ưu tiên thực phẩm dễ tiêu, ít dầu mỡ và kiểm soát năng lượng nạp vào."

else:
    if age < 18:
        age_advice = "Nữ dưới 18 tuổi cần bổ sung đầy đủ dinh dưỡng để hỗ trợ phát triển thể chất."
    elif age <= 30:
        age_advice = "Nữ từ 18–30 tuổi nên duy trì chế độ ăn đủ chất, giàu sắt, protein và rau xanh."
    elif age <= 50:
        age_advice = "Nữ trưởng thành nên cân bằng dinh dưỡng và duy trì lượng calories phù hợp mỗi ngày."
    else:
        age_advice = "Nữ trên 50 tuổi nên ưu tiên thực phẩm ít chất béo, giàu chất xơ và canxi."

st.write(age_advice)

# BMI
if bmi < 18.5:
    st.info(
        "📌 BMI của bạn đang ở mức thiếu cân. Bạn có thể tăng khẩu phần ăn, bổ sung thêm protein, sữa, trứng hoặc các loại hạt."
    )

elif bmi < 25:
    st.success(
        "📌 BMI của bạn ở mức bình thường. Hãy tiếp tục duy trì chế độ ăn uống hiện tại."
    )

elif bmi < 30:
    st.warning(
        "📌 BMI của bạn đang ở mức thừa cân. Nên hạn chế đồ ngọt, thức ăn nhanh và tăng rau xanh."
    )

else:
    st.error(
        "📌 BMI đang ở mức cao. Bạn nên kiểm soát lượng calories và tăng cường vận động."
    )

# So sánh calories bữa ăn với nhu cầu trong ngày
if remaining > 0:
    st.success(
        f"🍽️ Sau bữa ăn này bạn còn khoảng {remaining:.0f} kcal có thể nạp thêm trong hôm nay."
    )

else:
    st.warning(
        f"⚠️ Bạn đã vượt khoảng {abs(remaining):.0f} kcal so với nhu cầu khuyến nghị trong ngày."
    )