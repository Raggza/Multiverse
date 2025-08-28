import random
import base64
import io
from pathlib import Path
from collections import defaultdict
from typing import List

from PIL import Image
from source.utils.config_utils import get_config
from source.schemas.input import CharacterInput


class DwarfImgGenerate:
    def __init__(self):
        self.root_file = Path(get_config("image", "dwarf"))
        self.part = get_config("image", "dwarf_parts")

    def _filter_parts(self, input: CharacterInput) -> defaultdict:
        """Build dictionary of available parts based on dwarf sub-race."""
        body_parts = defaultdict(list)

        for f in self.part:
            prefix = f.split("-")[0]
            if prefix == "1" and input.sub_race.lower() != "ancient dwarf":
                continue
            body_parts[prefix].append(f)

        return body_parts

    def _apply_race_rules(self, body_parts: defaultdict, sub_race: str):
        """Modify parts list based on sub-race or random variation."""
        sub_race = sub_race.lower()

        # Rules shared between Gray Dwarf and random variant
        gray_removals = {
            "2": ["2-ear-3.png", "2-ear-4.png"],
            "4": ["4-face-4.png", "4-face-5.png", "4-face-6.png"],
            "5": ["5-body-1.png", "5-body-7.png"],
            "8": ["8-leg-4.png"],
        }
        gray_overrides = {
            "6": ["6-handleft-3.png"],
            "7": ["7-handright-3.png"],
        }

        other_removals = {
            "2": ["2-ear-1.png", "2-ear-2.png"],
            "4": ["4-face-1.png", "4-face-2.png", "4-face-3.png"],
            "5": ["5-body-6.png"],
            "6": ["6-handleft-3.png"],
            "7": ["7-handright-3.png"],
            "8": ["8-leg-3.png"],
        }

        def remove_parts(parts_map: dict):
            for k, items in parts_map.items():
                for item in items:
                    if item in body_parts[k]:
                        body_parts[k].remove(item)

        if sub_race == "gray dwarf":
            remove_parts(gray_removals)
            body_parts.update(gray_overrides)
        else:
            if random.random() < 0.36:
                remove_parts(gray_removals)
                body_parts.update(gray_overrides)
            else:
                remove_parts(other_removals)

    def _get_parts_list(self, input: CharacterInput) -> List[Path]:
        """Return ordered list of image paths to compose the dwarf."""
        body_parts = self._filter_parts(input)
        self._apply_race_rules(body_parts, input.sub_race)

        # Randomly select 1 from each part group
        parts_choice = {k: random.choice(v) for k, v in body_parts.items() if v}

        # Order by numeric prefix
        ordered_files = [
            Path(self.root_file, fname)
            for _, fname in sorted(parts_choice.items(), key=lambda x: int(x[0]))
        ]

        # Reverse order so later parts overlay earlier ones
        return ordered_files[::-1]

    def overlay_images(self, input: CharacterInput) -> str:
        """Generate composite dwarf image and return base64 string."""
        image_paths = self._get_parts_list(input)
        base = Image.open(image_paths[0]).convert("RGBA")
        canvas = Image.new("RGBA", base.size, (255, 255, 255, 0))  # transparent bg

        for path in image_paths:
            img = Image.open(path).convert("RGBA")
            canvas.paste(img, (0, 0), img)

        buffer = io.BytesIO()
        canvas.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")


if __name__ == "__main__":
    generator = DwarfImgGenerate()
    char_input = CharacterInput(race="dwarf", sub_race="mountain dwarf", weapon="")
    img_base64 = generator.overlay_images(char_input)

    img_bytes = base64.b64decode(img_base64)
    img = Image.open(io.BytesIO(img_bytes))
    img.show()
