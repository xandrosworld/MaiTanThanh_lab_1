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

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Khi temperature = 0.0, mô hình luôn trả về phản hồi gần như giống nhau và rất chắc chắn — nó chọn token có xác suất cao nhất. Khi temperature tăng dần lên 1.0 và 1.5, câu trả lời trở nên đa dạng hơn, sáng tạo hơn, đôi khi bất ngờ, nhưng cũng có thể kém chính xác hơn. Nói cách khác, temperature càng cao thì "độ ngẫu nhiên" càng lớn — phù hợp để khám phá ý tưởng, nhưng không phù hợp khi cần độ chính xác cao.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Tôi sẽ đặt temperature khoảng 0.2–0.3. Chatbot hỗ trợ khách hàng cần trả lời nhất quán, chính xác và đáng tin cậy — không cần sáng tạo. Temperature thấp giúp đảm bảo câu trả lời ổn định, tránh tình trạng mô hình "phát minh" thông tin sai hoặc trả lời không nhất quán giữa các lần hỏi cùng một câu.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Tổng token output mỗi ngày = 10.000 × 3 × 350 = 10.500.000 token ≈ 10.500 nghìn token.  
> Chi phí GPT-4o: 10.500 × $0.010 = **$105/ngày**  
> Chi phí GPT-4o-mini: 10.500 × $0.0006 = **$6.3/ngày**  
> → GPT-4o đắt hơn khoảng **16–17 lần** so với GPT-4o-mini cho cùng workload.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> **GPT-4o xứng đáng:** Phân tích hợp đồng pháp lý hoặc chẩn đoán y tế — nơi sai sót có thể gây hậu quả nghiêm trọng. Chất lượng reasoning và độ chính xác cao của GPT-4o là bắt buộc.  
> **GPT-4o-mini phù hợp hơn:** Chatbot FAQ tự động trả lời câu hỏi thường gặp (giờ mở cửa, chính sách đổi trả, v.v.) — nội dung đơn giản, lặp lại, không cần reasoning sâu, tiết kiệm chi phí là ưu tiên hàng đầu.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất khi người dùng chờ đợi câu trả lời dài — ví dụ chatbot, viết văn bản, giải thích code — vì nó tạo cảm giác phản hồi tức thì, giảm "perceived latency" dù tổng thời gian không đổi. Ngược lại, non-streaming phù hợp hơn khi cần xử lý kết quả như một khối hoàn chỉnh trước khi làm gì đó tiếp theo — ví dụ: phân tích JSON output, so sánh nhiều response, hoặc pipeline tự động không có người dùng trực tiếp quan sát. Tóm lại: streaming → UX tốt hơn cho con người; non-streaming → đơn giản hơn cho hệ thống tự động.


## Danh Sách Kiểm Tra Nộp Bài
- [x] Tất cả tests pass: `pytest tests/ -v`
- [x] `call_openai` đã triển khai và kiểm thử
- [x] `call_openai_mini` đã triển khai và kiểm thử
- [x] `compare_models` đã triển khai và kiểm thử
- [x] `streaming_chatbot` đã triển khai và kiểm thử
- [x] `retry_with_backoff` đã triển khai và kiểm thử
- [x] `batch_compare` đã triển khai và kiểm thử
- [x] `format_comparison_table` đã triển khai và kiểm thử
- [x] `exercises.md` đã điền đầy đủ
- [x] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 
