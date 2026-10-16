# Calcifer — desktop pet basic

Calcifer chibi ôm củi, lửa đung đưa và chớp mắt nhẹ. Bộ này lưu lại pet đã chốt, file cài và cách làm nhanh để lần sau không phải dựng lại từ đầu.

![Calcifer idle](assets/preview.gif)

## Cài lại nhanh

Cần Python 3.10 trở lên. Script cài chỉ dùng thư viện chuẩn, không cần API key hoặc cài thêm package.

```powershell
git clone https://github.com/VoDucNhatku/calcifer-desktop-pet.git
cd calcifer-desktop-pet
python scripts/install.py --dry-run
python scripts/install.py
```

Sau đó mở app → **Settings → Mini & Pets → Refresh → Calcifer** để chọn pet. Tên mục có thể là **Pets** tùy phiên bản app. File local nằm ở `%USERPROFILE%\.codex\pets\calcifer-basic` hoặc thư mục `pets` trong `CODEX_HOME` nếu đã cấu hình biến này.

Nếu dùng Codex Home khác:

```powershell
python scripts/install.py --codex-home "D:\MyCodexHome"
```

Script kiểm tra checksum và định dạng trước khi sao chép; nếu pet đích có nội dung khác, script dừng. Dùng `--force` để thay thế sau khi đã sao lưu pet cũ vào `CODEX_HOME/pet-backups/`. Script không đổi lựa chọn pet đang hoạt động; bước **Refresh → Calcifer** trong app hoàn tất việc kích hoạt.

Kiểm tra script cài bằng thư mục tạm, không thay pet đang dùng:

```powershell
python -m unittest discover -s tests -v
```

## Trong repo có gì?

- `assets/spritesheet.png`: atlas PNG RGBA, 1536×1872, 8 cột × 9 hàng, mỗi ô 192×208.
- `assets/frames/`: sáu khung gốc của chuyển động chờ đã duyệt.
- `assets/preview.gif`: GIF nền trong suốt, 384×416, sáu khung, lặp 2,72 giây.
- `assets/preview.apng`: bản động giữ alpha mượt hơn GIF.
- `assets/preview.mp4`: video nền nâu sẫm để xem khi trình đọc không phát GIF.
- `assets/contact-sheet.png`: sáu khung giải mã từ GIF để kiểm tra.
- `pet.json`, `checksums.json`: thông tin cài và kiểm tra toàn vẹn.
- [Quy trình làm nhanh](docs/QUICK_WORKFLOW.vi.md): cách dựng, kiểm tra, đóng gói và kích hoạt.

## Phạm vi bản basic

Các trạng thái của app dùng lại chuyển động nhẹ đã duyệt. Đây là một vòng lặp basic dùng trong các hàng của atlas, không phải chín động tác riêng. Bản v1 này không có 16 hướng nhìn của v2. Cảnh chảo đã bỏ; mẫu rồng và các mẫu bị loại không nằm trong gói này.

Đã kiểm tra với bản app Windows 26.1013.3656 tại thời điểm 17/10/2026. Trong phiên gốc, đã chọn Calcifer và xác nhận pet xuất hiện trên overlay, đồng thời API Pets trả về `is_active: true`. Máy khác vẫn cần tự chọn pet sau khi cài.

Calcifer là nhân vật từ *Howl’s Moving Castle*. Đây là bản fan art cá nhân, không phải sản phẩm chính thức. Ảnh xăm tham khảo và ảnh chụp chứa thông tin cá nhân không được đưa vào repo; không đính kèm giấy phép cấp quyền cho nhân vật gốc hoặc mã của các plugin OpenAI.
