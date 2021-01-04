import argparse
import os

from PIL import Image

BASE_DIM = 2000


def compress_image(input_path: str, output_path: str, quality: int = 95, resize: int = 0) -> str:
    img = Image.open(input_path)

    if resize == 1:
        w, h = img.size
        max_dim = max(w, h)
        if max_dim > BASE_DIM:
            scale = BASE_DIM / max_dim
            new_w, new_h = int(scale * w), int(scale * h)
            img = img.resize((new_w, new_h), Image.ANTIALIAS)
    img = img.convert('RGB')
    if 20 < quality < 100:
        pass
    else:
        quality = 95
    img.save(output_path, "jpeg", optimize=True, quality=quality)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Compress Image Tool")
    parser.add_argument("--input", "-i", required=True, help="Đường dẫn đến ảnh đầu vào.")
    parser.add_argument("--output", "-o", help="Đường dẫn lưu ảnh đầu ra.")
    parser.add_argument("--quality", "-q", required=False, default=95, type=int,
                        help="Chất lượng ảnh đầu ra. Gía trị int trong khoảng 20 - 100", )
    parser.add_argument("--resize", "-r", required=False, default=0, type=int,
                        help="Thay đổi kích thước ảnh. Mặc định là không thay đổi kích thước ảnh. Thay đổi kích thước ảnh nếu reszie=1", )
    args = parser.parse_args()

    file_path = args.input
    input_dir = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    file_id, ext = os.path.splitext(filename)

    output_path = args.output
    if output_path is None:
        output_path = os.path.join(input_dir, file_id + "_compressed.jpg")

    return compress_image(file_path, output_path, args.quality, args.resize)
