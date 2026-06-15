import pandas as pd
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import numpy as np


def train_model():
    print("=== Khởi động tiến trình xử lý dữ liệu và huấn luyện mô hình ===")

    # Đọc tệp dữ liệu sạch đã được nội địa hóa tiếng Việt
    try:
        df = pd.read_csv('Food and Calories - Sheet1.csv')
        print(f"-> Nạp thành công tệp dữ liệu thô: {len(df)} dòng bản ghi.")
    except FileNotFoundError:
        print("Lỗi hệ thống: Không tìm thấy tệp 'Food and Calories.csv'. Hãy kiểm tra lại đường dẫn.")
        return

    def extract_num(text, pattern):
        match = re.search(pattern, str(text))
        return float(match.group(1)) if match else None

    # Tạo trường Khối lượng (gram) và Số calo thực tế
    df['Weight_g'] = df['Serving'].apply(lambda x: extract_num(x, r'\((\d+\.?\d*)\s*g\)'))
    df['Calories_val'] = df['Calories'].apply(lambda x: extract_num(x, r'(\d+)'))

    # Tiến hành làm sạch dữ liệu, lọc bỏ giá trị khuyết thiếu hoặc sai lỗi
    df = df.dropna(subset=['Weight_g', 'Calories_val'])
    df = df[df['Weight_g'] > 0]
    print(f"-> Hoàn tất làm sạch dữ liệu. Số lượng mẫu đạt chuẩn giữ lại: {len(df)} dòng.")

    # Thực hiện chia tách dữ liệu thực nghiệm theo tỷ lệ chuẩn 80% huấn luyện và 20% kiểm thử
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    print(f"   Quy mô Tập huấn luyện (Training Set - 80%): {len(train_df)} mẫu.")
    print(f"   Quy mô Tập kiểm thử (Testing Set - 20%): {len(test_df)} mẫu.")

    # 4. Thực hiện thuật toán học trên Tập huấn luyện (80%) để xác định các trọng số
    # Tính toán lượng calo trên mỗi 1 gram của từng loại thực phẩm
    train_df['Cal_per_Gram'] = train_df['Calories_val'] / train_df['Weight_g']

    # Cấu trúc hóa kết quả thu được thành ma trận trọng số hồi quy dạng từ điển
    model_weights = pd.Series(train_df.Cal_per_Gram.values, index=train_df.Food_VN).to_dict()

    y_true = test_df['Calories_val'].values

    y_pred = test_df.apply(lambda row: model_weights.get(row['Food_VN'], 0) * row['Weight_g'], axis=1).values

    # Thực thi các phép tính thống kê toán học để lượng hóa sai số mô hình
    r2 = r2_score(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    # Xuất kết quả đánh giá chi tiết ra màn hình console của hệ thống
    print("KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH HỒI QUY TRÊN TẬP KIỂM THỬ:")
    print(f"  - Hệ số xác định (R2 Score)                 : {r2:.4f} (Xấp xỉ {r2 * 100:.1f}%)")
    print(f"  - Sai số tuyệt đối trung bình (MAE)        : {mae:.2f} kcal")
    print(f"  - Sai số bình phương trung bình căn (RMSE)  : {rmse:.2f} kcal")

    # 5. Đóng gói mô hình dưới dạng tệp tin bằng Joblib
    # Xuất ra tệp tin đồng bộ với file cấu hình app.py
    output_filename = 'vietnamese_popular_foods.pkl'
    joblib.dump(model_weights, output_filename)

    print(f"\n=== TIẾN TRÌNH HOÀN TẤT ===")
    print(f"Mô hình hồi quy đa biến đã được đóng gói thành công tại tệp: '{output_filename}'")
    print(f"Hệ thống đã lưu trữ sẵn sàng bộ hệ số năng lượng của {len(model_weights)} loại thực phẩm.")


if __name__ == "__main__":
    train_model()