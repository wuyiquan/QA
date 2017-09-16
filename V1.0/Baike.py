import sys
import Word2Vec
import os
import gensim
import jieba
import numpy as np
import re
import buildQuestion

def prepare(gensim_model, jieba_dict_path):
    name_list = []
    name_dict = {}
    for line in open("new_dict2.txt", encoding="utf-8").readlines():
        name_list.append(line.strip("\n").strip("\ufeff")) #读入疾病
    dirNames = ["content1",
                "content2",
                "content3",
                "content4", ]
    for dirName in dirNames: #构建每个疾病对应的路径的字典
        with open(os.path.join(dirName, "index.txt"), encoding="utf-8") as f:
            cnt = 1
            for line in f.readlines():
                name_dict[line.split()[1].strip("\n")] = os.path.join(dirName, str(cnt))
                cnt += 1
    model = gensim.models.Word2Vec.load(gensim_model)
    jieba.load_userdict(jieba_dict_path)
    diseases_catalog = (name_list, name_dict) #list和dict合成一个元祖
    return diseases_catalog, model

def find_question_vector(question, word2vec_model): #寻找问题对应的词向量，由question2embedding调用
    question_vector = np.zeros(128)
    num_words = 0
    for word in question:
        try:
            word_vector = word2vec_model[word] #加起来每个向量
            question_vector += word_vector
            num_words += 1
        except KeyError:
            continue
    if num_words == 0:
        return np.zeros(128)
    return (question_vector / num_words) # 取平均值

# question2embedding:question转为向量的总接口，如果不是User的问题，直接转成向量，否则还需要返回与问题相关的疾病list
def question2embedding(question, word2vec_model, diseases_catalog, isUser=True):  #catalog: list, dict
    question_words = jieba.cut(question, cut_all=False)
    question_words2 = []
    diseases = []
    for word in question_words:
        question_words2.append(word)
    if isUser:
        for disease_name in diseases_catalog[0]:
            for word in question_words2:
                if str(disease_name).find(word) >= 0:
                    diseases.append(disease_name) # 与问题相关的疾病list
                    break
        if len(diseases) == 0:
            print('找不到疾病信息')
            return None, diseases
        else:
            print('定位疾病: ', diseases)
    #转为向量
    question_vector = find_question_vector(question=question_words2, word2vec_model=word2vec_model)
    return question_vector, diseases

#计算vector1 vector2的cos
def cosine_distance(vector1, vector2):
    dot = np.dot(vector1, vector2)
    vector1_length = np.sqrt(np.sum(np.square(vector1)))
    vector2_length = np.sqrt(np.sum(np.square(vector2)))
    return dot / (float(vector1_length) * float(vector2_length))

def input_handle(user_question): #对user的问题进行处理
    marks = open("mark.txt", encoding="utf-8").read()
    for mark in marks:
        user_question = user_question.replace(mark, "")
    return user_question


#为问题寻找答案
def find_answer4user_question(user_question_vector, related_diseases, diseases_catalog, word2vec_model):
    #这里的相关疾病是一个list
    best_similarity = [] #相关疾病中，每个疾病的所有问题取出的最高相似度list
    best_question_list = []#相关疾病中，每个疾病的最高相似度问题list
    best_answer_list =[]#相关疾病中，每个疾病的最高相似度问题的答案list
    rate = 1
    for disease in related_diseases:#遍历每个疾病item
        cosine_similarity_list = [] #这个疾病所有问题的相似度list
        path_list = [] #这个疾病的的对应问题的路径list
        question_list = [] #这个疾病的问题list
        for question_index in os.listdir(diseases_catalog[1][disease]):#遍历该疾病下的所有txt
            if question_index == "目录.txt":
                continue
            path_list.append(os.path.join(diseases_catalog[1][disease], question_index))
            string = re.sub(re.compile("\\.txt"), "", question_index)
            question = buildQuestion.toQuestion(disease, string)
            question_list.append(question)
            question_vector, _ = question2embedding(question, word2vec_model, None, isUser=False)
            cosine_similarity_list.append(cosine_distance(question_vector, user_question_vector))
        cosine_similarity_sum = np.sum(np.array(cosine_similarity_list))
        cosine_similarity_list = cosine_similarity_list / cosine_similarity_sum

        #print(cosine_similarity_list)
        best_similarity.append(np.max(np.array(cosine_similarity_list)) * rate)#取出所有问题的最高相似度 * rate
        rate *= 0.80# rate是一个衰弱系数
        answer_index = np.argmax(np.array(cosine_similarity_list)) #取出相似度最高的问题的下标
        best_question_list.append(question_list[answer_index])# 加入这个问题
        best_answer_list.append(open(path_list[answer_index], encoding='utf-8').read()) # 加入这个问题的答案

        #print(question_list[answer_index])
        #print(open(path_list[answer_index], encoding='utf-8').read())
    print("--------------------------------------")
    best_index = np.argmax(np.array(best_similarity)) #输出所有疾病中最契合的问题的下标
    print(best_question_list[best_index]) #输入问题
    print(best_answer_list[best_index]) #输出答案


if __name__ == '__main__':
    gensim_model = "word2vec3.model" #使用的向量model
    jieba_dict_path = "new_dict2.txt" #jieba的词典
    diseases_catalog, model = prepare(gensim_model=gensim_model,
                             jieba_dict_path=jieba_dict_path) #数据准备
    while True:
        user_question = input()
        user_question = input_handle(user_question)
        print(user_question)
        user_question_vector, related_diseases = question2embedding(user_question, model, diseases_catalog)
        #返回问题向量与相关的疾病
        if user_question_vector is None: #无法分析问题
            continue
        else: #寻找答案
            find_answer4user_question(user_question_vector, related_diseases, diseases_catalog, model)
