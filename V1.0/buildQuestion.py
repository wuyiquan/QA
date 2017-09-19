# -*-coding: utf-8 -*-
def books(Name, aspect):
    return "有什么与" + Name + "相关的记载吗"

def relation(Name, aspect):
    return Name + aspect + "是什么"

def histroy(Name, aspect):
    return Name + "有什么历史吗"

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
}

def toQuestion(Name, aspect):
    if ques.get(Name) is None:
        return Name + "的" + aspect + "是什么"
    else:
        return ques[Name](aspect)