# Cách làm pet nhanh và giữ đúng mẫu

## 1. Nếu đã có bộ pet này: cài lại, không gen lại

1. Chạy `python scripts/install.py --dry-run` để kiểm tra file.
2. Chạy `python scripts/install.py` để cài vào Codex Home.
3. Mở **Settings → Mini & Pets → Refresh**.
4. Chọn **Calcifer**. Kiểm tra hình pet trong khung xem trước và overlay nổi.
5. Nếu có connector Pets, gọi `list_pets` và xác nhận pet đúng tên có `is_active: true`. ID cloud có thể khác ID local; app đã tự nhập bản local thành pet cloud ở lần cài gốc. Không suy ra ID chỉ từ tên hoặc hardcode ID của tài khoản khác.

**Điểm tiết kiệm công nhất:** dùng thư mục pet local và nút Refresh. Không cần giải nén app.asar, đọc source app, tìm IPC, sửa global-state hoặc khởi động lại app để chỉ đổi pet.

Chỉ điều khiển giao diện bằng công cụ được phép trong phiên hiện tại. Nếu công cụ hoặc skill chặn thao tác trên app, dùng API hỗ trợ; nếu không có API chọn pet local, để người dùng thực hiện bước Refresh/chọn pet. Không lách hạn chế bằng UI injection hoặc endpoint chưa được hỗ trợ.

## 2. Nếu làm pet mới: chốt tạo hình trước

- Xem kỹ ảnh tham khảo trước khi viết prompt: tỷ lệ đầu/thân, vị trí mắt, miệng, đường viền, bảng màu và đạo cụ.
- Với mẫu đã chốt: thân lửa gọn, mắt tròn hơi lệch, miệng cười đơn giản, tay nhỏ ôm củi; giữ nét mực và viền kem mảnh.
- Tạo một ảnh canonical, cho người dùng xem và chốt. Dùng chính ảnh này làm reference cho mọi hàng chuyển động.
- Không tự đổi sang kiểu bóng 3D, mắt anime quá lớn hoặc thêm nhiều chi tiết khi người dùng thích nét vẽ chibi đơn giản.
- Những mẫu rồng/chảo bị bỏ là phương án cũ; không đưa chúng trở lại phạm vi hiện tại.

## 3. Làm một vòng lặp chờ để duyệt

Vòng lặp trong repo có sáu pha:

| Khung | Chuyển động | Thời lượng xem trước |
|---|---|---:|
| 1 | Nghỉ, mở mắt | 1000 ms |
| 2 | Lửa nghiêng phải nhẹ | 240 ms |
| 3 | Mắt khép nửa | 120 ms |
| 4 | Chớp mắt | 120 ms |
| 5 | Lửa nghiêng trái, mở mắt | 240 ms |
| 6 | Trở lại gần dáng đầu | 1000 ms |

Khúc củi là mốc cố định: giữ cùng kích thước và đường đáy; tay bám cùng vị trí. Chỉ để đỉnh lửa đung đưa và mặt chớp mắt. Khung đầu/cuối cần gần nhau để nối vòng.

### Prompt hàng chuyển động để dùng lại

> Dùng ảnh canonical làm nguồn nhận diện và ảnh gốc làm tham khảo nét vẽ. Tạo đúng 6 tư thế hoàn chỉnh trong một hàng ngang, cách nhau rõ trên nền magenta phẳng #FF00FF; không vẽ ô hoặc nhãn. Giữ cùng tỷ lệ, mắt, miệng, bảng màu, viền và đạo cụ. Sáu pha: nghỉ mở mắt; lửa nghiêng phải nhẹ; mắt khép nửa; nhắm mắt; lửa nghiêng trái và mở mắt; trở lại gần tư thế đầu. Khúc củi đứng yên ở cùng đường đáy, tay ôm nguyên vị trí. Không thêm cảnh, khói, hào quang, motion blur hoặc hạt rời. Giữ nét chibi trong ảnh, không đổi phong cách.

Ảnh canonical phải được đính kèm khi gọi imagegen; prompt chữ không thay thế được ảnh nhận diện. Dùng layout guide cho khoảng cách nếu skill cung cấp. Mọi hình mới/sửa hình dùng imagegen; code chỉ xử lý layout, alpha, trích khung, encode và QA.

