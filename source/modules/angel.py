import random
import base64
import io

from PIL import Image
from pathlib import Path
from collections import defaultdict

from source.utils.config_utils import get_config

class AngelImgGenerate():
    def __init__(self):
        self.root_file = get_config("image","angel")
        self.parts = get_config("image","angel_parts")

    def _get_parts_list(self):
        body_parts = defaultdict(list)
        for f in self.parts:
            prefix = f.split("-")[0]
            body_parts[prefix].append(f)

        parts_choice = {}

        for k, v in body_parts.items():
            if k == "8":  # special rule cho access
                if random.random() < 0.9:
                    # 90% chọn 1 file random
                    parts_choice[k] = [random.choice(v)]
                else:
                    # 10% chọn tất cả file
                    parts_choice[k] = v
            else:
                parts_choice[k] = [random.choice(v)]

        parts_choice_order = dict(sorted(parts_choice.items(), key=lambda item: int(item[0])))
        temp_list = [item for sublist in parts_choice_order.values() for item in sublist]
        body_parts_list = []
        for item in temp_list[::-1]:
            path = Path(f"{self.root_file}\\{item}")
            body_parts_list.append(path)

        return body_parts_list

    def overlay_images(self):
        image_paths = self._get_parts_list()
        base = Image.open(image_paths[0]).convert("RGBA")
        canvas = Image.new("RGBA", base.size, (255, 255, 255, 255))

        for path in image_paths:
            img = Image.open(path).convert("RGBA")
            canvas.paste(img, (0, 0), img)

        buffer = io.BytesIO()
        canvas.save(buffer, format="PNG")
        base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return base64_str, image_paths


if __name__ == "__main__":
    generator = AngelImgGenerate()

    while True:
        img_base64, parts_list = generator.overlay_images()

        if len(parts_list) == 9:  # nghĩa là chọn cả 2 file
            # Giải mã base64 thành ảnh
            img_bytes = base64.b64decode(img_base64)
            img = Image.open(io.BytesIO(img_bytes))

            # Show ảnh
            img.show()
            break  # Thoát sau khi show, hoặc bỏ break nếu muốn tiếp tục loop
        else:
            print("Still generating...")