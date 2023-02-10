
# 1. waste not I and waste not II will override each other
import z3
# import src.skill as skill
import recipe
import crafter
import utils

SKILL_LIST_ALL = [
    'IDLE',
    'BasicSynthesis',
    'BasicSynthesis2',
    'BasicTouch',
    'MastersMend',
    'HastyTouch',       # banned
    'RapidSynthesis',   # banned
    'RapidSynthesis2',  # banned
    'Observe',
    'TricksOfTheTrade', # banned
    'WasteNot',
    'Veneration', 
    'StandardTouch',
    'GreatStrides',
    'Innovation',
    'FinalAppraisal',
    'WasteNotII',
    'ByregotsBlessing',
    'PreciseTouch',     # banned
    'MuscleMemory',
    'CarefulSynthesis',
    'CarefulSynthesis2',
    'Manipulation',
    'PrudentTouch',
    'FocusedSynthesis', # banned without combo
    'FocusedTouch',     # banned without combo
    'Reflect',
    'PreparatoryTouch',
    'GroundWork',
    'GroundWork2',
    'DelicateSynthesis',
    'IntensiveSynthesis', # banned
    'TrainedEye',
    'AdvancedTouch',
    'PrudentSynthesis',
    'TrainedFinesse'
]

SKILL_ENUM = dict(enumerate(SKILL_LIST_ALL))
SKILL_ENUM = dict([(value, key) for key, value in SKILL_ENUM.items()])
ID_ENUM = dict(enumerate(SKILL_LIST_ALL))


class skill:
    def __init__(self, crafter_info, recipe_info, max_step):
        self.max_step = max_step
        self.ID_sequence = utils.get_array(name="ID_sequence", length=self.max_step)
        self.constraint = []
        
        # self.add_level_constraint(crafter_info=crafter_info, recipe_info=recipe_info)
        

    def add_level_constraint(self, crafter_info:crafter.crafter, recipe_info:recipe.recipe):
        for index in range(self.max_step):
            skill_use_constraint = self.ID_sequence[index] == SKILL_ENUM['IDLE']
            # 不同等级可以放不同技能
            # 制作
            if crafter_info.level >= 1 and crafter_info.level < 31:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['BasicSynthesis'])
            # 制作2
            if crafter_info.level >= 31:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['BasicSynthesis2'])
            # 加工
            if crafter_info.level >= 5:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['BasicTouch'])
            # 精修
            if crafter_info.level >= 7:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['MastersMend'])
            # 观察
            if crafter_info.level >= 13:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['Observe'])
            # 俭约
            if crafter_info.level >= 15:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['WasteNot'])
            # 崇敬
            if crafter_info.level >= 15:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['Veneration'])
            # 中级加工
            if crafter_info.level >= 18:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['StandardTouch'])
            # 阔步
            if crafter_info.level >= 21:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['GreatStrides'])
            # 改革
            if crafter_info.level >= 26:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['Innovation'])
            # 最终确认
            if crafter_info.level >= 42:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['FinalAppraisal'])
            # 长期俭约
            if crafter_info.level >= 47:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['WasteNotII'])
            # 比尔格的祝福
            if crafter_info.level >= 50:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['ByregotsBlessing'])
            # 坚信
            if crafter_info.level >= 54:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['MuscleMemory'])
            # 模范制作
            if crafter_info.level >= 62 and crafter_info.level < 82:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['CarefulSynthesis'])
            # 模范制作2
            if crafter_info.level >= 82:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['CarefulSynthesis2'])
            # 掌握
            if crafter_info.level >= 65:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['Manipulation'])
            # 俭约加工
            if crafter_info.level >= 66:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['PrudentTouch'])
            # 注视制作
            if crafter_info.level >= 67:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['FocusedSynthesis'])
            # 注视加工
            if crafter_info.level >= 68:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['FocusedTouch'])
            # 闲静
            if crafter_info.level >= 69:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['Reflect'])
            # 坯料加工
            if crafter_info.level >= 71:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['PreparatoryTouch'])
            # 坯料制作
            if crafter_info.level >= 72 and crafter_info.level < 86:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['GroundWork'])
            # 坯料制作2
            if crafter_info.level >= 86:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['GroundWork2'])
            # 精密制作
            if crafter_info.level >= 76:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['DelicateSynthesis'])
            # 工匠的神速技巧
            if crafter_info.level >= 80 and (crafter_info.level - recipe_info.base_level) >= 10:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['TrainedEye'])
            # 上级加工
            if crafter_info.level >= 84:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['AdvancedTouch'])
            # 俭约制作
            if crafter_info.level >= 88:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['PrudentSynthesis'])
            # 工匠的神迹
            if crafter_info.level >= 90:
                skill_use_constraint = z3.Or(skill_use_constraint, self.ID_sequence[index] == SKILL_ENUM['TrainedFinesse'])
            self.constraint.append(skill_use_constraint)
        return utils.flatten_constraint_list(constraint_list=self.constraint)
        


        
