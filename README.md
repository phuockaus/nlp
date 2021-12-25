# Bài tập lớn môn Xử lý ngôn ngữ tự nhiên

**Sinh viên**: Đoàn Trần Hữu Phước\
**Student ID**: 1813636

## Đề bài

Xây dựng hệ thống hỏi đáp đơn giản về các chuyến tàu hỏa liên tỉnh bằng quan hệ văn phạm

## Cơ sở dữ liệu

(TRAIN B1) (TRAIN B2) (TRAIN B3)\
(TRAIN B4) (TRAIN B5) (TRAIN B6)

(ATIME B1 HUE 19:00HR)\
(ATIME B2 HUE 22:30HR)\
(ATIME B3 HCM 16:00HR)\
(ATIME B4 NTrang 16:30HR)\
(ATIME B5 HN 23:30HR)\
(ATIME B6 DANANG 11:30HR)

(DTIME B1 HCM 10:00HR)\
(DTIME B2 HN 14:30HR)\
(DTIME B3 DANANG 6:00HR)\
(DTIME B4 DANANG 8:30HR)\
(DTIME B5 HCM 3:30HR)\
(DTIME B6 HUE 7:30HR)

(RUN-TIME B1 HCM HUE 9:00HR)\
(RUN-TIME B2 HN HUE 8:00HR)\
(RUN-TIME B3 DANANG HCM 10:00HR)\
(RUN-TIME B4 DANANG NTrang 8:00HR)\
(RUN-TIME B5 HCM HN 18:00HR)\
(RUN-TIME B6 HUE DANANG 4:00HR)

## Câu truy vấn

1. Tàu hỏa nào đến thành phố Huế lúc 19:00HR ?
2. Thời gian tàu hỏa B3 chạy từ Đà Nẵng đến TP. Hồ Chí Minh là mấy giờ ?
3. Tàu hỏa nào đến thành phố Hồ Chí Minh ?
4. Tàu hỏa nào chạy từ Nha Trang, lúc mấy giờ ?
5. Tàu hỏa nào chạy từ TP.Hồ Chí Minh đến Hà Nội ?
6. Tàu hỏa B5 có chạy từ Đà Nẵng không ?

## Hiện thực

a) Xây dựng bộ phân tích cú pháp của văn phạm phụ thuộc.\
b) Phân tích cú pháp và xuất ra các quan hệ ngữ nghĩa của các câu truy vấn.\
c) Từ kết quả ở b) tạo các quan hệ văn phạm cho về các chuyến tàu hỏa giữa thành phố Hồ Chí Minh, Huế, Đà Nẵng, Nha Trang và Hà Nội với cơ sở dữ liệu đã cho ở trên.\
d) Tạo dạng luận lý từ các quan hệ văn phạm ở c).\
e) Tạo ngữ nghĩa thủ tục từ dạng luận lý ở d).\
f) Truy xuất dữ liệu để tìm thông tin trả lời cho các câu truy vấn trên.

## Thiết lập môi trường

Để có thể thực thi chương trình, các thư viện hỗ trợ cần cài đặt:

- `nltk` thông qua câu lệnh `pip install nltk` (yêu cầu máy đã cài đặt `pip`).

## Chạy chương trình

Với các câu truy vấn được lưu trong đường dẫn `input/queries/`, chương trình sẽ đọc tất cả các file có trong thư mục và sẽ ghi output cho từng câu truy vấn ở từng giai đoạn phân tích. Yêu cầu về tên của file chứa câu truy vấn: `[digit].txt`.

Để chạy chương trình, ta chỉ cần chạy lệnh sau ở terminal:

```sh
$python3 main.py
```
