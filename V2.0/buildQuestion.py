def books(Name, aspect):
    return "有什么与" + Name + "相关的记载吗"

def relation(Name, aspect):
    return Name + aspect + "是什么"

def histroy(Name, aspect):
    return Name + "有什么历史吗"

def meaning(Name, aspect):
    result = Name + '有什么临床运用'
    result += '|||' + Name + '在临床的表现如何'
    result += '|||' + Name + '如何运用到临床中'
    result += '|||' + Name + '有什么临床意义'
    result += '|||' + Name + '有哪些临床意义'
    return result

def introduction(Name, aspect):
    result = Name + '是什么'
    result += '|||' + '什么是' + Name
    result += '|||' + '我想了解' + Name + '是什么'
    result += '|||' + '你知道' + Name + '是什么吗'
    result += '|||' + Name + '的介绍?'
    return result

def manifestation(Name, aspect):
    result = Name + '会怎么样'
    result += '|||' + Name + '的临床表现是什么样的'
    result += '|||' + Name + '有哪些临床表现'
    result += '|||' + Name + '的具体症状有哪些'
    result += '|||' + '临床上' + Name + '有哪些表现'
    return result

def causeOf(Name, aspect):
    result = '为什么会得' + Name + ''
    result += '|||' + '为什么会患上' + Name + ''
    result += '|||' + '可能会患上' + Name + '的渠道有哪些'
    result += '|||' + '做什么可能会得' + Name + ''
    result += '|||' + Name + '的病因有哪些'
    return result

def normal(Name, aspect):
    result = Name + '的正常值是什么样的'
    result += '|||' + Name + '应该要怎样'
    result += '|||' + Name + '正常结果是什么样的'
    result += '|||' + Name + '正常结果是什么样的'
    result += '|||' "正常情况下 " + Name + '是怎么样'
    return result

def examination(Name, aspect):
    result = '如何检查' + Name + ''
    result += '|||' + Name + '要如何发现'
    result += '|||' + '检查' + Name + '的方法有什么'
    result += '|||' + '如何判断是否患上了' + Name + ''
    result += '|||' + '用什么检查' + Name + ''
    return result

def judge(Name, aspect):
    result = '如何鉴别' + Name + ''
    result += '|||' + '怎样确定有没有患上' + Name + ''
    result += '|||' + '鉴别' + Name + '的方法有哪些'
    result += '|||' + '我这样是患上' + Name + '了吗'
    result += '|||' + '怎样才算' + Name + ''
    result += '|||' + '得了' + Name + '有什么相关症状吗'
    result += '|||' + '得了' + Name + '有什么表现吗'
    return result

def cure(Name, aspect):
    result = '得了' + Name + '怎么办'
    result += '|||' + Name + '要怎么治'
    result += '|||' + Name + '如何才能痊愈'
    result += '|||' + '如何治好' + Name + ''
    result += '|||' + '得了' + Name + '要吃什么药'
    return result

def process(Name, aspect):
    result = Name + '的检查过程是什么样的'
    result += '|||' + Name + '要如何检查'
    result += '|||' + Name + '有什么检查流程'
    result += '|||' + Name + '是如何检查的'
    return result

