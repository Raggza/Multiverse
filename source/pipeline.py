from source.modules.angel import AngelImgGenerate
from source.schemas.input import CharacterInput


class Pipeline:
    def __init__(self):
        self.angel_img_generate = AngelImgGenerate()

    def invoke(self, character_input: CharacterInput) -> str:
        if character_input.race == "angel":
            return self.angel_img_generate.overlay_images()
        return ""
