# -*-coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import gensim
import jieba
import numpy as np
import re
import buildQuestion
import io


class medicalQA:
    def __init__(self, gensim_model_path, jieba_dict_path):
        self.name_list = []
        self.name_dict = {}
        for line in io.open(jieba_dict_path, encoding="utf-8").readlines():
            self.name_list.append(line.split()[0])  # 读入疾病
        #for name in self.name_list:
        #    print(name)
        dirNames = ["./data/content1",
                    "./data/content2",
                    "./data/content3",
                    "./data/content4", ]
        for dirName in dirNames:  # 构建每个疾病对应的路径的字典
            with io.open(os.path.join(dirName, "index.txt"), encoding="utf-8") as f:
                cnt = 1
                for line in f.readlines():
                    self.name_dict[line.split()[1].strip("\n")] = os.path.join(dirName, str(cnt))
                    cnt += 1
        self.word2vec_model = gensim.models.Word2Vec.load(gensim_model_path)
        jieba.load_userdict(jieba_dict_path)

    def question2embedding(self, question_words):
        question_vector = np.zeros(128)
        num_words = 0
        for word in question_words:
            try:
                word_vector = self.word2vec_model[word]  # 加起来每个向量
                question_vector += word_vector
                num_words += 1
            except KeyError:
                continue
        if num_words == 0:
            return np.zeros(128)
        return (question_vector / num_words)  # 取平均值

    @staticmethod
    def isCutWord(word):
        if re.match(re.compile("[A-Za-z]+"), word):
            return True
        if word == "是" or word == "什么" or word == "的" or word == "我" or \
            word == "你" or word == "他" or word == "她" or word == "它"  or word == "了" or \
            word == "了" or word == "治疗" or word == "和" or word == "或" or word == "治":
            return True
        return False

    def __findRelatedName(self):
        self.related_name_list = []
        now = set(self.name_list)
        for word in self.user_question_words:
            if medicalQA.isCutWord(word):
                continue
            s = set()
            for name in self.name_list:
                if str(name).find(word) >= 0:
                    s.add(name) # 与问题相关的疾病list
            if len(s) == 0:
                continue
            now = s & now
            if len(now) < 3:
                break
            #for name in now:
            #    print name
        self.related_name_list = list(now)
        if len(self.related_name_list) > 0:
            return

        self.related_name_list = []

        for name in self.name_list:
            for word in self.user_question_words:
                if medicalQA.isCutWord(word):
                    continue
                if str(name).find(word) >= 0:
                    if str(word).find(name) >= 0:
                        self.related_name_list = [name]
                        return
                    self.related_name_list.append(name) # 与问题相关的疾病list
                    break
        if len(self.related_name_list) == 0:
            print '找不到疾病信息'
        else:
            print '定位疾病: ' 
            for name in self.related_name_list:
                print name

    def __question2segmentation(self, question):
        question_words = []
        for word in jieba.cut(question, cut_all=False):
            question_words.append(word)
#        for word in question_words:
#            print word
        return question_words

    def __findSimilarity(self, question):
        question_words = jieba.cut(question, cut_all=False)
        question_embedding = self.question2embedding(question_words)
        dot = np.dot(self.user_question_embedding, question_embedding)
        user_question_embedding_length = np.sqrt(np.sum(np.square(self.user_question_embedding)))
        question_embedding_length = np.sqrt(np.sum(np.square(question_embedding)))
        return dot / (float(user_question_embedding_length) * float(question_embedding_length))

    def readInput(self):
        self.user_question = raw_input('输入所问问题 ： ')
        marks = io.open("./mark.txt", encoding="utf-8").read()
        for mark in marks:
            self.user_question = self.user_question.replace(mark, "")
        self.user_question_words = self.__question2segmentation(self.user_question)
        self.user_question_embedding = self.question2embedding(self.user_question_words)
        #print(self.user_question_embedding)

    def showAnswer(self):
        self.__findRelatedName()
        if len(self.related_name_list) == 0:
            return
        best_question_list = []
        best_similarity_list = []
        best_answer_list = []
        rate = 1
        for name in self.related_name_list:
            cosine_similarity_list = []  # 这个疾病所有问题的相似度list
            path_list = []  # 这个疾病的的对应问题的路径list
            questions_list = []  # 这个疾病的问题list
#            print "path" + self.name_dict[name]
            for index in os.listdir(self.name_dict[name]):
                if index == "目录.txt":
                    continue
                string = re.sub(re.compile("\\.txt"), "", index)
                questions = buildQuestion.toQuestion(name, string)
                #print(questions)
                #print(name)
                max_similarity = 0
                for q in questions:
                    tmp = self.__findSimilarity(q)
                    #print("tmp is", tmp)
                    if tmp > max_similarity:
                        max_similarity = tmp
                        question = q
                #print("???", max_similarity)
                questions_list.append(question)
                cosine_similarity_list.append(max_similarity)
                path_list.append(os.path.join(self.name_dict[name], index))
            cosine_similarity_sum = np.sum(np.array(cosine_similarity_list))
            cosine_similarity_list = cosine_similarity_list / cosine_similarity_sum

            best_similarity_list.append(np.max(np.array(cosine_similarity_list)) * rate)
            #rate *= 0.5
            answer_index = np.argmax(np.array(cosine_similarity_list))  # 取出相似度最高的词条的下标
            best_question_list.append(questions_list[answer_index])  # 加入这个词条的对应问题
            best_answer_list.append(io.open(path_list[answer_index], encoding='utf-8').read()) # 加入这个问题的答案

        print "--------------------------------------"
        best_index = np.argmax(np.array(best_similarity_list))  # 输出所有疾病中最契合的问题的下标
        print best_question_list[best_index]  # 输入问题
        print best_answer_list[best_index]  # 输出答案

QA = medicalQA("./word2vec3.model", "./new_dict2.txt")
while True:
    QA.readInput()
    QA.showAnswer()