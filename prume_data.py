import case_data_augment as case_data
import prob_calculate as prob
from cleanlab.pruning import get_noise_indices

def predict(df):
    df['正确概率'] = 1
    # 学科、年级、学段、有图、有表、有公式
    df['学科'] = prob.subject_prop[df['学科']]
    df['正确概率'] *= 1 - df['学科']
    df['年级'] = prob.grade_prop[df['年级']]
    df['正确概率'] *= 1 - df['年级']
    df['学段'] = prob.phase_prop[df['学段']]
    df['正确概率'] *= 1 - df['学段']
    df['是否有图'] = prob.has_pic_prop[df['是否有图']]
    df['正确概率'] *= 1 - df['是否有图']
    df['是否有表'] = prob.has_form_prop[df['是否有表']]
    df['正确概率'] *= 1 - df['是否有表']
    df['是否有公式'] = prob.has_formula_prop[df['是否有公式']]
    df['正确概率'] *= 1 - df['是否有公式']

    # 添加bug原因，是没用的
    df['正确概率'] *= prob.process

    # 添加题型、系列或者出版社
    if df['题型'] in prob.q_type_prop.keys():
        df['题型'] = prob.q_type_prop[df['题型']]
        df['正确概率'] *= 1 - df['题型']

    if df['书本特征'] in prob.series_prop.keys():
        df['书本特征'] = prob.series_prop[df['书本特征']]
        df['正确概率'] *= 1 - df['书本特征']

    df['错误概率'] = 1 - df['正确概率']
    return df


def getHits(find_errors, real_errors):
    sum = 0
    for index in find_errors:
        if index in real_errors:
            sum += 1
    return sum


def prume_bug():
    # test case一共1329个
    test_case = case_data.test_case
    # 获取全部错误题目的id
    test_id = test_case['题目id']
    test_id_map = dict(zip(test_id, [i for i in range(len(test_id))]))
    # 获取被标记为是正确的题目
    pos_id = test_case[test_case['是否是错题'] == '0']['题目id']
    pos_index = [test_id_map[pos] for pos in pos_id]
    # 获取要捕获的标记错误
    aims_id = case_data.aim_case['题目id']
    aims_index = [test_id_map[aim] for aim in aims_id]

    # 进行置信学习
    test_case = test_case.apply(predict, axis=1)
    bug_prob = test_case[['正确概率', '错误概率']].to_numpy()
    all_label = test_case['是否是错题'].apply(int)

    ordered_label_errors = get_noise_indices(
        s=all_label,
        psx=bug_prob,
        sorted_index_method='normalized_margin',  # Orders label errors
    )
    # 统计一下找出错误的数量
    hits = getHits(ordered_label_errors, aims_index)
    print("hits:", hits)
    print("标注错误数量：", len(aims_index))
    # 查全率
    acc = hits / len(aims_index)
    # 查准率
    find_label_error = []
    for i in ordered_label_errors:
        if i in pos_index:
            find_label_error.append(i)
    print("CL捕捉错误数量", len(find_label_error))
    pre = hits / len(find_label_error)
    print('查准率: {}, 查全率: {}'.format(pre, acc))


if __name__ == "__main__":
    prume_bug()