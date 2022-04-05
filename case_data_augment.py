import pandas as pd

# load data
all_case = pd.read_csv('../Data/题目质量-工作表1-0316.csv')
all_case = all_case.rename(columns={'Unnamed: 5':'年级', 'Unnamed: 6':'题型', 'Unnamed: 7':'学段学科',
                                    'Unnamed: 8':'是否有图表', 'Unnamed: 9':'是否有公式'})
# 删除无效的列，包括空列、截图、题目URL
all_case = all_case.drop(['书本id', '题目url', '是否埋点', '原题', '埋点', '截图', '埋点是否恢复', 'Unnamed: 18', '截图.1', 'Unnamed: 25',
                          'Unnamed: 26', 'Unnamed: 27', 'Unnamed: 28', 'Unnamed: 29',
                          'Unnamed: 30', 'Unnamed: 31', 'Unnamed: 32', 'Unnamed: 33',
                          'Unnamed: 34', '0'], axis = 1)

# 问题分类只有：编排问题、学科问题、产研问题、（学科问题，编排问题）
# 需要做的是把文本中的错误，替换为问题
# print(all_case['问题分类'].drop_duplicates())
all_case['问题分类'] = all_case['问题分类'].mask(all_case['问题分类'] == '学科错误', '学科问题')
all_case['问题分类'] = all_case['问题分类'].mask(all_case['问题分类'] == '编排错误', '编排问题')
all_case['问题分类'] = all_case['问题分类'].mask(all_case['问题分类'] == '学科问题，编排问题', '学科问题')

# 获取书本，从书本名中获取年级、学科和学段
# 一共37本书，有一行有问题，删掉
book_names = all_case['书本名'].drop_duplicates()
# 删除异常数据
all_case = all_case.drop(all_case[all_case['书本名'].isna()].index)
# 获取书本名
book_names = all_case['书本名'].drop_duplicates()

# 添加年级
# 第一步：创建书本名与年级的字典
grade = []
for book_name in book_names:
    if '三年级' in book_name:
        grade.append(3)
    elif '四年级' in book_name:
        grade.append(4)
    elif '五年级' in book_name:
        grade.append(5)
    elif '七年级' in book_name or '7年级' in book_name:
        grade.append(7)
    elif '八年级' in book_name:
        grade.append(8)
    elif '九年级' in book_name or '中考' in book_name or '精编初中英语教学与评估' in book_name:
        grade.append(9)
    elif '高一' in book_name or '必修第一册' in book_name or '必修1' in book_name \
            or '必修2' in book_name or '必修 2' in book_name \
            or '普通高中教科书 历史 必修 中外历史纲要上册 练习部分' in book_name\
            or '普通高中教科书语文必修下册练习部分' in book_name:
        grade.append(10)
    elif '高二' in book_name or '必修3' in book_name:
        grade.append(11)
    elif '高三' in book_name or '红楼梦' in book_name or '高考' in book_name \
            or '高中英语语法试题精编' in book_name or '高中英语教学基本要求词汇默写本' in book_name \
            or '历年模拟试卷' in book_name:
        grade.append(12)
    else:
        # 如果这本书没有被归类，把书的名字打印出来
        print(book_name)
        grade.append('未知')

grade_dict = dict(zip(list(book_names), grade))
# 第二步：添加到表中
all_case['年级'] = all_case['书本名'].map(grade_dict)

# 添加学段
all_case['学段'] = '未知'

def get_level(df):
    if df['年级'] < 7:
        df['学段'] = '小学'
    elif df['年级'] < 10:
        df['学段'] = '初中'
    else:
        df['学段'] = '高中'
    return df

all_case = all_case.apply(get_level, axis=1)

# 添加学科
# 构造书本名字与学科构成的字典
subject = []
for book_name in book_names:
    if '数学' in book_name:
        subject.append('数学')
    elif '物理' in book_name:
        subject.append('物理')
    elif '语文' in book_name or '文言文' in book_name or '红楼梦' in book_name:
        subject.append('语文')
    elif '英语' in book_name:
        subject.append('英语')
    elif '地理' in book_name:
        subject.append('地理')
    elif '生命科学' in book_name or '生物' in book_name:
        subject.append('生物')
    elif '化学' in book_name:
        subject.append('化学')
    elif '历史' in book_name:
        subject.append('历史')
    else:
        # 把例外情况打印出来
        print(book_name)
        subject.append('未知')

# 添加到表中
subject_dict = dict(zip(list(book_names), subject))
all_case['学科'] = all_case['书本名'].map(subject_dict)

# 完成基本信息的添加，添加了学科、年级、学段

# 是否有图、是否有表的这个特征还是没有办法来做，如果要做的话就需要在人工标注的时候额外标注
# 但是希望可以构造出来，除了学科、年级、学段的特征

# 为了更好的区分，更新一下列名
all_case = all_case.rename(columns={'是否有问题（0:：没有问题，1：有问题）': '是否是错题', '是否有问题（0表示没有，1表示有）': '是否标注有误'})

