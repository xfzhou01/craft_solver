import z3
import recipe
import crafter
# import src.utils as utils

def get_array(name, length):
    arr_tmp = []
    for i in range(length):
        arr_tmp.append(z3.Int("{}_{}".format(name, i)))
    return arr_tmp

def get_boolean_array(name, length):
    arr_tmp = []
    for i in range(length):
        arr_tmp.append(z3.Bool("{}_{}".format(name, i)))
    return arr_tmp

# calculate basic progress increase
def cal_basic_progress_increase(recipe_info:recipe.recipe, crafter_info:crafter.crafter):
    basic_prog_inc = (crafter_info.craftermanship * 10) / recipe_info.progress_divider + 2
    progress_modifier_tmp = 100
    if recipe_info.progress_modifier:
        progress_modifier_tmp = recipe_info.progress_modifier
    if crafter_info.level <= recipe_info.level:
        basic_prog_inc *= (progress_modifier_tmp * 0.01)
    return int(basic_prog_inc)

def cal_basic_quality_increase(recipe_info:recipe.recipe, crafter_info:crafter.crafter):
    basic_qual_inc = (crafter_info.control * 10) / recipe_info.quality_divider + 35
    quality_modifier_tmp = 100
    if recipe_info.quality_modifier:
        quality_modifier_tmp = recipe_info.quality_modifier
    if crafter_info.level <= recipe_info.level:
        basic_qual_inc *= (quality_modifier_tmp * 0.01)
    return int(basic_qual_inc)

def flatten_constraint_list(constraint_list:list):
    constraint = z3.Const(True, z3.BoolSort())
    for c in constraint_list:
        constraint = z3.And(constraint, c)
    return constraint

def select_array(arr:list, index):
    if len(arr) == 1:
        return arr[0]
    return z3.If(index==len(arr)-1, arr[len(arr)-1], select_array(arr=arr[0:-1], index=index))