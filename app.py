import io
import docx
import google.generativeai as genai
import streamlit as st

# 1. C?u hình giao di?n trang web
st.set_page_config(
    page_title="App So?n Giáo Án 7991", page_icon="??", layout="wide"
)

st.title("?? ?ng D?ng So?n K? Ho?ch Bài D?y Chu?n Công Van 7991")
st.write(
    "H? tr? giáo viên kh?i t?o K? ho?ch bài d?y chi ti?t, dúng c?u trúc và xu?t"
    " file Word nhanh chóng."
)

# 2. Thanh c?u hình API Key ? phía bên trái (Sidebar)
with st.sidebar:
  st.header("?? C?u hình API")
  api_key = st.text_input(
      "Nh?p Gemini API Key c?a th?y/cô:", type="password"
  )
  st.markdown(
      "[?? L?y Gemini API Key mi?n phí t?i"
      " dây](https://aistudio.google.com/app/apikey)"
  )
  st.info(
      "API Key du?c gi? b?o m?t và ch? dùng trong phiên làm vi?c hi?n t?i."
  )

# 3. Form nh?p thông tin bài h?c
st.subheader("?? Nh?p thông tin bài h?c")
col1, col2 = st.columns(2)

with col1:
  ten_bai = st.text_input(
      "Tên bài h?c:", placeholder="Ví d?: Hình ch? nh?t - Hình xoang"
  )
  mon_hoc = st.text_input("Môn h?c & L?p:", placeholder="Ví d?: Toán 6")

with col2:
  bo_sach = st.selectbox(
      "B? sách giáo khoa:",
      [
          "K?t n?i tri th?c v?i cu?c s?ng",
          "Cánh di?u",
          "Chân tr?i sáng t?o",
          "Chuong trình THPT/Khác",
      ],
  )
  thoi_luong = st.text_input(
      "Th?i lu?ng th?c hi?n:", placeholder="Ví d?: 1 ti?t (45 phút)"
  )

# System Prompt dính kèm theo chu?n 7991
SYSTEM_PROMPT = """
B?n là m?t Tr? lý AI Chuyên gia Giáo d?c Vi?t Nam, có nhi?m v? h? tr? giáo viên biên so?n K? ho?ch bài d?y chi ti?t theo chu?n Công van 7991.

B?T BU?C xu?t ra dúng c?u trúc 4 ph?n:
I. M?C TIÊU (Ki?n th?c, Nang l?c chung/d?c thù, Ph?m ch?t)
II. THI?T B? D?Y H?C VÀ H?C LI?U (Giáo viên, H?c sinh)
III. TI?N TRÌNH D?Y H?C (Ð? 4 ho?t d?ng: M? d?u, Hình thành ki?n th?c, Luy?n t?p, V?n d?ng. M?i ho?t d?ng B?T BU?C d? 4 m?c: a. M?c tiêu, b. N?i dung, c. S?n ph?m, d. T? ch?c th?c hi?n d? 4 bu?c).
IV. D?N DÒ VÀ HU?NG D?N V? NHÀ
"""

# 4. X? lý khi nh?n nút t?o bài
if st.button("?? Kh?i T?o K? Ho?ch Bài D?y", type="primary"):
  if not api_key:
    st.error("?? Vui lòng nh?p Gemini API Key ? thanh bên trái!")
  elif not ten_bai or not mon_hoc:
    st.warning("?? Vui lòng di?n Tên bài h?c và Môn h?c/L?p!")
  else:
    try:
      # Tích h?p Gemini API
      genai.configure(api_key=api_key)
      model = genai.GenerativeModel("gemini-1.5-flash")

      prompt_yeu_cau = f"""
            {SYSTEM_PROMPT}

            THÔNG TIN BÀI H?C:
            - Tên bài h?c: {ten_bai}
            - Môn h?c & L?p: {mon_hoc}
            - B? sách: {bo_sach}
            - Th?i lu?ng: {thoi_luong}
            """

      with st.spinner(
          "? AI dang biên so?n k? ho?ch bài d?y, th?y/cô vui lòng d?i trong"
          " giây lát..."
      ):
        response = model.generate_content(prompt_yeu_cau)
        noi_dung_giao_an = response.text

      st.success("?? T?o K? ho?ch bài d?y thành công!")
      st.markdown("---")

      # Hi?n th? k?t qu? ra màn hình
      st.markdown(noi_dung_giao_an)

      # T?o file .docx t? d?ng
      doc = docx.Document()
      doc.add_heading(f"K? HO?CH BÀI D?Y: {ten_bai.upper()}", level=1)
      doc.add_paragraph(f"Môn h?c & L?p: {mon_hoc} | B? sách: {bo_sach}")
      doc.add_paragraph(f"Th?i lu?ng: {thoi_luong}\n")

      # Thêm n?i dung text vào file Word
      for line in noi_dung_giao_an.split("\n"):
        doc.add_paragraph(line)

      # Luu vào b? nh? d?m
      buffer = io.BytesIO()
      doc.save(buffer)
      buffer.seek(0)

      # Nút t?i file Word
      st.download_button(
          label="?? T?i File Giáo Án Word (.docx)",
          data=buffer,
          file_name=f"Giao_an_{ten_bai.replace(' ', '_')}.docx",
          mime=(
              "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          ),
      )

    except Exception as e:
      st.error(f"? Có l?i x?y ra: {str(e)}")