# # # 统计章节题量，一共948个章节
# chapter_stat = all_case.groupby('章节名')['题目id'].count()
# chapter_stat = pd.DataFrame({'章节名':chapter_stat.index, '章节题量':chapter_stat.values})
# # 大数定理，可以做到用样本概率去估计总体的样本
# chapter_stat = chapter_stat[chapter_stat['章节题量'] > 30]
# print(chapter_stat)

# chapter_stat = all_case[~(all_case['章节名'].str.contains('综合训练') |
#                           all_case['章节名'].str.contains('默写训练') |
#                           all_case['章节名'].str.contains('2021年精编初中英语教学与评估') |
#                           all_case['章节名'].str.contains('本章测试') |
#                           all_case['章节名'].str.contains('每周一练') |
#                           all_case['章节名'].str.contains('复习与小结') |
#                           all_case['章节名'].str.contains('单元测试'))]['章节名'].drop_duplicates()
# print(chapter_stat)


# # 看一下错误原因，应该是没有用的，因为不能已知错题，可能需要再探究一下
# bug_list = all_case['错误分类'].drop_duplicates()
# # 一共65种错误，除去nan
# bug_list_without_nan = bug_list[1:]

# # 在分割数据的时候，发现一共10个项目
# print(len(all_case['项目'].drop_duplicates()))
# # 查看项目中书本和题目的分布
# print(all_case.groupby(['项目', '书本名'])['题目id'].count())

# 添加题型
# all_case['题型'] = ""
# all_case['题型'] = all_case['题型'].mask(all_case['书本名'].str.contains('默写'), '默写')
# all_case['题型'] = all_case['题型'].mask((all_case['书本名'].str.contains('阅读理解')), '阅读理解')

# 添加是否有图表
all_case['是否有图'] = '无图'
all_case['是否有图'] = all_case['是否有图'].mask((all_case['是否有图表'] == '有图'), '有图')
all_case['是否有表'] = '无表'
all_case['是否有表'] = all_case['是否有表'].mask((all_case['是否有图表'] == '有表格'), '有表')

# 添加系列or出版社，中考英语核心词汇默写本（上海教育出版社）有两本一样的书
all_case['书本名'] = all_case['书本名'].mask((all_case['书本名'].str.contains('上海教育出版社')
                                        & all_case['项目'] == '寒假用书2020/01/23'), '中考英语核心词汇默写本test（上海教育出版社）')
all_case['书本特征'] = ""
all_case['书本特征'] = all_case['书本特征'].mask(all_case['书本名'].str.contains('上海教育出版社'), '上海教育出版社')
all_case['书本特征'] = all_case['书本特征'].mask(all_case['书本名'].str.contains('高中英语星级训练'), '高中英语星级训练')
all_case['书本特征'] = all_case['书本特征'].mask(all_case['书本名'].str.contains('40分钟同步精准练'), '40分钟同步精准练')
all_case['书本特征'] = all_case['书本特征'].mask(all_case['书本名'].str.contains('华东师大版一课一练'), '华东师大版一课一练')

# # 查看质检相关的两个指标的情况
# print(all_case[['是否质检', '是否标注有误']].drop_duplicates())
# print(all_case.groupby(['是否质检', '是否标注有误', '是否是错题'])['题目id'].count())

# 找到那些，确认的，标注有问题的题目，一共104道题
test_case = all_case[all_case['是否质检'] == '是']
test_wrong_case = test_case[test_case['是否标注有误'] == 1]
test_wrong_label_case = test_wrong_case[test_wrong_case['是否是错题'] == '0']

# 手工挑选出来的test——book，一共11本书
test_book_list = ['中考英语核心词汇默写本test（上海教育出版社）',
                  '高中生物历年模拟试卷（一）',
                  '高二下册历史练习部分 人教版教材课本高中历史选择性必修2 练习册',
                  '40分钟同步精准练 高中历史选择性必修1',
                  '40分钟同步精准练 高中历史选择性必修3',
                  '红楼梦整本书阅读与研习手册',
                  '高中英语星级训练 阅读理解+完型填空 高考新题型 第2版高二',
                  '2021 配套人教版 上海 普通高中教科书 历史 选择性必修3 文化交流与传播 练习部分',
                  '2021上海部编人教版高中历史练习部分中外历史纲要必修下册高一',
                  '（9656--）华东师大版一课一练·八年级英语（N版 第二学期）（增强版）',
                  '（9692--）华东师大版一课一练·七年级英语（N版 第二学期）（增强版）']

# 分割数据集
his_case = all_case[~all_case['书本名'].isin(test_book_list)]
test_case = all_case[all_case['书本名'].isin(test_book_list)]

# 标注有问题的题目中，并且存在于测试集中的一共有77道
aim_case = test_wrong_label_case[test_wrong_label_case['书本名'].isin(test_book_list)]