## 4. Dùng pipeline có sẵn để xử lý và kiểm tra

Khi plugin `work-pets:create-pet` có sẵn, đọc `SKILL.md` và shared sprite contract của đúng phiên bản cài đặt. Dùng các script bundled; repo này không sao chép mã plugin:

1. `prepare_pet_run.py`: tạo manifest, prompt và layout guide.
2. Tạo canonical bằng imagegen, rồi tạo từng hàng có reference canonical.
3. `extract_strip_frames.py --states idle --method components`: trích nhóm pose hoàn chỉnh, giữ scale/registration chung; không cắt đều khi khoảng cách source không đều.
4. `inspect_frames.py --states idle --require-components`: kiểm tra số khung, alpha, clipping và nền chroma.
5. `despill_chroma_edges.py`: làm sạch viền chroma một lượt ở artifact cuối.
6. Render GIF/APNG/MP4 từ chính khung đã xử lý. Xem contact sheet và khung giải mã từ file động cuối.

Không thay pipeline của skill bằng báo cáo thành công tự viết. Nếu làm pet v2 đầy đủ, phải theo đủ các hàng, 16 hướng nhìn và gate của skill; không xem bộ basic này là ví dụ đã vượt gate v2.

## 5. Lưu ý GIF: tránh viền lấm tấm

RGBA PNG có alpha nhiều mức; GIF chỉ có trong suốt một mức. Khi resize rồi lưu GIF trực tiếp, các pixel alpha rất nhỏ ở viền có thể thành viền sáng lấm tấm.

Bản cuối dùng chung bảng màu 255 màu cho tất cả khung, một chỉ số trong suốt riêng, không dithering, alpha cutoff 128, `disposal=2`, `loop=0`. APNG giữ alpha mượt hơn nên cũng lưu kèm. Sau khi encode, giải mã lại GIF và kiểm tra đủ khung, thời lượng, nền trong suốt và hình chớp mắt.

## 6. Đóng gói basic đã chốt

Lần này người dùng đã chọn **basic**: dùng lại vòng lặp nhẹ cho các trạng thái, không tạo thêm cảnh phức tạp. Atlas v1 dùng 8 cột × 9 hàng, ô 192×208:

| Hàng | Tên trạng thái của app | Số ô có hình |
|---:|---|---:|
| 0 | idle | 6 |
| 1 | running-right | 8 |
| 2 | running-left | 8 |
| 3 | waving | 4 |
| 4 | jumping | 5 |
| 5 | failed | 8 |
| 6 | waiting | 6 |
| 7 | running | 6 |
| 8 | review | 6 |

Tổng 57 ô có hình; 15 ô thừa phải hoàn toàn trong suốt. Tên hàng mô tả slot app, không có nghĩa bản basic đã vẽ động tác tương ứng. Trạng thái trong app dùng timing riêng, có thể khác thời lượng GIF xem trước.

Đã chạy validator bundled trên đúng PNG đã cài: RGBA, 1536×1872, không còn RGB ẩn ở pixel trong suốt, không lỗi/cảnh báo. Checksum bản này nằm ở `checksums.json`. Không ghi đè pet đang dùng bằng một sheet chưa được kiểm tra.

## 7. Cài và xác nhận

Manifest local tối thiểu:

```json
{
  "displayName": "Calcifer",
  "description": "Calcifer chibi ôm củi. Bản basic: lửa đung đưa và chớp mắt nhẹ.",
  "spriteVersionNumber": 1,
  "spritesheetPath": "spritesheet.png"
}
```

Đặt manifest và sheet trong `CODEX_HOME/pets/calcifer-basic/`, rồi Refresh/chọn trong app. Chỉ nói đã thay pet khi thấy overlay đổi và/hoặc API xác nhận đúng active pet. File đã có trên đĩa chưa chứng minh pet đang được chọn.

Không commit token GitHub, app global-state, config tài khoản, pet ID cá nhân, ảnh chụp tài khoản hoặc ảnh cơ thể tham khảo. Chỉ đẩy gói artifact đã chọn và hướng dẫn.
