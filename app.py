import streamlit as st
import joblib

st.set_page_config(
    page_title="Tính Calo & BMI Dinh Dưỡng",
    page_icon="🍱",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Nhúng mã CSS để tùy biến giao diện cao cấp (Glassmorphism & Dark Mode)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Thiết lập font và nền động */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #0b0f19 !important;
        background-image: radial-gradient(at 0% 0%, rgba(30, 27, 75, 0.4) 0, transparent 50%), 
                          radial-gradient(at 50% 0%, rgba(17, 24, 39, 0.4) 0, transparent 50%),
                          radial-gradient(at 100% 0%, rgba(76, 29, 149, 0.2) 0, transparent 50%) !important;
        background-attachment: fixed !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 820px !important;
    }
    
    /* Khung tiêu đề chính */
    .title-box {
        background: linear-gradient(135deg, rgba(20, 30, 50, 0.6) 0%, rgba(10, 15, 30, 0.8) 100%);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .title-box h1 {
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(135deg, #a78bfa 0%, #ec4899 50%, #f43f5e 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 2.3rem !important;
        margin: 0 !important;
    }
    
    .subtitle {
        color: #94a3b8;
        margin-top: 0.5rem;
        font-size: 1rem;
        font-weight: 500;
    }
    
    /* Tùy biến các khung container biên thành dạng Card cao cấp */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(17, 24, 39, 0.5) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
        margin-bottom: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(167, 139, 250, 0.2) !important;
        box-shadow: 0 12px 35px rgba(167, 139, 250, 0.05) !important;
    }
    
    /* Thiết kế tiêu đề mục con */
    .section-title {
        color: #f8fafc;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1.2rem;
        border-left: 4px solid #a78bfa;
        padding-left: 0.75rem;
        line-height: 1.2;
    }
    
    /* Làm đẹp các khối chỉ số metrics */
    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.6) !important;
        padding: 0.8rem 1.2rem !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
    }
    
    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
    }
    
    /* Cải tiến các nút bấm */
    button[data-testid="stBaseButton-secondary"], button[data-testid="stBaseButton-primary"] {
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1.2rem !important;
        transition: all 0.2s ease !important;
    }
    
    button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(135deg, #7c3aed 0%, #db2777 100%) !important;
        border: none !important;
        color: white !important;
    }
    
    button[data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4) !important;
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
    st.error("Không tìm thấy file vietnamese_popular_foods.pkl. Hãy chạy train.py và loc_mon_an.py trước.")
    st.stop()

def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return weight / (height_m ** 2)

def calculate_bmr(gender, weight, height_cm, age):
    if gender == "Nam":
        return 10 * weight + 6.25 * height_cm - 5 * age + 5
    return 10 * weight + 6.25 * height_cm - 5 * age - 161

# Khung tiêu đề chính
st.markdown("""
<div class="title-box">
    <h1>🍱 Tính Toán Dinh Dưỡng & Calo</h1>
    <div class="subtitle">Hệ thống phân tích BMI, nhu cầu BMR và lập kế hoạch bữa ăn thông minh</div>
</div>
""", unsafe_allow_html=True)

