# Bối cảnh Calcifer

- Mục tiêu: lưu bộ pet đã chốt và quy trình cài lại dễ dùng trên Windows.
- Người dùng thích Calcifer chibi theo ảnh xăm ôm củi: mắt tròn hơi lệch, miệng cười đơn giản, lửa đỏ và nét mực rõ. Quan sát tỷ lệ ảnh gốc trước khi viết prompt.
- Chỉ giữ bản basic: lửa đung đưa và chớp mắt. Người dùng đã bỏ cảnh chảo; mẫu rồng, chảo và các phương án bị loại không thuộc repo này.
- Có sẵn `assets/spritesheet.png`, sáu khung và các preview; không gen lại khi chỉ cần cài lại.
- Cách nhanh: script cài → app Settings/Mini & Pets → Refresh → chọn Calcifer → kiểm tra overlay/active pet.
- Bản basic dùng atlas v1 tương thích phiên app đã kiểm tra; không tuyên bố đủ động tác v2 hoặc 16 hướng nhìn. Nếu phát triển bản đầy đủ, theo đúng skill và validator đang cài.
- App có thể tự nhập pet local sang cloud và đổi ID. Không hardcode ID tài khoản vào hướng dẫn cài hoặc repo.
- Không đọc app.asar hoặc tìm IPC cho tác vụ chỉ cài/chọn pet. Chỉ dùng công cụ điều khiển app được phép; nếu bị chặn, dùng API được hỗ trợ hoặc để người dùng chọn trong UI.
- GIF cần palette chung, alpha cutoff và kiểm tra sau encode để tránh viền sáng lấm tấm. Giữ APNG để có alpha mượt.
- Repo public do người dùng yêu cầu rõ. Không đưa ảnh cơ thể tham khảo, ảnh chụp tài khoản, global-state, token hoặc mã plugin vào repo.
