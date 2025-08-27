PROMPT = """
Instruction: Create a Stable Diffusion prompt based on the following details:
- Race: {{ race }}
- Description / Sub-race: {{ sub_race }}
- Weapon: {{ weapon }}
- Art style: Anime

Note: 
- The prompt **must** clearly describe the character **holding** the specified weapon.
- Provide both a **prompt** and a **negative prompt**.
"""
