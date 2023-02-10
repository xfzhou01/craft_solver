import z3

class recipe:
    def __init__(self, base_level, difficulty, durability, level, max_quality, name, progress_divider, 
                 progress_modifier, quality_divider, quality_modifier, recipe_id, stars) -> None:
        self.base_level = base_level
        self.difficulty = difficulty
        self.durability = durability
        self.level = level
        self.max_quality = max_quality
        self.name = name
        self.progress_divider = progress_divider
        self.progress_modifier = progress_modifier
        self.quality_divider = quality_divider
        self.quality_modifier = quality_modifier
        self.recipe_id = recipe_id
        self.stars = stars
        pass

