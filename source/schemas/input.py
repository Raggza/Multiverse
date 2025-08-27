from pydantic import BaseModel, Field

class CharacterInput(BaseModel):  
    race: str = Field(..., title="Race of the character")
    sub_race: str = Field(..., title="Subrace or detail description of the character")
    weapon: str = Field(..., title="Weapon of the character")
    model_name: str = Field(..., title="Model name")
