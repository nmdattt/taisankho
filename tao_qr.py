import streamlit as st
import pandas as pd

# === Cấu hình ===
SHEET_ID = "1K5EM2wWmKWs5_FSg6SBsUyD8UkGSMAhPnn5ED_VmUPE"
SHEET_NAME = "Sheet1"  # đổi nếu tên sheet khác

# === Đọc dữ liệu từ Google Sheets ===
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
df = pd.read_csv(url, skiprows=0)  # Bỏ qua 2 dòng đầu (vì tiêu đề thật bắt đầu từ hàng 3)


# Chuẩn hóa tên cột (loại bỏ khoảng trắng và ký tự ẩn)
df.columns = df.columns.str.strip().str.replace("\ufeff", "", regex=True)

# --- Lấy tham số URL ---
query_params = st.query_params
so_the = query_params.get("so_the", "").strip().upper()

# --- Kiểm tra dữ liệu ---
if "Số thẻ" not in df.columns:
    st.error(f"❌ Không tìm thấy cột 'Số thẻ' trong dữ liệu. Các cột hiện có: {list(df.columns)}")
else:
    # Chuẩn hóa cột Số thẻ
    df["Số thẻ"] = (
        df["Số thẻ"]
        .astype(str)
        .str.strip()
        .str.upper()
        .str.replace(".0", "", regex=False)
    )

    if so_the:
        st.subheader(f"Mã tài sản: {so_the}")
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
