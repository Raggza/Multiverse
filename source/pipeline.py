from source.modules.angel import AngelImgGenerate
from source.modules.demon import DemonImgGenerate
from source.modules.dragon import DragonImgGenerate
from source.modules.dryad import DryadImgGenerate
from source.modules.dwarf import DwarfImgGenerate

from source.schemas.input import CharacterInput


class Pipeline:
    def __init__(self):
        self.angel_img_generate = AngelImgGenerate()
        self.demon_img_generate = DemonImgGenerate()
        self.dragon_img_generate = DragonImgGenerate()
        self.dryad_img_generate = DryadImgGenerate()
        self.dwarf_img_generate = DwarfImgGenerate()

    def invoke(self, character_input: CharacterInput) -> str:
        if character_input.race.lower() == "angel":
            return self.angel_img_generate.overlay_images()
        if character_input.race.lower() == "demon":
            return self.demon_img_generate.overlay_images()
        if character_input.race.lower() == "dragon":
            return self.dragon_img_generate.overlay_images(character_input)
        if character_input.race.lower() == "dryad":
            return self.dryad_img_generate.overlay_images()
        if character_input.race.lower() == "dryad":
            return self.dwarf_img_generate.overlay_images(character_input)
        return ""
