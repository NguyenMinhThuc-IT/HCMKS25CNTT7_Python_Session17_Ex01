raw_logs = [] 
processed_logs = []

def get_validate_input(prompt: str) -> str:
    """Yêu cầu người dùng nhập dữ liệu từ bàn phím và bắt buộc không được để trống.

    Args:
        prompt (str): Câu lệnh hướng dẫn hiển thị ra màn hình cho người dùng.

    Returns:
        str: Chuỗi ký tự hợp lệ đã được loại bỏ khoảng trắng thừa ở hai đầu.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        print("Lỗi: Dữ liệu không hợp lệ, vui lòng không bỏ trống!")

def input_and_clean_logs() -> None:
    """Tiếp nhận chuỗi log thô, thực hiện tẩy sạch ký tự đặc biệt (!@#$) 
    và phân tách dữ liệu thành danh sách log bằng dấu chấm phẩy (;).
    """
    print("\n-------------------------------------------------")
    print("--- 1. NẠP VÀ LÀM SẠCH DỮ LIỆU LOG THÔ ---")
    print("-------------------------------------------------")
    
    raw_data = get_validate_input("Nhập chuỗi log thô (cách nhau bởi dấu ;): ")
    
    # 💡 Ứng dụng Bảng dịch chuyển (Translation Table) để loại bỏ ký tự đặc biệt
    remove_chars = "!@#$"
    trans_table = str.maketrans('', '', remove_chars)
    cleaned_data = raw_data.translate(trans_table)
    
    # Phân tách chuỗi phẳng thành mảng dữ liệu qua dấu phân tách ';'
    global raw_logs
    raw_logs = [log.strip() for log in cleaned_data.split(';') if log.strip()]
    
    print("\n=> THÀNH CÔNG: Hệ thống đã xử lý sạch dữ liệu.")
    print(f"=> Hiện đang lưu trữ: {len(raw_logs)} dòng log.")


def filter_high_level_logs() -> None:
    """Rà soát và trích xuất các dòng log chứa từ khóa nguy hiểm cấp độ cao 
    bao gồm 'ERROR' hoặc 'CRITICAL' bằng kỹ thuật List Comprehension.
    """
    print("\n-------------------------------------------------")
    print("--- 2. LỌC CẢNH BÁO MỨC ĐỘ CAO (ERROR/CRITICAL) ---")
    print("-------------------------------------------------")
    
    global raw_logs, processed_logs
    if not raw_logs:
        print("Cảnh báo: Chưa có dữ liệu log! Vui lòng thực hiện chức năng 1 trước.")
        return
    
    # 💡 Lọc thông minh không phân biệt hoa thường nhờ .lower()
    processed_logs = [log for log in raw_logs 
                      if "error" in log.lower() or "critical" in log.lower()]
                      
    if processed_logs:
        print(f"Tìm thấy {len(processed_logs)} cảnh báo nguy hiểm trong hệ thống:")
        for idx, log in enumerate(processed_logs, 1):
            print(f"  [{idx}] {log}")
    else:
        print("Kết quả: Hệ thống an toàn, không tìm thấy cảnh báo nguy hiểm.")


def mask_ip_in_logs() -> list:
    """Tìm kiếm tất cả các địa chỉ IPv4 (dạng X.X.X.X) xuất hiện trong log 
    và tiến hành ẩn danh (masking) 2 phân đoạn cuối cùng thành dạng X.X.*.*.

    Returns:
        list: Danh sách các chuỗi log an toàn đã được mã hóa IP thành công.
    """
    print("\n-------------------------------------------------")
    print("--- 3. MÃ HÓA ĐỊA CHỈ IP (MASKING) ---")
    print("-------------------------------------------------")
    
    global processed_logs
    if not processed_logs:
        print("Cảnh báo: Chưa có dữ liệu log cảnh báo! Vui lòng chạy chức năng 2.")
        return []
    
    masked_logs = []
    for log in processed_logs:
        words = log.split()
        new_words = []
        
        for w in words:
            # Thuật toán cô lập phần tử nghi vấn là IP
            if "." in w:
                parts = w.split(".")
                # Kiểm tra cấu trúc IPv4 gồm đúng 4 cụm số nguyên
                if len(parts) == 4 and all(p.isdigit() for p in parts):
                    # Khóa cấu trúc 2 octet đầu, che giấu 2 octet cuối
                    w = ".".join(parts[:2] + ["*", "*"])
            new_words.append(w)
            
        masked_logs.append(" ".join(new_words))
    
    print("Báo cáo danh sách log an toàn sau khi ẩn danh IP:")
    for i, log in enumerate(masked_logs, 1):
        print(f"  {i}. {log}")
        
    return masked_logs


def display_menu() -> None:
    """Hiển thị giao diện Menu điều khiển trực quan dạng Console."""
    show_menu = """
============= SECURITY LOG ANALYZER =============
1. Nhập và làm sạch dữ liệu Log thô
2. Lọc các Log cảnh báo mức độ cao (ERROR/CRITICAL)
3. Mã hóa địa chỉ IP (Masking)
4. Đóng hệ thống
================================================="""
    print(show_menu)


def main() -> None:
    """Hàm khởi chạy trung tâm, quản lý điều hướng vòng lặp tương tác người dùng."""
    while True:
        display_menu()
        choice = get_validate_input("Nhập lựa chọn của bạn (1-4): ")

        if choice == "1":
            input_and_clean_logs()
        elif choice == "2":
            filter_high_level_logs()
        elif choice == "3":
            mask_ip_in_logs()
        elif choice == "4":
            print("\n[HỆ THỐNG ĐANG ĐÓNG] Tiến hành lưu và kết thúc ca trực...")
            print("=> Trạng thái: Đã thoát chương trình an toàn!")
            break
        else:
            print("\nLỗi: Lựa chọn không hợp lệ! Vui lòng nhập số trong khoảng từ 1 đến 4.")


if __name__ == "__main__":
    main()