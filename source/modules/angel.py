import random
import base64
import io

from PIL import Image
from pathlib import Path
from collections import defaultdict

from source.utils.config_utils import get_config

class AngelImgGenerate():
    def __init__(self):
        self.angel_parts = get_config("image","angel_parts")
        self.root_file = get_config("image","angel")

    def _get_parts_list(self):
        body_parts = defaultdict(list)
        for f in self.angel_parts:
            prefix = f.split("-")[0]
            body_parts[prefix].append(f)

        parts_choice = {k: random.choice(v) for k, v in body_parts.items()}

        body_parts_list = []
        for i in range(8, 0, -1):
            path = Path(f"{self.root_file}\\{parts_choice[str(i)]}")
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

        return base64_str


if __name__ == "__main__":
    generator = AngelImgGenerate()
    img_base64 = generator.overlay_images()

    # Giải mã base64 thành ảnh
    img_bytes = base64.b64decode(img_base64)
    img = Image.open(io.BytesIO(img_bytes))

    # Show ảnh
    img.show()