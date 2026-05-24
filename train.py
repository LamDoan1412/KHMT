import pandas as pd
import re
import joblib


def train_model():
    # 1. Đọc dữ liệu đã dịch của bạn
    df = pd.read_csv('Food_Calories_Vietnamese.csv')

    # 2. Hàm trích xuất số liệu từ chuỗi
    def extract_num(text, pattern):
        match = re.search(pattern, str(text))
        return float(match.group(1)) if match else None

    # Trích xuất trọng lượng (g) và Calo
    df['Weight_g'] = df['Serving'].apply(lambda x: extract_num(x, r'\((\d+\.?\d*)\s*g\)'))
    df['Calories_val'] = df['Calories'].apply(lambda x: extract_num(x, r'(\d+)'))

    # 3. Làm sạch: Loại bỏ dòng thiếu dữ liệu hoặc trọng lượng bằng 0
    df = df.dropna(subset=['Weight_g', 'Calories_val'])
    df = df[df['Weight_g'] > 0]

    # 4. Tính toán hệ số hồi quy (Calo/Gram) cho từng món
    # Đây chính là các trọng số beta trong phương trình hồi quy
    df['Cal_per_Gram'] = df['Calories_val'] / df['Weight_g']

    # 5. Lưu từ điển hệ số để ứng dụng tra cứu
    model_weights = pd.Series(df.Cal_per_Gram.values, index=df.Food_VN).to_dict()
    joblib.dump(model_weights, 'model_weights.pkl')

    print(f"Thành công! Đã huấn luyện hệ số cho {len(model_weights)} loại thực phẩm.")


if __name__ == "__main__":
    train_model()