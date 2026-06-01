import streamlit as st
import joblib

st.set_page_config(
    page_title="Tính Calo & BMI",
    page_icon="🍱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 860px;
    }
    .title-box {
        background: linear-gradient(135deg, #1f2937, #111827);
        padding: 1.4rem 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        margin-bottom: 1.2rem;
    }
    .title-box h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
    }
    .subtitle {
        color: #cbd5e1;
        margin-top: .35rem;
        font-size: .95rem;
    }
    .card {
        background: rgba(17,24,39,0.95);
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        margin-bottom: 1rem;
    }
    .section-title {
        color: #f8fafc;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: .8rem;
    }
    .small-text {
        color: #94a3b8;
        font-size: .9rem;
    }
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #0f172a !important;
        border-color: rgba(255,255,255,0.12) !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load("vietnamese_popular_foods.pkl")

try:
    weights = load_model()
    food_options = sorted(list(weights.keys()))
except:
    st.error("Không tìm thấy file model_weights.pkl. Hãy chạy train.py trước.")
    st.stop()

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def calculate_bmr(gender, weight, height_cm, age):
    if gender == "Nam":
        return 10 * weight + 6.25 * height_cm - 5 * age + 5
    return 10 * weight + 6.25 * height_cm - 5 * age - 161

st.markdown("""
<div class="title-box">
    <h1>🍱 Tính toán calo cho bữa ăn</h1>
    <div class="subtitle">Ước tính BMI, BMR và calo bữa ăn theo nguyên liệu bạn nhập</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Thông tin cơ thể</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
    age = st.number_input("Tuổi", min_value=1, max_value=100, value=20)
with col2:
    height = st.number_input("Chiều cao (cm)", min_value=50.0, max_value=250.0, value=170.0)
    body_weight = st.number_input("Cân nặng (kg)", min_value=10.0, max_value=300.0, value=60.0)

bmi = calculate_bmi(body_weight, height)
bmr = calculate_bmr(gender, body_weight, height, age)

m1, m2 = st.columns(2)
m1.metric("BMI", f"{bmi:.2f}")
m2.metric("BMR", f"{bmr:.0f} kcal/ngày")

if bmi < 18.5:
    st.info("Bạn đang thiếu cân.")
elif bmi < 25:
    st.success("BMI bình thường.")
elif bmi < 30:
    st.warning("Bạn đang thừa cân.")
else:
    st.error("Bạn đang béo phì.")

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Nhập món ăn</div>', unsafe_allow_html=True)

if "rows" not in st.session_state:
    st.session_state.rows = 1

current_entries = []

for i in range(st.session_state.rows):
    c1, c2 = st.columns([3, 1])
    with c1:
        food = st.selectbox(f"Thành phần {i+1}", food_options, key=f"food_{i}")
    with c2:
        gram = st.number_input(f"Gram {i+1}", min_value=0.0, step=1.0, key=f"gram_{i}")
    current_entries.append((food, gram))

b1, b2 = st.columns([1, 3])
with b1:
    if st.button("➕ Thêm", use_container_width=True):
        st.session_state.rows += 1
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

if st.button("TÍNH TOÁN", type="primary", use_container_width=True):
    total_calories = 0
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Kết quả bữa ăn</div>', unsafe_allow_html=True)

    for food, gram in current_entries:
        if gram > 0:
            cal = weights[food] * gram
            total_calories += cal
            st.write(f"• **{food}** ({gram}g): {cal:.1f} kcal")

    remaining = bmr - total_calories
    percent = (total_calories / bmr) * 100 if bmr > 0 else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Tổng calo", f"{total_calories:.1f} kcal")
    c2.metric("So với nhu cầu", f"{percent:.1f}%")
    c3.metric("Còn lại", f"{remaining:.0f} kcal")

    if percent < 20:
        st.info("Bữa ăn nhẹ, lượng calo thấp.")
    elif percent < 35:
        st.success("Lượng calo phù hợp cho một bữa ăn.")
    elif percent < 50:
        st.warning("Bữa ăn hơi nhiều calo.")
    else:
        st.error("Bữa ăn khá cao calo, nên cân nhắc điều chỉnh khẩu phần.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Tư vấn dinh dưỡng cá nhân</div>', unsafe_allow_html=True)

if gender == "Nam":
    if age < 18:
        age_advice = "Nam dưới 18 tuổi nên ưu tiên đạm, canxi và năng lượng."
    elif age <= 30:
        age_advice = "Nam 18–30 tuổi thường cần năng lượng cao, nên ăn cân bằng và vận động đều."
    elif age <= 50:
        age_advice = "Nam trưởng thành nên cân đối calo và vận động để giữ thể trạng."
    else:
        age_advice = "Nam trên 50 tuổi nên ưu tiên thực phẩm dễ tiêu và ít dầu mỡ."
else:
    if age < 18:
        age_advice = "Nữ dưới 18 tuổi cần đủ dinh dưỡng để phát triển thể chất."
    elif age <= 30:
        age_advice = "Nữ 18–30 tuổi nên ăn đủ chất, giàu sắt, protein và rau xanh."
    elif age <= 50:
        age_advice = "Nữ trưởng thành nên cân bằng dinh dưỡng và duy trì lượng calo phù hợp."
    else:
        age_advice = "Nữ trên 50 tuổi nên ưu tiên thực phẩm ít béo, nhiều chất xơ và canxi."

st.write(age_advice)

if bmi < 18.5:
    st.info("Bạn đang thiếu cân, có thể tăng khẩu phần và bổ sung đạm.")
elif bmi < 25:
    st.success("BMI của bạn ở mức tốt, hãy duy trì thói quen hiện tại.")
elif bmi < 30:
    st.warning("Bạn đang thừa cân, nên giảm đồ ngọt và tăng rau xanh.")
else:
    st.error("Bạn nên kiểm soát calories và tăng vận động.")

st.markdown('</div>', unsafe_allow_html=True)