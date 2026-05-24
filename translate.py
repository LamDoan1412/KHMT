import pandas as pd
from deep_translator import GoogleTranslator
import time


def translate_full_dataset(file_path):
    # 1. Đọc dữ liệu gốc
    df = pd.read_csv(file_path)

    # 2. Lấy danh sách các món ăn duy nhất (để tiết kiệm thời gian dịch)
    unique_foods = df['Food'].unique().tolist()
    print(f"Bắt đầu dịch {len(unique_foods)} hạng mục thực phẩm...")

    # 3. Thực hiện dịch thuật tự động
    translator = GoogleTranslator(source='en', target='vi')
    translated_dict = {}

    for i, food in enumerate(unique_foods):
        try:
            translated_name = translator.translate(food)
            translated_dict[food] = translated_name

            # Hiển thị tiến độ
            if (i + 1) % 50 == 0:
                print(f"Đã hoàn thành: {i + 1}/{len(unique_foods)}")

            # Nghỉ một chút để tránh bị chặn bởi API
            time.sleep(0.1)
        except Exception as e:
            print(f"Lỗi tại dòng {food}: {e}")
            translated_dict[food] = food  # Nếu lỗi thì giữ nguyên tiếng Anh

    # 4. Áp dụng từ điển đã dịch vào DataFrame
    df['Food_VN'] = df['Food'].map(translated_dict)

    # 5. Lưu kết quả ra file mới
    df.to_csv('Food_Calories_Vietnamese.csv', index=False, encoding='utf-8-sig')
    print("--- Hoàn thành! Đã tạo file Food_Calories_Vietnamese.csv với đầy đủ 562 dòng. ---")


if __name__ == "__main__":
    translate_full_dataset('Food and Calories - Sheet1.csv')