import pandas as pd
import re
import sys

# Thiết lập encoding UTF-8 cho Windows Console để in tiếng Việt không lỗi
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


def filter_only_grams(input_file, output_file):
    print(f"=== Đang tiến hành lọc tệp: '{input_file}' ===")
    try:
        # Đọc file dữ liệu
        df = pd.read_csv(input_file)
        initial_count = len(df)
        print(f"-> Nạp thành công {initial_count} dòng dữ liệu gốc.")

        # Lọc các dòng có chứa trọng lượng là gram (g) trong Serving
        # Ví dụ: "(128 g)" hoặc "(2.5 g)"
        # Regex kiểm tra số đi kèm chữ 'g' nằm trong dấu ngoặc đơn
        pattern = r'\(\d+\.?\d*\s*g\)'
        mask_grams = df['Serving'].str.contains(pattern, regex=True, na=False)

        filtered_df = df[mask_grams]
        final_count = len(filtered_df)
        removed_count = initial_count - final_count

        # Ghi ra tệp mới với định dạng UTF-8 có BOM để Excel hiển thị tốt
        filtered_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"-> Lọc thành công: Giữ lại {final_count} dòng (đơn vị gam).")
        print(f"-> Đã loại bỏ {removed_count} dòng (chứa ml hoặc không có trọng lượng gram).")
        print(f"-> Tệp kết quả lưu tại: '{output_file}'")
        print("=== HOÀN TẤT TIẾN TRÌNH ===")

    except FileNotFoundError:
        print(f"Lỗi hệ thống: Không tìm thấy tệp đầu vào '{input_file}'. Hãy kiểm tra lại.")
    except Exception as e:
        print(f"Đã xảy ra lỗi ngoài ý muốn: {e}")


if __name__ == "__main__":
    filter_only_grams('DatasetGoc.csv', 'Food and Calories - OnlyGrams.csv')
