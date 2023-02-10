
import recipe
import crafter
# imporas status
import utils
import z3

class status():
    def __init__(self, crafter_info, recipe_info, max_step):
        self.constraint = []
        # maximum steps taken
        self.max_step = max_step 

        # crafter related
        # 剩余制作力
        self.remain_cp_status = utils.get_array(name="remain_cp_status", length=self.max_step)

        # recipe related
        # 剩余耐久
        self.remain_dur_status = utils.get_array(name="remain_dur_status", length=self.max_step)
        # 当前品质
        self.quality_status = utils.get_array(name="quality_status", length=self.max_step)
        # 当前进展
        self.progress_status = utils.get_array(name="progress_status", length=self.max_step)
        
        # crafting buffs
        # 内静状态
        self.inner_quiet_status = utils.get_array(name="inner_quiet_status", length=self.max_step)
        # 俭约状态
        self.waste_not_I_status = utils.get_array(name="waste_not_I_status", length=self.max_step)
        # 崇敬状态
        self.veneration_status = utils.get_array(name="veneration_status", length=self.max_step)
        # 阔步状态
        self.great_strides_status = utils.get_array(name="great_strides_status", length=self.max_step)
        # 改革状态
        self.innovation_status = utils.get_array(name="innovation_status",length=self.max_step)
        # 最终确认状态
        self.final_appraisal_status = utils.get_array(name="innovation_status",length=self.max_step)
        # 长期俭约状态
        self.waste_not_II_status = utils.get_array(name="waste_not_II_status", length=self.max_step)
        # 掌握状态
        self.manipulation_status = utils.get_array(name="manipulation_status", length=self.max_step)
        # 坚信状态
        self.muscle_memory_status = utils.get_array(name="muscle_memory_status", length=self.max_step)

        # combos
        # 可以发动中级加工
        self.standard_touch_combo = utils.get_boolean_array(name="standard_touch_combo", length=self.max_step)
        # 可以发动上级加工
        self.advanced_touch_combo = utils.get_boolean_array(name="advanced_touch_combo", length=self.max_step)
        # 可以发动比尔格的祝福
        self.byregot_Blessing_combo = utils.get_boolean_array(name="byregot_Blessing_combo", length=self.max_step)
        # 可以发动注视制作
        self.focused_synthesis_combo = utils.get_boolean_array(name="focused_synthesis_combo", length=self.max_step)
        # 可以发动注视加工
        self.focused_touch_combo = utils.get_boolean_array(name="focused_synthesis_combo", length=self.max_step)
        # 可以发动坚信
        self.muscle_memory_combo = utils.get_boolean_array(name="muscle_memory_combo", length=self.max_step)
        # 可以发动闲静
        self.reflect_combo = utils.get_boolean_array(name="reflect_combo", length=self.max_step)
        # 可以发动工匠的神技
        self.trained_finesse_combo = utils.get_boolean_array(name="trained_finesse_combo", length=self.max_step)
        # 可以发动工匠的神速技巧
        self.trained_eye_combo = utils.get_boolean_array(name="trained_eye_combo", length=self.max_step)

        # the range of status
        self.constraint_flattten = self.add_constraints(crafter_info=crafter_info, recipe_info=recipe_info)
        pass
    
    def add_range(self, status_list:list, upper_bound):
        for i in range(self.max_step):
            self.constraint.append(status_list[i] <= upper_bound)
            self.constraint.append(status_list[i] >= 0)
    
    def ban_use(self, status_list:list):
        for i in range(self.max_step):
            self.constraint.append(status_list[i] == False)

    def first_launch_only(self, status_list:list):
        for i in range(self.max_step):
            if i > 0:
                self.constraint.append(status_list[i]==False)
        self.constraint.append(status_list[0]==True)

    def add_constraints(self, crafter_info:crafter.crafter, recipe_info:recipe.recipe):
        # initialize
        self.constraint.append(self.remain_cp_status[0] == crafter_info.cp)
        self.constraint.append(self.remain_dur_status[0] == recipe_info.durability)
        self.constraint.append(self.progress_status[0] == 0)

        # we assume quality start from zero
        self.constraint.append(self.quality_status[0] == 0)

        # initialize bufs
        self.constraint.append(self.inner_quiet_status[0] == 0)
        self.constraint.append(self.waste_not_I_status[0] == 0)
        self.constraint.append(self.veneration_status[0] == 0)
        self.constraint.append(self.great_strides_status[0] == 0)
        self.constraint.append(self.innovation_status[0] == 0)
        self.constraint.append(self.final_appraisal_status[0] == 0)
        self.constraint.append(self.waste_not_II_status[0] == 0)
        self.constraint.append(self.manipulation_status[0] == 0)
        self.constraint.append(self.muscle_memory_status[0] == 0)

        self.constraint.append(self.standard_touch_combo[0] == False)
        self.constraint.append(self.advanced_touch_combo[0] == False)
        self.constraint.append(self.byregot_Blessing_combo[0] == False)
        self.constraint.append(self.focused_synthesis_combo[0] == False)
        self.constraint.append(self.focused_touch_combo[0] == False)
        self.constraint.append(self.trained_finesse_combo[0] == False)


        # 内静档数不超过10
        # 11级 习得内静
        self.add_range(self.inner_quiet_status, 10)

        # 俭约持续作业次数为4
        # 15级 习得俭约
        self.add_range(self.waste_not_I_status, 4)

        
        # 崇敬持续作业次数为4
        # 15级 习得崇敬
        self.add_range(self.veneration_status, 4)
       
        # 阔步持续作业次数为3
        # 21级 习得阔步
        self.add_range(self.great_strides_status, 3)

        # 改革持续作业次数为4
        # 26级 习得改革
        self.add_range(self.innovation_status, 4)

        # 最终确认持续作业次数为5
        self.add_range(self.final_appraisal_status, 5)

        # 长期俭约持续作业次数为8
        self.add_range(self.waste_not_II_status, 8)

        # 掌握持续作业次数为8
        # 65级 习得掌握
        self.add_range(self.manipulation_status, 8)

        # 坚信持续作业次数为5
        self.add_range(self.muscle_memory_status, 5)

        self.add_range(self.remain_dur_status, recipe_info.durability)
        
        # 18级习得中级加工
        # if (crafter_info.level < 18):
        #     self.ban_use(self.standard_touch_combo)
        # 84级习得上级加工
        # if (crafter_info.level < 84):
        #     self.ban_use(self.advanced_touch_combo)
        # 50级习得比尔格的祝福
        # if (crafter_info.level < 50):
        #     self.ban_use(self.byregot_Blessing_combo)
        # 67级习得注视制作
        # if (crafter_info.level < 67):
        #     self.ban_use(self.focused_synthesis_combo)
        # 68级习得注视加工
        # if (crafter_info.level < 68):
        #     self.ban_use(self.focused_touch_combo)
        # 54级习得坚信
        if (crafter_info.level < 54):
            self.ban_use(self.muscle_memory_combo)
        else:
            self.first_launch_only(self.muscle_memory_combo)
        # 69级习得闲静
        if (crafter_info.level < 69):
            self.ban_use(self.reflect_combo)
        else:
            self.first_launch_only(self.reflect_combo)
        
        return utils.flatten_constraint_list(constraint_list=self.constraint)
    
    



    
