import case_data_augment as case_data
import prob_calculate as prob

print(prob.series_prop)
all_case = case_data.all_case
case_with_book_feat = all_case[all_case['书本特征'] == "高中英语星级训练"]

# 题型分布
q_type = case_with_book_feat.groupby(['书本特征', '题型'])['题目id'].count()
print(q_type)

# 图分布
pic = case_with_book_feat.groupby(['书本特征', '是否有图'])['题目id'].count()
print(pic)

# 表分布
form = case_with_book_feat.groupby(['书本特征', '是否有表'])['题目id'].count()
print(form)

# 公式分布
formula = case_with_book_feat.groupby(['书本特征', '是否有公式'])['题目id'].count()
print(formula)

# 错误分布
bug_loc = case_with_book_feat.groupby(['书本特征', '错误分类'])['题目id'].count()
print(bug_loc)

# 错误程度分布
bug_level = case_with_book_feat.groupby(['书本特征', '问题分类'])['题目id'].count()
print(bug_level)

# 错因阶段分布
bug_cause = case_with_book_feat.groupby(['书本特征', 'bug原因'])['题目id'].count()
print(bug_cause)

bug_cause = case_with_book_feat.groupby(['书本特征', '题型', '错误分类'])['题目id'].count()
print(bug_cause)

bug_with_book_feat = all_case[(all_case['书本特征'] == "高中英语星级训练") & (all_case['是否是错题'] == "1")]
bug_prop = bug_with_book_feat.groupby(['书本特征', '题型'])['题目id'].count() / q_type
print(bug_prop)