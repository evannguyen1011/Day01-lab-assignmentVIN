# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**
<!-- 0.0: Một sự thật thú vị về Việt Nam là đất nước này có hơn 4.000 năm lịch sử và là nơi khai sinh ra nhiều nền văn minh và văn hóa phong phú. Việt Nam còn nổi tiếng với điệu múa rối nước, một loại hình nghệ thuật truyền thống độc đáo chỉ có ở Việt Nam. Múa rối nước thể hiện những câu chuyện dân gian, phong tục tập quán của người Việt, và thường được biểu diễn trong các lễ hội và dịp lễ đặc biệt. Đây là một phần quan trọng trong di sản văn hóa của đất nước.
0.5: Một sự thật thú vị về Việt Nam là đất nước này có hơn 4.000 đảo, chủ yếu tập trung ở vịnh Hạ Long. Vịnh Hạ Long không chỉ nổi tiếng với cảnh đẹp kỳ vĩ của những hòn đảo đá vôi và nước biển trong xanh, mà còn được UNESCO công nhận là di sản thế giới. Vịnh Hạ Long còn được xem là một trong những kỳ quan thiên nhiên của thế giới, thu hút hàng triệu khách du lịch mỗi năm. Những chiếc thuyền truyền thống (du thuyền) trên vịnh đã trở thành biểu tượng du lịch của Việt Nam.
1.0: Một sự thật thú vị về Việt Nam là quốc gia này có nhiều loại trà nổi tiếng, và một trong số đó là trà ô long. Việt Nam hiện là một trong những quốc gia sản xuất ô long lớn nhất thế giới, đặc biệt từ vùng trà Tân Cương (Thái Nguyên) và các khu vực miền núi phía Bắc. Trà ô long không chỉ được yêu thích trong nước mà còn xuất khẩu sang nhiều nước khác, phục vụ cho những người yêu thích trà trên toàn thế giới. Hương vị của trà ô long rất đặc trưng, với sự kết hợp giữa trà xanh và trà đen, mang đến cho người thưởng thức một trải nghiệm độc đáo. -->

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> *Câu trả lời của bạn*
-->em thấy là càng để temperature lên cao thì nó viết càng sai lệch nhiều so với thực tế, ngoài ra thì em có cảm giác nó bay bổng hơn, nhưng đồng thời sai cũng nhiều, rồi còn lệch lạc kiểu râu ông nọ cắm cằm bà kia nữa

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> *Câu trả lời của bạn*
-->em sẽ để ở khoảng 0.2 đến 0.5 vì em nghĩ ở khoảng đó thì văn phong vừa ổn, ít bị sai lệch nhưng cũng không đến nỗi trả lời quá học thuật và cứng nhắc khiến người dùng khó hiểu

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> *Câu trả lời của bạn*
-->theo như em tính là khoảng 15 lần
**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> *Câu trả lời của bạn*
--> theo em nên dùng 4o khi làm về các tác vụ nặng về suy luận phức tạp, code hệ thống lớn hoặc phân tích cấu trúc dữ liệu cần có độ chính xác cao, còn mini khi làm các tác vụ đơn giản như chăm sóc khách hàng, trích xuất các thông tin cơ bản không cần độ chính xác quá cao
---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> *Câu trả lời của bạn*
-> theo em thì streaming nên dùng khi làm chatbot hỗ trợ khách hàng vì nó nhìn sẽ rất mượt và tránh việc khách hàng buồn chán, sốt ruột vì phải chờ câu trả lời, còn non-streaming dùng khi mà làm các tác vụ bên dưới như trích xuất dữ liệu, các tác vụ chạy ngầm

## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
