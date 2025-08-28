import random
import base64
import io

from PIL import Image
from pathlib import Path
from collections import defaultdict

from source.utils.config_utils import get_config
from source.schemas.input import CharacterInput


class DragonImgGenerate:
    FIXED_PARTS = {
        "crimson dragon": ("3-face-7.png", "5-body-6.png"),
        "stone dragon": ("3-face-6.png", "5-body-5.png"),
        "amethyst dragon": ("3-face-5.png", "5-body-5.png"),
        "ancient dragon": ("3-face-1.png", "5-body-1.png"),
        "undead dragon": ("3-face-3.png", "5-body-3.png"),
        "zephyrian dragon": ("3-face-2.png", "5-body-2.png"),
        "tideborn dragon": ("3-face-4.png", "5-body-4.png"),
        "thunder dragon": ("3-face-1.png", "5-body-1.png"),
        "flame dragon": ("3-face-7.png", "5-body-6.png"),
        "ice dragon": ("3-face-2.png", "5-body-2.png"),
    }

    def __init__(self):
        self.root_file = get_config("image", "dragon")
        self.part = get_config("image", "dragon_parts")

    def _get_parts_list(self, input: CharacterInput):
        body_parts = defaultdict(list)
        for f in self.part:
            prefix = f.split("-")[0]
            if (
                prefix == "3"
                or prefix == "5"
                and input.sub_race.lower() != "chaos dragon"
            ):
                continue
            else:
                body_parts[prefix].append(f)

        sub_race_key = input.sub_race.lower()

        if sub_race_key in self.FIXED_PARTS:
            face, body = self.FIXED_PARTS[sub_race_key]
            body_parts["3"] = [face]
            body_parts["5"] = [body]

        parts_choice = {k: [random.choice(v)] for k, v in body_parts.items()}

        parts_choice_order = dict(
            sorted(parts_choice.items(), key=lambda item: int(item[0]))
        )
        temp_list = [
            item for sublist in parts_choice_order.values() for item in sublist
        ]
        body_parts_list = []
        for item in temp_list[::-1]:
            path = Path(f"{self.root_file}\\{item}")
            body_parts_list.append(path)

        return body_parts_list

    def overlay_images(self, input: CharacterInput):
        image_paths = self._get_parts_list(input)
        base = Image.open(image_paths[0]).convert("RGBA")
        canvas = Image.new("RGBA", base.size, (255, 255, 255, 0))

        for path in image_paths:
            img = Image.open(path).convert("RGBA")
            canvas.paste(img, (0, 0), img)

        buffer = io.BytesIO()
        canvas.save(buffer, format="PNG")
        base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return base64_str


if __name__ == "__main__":
    generator = DragonImgGenerate()
    input = CharacterInput(race="Dragon", sub_race="Ice Dragon", weapon="")
    img_base64 = generator.overlay_images(input)
    img_bytes = base64.b64decode(img_base64)
    img = Image.open(io.BytesIO(img_bytes))
    img.show()
