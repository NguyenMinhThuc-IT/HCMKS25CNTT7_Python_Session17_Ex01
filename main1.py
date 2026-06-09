raw_logs = [] 
processed_logs = []

def get_validate_input(prompt: str) -> str:
    
    while True:
        user_input = input(prompt).strip()
        if user_input:  # kiểm tra không rỗng
            return user_input
        else:
            print("Dữ liệu không hợp lệ, vui lòng nhập lại.")

def input_and_clean_logs():
    print("--- NẠP DỮ LIỆU LOG ---")
    raw_data = get_validate_input("Nhập chuỗi log thô (cách nhau bởi dấu ;): ")
    
    # Loại bỏ ký tự đặc biệt
    remove_chars = "!@#$"
    trans_table = str.maketrans('', '', remove_chars)
    cleaned_data = raw_data.translate(trans_table)
    
    # Tách thành danh sách log
    global raw_logs
    raw_logs = cleaned_data.split(';')
    
    print(f"Đã làm sạch và lưu {len(raw_logs)} dòng log vào hệ thống.")

def filter_high_level_logs():
    
    global raw_logs, processed_logs
    if not raw_logs:
        print("Chưa có dữ liệu log, vui lòng thực hiện chức năng 1")
        return
    
    # Lọc bằng List Comprehension
    processed_logs = [log for log in raw_logs 
                      if "error" in log.lower() or "critical" in log.lower()]
    
    if processed_logs:
        print("--- LỌC CẢNH BÁO ---")
        print(f"Tìm thấy {len(processed_logs)} cảnh báo nguy hiểm:")
        for log in processed_logs:
            print(f"- {log}")
    else:
        print("Không tìm thấy cảnh báo nguy hiểm nào.")

def mask_ip_in_logs():
    
    global processed_logs
    if not processed_logs:
        print("Chưa có dữ liệu log, vui lòng thực hiện chức năng 1 hoặc 2")
        return
    
    masked_logs = []
    for log in processed_logs:
        words = log.split()
        new_words = []
        for w in words:
            if "." in w:  # có thể là IP
                parts = w.split(".")
                if len(parts) == 4 and all(p.isdigit() for p in parts):
                    # Mã hóa 2 số cuối
                    w = ".".join(parts[:2] + ["*", "*"])
            new_words.append(w)
        masked_logs.append(" ".join(new_words))
    
    print("--- MÃ HÓA IP ---")
    print("Báo cáo log an toàn:")
    for i, log in enumerate(masked_logs, 1):
        print(f"{i}. {log}")
    
    return masked_logs

def menu():
    show_menu = """ 
\n============= SECURITY LOG ANALYZER =============
1. Nhập và làm sạch dữ liệu Log thô
2. Lọc các Log cảnh báo mức độ cao (ERROR/CRITICAL)
3. Mã hóa địa chỉ IP (Masking)
4. Đóng hệ thống
================================================="""
    print(show_menu)

def main ():
    while True:
        menu()
        choice = get_validate_input("Nhập lựa chọn của bạn: ")

        if choice == "1":
            input_and_clean_logs()
        elif choice == "2":
            filter_high_level_logs()
        elif choice == "3":
            mask_ip_in_logs()
        elif choice == "4":
            print("Thoát chương trình!!!!! Đợi loading....")
            break
        else:
            print("Nhập sai lựa chọn rồi")
main()