import io
import docx
import google.generativeai as genai
import streamlit as st

# 1. Cấu hình giao diện trang web
st.set_page_config(
    page_title="App Soạn Giáo Án 7991", page_icon="📚", layout="wide"
)

st.title("📚 Ứng Dụng Soạn Kế Hoạch Bài Dạy Chuẩn Công Văn 7991")
st.write(
    "Hỗ trợ giáo viên khởi tạo Kế hoạch bài dạy chi tiết, đúng cấu trúc và xuất"
    " file Word nhanh chóng."
)

# 2. Thanh cấu hình API Key ở phía bên trái (Sidebar)
with st.sidebar:
  st.header("⚙️ Cấu hình API")
  api_key = st.text_input(
      "Nhập Gemini API Key của thầy/cô:", type="password"
  )
  st.markdown(
      "[👉 Lấy Gemini API Key miễn phí tại"
      " đây](https://aistudio.google.com/app/apikey)"
  )
  st.info(
      "API Key được giữ bảo mật và chỉ dùng trong phiên làm việc hiện tại."
  )

# 3. Form nhập thông tin bài học
st.subheader("📝 Nhập thông tin bài học")
col1, col2 = st.columns(2)

with col1:
  ten_bai = st.text_input(
      "Tên bài học:", placeholder="Ví dụ: Hình chữ nhật - Hình xoang"
  )
  mon_hoc = st.text_input("Môn học & Lớp:", placeholder="Ví dụ: Toán 6")

with col2:
  bo_sach = st.selectbox(
      "Bộ sách giáo khoa:",
      [
          "Kết nối tri thức với cuộc sống",
          "Cánh diều",
          "Chân trời sáng tạo",
          "Chương trình THPT/Khác",
      ],
  )
  thoi_luong = st.text_input(
      "Thời lượng thực hiện:", placeholder="Ví dụ: 1 tiết (45 phút)"
  )

# System Prompt đính kèm theo chuẩn 7991
SYSTEM_PROMPT = """
Bạn là một Trợ lý AI Chuyên gia Giáo dục Việt Nam, có nhiệm vụ hỗ trợ giáo viên biên soạn Kế hoạch bài dạy chi tiết theo chuẩn Công văn 7991.

BẮT BUỘC xuất ra đúng cấu trúc 4 phần:
I. MỤC TIÊU (Kiến thức, Năng lực chung/đặc thù, Phẩm chất)
II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU (Giáo viên, Học sinh)
III. TIẾN TRÌNH DẠY HỌC (Đủ 4 hoạt động: Mở đầu, Hình thành kiến thức, Luyện tập, Vận dụng. Mỗi hoạt động BẮT BUỘC đủ 4 mục: a. Mục tiêu, b. Nội dung, c. Sản phẩm, d. Tổ chức thực hiện đủ 4 bước).
IV. DẶN DÒ VÀ HƯỚNG DẪN VỀ NHÀ
"""

# 4. Xử lý khi nhấn nút tạo bài
if st.button("🚀 Khởi Tạo Kế Hoạch Bài Dạy", type="primary"):
  if not api_key:
    st.error("⚠️ Vui lòng nhập Gemini API Key ở thanh bên trái!")
  elif not ten_bai or not mon_hoc:
    st.warning("⚠️ Vui lòng điền Tên bài học và Môn học/Lớp!")
  else:
    try:
      # Tích hợp Gemini API
      genai.configure(api_key=api_key)
      model = genai.GenerativeModel("gemini-1.5-flash")

      prompt_yeu_cau = f"""
            {SYSTEM_PROMPT}

            THÔNG TIN BÀI HỌC:
            - Tên bài học: {ten_bai}
            - Môn học & Lớp: {mon_hoc}
            - Bộ sách: {bo_sach}
            - Thời lượng: {thoi_luong}
            """

      with st.spinner(
          "⏳ AI đang biên soạn kế hoạch bài dạy, thầy/cô vui lòng đợi trong"
          " giây lát..."
      ):
        response = model.generate_content(prompt_yeu_cau)
        noi_dung_giao_an = response.text

      st.success("🎉 Tạo Kế hoạch bài dạy thành công!")
      st.markdown("---")

      # Hiển thị kết quả ra màn hình
      st.markdown(noi_dung_giao_an)

      # Tạo file .docx tự động
      doc = docx.Document()
      doc.add_heading(f"KẾ HOẠCH BÀI DẠY: {ten_bai.upper()}", level=1)
      doc.add_paragraph(f"Môn học & Lớp: {mon_hoc} | Bộ sách: {bo_sach}")
      doc.add_paragraph(f"Thời lượng: {thoi_luong}\n")

      # Thêm nội dung text vào file Word
      for line in noi_dung_giao_an.split("\n"):
        doc.add_paragraph(line)

      # Lưu vào bộ nhớ đệm
      buffer = io.BytesIO()
      doc.save(buffer)
      buffer.seek(0)

      # Nút tải file Word
      st.download_button(
          label="📥 Tải File Giáo Án Word (.docx)",
          data=buffer,
          file_name=f"Giao_an_{ten_bai.replace(' ', '_')}.docx",
          mime=(
              "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          ),
      )

    except Exception as e:
      st.error(f"❌ Có lỗi xảy ra: {str(e)}")
