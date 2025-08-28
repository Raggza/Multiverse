from source.modules.angel import AngelImgGenerate
from source.modules.demon import DemonImgGenerate
from source.modules.dragon import DragonImgGenerate
from source.schemas.input import CharacterInput


class Pipeline:
    def __init__(self):
        self.angel_img_generate = AngelImgGenerate()
        self.demon_img_generate = DemonImgGenerate()
        self.dragon_img_generate = DragonImgGenerate()

    def invoke(self, character_input: CharacterInput) -> str:
        if character_input.race.lower() == "angel":
            return self.angel_img_generate.overlay_images()
        if character_input.race.lower() == "demon":
            return self.demon_img_generate.overlay_images()
        if character_input.race.lower() == "dragon":
            return self.dragon_img_generate.overlay_images()
        return ""
