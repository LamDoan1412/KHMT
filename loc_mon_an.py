import pickle
import sys

# Thiết lập encoding UTF-8 cho Windows Console
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# 1. Định nghĩa danh sách các món ăn Việt Nam & món ăn cực kỳ phổ biến tại Việt Nam từ dữ liệu gốc
vietnamese_foods = [
    # Rau củ quả, gia vị quen thuộc
    "Măng tây", "cà tím", "bông cải xanh", "Bắp cải", "ớt", "cà rốt", "Súp lơ", "cần tây", "củ cải",
    "cà chua bi", "hẹ", "cải xanh", "ngô", "Bí xanh", "Quả dưa chuột", "Tỏi", "dưa chuột", "bầu",
    "Đậu xanh", "hành lá", "Su hào", "tỏi tây", "Rau xà lách", "nấm", "Củ hành", "khoai tây", "bí ngô",
    "Bắp cải đỏ", "Rau chân vịt", "bí", "khoai lang", "Cà chua", "củ cải xanh", "bí xanh",
    # Trái cây nhiệt đới và phổ biến
    "Quả táo", "Quả mơ", "quả bơ", "Chuối", "Cam máu", "dưa đỏ", "Anh đào", "quýt", "nho", "mãng cầu",
    "mít", "Chanh vàng", "Chanh xanh", "Vải thiều", "Quả quýt", "Quả xoài", "Quả cam", "đu đủ",
    "Quả đào", "Quả lê", "Quả hồng", "Quả dứa", "chuối", "mận", "Lựu", "nho khô", "chôm chôm", "Khế",
    "dâu tây", "me", "dưa hấu", "thanh long", "sầu riêng", "quất", "măng cụt", "dưa lưới", "bưởi hồng", "bưởi",
    "mãng cầu xiêm",
    # Món ăn cơm hàng ngày, món nước & thức ăn nhanh phổ biến tại VN
    "Thịt xông khói và trứng", "Đậu nướng", "thịt bò hầm", "gạo đen", "Gạo lứt", "gà bơ", "cơm chiên",
    "Tôm chiên", "Sandwich phô mai nướng", "khoai tây nghiền", "bánh mì thịt", "Gà Cam", "cơm thập cẩm",
    "Vịt quay Bắc Kinh", "pizza", "Sườn heo", "Salad khoai tây", "Ramen", "Thịt bò nướng", "cuộn xúc xích",
    "chả giò", "Nem rán", "taco", "Gà Tandoori", "gà cốm", "gà viên", "Sandwich gà", "Cánh gà", "khoai tây chiên",
    "bánh mì kẹp thịt", "xúc xích",
    # Các loại bột, mì, bún, miến
    "Bột ngô", "bột bắp", "bánh quy giòn", "hạt hướng dương", "bánh ngô", "Bánh Tortilla", "Mầm lúa mì",
    "Lúa mì nguyên hạt", "Yến mạch nguyên hạt",
    "mì trứng", "miến", "mì ống", "mì spaghetti", "Bún", "mì ngũ cốc nguyên hạt", "Spaghetti nguyên hạt",
    # Nước dùng, súp, canh quen thuộc
    "Nước dùng thịt bò", "Bún bò", "Súp Bò", "nước dùng", "Súp bông cải xanh", "Súp cà rốt", "nước luộc gà", "Bún gà",
    "Nước dùng gà", "Súp rau gà", "Súp cơm gà", "Súp kem gà", "Súp kem nấm", "Phở gà kem", "Ramen ăn liền",
    "Súp thịt viên",
    "bún nước lèo", "Súp đuôi bò", "Súp khoai tây", "Súp bí ngô", "Súp cà chua", "Nước luộc rau", "Súp rau",
    "Nước kho rau củ",
    # Kem món tráng miệng
    "Kem sô-cô-la chip", "Kem sô cô la", "Kem cà phê", "Kem đá lạnh", "Kem Vani", "Kem Dâu", "Sundae dâu", "Sundae",
    "nón vani"
]

file_in = "model_weights.pkl"
file_out = "vietnamese_popular_foods.pkl"

print("Đang tiến hành đọc và lọc tệp dữ liệu...")

try:
    # 2. Mở file pickle gốc
    with open(file_in, 'rb') as f:
        data = pickle.load(f)

    # Đưa danh sách thực phẩm Việt Nam về chữ thường để khớp không phân biệt hoa thường
    vietnamese_foods_lower = {f.lower().strip() for f in vietnamese_foods}

    # 3. Kiểm tra cấu trúc của dữ liệu bên trong để áp dụng thuật toán lọc chính xác
    if isinstance(data, dict):
        # Nếu là Dictionary (Từ điển chứa dạng Tên_Món: Trọng_Số)
        filtered_data = {k: v for k, v in data.items() if k.lower().strip() in vietnamese_foods_lower}

    elif isinstance(data, list):
        # Nếu là List (Danh sách chứa các phần tử món ăn hoặc tuple)
        if len(data) > 0 and isinstance(data[0], tuple):
            # Dạng danh sách các tuple [(Tên_Món, Trọng_Số), ...]
            filtered_data = [item for item in data if item[0].lower().strip() in vietnamese_foods_lower]
        else:
            # Dạng danh sách thuần tên món ăn ["Món 1", "Món 2", ...]
            filtered_data = [item for item in data if item.lower().strip() in vietnamese_foods_lower]

    else:
        # Trường hợp dữ liệu là mảng đặc biệt (Ví dụ Numpy array hoặc Object phức tạp)
        print("Cấu trúc dữ liệu lạ. Hệ thống sẽ thử lọc ép kiểu theo dạng chuỗi văn bản...")
        filtered_data = {}

    # 4. Ghi dữ liệu đã lọc thành file .pkl mới
    with open(file_out, 'wb') as f:
        pickle.dump(filtered_data, f)

    print("=" * 50)
    print(f"XỬ LÝ THÀNH CÔNG!")
    print(f"Đã xuất ra tệp mới: {file_out}")
    print(f"Số lượng phần tử món ăn phổ biến của người Việt giữ lại được: {len(filtered_data)}")
    print("=" * 50)

except FileNotFoundError:
    print(
        f"LỖI: Không tìm thấy tệp '{file_in}' ở thư mục hiện tại. Bạn hãy chắc chắn đã đặt file code này chung thư mục với tệp pkl.")
except Exception as e:
    print(f"ĐÃ XẢY RA LỖI TRONG QUÁ TRÌNH XỬ LÝ: {e}")