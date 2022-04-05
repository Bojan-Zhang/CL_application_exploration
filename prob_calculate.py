import case_data_augment as case_data

# 计算概率
# 获取所有的历史题目
his_case = case_data.his_case
# 获取所有的错题
his_bug_case = his_case[his_case['是否是错题'] == '1']

# 基本特征
# 学科
subject_all = his_case.groupby(['学科'])['题目id'].count()
subject_bug = his_bug_case.groupby(['学科'])['题目id'].count()
subject_prop = (subject_bug / subject_all).to_dict()
print(subject_prop)
# 年级
grade_all = his_case.groupby(['年级'])['题目id'].count()
grade_bug = his_bug_case.groupby(['年级'])['题目id'].count()
grade_prop = (grade_bug / grade_all).to_dict()
print(grade_prop)
# 学段
phase_all = his_case.groupby(['学段'])['题目id'].count()
phase_bug = his_bug_case.groupby(['学段'])['题目id'].count()
phase_prop = (phase_bug / phase_all).to_dict()
print(phase_prop)
# 处理流程
process_bug = his_case.groupby(['bug原因'])['题目id'].count()
process_prop = (process_bug / len(his_case)).to_dict()
process = 1
for prop in process_prop.values():
    process *= 1 - prop

# 额外特征
# 题型
q_type_all = his_case.groupby(['题型'])['题目id'].count()
q_type_bug = his_bug_case.groupby(['题型'])['题目id'].count()
q_type_prop = q_type_bug / q_type_all
q_type_prop = q_type_prop.mask(q_type_prop.isna(), 0).to_dict()
print(q_type_prop)
# 系列or出版社
series_all = his_case.groupby(['书本特征'])['题目id'].count()
series_bug = his_bug_case.groupby(['书本特征'])['题目id'].count()
series_prop = (series_bug / series_all).to_dict()
series_prop.pop('')
print(series_prop)
# 是否有图
has_pic_all = his_case.groupby(['是否有图'])['题目id'].count()
has_pic_bug = his_bug_case.groupby(['是否有图'])['题目id'].count()
has_pic_prop = (has_pic_bug / has_pic_all).to_dict()

# 是否有表
has_form_all = his_case.groupby(['是否有表'])['题目id'].count()
has_form_bug = his_bug_case.groupby(['是否有表'])['题目id'].count()
has_form_prop = (has_form_bug / has_form_all).to_dict()

# 是否有公式
has_formula_all = his_case.groupby(['是否有公式'])['题目id'].count()
has_formula_bug = his_bug_case.groupby(['是否有公式'])['题目id'].count()
has_formula_prop = (has_formula_bug / has_formula_all).to_dict()