# 1. Khung thông tin cá nhân
with st.container(border=True):
    st.markdown('<div class="section-title">Thông Tin Cơ Thể</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Giới tính", ["Nam", "Nữ"])
        age = st.number_input("Tuổi", min_value=1, max_value=100, value=20)
    with col2:
        height = st.number_input("Chiều cao (cm)", min_value=50.0, max_value=250.0, value=170.0)
        body_weight = st.number_input("Cân nặng (kg)", min_value=10.0, max_value=300.0, value=60.0)
    
    bmi = calculate_bmi(body_weight, height)
    bmr = calculate_bmr(gender, body_weight, height, age)
    
    st.write("")
    m1, m2 = st.columns(2)
    m1.metric("Chỉ số BMI", f"{bmi:.2f}")
    m2.metric("Nhu cầu BMR cơ bản", f"{bmr:.0f} kcal/ngày")
    
    if bmi < 18.5:
        st.info("Chỉ số BMI chỉ ra rằng bạn đang thiếu cân. Hãy tham khảo thêm tư vấn dinh dưỡng bên dưới.")
    elif bmi < 25:
        st.success("Chỉ số BMI của bạn đang ở mức lý tưởng (Bình thường). Hãy tiếp tục duy trì phong độ.")
    elif bmi < 30:
        st.warning("Chỉ số BMI chỉ ra rằng bạn đang thừa cân. Hãy chú ý kiểm soát năng lượng.")
    else:
        st.error("Chỉ số BMI báo động bạn đang béo phì. Cần có chế độ ăn kiêng và tập luyện khoa học.")

# 2. Khung nhập món ăn
with st.container(border=True):
    st.markdown('<div class="section-title">Lên Thực Đơn Bữa Ăn</div>', unsafe_allow_html=True)
    
    if "rows" not in st.session_state:
        st.session_state.rows = 1
        
    current_entries = []
    
    for i in range(st.session_state.rows):
        c1, c2 = st.columns([3, 1])
        with c1:
            food = st.selectbox(f"Thành phần {i+1}", food_options, key=f"food_{i}")
        with c2:
            gram = st.number_input(f"Gram {i+1}", min_value=0.0, step=10.0, value=100.0, key=f"gram_{i}")
        current_entries.append((food, gram))
        
    st.write("")
    b1, b2, b3 = st.columns([1, 1, 2])
    with b1:
        if st.button("➕ Thêm món", use_container_width=True):
            st.session_state.rows += 1
            st.rerun()
    with b2:
        if st.button("➖ Bớt món", use_container_width=True):
            if st.session_state.rows > 1:
                # Xóa dữ liệu rác để tránh tràn bộ nhớ session_state
                last_idx = st.session_state.rows - 1
                if f"food_{last_idx}" in st.session_state:
                    del st.session_state[f"food_{last_idx}"]
                if f"gram_{last_idx}" in st.session_state:
                    del st.session_state[f"gram_{last_idx}"]
                st.session_state.rows -= 1
                st.rerun()

# Khởi tạo trạng thái tính toán
if "calculated" not in st.session_state:
    st.session_state.calculated = False

# Nút bấm tính toán chính
if st.button("TÍNH TOÁN CALO BỮA ĂN", type="primary", use_container_width=True):
    st.session_state.calculated = True

# 3. Khung hiển thị kết quả tính calo
if st.session_state.calculated:
    with st.container(border=True):
        st.markdown('<div class="section-title">📊 Kết Quả Phân Tích Bữa Ăn</div>', unsafe_allow_html=True)
        
        total_calories = 0
        has_items = False
        
        for food, gram in current_entries:
            if gram > 0:
                cal = weights[food] * gram
                total_calories += cal
                st.markdown(f"🔹 **{food}** ({gram}g) $\\rightarrow$ `{cal:.1f}` kcal")
                has_items = True
                
        if not has_items:
            st.info("Vui lòng nhập khối lượng (gram) lớn hơn 0 để tính toán.")
            
        remaining = bmr - total_calories
        percent = (total_calories / bmr) * 100 if bmr > 0 else 0
        
        st.write("")
        c1, c2, c3 = st.columns(3)
        c1.metric("Tổng calo nạp vào", f"{total_calories:.1f} kcal")
        c2.metric("So với BMR ngày", f"{percent:.1f}%")
        c3.metric("Calo còn lại", f"{remaining:.0f} kcal")
        
        # Thanh tiến trình calo trực quan
        progress_val = min(percent / 100.0, 1.0)
        
        if percent < 20:
            st.info("Bữa ăn nhẹ, lượng calo tương đối thấp.")
            st.progress(progress_val, text=f"Mức nhẹ: {percent:.1f}% nhu cầu ngày")
        elif percent < 35:
            st.success("Lượng calo lý tưởng và phù hợp cho một bữa ăn chính.")
            st.progress(progress_val, text=f"Mức tốt: {percent:.1f}% nhu cầu ngày")
        elif percent < 50:
            st.warning("Bữa ăn chứa lượng calo hơi cao. Hãy vận động thêm.")
            st.progress(progress_val, text=f"Mức cao: {percent:.1f}% nhu cầu ngày")
        else:
            st.error("Bữa ăn quá nhiều calo, nên cân nhắc điều chỉnh khẩu phần.")
            st.progress(progress_val, text=f"Mức báo động: {percent:.1f}% nhu cầu ngày")
            
        st.write("")
        if st.button("🔄 Đặt lại / Xóa kết quả", use_container_width=True):
            st.session_state.calculated = False
            st.rerun()

# 4. Khung tư vấn dinh dưỡng cá nhân
with st.container(border=True):
    st.markdown('<div class="section-title">💡 Tư Vấn Dinh Dưỡng Cá Nhân Hóa</div>', unsafe_allow_html=True)
    
    col_adv1, col_adv2 = st.columns(2)
    with col_adv1:
        st.markdown("##### 👥 Theo độ tuổi & giới tính")
        if gender == "Nam":
            if age < 18:
                age_advice = "Nam dưới 18 tuổi nên ưu tiên protein, canxi và dinh dưỡng năng lượng cao để hỗ trợ phát triển chiều cao tối đa."
            elif age <= 30:
                age_advice = "Nam 18–30 tuổi có tốc độ trao đổi chất mạnh, nên duy trì chế độ ăn cân bằng kết hợp tập luyện thể chất."
            elif age <= 50:
                age_advice = "Nam trưởng thành nên kiểm soát tốt tinh bột xấu, tăng cường protein nách và tập trung duy trì cân nặng ổn định."
            else:
                age_advice = "Nam trên 50 tuổi nên ưu tiên thực phẩm mềm, dễ tiêu hóa, giảm lượng muối và hạn chế dầu mỡ để bảo vệ tim mạch."
        else:
            if age < 18:
                age_advice = "Nữ dưới 18 tuổi cần chú ý ăn uống đủ chất, đặc biệt là canxi và sắt để phát triển toàn diện thể trạng."
            elif age <= 30:
                age_advice = "Nữ 18–30 tuổi nên xây dựng thực đơn dồi dào chất xơ, vitamin, protein sạch và hạn chế các món ăn nhanh nhiều dầu mỡ."
            elif age <= 50:
                age_advice = "Nữ trưởng thành cần điều hòa lượng năng lượng, bổ sung nhiều chất chống oxy hóa từ trái cây để giữ vóc dáng."
            else:
                age_advice = "Nữ trên 50 tuổi nên bổ sung canxi ngừa loãng xương, ăn nhiều rau xanh, cá hồi và giảm đường trong thực đơn hàng ngày."
        st.info(age_advice)
        
    with col_adv2:
        st.markdown("##### ⚖️ Khuyến nghị theo chỉ số BMI")
        if bmi < 18.5:
            bmi_advice = "Bạn đang thiếu cân. Hãy chia nhỏ thành nhiều bữa ăn, bổ sung sữa, protein và tinh bột tốt để tăng cân lành mạnh."
        elif bmi < 25:
            bmi_advice = "Chỉ số cơ thể rất tuyệt vời! Hãy duy trì lối sống lành mạnh, uống đủ nước và tập thể dục tối thiểu 3 lần một tuần."
        elif bmi < 30:
            bmi_advice = "Bạn đang ở mức thừa cân. Nên giảm bớt đồ chiên rán, giảm đồ ngọt và nước có ga, ưu tiên các món hấp/luộc."
        else:
            bmi_advice = "Bạn đang béo phì. Nên thiết lập chế độ giảm calo thông minh, giảm khẩu phần ăn và tăng cường tập các bài cardio."
        st.info(bmi_advice)