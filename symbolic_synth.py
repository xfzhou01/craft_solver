import skill
import recipe
import crafter
import status
import utils
import z3

class symbolic_synthesizer:
    def __init__(self, recipe_info:recipe.recipe,
                       crafter_info:crafter.crafter, 
                       skill_info:skill.skill, 
                       status_info:status.status
                ):
        self.recipe_info = recipe_info
        self.crafter_info = crafter_info
        self.base_prog_inc = utils.cal_basic_progress_increase(recipe_info=recipe_info, crafter_info=crafter_info)
        self.base_qual_inc = utils.cal_basic_quality_increase(recipe_info=recipe_info, crafter_info=crafter_info)
        
        self.status_info = status_info
        self.skill_info = skill_info
        self.constraint = []
    def dur_loss_common_5(self, step):
        maniputation_effective = z3.And(self.status_info.manipulation_status[step] > 0, self.status_info.remain_dur_status[step] > 5)
        dur_loss = z3.If(maniputation_effective, 0, 5)
        return dur_loss


    def dur_loss_common_10(self, step):
        waste_not_effective = z3.Or(self.status_info.waste_not_I_status[step] > 0, self.status_info.waste_not_II_status[step] > 0)
        manipulation_effective = self.status_info.manipulation_status[step] > 0
        dur_loss_after_waste_not_process = z3.If(waste_not_effective, 5, 10)
        dur_enough_to_next_step = self.status_info.remain_dur_status[step] > dur_loss_after_waste_not_process
        dur_loss_after_manipulation_process_if_manpulation_effective = z3.If(dur_enough_to_next_step, dur_loss_after_waste_not_process-5, dur_loss_after_waste_not_process)
        dur_loss_after_manipulation_process = z3.If(manipulation_effective, dur_loss_after_manipulation_process_if_manpulation_effective, dur_loss_after_waste_not_process)
        dur_loss = dur_loss_after_manipulation_process
        return dur_loss

    def dur_loss_common_20(self, step):        
        waste_not_effective = z3.Or(self.status_info.waste_not_I_status[step] > 0, self.status_info.waste_not_II_status[step] > 0)
        manipulation_effective = self.status_info.manipulation_status[step] > 0
        dur_loss_after_waste_not_process = z3.If(waste_not_effective, 10, 20)
        dur_enough_to_next_step = self.status_info.remain_dur_status[step] > dur_loss_after_waste_not_process
        dur_loss_after_manipulation_process_if_manpulation_effective = z3.If(dur_enough_to_next_step, dur_loss_after_waste_not_process-5, dur_loss_after_waste_not_process)
        dur_loss_after_manipulation_process = z3.If(manipulation_effective, dur_loss_after_manipulation_process_if_manpulation_effective, dur_loss_after_waste_not_process)
        dur_loss = dur_loss_after_manipulation_process
        return dur_loss
    
    def dur_gain_common_0(self, step):
        manipulation_effective = self.status_info.manipulation_status[step] > 0
        dur_gain = z3.If(manipulation_effective, 5, 0)
        return dur_gain
    
    def dur_gain_common_30(self, step):
        manipulation_effective = self.status_info.manipulation_status[step] > 0
        dur_gain = z3.If(manipulation_effective, 35, 30)
        return dur_gain

    def progress_gain_common(self, step, skill_name):
        p1 = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                     skill_can_increase_progress=True,
                                     status_has_muscle_memory=True,
                                     status_has_veneration=True,
                                     status_dur_not_enough=False)
        p2 = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                     skill_can_increase_progress=True,
                                     status_has_muscle_memory=True,
                                     status_has_veneration=False,
                                     status_dur_not_enough=False)
        p3 = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                     skill_can_increase_progress=True,
                                     status_has_muscle_memory=False,
                                     status_has_veneration=True,
                                     status_dur_not_enough=False)
        p4 = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                     skill_can_increase_progress=True,
                                     status_has_muscle_memory=False,
                                     status_has_veneration=False,
                                     status_dur_not_enough=False)
        status_has_muscle_memory = self.status_info.muscle_memory_status[step] > 0
        status_has_veneration = self.status_info.veneration_status[step] > 0 
        status_has_both = z3.And(status_has_muscle_memory, status_has_veneration)
        progress_increase_value = z3.If(status_has_both, p1, z3.If(status_has_muscle_memory, p2, z3.If(status_has_veneration, p3, p4)))
        status_has_final_appraisal = self.status_info.final_appraisal_status[step] > 0
        progress_value_next = progress_increase_value + self.status_info.progress_status[step]
        use_final_appraisal = z3.And(progress_value_next >= self.recipe_info.difficulty, status_has_final_appraisal)
        final_progress_value = z3.If(use_final_appraisal, self.recipe_info.difficulty-1, progress_value_next)
        return (final_progress_value, use_final_appraisal)

    def progress_gain_ground_work(self, step, skill_name):

        p1 = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                     skill_can_increase_progress=True,
                                     status_has_muscle_memory=True,
                                     status_has_veneration=True,
                                     status_dur_not_enough=False)
        p2 = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                     skill_can_increase_progress=True,
                                     status_has_muscle_memory=True,
                                     status_has_veneration=False,
                                     status_dur_not_enough=False)
        p3 = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                     skill_can_increase_progress=True,
                                     status_has_muscle_memory=False,
                                     status_has_veneration=True,
                                     status_dur_not_enough=False)
        p4 = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                     skill_can_increase_progress=True,
                                     status_has_muscle_memory=False,
                                     status_has_veneration=False,
                                     status_dur_not_enough=False)

        p1_nd = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                        skill_can_increase_progress=True,
                                        status_has_muscle_memory=True,
                                        status_has_veneration=True,
                                        status_dur_not_enough=True)
        p2_nd = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                        skill_can_increase_progress=True,
                                        status_has_muscle_memory=True,
                                        status_has_veneration=False,
                                        status_dur_not_enough=True)
        p3_nd = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                        skill_can_increase_progress=True,
                                        status_has_muscle_memory=False,
                                        status_has_veneration=True,
                                        status_dur_not_enough=True)
        p4_nd = self.calculate_progress(skill_ID=skill.SKILL_ENUM[skill_name],
                                        skill_can_increase_progress=True,
                                        status_has_muscle_memory=False,
                                        status_has_veneration=False,
                                        status_dur_not_enough=True)
                            
        status_has_muscle_memory = self.status_info.muscle_memory_status[step] > 0
        status_has_veneration = self.status_info.veneration_status[step] > 0 
        status_has_both = z3.And(status_has_muscle_memory, status_has_veneration)
        # when there is waste not I/II, the dur < 10 called dur not enough
        # otherwise, dur < 20 called not enough
        status_dur_not_enough_waste_not = z3.And(z3.Or(self.status_info.waste_not_I_status[step]>0, self.status_info.waste_not_II_status[step]>0), self.status_info.remain_dur_status[step] < 10)
        status_dur_not_enough_common = z3.And(z3.Not(z3.Or(self.status_info.waste_not_I_status[step]>0, self.status_info.waste_not_II_status[step]>0)), self.status_info.remain_dur_status < 20)
        status_dur_not_enough = z3.And(status_dur_not_enough_common, status_dur_not_enough_waste_not)


        progress_increase_value_dur_enough = z3.If(status_has_both, p1, z3.If(status_has_muscle_memory, p2, z3.If(status_has_veneration, p3, p4)))
        progress_increase_value_dur_not_enough = z3.If(status_has_both, p1_nd, z3.If(status_has_muscle_memory, p2_nd, z3.If(status_has_veneration, p3_nd, p4_nd)))
        progress_increase_value = z3.If(status_dur_not_enough, progress_increase_value_dur_not_enough, progress_increase_value_dur_enough)
        status_has_final_appraisal = self.status_info.final_appraisal_status[step] > 0
        progress_value_next = progress_increase_value + self.status_info.progress_status[step]
        use_final_appraisal = z3.And(progress_value_next >= self.recipe_info.difficulty, status_has_final_appraisal)
        final_progress_value = z3.If(use_final_appraisal, self.recipe_info.difficulty-1, progress_value_next)
        return (final_progress_value, use_final_appraisal)


    def quality_gain_common(self, step, skill_name):
        p_gs_inn_list = []
        p_gs_list = []
        p_inn_list = []
        p_no_buf_list = []
        # the level of inner quiet is 0 ~ 10
        for i in range(11):
            p_gs_inn_tmp = self.calculate_quality(skill_ID=skill.SKILL_ENUM[skill_name],
                                                  skill_can_increase_quality=True,
                                                  status_has_great_stride=True,
                                                  status_has_innovation=True,
                                                  status_inner_quiet_level=i)
            p_gs_tmp = self.calculate_quality(skill_ID=skill.SKILL_ENUM[skill_name],
                                              skill_can_increase_quality=True,
                                              status_has_great_stride=True,
                                              status_has_innovation=False,
                                              status_inner_quiet_level=i)
            p_inn_tmp = self.calculate_quality(skill_ID=skill.SKILL_ENUM[skill_name],
                                               skill_can_increase_quality=True,
                                               status_has_great_stride=False,
                                               status_has_innovation=True,
                                               status_inner_quiet_level=i)
            p_no_buf_tmp = self.calculate_quality(skill_ID=skill.SKILL_ENUM[skill_name],
                                                  skill_can_increase_quality=True,
                                                  status_has_great_stride=False,
                                                  status_has_innovation=False,
                                                  status_inner_quiet_level=i)
            p_gs_inn_list.append(p_gs_inn_tmp)
            p_gs_list.append(p_gs_tmp)
            p_inn_list.append(p_inn_tmp)
            p_no_buf_list.append(p_no_buf_tmp)
        p_gs_inn_inner_quiet_select = utils.select_array(arr=p_gs_inn_list, index=self.status_info.inner_quiet_status[step])
        p_gs_inner_quiet_select = utils.select_array(arr=p_gs_inn_list, index=self.status_info.inner_quiet_status[step])
        p_inn_inner_quiet_select = utils.select_array(arr=p_inn_list, index=self.status_info.inner_quiet_status[step])
        p_no_buf_select = utils.select_array(arr=p_no_buf_list, index=self.status_info.inner_quiet_status[step])
        status_has_great_stride = self.status_info.great_strides_status[step] > 0
        status_has_innovation = self.status_info.innovation_status[step] > 0
        status_has_both = z3.And(status_has_great_stride, status_has_innovation)
        quality_increase_value = z3.If(status_has_both, p_gs_inn_inner_quiet_select, z3.If(status_has_great_stride, p_gs_inner_quiet_select, z3.If(status_has_innovation, p_inn_inner_quiet_select, p_no_buf_select)))
        quality_value_next = quality_increase_value + self.status_info.quality_status[step]
        #print(quality_value_next)
        return quality_value_next

    def time_countdown_buff_common(self, step, status_list):
        has_buff = status_list[step] > 0
        return z3.If(has_buff, status_list[step]-1, 0)

    # step: ????????????????????????
    def basic_synthesis_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step])
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ???????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='BasicSynthesis', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ??????-1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == z3.If(use_final_appraisal, 0, self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status)))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? ??????0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step])
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)
    
    def basic_synthesis_2_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step])
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ???????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='BasicSynthesis2', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ??????-1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == z3.If(use_final_appraisal, 0, self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status)))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? ??????0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step])
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)
    
    def basic_touch_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 18 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-18)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='BasicTouch')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ?????? +1??? ????????????
        if (self.crafter_info.level >= 11):
            constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == z3.If(self.status_info.inner_quiet_status[step]==10, 10, self.status_info.inner_quiet_status[step]+1))
        else:
            constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? ????????? 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == True)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == True) # ?????????????????????????????????
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == (self.status_info.inner_quiet_status[step] >= 9)) 
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)
    
    def masters_mend_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 88 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-88)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_30(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step]) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)
    # ??????
    def observe_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 7 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-7)
        # ????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_0(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step]) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == True)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == True)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)
    # ??????
    def waste_not_I_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 56 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-56)
        # ????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_0(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? ??????4
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == 4)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? ?????????
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step]) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)
    # ??????
    def veneration_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 18 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-18)
        # ????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_0(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? ??????4
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == 4)
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step]) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????
    def standard_touch_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 32 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-32)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='StandardTouch')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ?????? +1??? ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == z3.If(self.status_info.inner_quiet_status[step]==10, 10, self.status_info.inner_quiet_status[step]+1))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? ??????
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == True)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == True) # ?????????????????????????????????
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == (self.status_info.inner_quiet_status[step] >= 9)) 
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)


    # ??????
    def great_strides_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 32 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-32)
        # ????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_0(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? ??????3
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 3)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step]) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ??????
    def innovation_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 18 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-18)
        # ????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_0(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? ??????4
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == 4)
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step]) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)
    
    # ????????????
    def final_appraisal_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 1 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-1)
        # ????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_0(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ???????????? ??????5
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == 5)
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step]) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????
    def waste_not_II_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 98 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-98)
        # ????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_0(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? ?????????
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? ??????8
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == 8)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step]) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ??????????????????
    def byregots_blessing_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 24 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-24)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='ByregotsBlessing')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? ??????
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == False) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == False) 
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ??????
    def muscle_memory_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 6 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-6)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ???????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='MuscleMemory', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ?????????0 ??????????????????????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == 0)
        # ?????????0 ??????????????????????????????
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == 0)
        # ?????? ???0 ??????????????????????????????
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == 0)
        # ?????? ???0 ?????????????????????????????? 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? ???0 ??????????????????????????????
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == 0)
        # ???????????? ???0 ??????????????????????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == 0)
        # ???????????? ???0 ??????????????????????????????
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == 0)
        # ?????? ???0 ??????????????????????????????
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == 0)
        # ?????? ??????5
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 5)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????
    def careful_synthesis_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 7 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-7)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ???????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='CarefulSynthesis', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == z3.If(use_final_appraisal, 0, self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status)))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? ??????0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step])
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????2
    def careful_synthesis_2_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 7 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-7)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ???????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='CarefulSynthesis2', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == z3.If(use_final_appraisal, 0, self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status)))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? ??????0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step])
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ??????
    def manipulation_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 96 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-96)
        # ????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_0(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? ??????8
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == 8)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step]) 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????
    def prudent_touch_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 25 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-25)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_5(step))
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='PrudentTouch')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ?????? +1??? ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == z3.If(self.status_info.inner_quiet_status[step]==10, 10, self.status_info.inner_quiet_status[step]+1))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? ??????
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == True) # ?????????????????????????????????
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == (self.status_info.inner_quiet_status[step] >= 9)) 
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????
    def focused_synthesis_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 5 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-5)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ???????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='FocusedSynthesis', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ??????-1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == z3.If(use_final_appraisal, 0, self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status)))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? ??????0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step])
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)
    # ????????????
    def focused_touch_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 18 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-18)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='FocusedTouch')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ?????? +1??? ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == z3.If(self.status_info.inner_quiet_status[step]==10, 10, self.status_info.inner_quiet_status[step]+1))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? ??????
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == True) # ?????????????????????????????????
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == (self.status_info.inner_quiet_status[step] >= 9)) 
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ??????
    def reflect_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 6 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-6)
        # ?????????????????? ??????????????????????????????????????????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step])
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='Reflect')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ?????? ??????????????????????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == 0)
        # ?????? 2
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == 2)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == 0)
        # ???????????? 0
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == 0)
        # ???????????? 0
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == True) # ?????????????????????2?????????
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == False) 
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????
    def preparatory_touch_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 40 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-40)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_20(step))
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='PreparatoryTouch')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ?????? +2??? ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == z3.If(self.status_info.inner_quiet_status[step]>=9, 10, self.status_info.inner_quiet_status[step]+2))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? ??????
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == True) # 
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == (self.status_info.inner_quiet_status[step] >= 8)) 
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????
    def ground_work_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 18 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-18)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_20(step))
        # ???????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='GroundWork', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ??????-1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == z3.If(use_final_appraisal, 0, self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status)))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? ??????0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step])
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)

        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????2
    def ground_work_2_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 18 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-18)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_20(step))
        # ???????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='GroundWork2', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ??????-1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == z3.If(use_final_appraisal, 0, self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status)))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? ??????0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step])
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????
    def delicate_synthesis_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 32 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-32)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='DelicateSynthesis')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='DelicateSynthesis', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ?????? +1
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == z3.If(self.status_info.inner_quiet_status[step]==10, 10, self.status_info.inner_quiet_status[step]+1))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == z3.If(use_final_appraisal, 0, self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status)))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? ??????0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == True)
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == (self.status_info.inner_quiet_status[step] >= 9))
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ?????????????????????
    def trained_eye_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 250 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-250)
        # ????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.recipe_info.durability)
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.recipe_info.max_quality)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == 0)
        # ???????????? 0
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == 0)
        # ???????????? 0
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == 0)
        # ?????? 0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ????????????
    def advanced_touch_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 46 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-46)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_10(step))
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='AdvancedTouch')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ?????? +1??? ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == z3.If(self.status_info.inner_quiet_status[step]==10, 10, self.status_info.inner_quiet_status[step]+1))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? ??????
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == 0)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == True) # ?????????????????????????????????
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == (self.status_info.inner_quiet_status[step] >= 9)) 
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp) 
    
    # ????????????
    def prudent_synthesis_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 18 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-18)
        # ??????????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]-self.dur_loss_common_5(step))
        # ????????????
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == self.status_info.quality_status[step])
        # ????????????
        (final_progress_value, use_final_appraisal) = self.progress_gain_common(skill_name='PrudentSynthesis', step=step)
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == final_progress_value)
        # ????????????
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ????????????
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == z3.If(use_final_appraisal, 0, self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status)))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? ??????0
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == 0)
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step])
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    # ???????????????
    def trained_finesse_symbolic_do(self, step):
        # ???????????????????????????constraint list
        constraint_list_tmp = []
        # ?????? 32 cp
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1] == self.status_info.remain_cp_status[step]-32)
        # ???????????????
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step]+self.dur_gain_common_0(step))
        # ??????????????????
        quality_new = self.quality_gain_common(step=step, skill_name='TrainedFinesse')
        constraint_list_tmp.append(self.status_info.quality_status[step+1] == quality_new)
        # ????????????
        constraint_list_tmp.append(self.status_info.progress_status[step+1] == self.status_info.progress_status[step])
        # ????????????????????????10
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == 10)
        # ?????? -1
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_I_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.veneration_status))
        # ?????? -1 
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.great_strides_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.innovation_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.final_appraisal_status))
        # ???????????? -1
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.waste_not_II_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.manipulation_status))
        # ?????? -1
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.time_countdown_buff_common(step=step, status_list=self.status_info.muscle_memory_status))
        # combos
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == True)
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == False)
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == True)
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == False)
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)

    def IDLE_symbolic_do(self, step):
        # ???????????????????????????constraint list
        # ?????????
        constraint_list_tmp = []
        constraint_list_tmp.append(self.status_info.remain_cp_status[step+1]  == self.status_info.remain_cp_status[step])
        constraint_list_tmp.append(self.status_info.remain_dur_status[step+1] == self.status_info.remain_dur_status[step])
        constraint_list_tmp.append(self.status_info.quality_status[step+1]    == self.status_info.quality_status[step])
        constraint_list_tmp.append(self.status_info.progress_status[step+1]   == self.status_info.progress_status[step])
        constraint_list_tmp.append(self.status_info.inner_quiet_status[step+1] == self.status_info.inner_quiet_status[step])
        constraint_list_tmp.append(self.status_info.waste_not_I_status[step+1] == self.status_info.waste_not_I_status[step])
        constraint_list_tmp.append(self.status_info.veneration_status[step+1] == self.status_info.veneration_status[step])
        constraint_list_tmp.append(self.status_info.great_strides_status[step+1] == self.status_info.great_strides_status[step])
        constraint_list_tmp.append(self.status_info.innovation_status[step+1] == self.status_info.innovation_status[step])
        constraint_list_tmp.append(self.status_info.final_appraisal_status[step+1] == self.status_info.final_appraisal_status[step])
        constraint_list_tmp.append(self.status_info.waste_not_II_status[step+1] == self.status_info.waste_not_II_status[step])
        constraint_list_tmp.append(self.status_info.manipulation_status[step+1] == self.status_info.manipulation_status[step])
        constraint_list_tmp.append(self.status_info.muscle_memory_status[step+1] == self.status_info.muscle_memory_status[step])
        constraint_list_tmp.append(self.status_info.standard_touch_combo[step+1] == self.status_info.standard_touch_combo[step])
        constraint_list_tmp.append(self.status_info.advanced_touch_combo[step+1] == self.status_info.advanced_touch_combo[step])
        constraint_list_tmp.append(self.status_info.byregot_Blessing_combo[step+1] == self.status_info.byregot_Blessing_combo[step])
        constraint_list_tmp.append(self.status_info.focused_synthesis_combo[step+1] == self.status_info.focused_synthesis_combo[step])
        constraint_list_tmp.append(self.status_info.focused_touch_combo[step+1] == self.status_info.focused_touch_combo[step])
        constraint_list_tmp.append(self.status_info.muscle_memory_combo[step+1] == self.status_info.muscle_memory_combo[step])
        constraint_list_tmp.append(self.status_info.reflect_combo[step+1] == self.status_info.reflect_combo[step])
        constraint_list_tmp.append(self.status_info.trained_finesse_combo[step+1] == self.status_info.trained_finesse_combo[step])
        constraint_list_tmp.append(self.status_info.trained_eye_combo[step+1] == self.status_info.trained_eye_combo[step])
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)


    def skill_launch_symbolic_constraint(self, step):
        skill_ID = self.skill_info.ID_sequence[step]
        lauch_IDLE = z3.If(skill_ID==skill.SKILL_ENUM['IDLE'], self.IDLE_symbolic_do(step), False)
        launch_BasicSynthesis = z3.If(skill_ID==skill.SKILL_ENUM['BasicSynthesis'], self.basic_synthesis_symbolic_do(step), lauch_IDLE)
        launch_BasicSynthesis2 = z3.If(skill_ID==skill.SKILL_ENUM['BasicSynthesis2'], self.basic_synthesis_2_symbolic_do(step), launch_BasicSynthesis)
        launch_BasicTouch = z3.If(skill_ID==skill.SKILL_ENUM['BasicTouch'], self.basic_touch_symbolic_do(step), launch_BasicSynthesis2)
        launch_MasterMend = z3.If(skill_ID==skill.SKILL_ENUM['MastersMend'], self.masters_mend_symbolic_do(step), launch_BasicTouch)
        launch_Observe = z3.If(skill_ID==skill.SKILL_ENUM['Observe'], self.observe_symbolic_do(step), launch_MasterMend)
        launch_WasteNot = z3.If(skill_ID==skill.SKILL_ENUM['WasteNot'],self.waste_not_I_symbolic_do(step), launch_Observe)
        launch_Veneration = z3.If(skill_ID==skill.SKILL_ENUM['Veneration'], self.veneration_symbolic_do(step), launch_WasteNot)
        launch_StandardTouch = z3.If(skill_ID == skill.SKILL_ENUM['StandardTouch'], self.standard_touch_symbolic_do(step), launch_Veneration)
        launch_GreatStrides = z3.If(skill_ID == skill.SKILL_ENUM['GreatStrides'], self.great_strides_symbolic_do(step), launch_StandardTouch)
        launch_Innovation = z3.If(skill_ID == skill.SKILL_ENUM['Innovation'], self.innovation_symbolic_do(step), launch_GreatStrides)
        launch_FinalAppraisal = z3.If(skill_ID == skill.SKILL_ENUM['FinalAppraisal'], self.final_appraisal_symbolic_do(step), launch_Innovation)
        launch_WasteNotII = z3.If(skill_ID == skill.SKILL_ENUM['WasteNotII'], self.waste_not_II_symbolic_do(step), launch_FinalAppraisal)
        launch_ByregotsBlessing = z3.If(skill_ID == skill.SKILL_ENUM['ByregotsBlessing'], self.byregots_blessing_symbolic_do(step), launch_WasteNotII)
        launch_MuscleMemory = z3.If(skill_ID == skill.SKILL_ENUM['MuscleMemory'], self.muscle_memory_symbolic_do(step), launch_ByregotsBlessing)
        launch_CarefulSynthesis = z3.If(skill_ID == skill.SKILL_ENUM['CarefulSynthesis'], self.careful_synthesis_symbolic_do(step), launch_MuscleMemory)
        launch_CarefulSynthesis2 = z3.If(skill_ID == skill.SKILL_ENUM['CarefulSynthesis2'], self.careful_synthesis_2_symbolic_do(step), launch_CarefulSynthesis)
        launch_Manipulation = z3.If(skill_ID == skill.SKILL_ENUM['Manipulation'], self.manipulation_symbolic_do(step), launch_CarefulSynthesis2)
        launch_PrudentTouch = z3.If(skill_ID == skill.SKILL_ENUM['PrudentTouch'], self.prudent_touch_symbolic_do(step), launch_Manipulation)
        launch_FocusedSynthesis = z3.If(skill_ID == skill.SKILL_ENUM['FocusedSynthesis'], self.focused_synthesis_symbolic_do(step), launch_PrudentTouch)
        launch_FocusedTouch = z3.If(skill_ID == skill.SKILL_ENUM['FocusedTouch'], self.focused_touch_symbolic_do(step), launch_FocusedSynthesis)
        launch_Reflect = z3.If(skill_ID == skill.SKILL_ENUM['Reflect'], self.reflect_symbolic_do(step), launch_FocusedTouch)
        launch_PreparatoryTouch = z3.If(skill_ID == skill.SKILL_ENUM['PreparatoryTouch'], self.preparatory_touch_symbolic_do(step), launch_Reflect)
        launch_GroundWork = z3.If(skill_ID == skill.SKILL_ENUM['GroundWork'], self.ground_work_symbolic_do(step), launch_PreparatoryTouch)
        launch_GroundWork2 = z3.If(skill_ID == skill.SKILL_ENUM['GroundWork2'], self.ground_work_2_symbolic_do(step), launch_GroundWork)
        launch_DelicateSynthesis = z3.If(skill_ID == skill.SKILL_ENUM['DelicateSynthesis'], self.delicate_synthesis_symbolic_do(step), launch_GroundWork2)
        launch_TrainedEye = z3.If(skill_ID == skill.SKILL_ENUM['TrainedEye'], self.trained_eye_symbolic_do(step), launch_DelicateSynthesis)
        launch_AdvancedTouch = z3.If(skill_ID == skill.SKILL_ENUM['AdvancedTouch'], self.advanced_touch_symbolic_do(step), launch_TrainedEye)
        launch_PrudentSynthesis = z3.If(skill_ID == skill.SKILL_ENUM['PrudentSynthesis'], self.prudent_synthesis_symbolic_do(step), launch_AdvancedTouch)
        launch_TrainedFinesse = z3.If(skill_ID == skill.SKILL_ENUM['TrainedFinesse'], self.trained_finesse_symbolic_do(step), launch_PrudentSynthesis)
        launch_all = launch_TrainedFinesse
        return launch_all


    def skill_issue_symbolic_constraint(self, step):
        constraint_list_tmp = []
        # ???????????? <= 0??? ???????????????IDLE
        # ???????????? >= ??????????????????????????????IDLE
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_dur_status[step] <= 0, self.skill_info.ID_sequence[step] == skill.SKILL_ENUM['IDLE']))
        constraint_list_tmp.append(z3.Implies(self.status_info.progress_status[step] >= self.recipe_info.difficulty, self.skill_info.ID_sequence[step] == skill.SKILL_ENUM['IDLE']))
        
        # ???????????? > 0 ????????? < ??????????????????????????????IDLE
        not_IDLE_condition = z3.And(self.status_info.remain_dur_status[step] > 0, self.status_info.progress_status[step] < self.recipe_info.difficulty)
        constraint_list_tmp.append(z3.Implies(not_IDLE_condition, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['IDLE']))

        # ????????????????????????????????????
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 18, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['BasicTouch']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 88, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['MastersMend']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 7, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['Observe']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 56, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['WasteNot']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 18, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['Veneration']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 32, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['StandardTouch']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 32, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['GreatStrides']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 18, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['Innovation']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 1,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['FinalAppraisal']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 98,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['WasteNotII']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 24,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['ByregotsBlessing']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 6,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['MuscleMemory']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 7,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['CarefulSynthesis']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 7,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['CarefulSynthesis2']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 96,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['Manipulation']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 25,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['PrudentTouch']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 5,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['FocusedSynthesis']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 18,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['FocusedTouch']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 24,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['Reflect']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 40,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['PreparatoryTouch']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 18,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['GroundWork']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 18,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['GroundWork2']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 32,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['DelicateSynthesis']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 250,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['TrainedEye']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 46,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['AdvancedTouch']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 18,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['PrudentSynthesis']))
        constraint_list_tmp.append(z3.Implies(self.status_info.remain_cp_status[step] < 32,  self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['TrainedFinesse']))
        
        # ??????combo??????
        constraint_list_tmp.append(z3.Implies(self.status_info.standard_touch_combo[step]==False, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['StandardTouch']))
        constraint_list_tmp.append(z3.Implies(self.status_info.advanced_touch_combo[step]==False, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['AdvancedTouch']))
        constraint_list_tmp.append(z3.Implies(self.status_info.byregot_Blessing_combo[step]==False, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['ByregotsBlessing']))
        constraint_list_tmp.append(z3.Implies(self.status_info.focused_synthesis_combo[step]==False, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['FocusedSynthesis']))
        constraint_list_tmp.append(z3.Implies(self.status_info.focused_touch_combo[step]==False, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['FocusedTouch']))
        constraint_list_tmp.append(z3.Implies(self.status_info.muscle_memory_combo[step]==False, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['MuscleMemory']))
        constraint_list_tmp.append(z3.Implies(self.status_info.reflect_combo[step]==False, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['Reflect']))
        constraint_list_tmp.append(z3.Implies(self.status_info.trained_finesse_combo[step]==False, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['TrainedFinesse']))
        constraint_list_tmp.append(z3.Implies(self.status_info.trained_eye_combo[step]==False, self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['TrainedEye']))
        
        # ?????? or ????????????????????????????????????????????????
        constraint_list_tmp.append(z3.Implies(
            z3.Or(self.status_info.waste_not_I_status[step] > 0, self.status_info.waste_not_II_status[step] > 0),
            self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['PrudentTouch']
        ))
        constraint_list_tmp.append(z3.Implies(
            z3.Or(self.status_info.waste_not_I_status[step] > 0, self.status_info.waste_not_II_status[step] > 0),
            self.skill_info.ID_sequence[step] != skill.SKILL_ENUM['PrudentSynthesis']
        ))
        return utils.flatten_constraint_list(constraint_list=constraint_list_tmp)


    # such that we do not need to do multiplication during solving
    def calculate_progress(self, 
                           skill_ID,
                           skill_can_increase_progress,
                           status_has_muscle_memory,
                           status_has_veneration,
                           status_dur_not_enough):
        prog_inc_mul = 1
        prog_inc_skill_mul = 0
        if skill_can_increase_progress and status_has_muscle_memory:
            prog_inc_mul += 1
        if status_has_veneration:
            prog_inc_mul += 0.5
        if status_dur_not_enough and (skill.SKILL_ENUM['GroundWork'] == skill_ID or skill.SKILL_ENUM['GroundWork2'] == skill_ID):
            prog_inc_mul *= 0.5
        if skill_can_increase_progress:
            if skill.SKILL_ENUM['BasicSynthesis'] == skill_ID:
                prog_inc_skill_mul = 1
            if skill.SKILL_ENUM['BasicSynthesis2'] == skill_ID:
                prog_inc_skill_mul = 1.2
            if skill.SKILL_ENUM['MuscleMemory'] == skill_ID:
                prog_inc_mul = 3
            if skill.SKILL_ENUM['CarefulSynthesis'] == skill_ID:
                prog_inc_mul = 1.5
            if skill.SKILL_ENUM['CarefulSynthesis2'] == skill_ID:
                prog_inc_mul = 1.8
            if skill.SKILL_ENUM['FocusedSynthesis'] == skill_ID:
                prog_inc_mul = 2
            if skill.SKILL_ENUM['GroundWork'] == skill_ID:
                prog_inc_mul = 3
            if skill.SKILL_ENUM['GroundWork2'] == skill_ID:
                prog_inc_mul = 3.6
            if skill.SKILL_ENUM['DelicateSynthesis'] == skill_ID:
                prog_inc_mul = 1
            if skill.SKILL_ENUM['PrudentSynthesis'] == skill_ID:
                prog_inc_mul = 1.8
        return int(self.base_prog_inc * prog_inc_mul* prog_inc_skill_mul)
    
    def calculate_quality(self,
                          skill_ID,
                          skill_can_increase_quality,
                          status_has_great_stride,
                          status_has_innovation,
                          status_inner_quiet_level
                          ):
        qual_gain = 0
        qual_inc_mul = 1
        qual_inc_skill_mul = 0
        inner_quiet_mul = 1
        if skill_can_increase_quality and status_has_great_stride:
            qual_inc_mul += 1
        if status_has_innovation:
            qual_inc_mul += 0.5
        if skill.SKILL_ENUM['ByregotsBlessing'] == skill_ID and status_inner_quiet_level > 0:
            qual_inc_mul *= 1 + (0.2 * status_inner_quiet_level)

        if status_inner_quiet_level > 0:
            inner_quiet_mul = 1 + 0.1 * status_inner_quiet_level
        
        if skill.SKILL_ENUM['BasicTouch'] == skill_ID:
            qual_inc_skill_mul = 1
        if skill.SKILL_ENUM['StandardTouch'] == skill_ID:
            qual_inc_skill_mul = 1.25
        if skill.SKILL_ENUM['ByregotsBlessing'] == skill_ID:
            qual_inc_skill_mul = 1 # cal by inner quiet
        if skill.SKILL_ENUM['PrudentTouch'] == skill_ID:
            qual_inc_skill_mul = 1
        if skill.SKILL_ENUM['FocusedTouch'] == skill_ID:
            qual_inc_skill_mul = 1.5
        if skill.SKILL_ENUM['Reflect'] == skill_ID:
            qual_inc_skill_mul = 1
        if skill.SKILL_ENUM['PreparatoryTouch'] == skill_ID:
            qual_inc_skill_mul = 2
        if skill.SKILL_ENUM['DelicateSynthesis'] == skill_ID:
            qual_inc_skill_mul = 1
        if skill.SKILL_ENUM['AdvancedTouch'] == skill_ID:
            qual_inc_skill_mul = 1.5
        if skill.SKILL_ENUM['TrainedFinesse'] == skill_ID:
            qual_inc_skill_mul = 1    
        qual_gain = int(self.base_qual_inc * qual_inc_mul * qual_inc_skill_mul * inner_quiet_mul)
        if skill.SKILL_ENUM['TrainedEye'] == skill_ID:
            qual_gain = self.recipe_info.max_quality
        return qual_gain
    

    def generate_constraint_all(self):
        c_tmp = []
        level_skill_constraint = self.skill_info.add_level_constraint(crafter_info=self.crafter_info, recipe_info=self.recipe_info)
        basic_status_constraint = self.status_info.constraint_flattten
        skill_launch_constraint_all = z3.Const(True, z3.BoolSort())
        skill_issue_constraint_all = z3.Const(True, z3.BoolSort())
        for i in range(self.status_info.max_step-1):
            skill_launch_constraint_all = z3.And(skill_launch_constraint_all, self.skill_launch_symbolic_constraint(step=i))
        for i in range(self.status_info.max_step):
            skill_issue_constraint_all = z3.And(skill_issue_constraint_all, self.skill_issue_symbolic_constraint(step=i))
        c_tmp.append(level_skill_constraint)
        c_tmp.append(basic_status_constraint)
        c_tmp.append(skill_launch_constraint_all)
        c_tmp.append(skill_issue_constraint_all)
        return utils.flatten_constraint_list(constraint_list=c_tmp)


    