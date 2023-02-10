##### this version assume that the status is always "normal" and trying to 
##### find a solution
import z3
import  skill
import recipe
import crafter
import status
import symbolic_synth

def log_from_model(model:z3.ModelRef, N):
    has_IDLE = 0
    for i in range(N):
        if has_IDLE:
            continue
        skill_ID_z3:z3.IntNumRef = model[skill_info.ID_sequence[i]]
        if skill.ID_ENUM[skill_ID_z3.as_long()] == 'IDLE':
            has_IDLE = 1
        else:
            has_IDLE = 0
        print("-------------- step {} --------------".format(i))
        
        print("skill:                   {}".format(skill.ID_ENUM[skill_ID_z3.as_long()]))
        print("cp:                      {}".format(model[status_info.remain_cp_status[i]]))
        print("durability:              {}".format(model[status_info.remain_dur_status[i]]))
        print("progress:                {}".format(model[status_info.progress_status[i]]))
        print("quality:                 {}".format(model[status_info.quality_status[i]]))
        print("inner quiet:             {}".format(model[status_info.inner_quiet_status[i]]))
        print("waste not:               {}".format(model[status_info.waste_not_I_status[i]]))
        print("veneration:              {}".format(model[status_info.veneration_status[i]]))
        print("great strides:           {}".format(model[status_info.great_strides_status[i]]))
        print("innovation:              {}".format(model[status_info.innovation_status[i]]))
        print("final appraisal:         {}".format(model[status_info.final_appraisal_status[i]]))
        print("waste not II:            {}".format(model[status_info.waste_not_II_status[i]]))
        print("manipulation:            {}".format(model[status_info.manipulation_status[i]]))
        print("muscle memory:           {}".format(model[status_info.muscle_memory_status[i]]))
        print("standard touch combo:    {}".format(model[status_info.standard_touch_combo[i]]))
        print("advanced touch combo:    {}".format(model[status_info.advanced_touch_combo[i]]))
        print("byregot blessing combo:  {}".format(model[status_info.byregot_Blessing_combo[i]]))
        print("focused synthesis combo: {}".format(model[status_info.focused_synthesis_combo[i]]))
        print("foucused touch combo:    {}".format(model[status_info.focused_touch_combo[i]]))
        print("muscle memory combo:     {}".format(model[status_info.muscle_memory_combo[i]]))
        print("reflect combo:           {}".format(model[status_info.reflect_combo[i]]))
        print("trained finesse combo:   {}".format(model[status_info.trained_finesse_combo[i]]))
        print("trained eye combo:       {}".format(model[status_info.trained_eye_combo[i]]))

        # print("skill: {}".format(skill.ID_ENUM[model[skill_info.ID_sequence[i]]]))


    return 0



N = 50

log = open("log.log", "w+")

crafter_info = crafter.crafter(
    craftermanship=1645,
    control=1532,
    cp=400,
    level=77)
recipe_info = recipe.recipe(
    base_level=78,
    difficulty=1640,
    durability=80,
    level=415,
    max_quality=4100,
    name="青铜骑兵剑",
    progress_divider=108,
    progress_modifier=100,
    quality_divider=88,
    quality_modifier=100,
    recipe_id=0,
    stars=0
)
skill_info = skill.skill(
    crafter_info=crafter_info,
    recipe_info=recipe_info,
    max_step=N
)
status_info = status.status(
    crafter_info=crafter_info,
    recipe_info=recipe_info,
    max_step=N
)

symbolic_synth_info = symbolic_synth.symbolic_synthesizer(
    recipe_info=recipe_info,
    crafter_info=crafter_info,
    skill_info=skill_info,
    status_info=status_info
)

c_skill = symbolic_synth_info.generate_constraint_all()

# 可完成
c_finish = status_info.progress_status[N-1] >= recipe_info.difficulty
# 品质
c_quality = status_info.quality_status[N-1] >= recipe_info.max_quality

s = z3.Solver()
s.add(c_skill)
s.add(c_finish)
s.add(c_quality)
# s.set("timeout", 60000)
result = (s.check())
print(result)
if result == z3.sat:
    model_s = s.model()
    log_from_model(model_s, N)
else:
    print("unsat")
