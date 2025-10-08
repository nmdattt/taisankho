import streamlit as st
import pandas as pd

# === Cấu hình ===
SHEET_ID = "1K5EM2wWmKWs5_FSg6SBsUyD8UkGSMAhPnn5ED_VmUPE"
SHEET_NAME = "Sheet1"  # đổi nếu tên sheet khác

# === Đọc dữ liệu từ Google Sheets ===
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
df = pd.read_csv(url, skiprows=2)  # Bỏ qua 2 dòng đầu (hàng 1-2 không phải tiêu đề)

# === Thiết lập giao diện ===
st.set_page_config(page_title="Tra cứu tài sản", page_icon="📦", layout="centered")

st.title("📦 Tra cứu thông tin tài sản")

# --- Lấy tham số URL ---
query_params = st.experimental_get_query_params()
so_the = query_params.get("so_the", [""])[0].strip().upper()

# --- Chuẩn hóa dữ liệu ---
df.columns = df.columns.str.strip()  # Xóa khoảng trắng ở tên cột
if "Số thẻ" not in df.columns:
    st.error("❌ Không tìm thấy cột 'Số thẻ' trong dữ liệu Google Sheets.")
else:
    df["Số thẻ"] = df["Số thẻ"].astype(str).str.strip().str.upper().str.replace(".0", "", regex=False)

    # --- Xử lý truy vấn ---
    if so_the:
        st.subheader(f"Mã số thẻ: {so_the}")
        ts = df[df["Số thẻ"] == so_the]

        if not ts.empty:
            record = ts.iloc[0]
            st.markdown(f"""
            **Tên tài sản:** {record['TÊN TÀI SẢN']}  
            **Đơn vị tính:** {record['Đơn vị tính']}  
            **Năm sử dụng:** {int(record['Năm Sử dụng']) if not pd.isna(record['Năm Sử dụng']) else 'N/A'}  
            **Số lượng:** {int(record['Số lượng']) if not pd.isna(record['Số lượng']) else 'N/A'}  
            **Nguyên giá:** {record['Nguyên giá']} VNĐ  
            **Hao mòn:** {record['Hao Mòn']} VNĐ  
            **Giá trị còn lại:** {record['Giá trị còn lại'] if 'Giá trị còn lại' in record else 'N/A'} VNĐ  
            """)
        else:
            st.warning("⚠️ Không tìm thấy tài sản với mã số thẻ này.")
    else:
        st.info("🔎 Hãy nhập mã số thẻ vào URL, ví dụ: `...?so_the=B02`")