ques = {
    "古文摘录": books,
    "《产科心法》卷上": books,
    "《北京市中药成方选集》": books,
    "《医彻》卷四": books,
    "《圣济总录》卷六十五": books,
    "《寿亲养老新书》卷四": books,
    "《易简方》": books,
    "《普济方》卷三九七": books,
    "《普济方》卷三五三": books,
    "《杨氏家藏方》卷六": books,
    "《济急丹方》卷下": books,
    "《经验奇方》卷上": books,
    "《解围元薮》卷四": books,
    "《魏氏家藏方》卷九": books,
    "与姜黄的区别": relation,
    "与西医病名的关系": relation,
    "与针灸的关系": relation,
    "历史": histroy,
    "历史典故": histroy,
    "历史文献": histroy,
    "历史沿革": histroy,
    "历史记载": histroy,
    "历史进程": histroy,
    "发现历史和流行病学": histroy,
    "介绍": introduction,
    "基本简介": introduction,
    "病因": causeOf,
    "发病原因": causeOf,
    "发病原因与发病机制": causeOf,
    "疾病分类及病因": causeOf,
    "病因": causeOf,
    "病因及临床特点": causeOf,
    "病因及分类": causeOf,
    "病因及发病机制": causeOf,
    "病因及常见疾病": causeOf,
    "病因及治疗": causeOf,
    "病因及病理生理": causeOf,
    "病因及诱因": causeOf,
    "病因和传播": causeOf,
    "病因和发病机制": causeOf,
    "病因和病理": causeOf,
    "病因病机": causeOf,
    "病因病理": causeOf,
    "病机": causeOf,
    "病理": causeOf,
    "病理和病因": causeOf,
    "病机及临床表现": manifestation,
    "临床表现": manifestation,
    "临床表现及分类": manifestation,
    "临床表现及分类": manifestation,
    "抑郁症有什么症状表现": manifestation,
    "病理表现": manifestation,
    "病理特点": manifestation,
    "病理生理": manifestation,
    "病理生理改变": manifestation,
    "表现": manifestation,
    "临床表现和疾病分期": manifestation,
    "乙肝五项检查对照表内容": examination,
    "前检查及注意事项": examination,
    "实验室及其他检查": examination,
    "实验室检查": examination,
    "引产前检查": examination,
    "影像学检查": examination,
    "新生儿疾病筛查": examination,
    "术前检查": examination,
    "检查": examination,
    "检查与评估": examination,
    "检查与诊断": examination,
    "检查内容": examination,
    "检查方法": examination,
    "检查过程": examination,
    "检查时间": examination,
    "检查项目及应用适应证": examination,
    "检查须知": examination,
    "特殊人群的相关检查": examination,
    "理化检查": examination,
    "相关检查": examination,
    "精液检查": examination,
    "辅助检查": examination,
    "检查须知": examination,
    "检查须知": examination,
    "抑郁症有什么症状表现": judge,
    "治疗症状": judge,
    "治疗症状": judge,
    "症情分析": judge,
    "相关症状": judge,
    "躁狂抑郁症的症状": judge,
    "常见疾病及症状": judge,
    "诊断": judge,
    "诊断与鉴别": judge,
    "诊断与鉴别诊断": judge,
    "诊断依据": judge,
    "诊断及鉴别诊断": judge,
    "诊断和鉴别诊断": judge,
    "诊断标准": judge,
    "诊查要点": judge,
    "诊查依据": judge,
    "鉴别诊断": judge,
    "中医治疗": cure,
    "中西医结合治疗": cure,
    "中医治疗": cure,
    "临床治疗": cure,
    "保健食疗": cure,
    "光疗方法": cure,
    "其他治疗": cure,
    "其他治法": cure,
    "其他疗法": cure,
    "常见病治疗": cure,
    "常用疗法介绍": cure,
    "手术治疗早泄的理论基础": cure,
    "抑郁症心理治疗": cure,
    "治疗": cure,
    "治疗与防护": cure,
    "治疗原则": cure,
    "治疗及预后": cure,
    "中医治疗": cure,
    "治疗和监测": cure,
    "治疗技术": cure,
    "治疗方法": cure,
    "治疗疾病": cure,
    "治疗程序": cure,
    "治疗要点": cure,
    "物理治疗": cure,
    "疾病治疗": cure,
    "痛风治疗": cure,
    "红米食疗": cure,
    "经支气管镜的治疗技术": cure,
    "西医治疗": cure,
    "评估治疗": cure,
    "过敏反应及治疗": cure,
    "配伍治疗": cure,
    "针灸治疗": cure,
    "针灸疗法": cure,
    "预防与治疗": cure,
    "食物疗法": cure,
    "食疗": cure,
    "饮食疗法": cure,
    "临床意义": meaning,
    "临床应用": meaning,
    "临床疗效": meaning,
    "临床诊断意义": meaning,
    "临床诊断意义": meaning,
    "中医应用": meaning,
    "临床麻醉应用": meaning,
    "其他应用": meaning,
    "应用": meaning,
    "心电图的应用": meaning,
    "技术应用": meaning,
    "现代临床应用": meaning,
    "现代应用": meaning,
    "现在应用": meaning,
    "体温测量与正常波动": normal,
    "正常值": normal,
    "正常值参考范围": normal,
    "正常参考值": normal,
    "正常发育的子宫": normal,
    "正常精液的标准": normal,
    "正常胎动": normal,
    "体温测量与正常波动": normal,
    "操作过程": process,
    "检查过程": process,
    "手术程序": process,
    "治疗程序": process,
}

def toQuestion(Name, aspect):
    if ques.get(aspect) is None:
        return [Name + "的" + aspect + "是什么"]
    else:
        #print(Name, aspect)
        list = ques[aspect](Name, aspect).split("|||")
        list.append(Name + "的" + aspect + "是什么")
        return list

if __name__ == "__main__":
    print(toQuestion("糖尿病", "病因"))
