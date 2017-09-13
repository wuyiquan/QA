#! /usr/env/bin python
# -*-coding: utf-8 -*-

#本代码用于对于输入的问题，首先确定其属于哪一种疾病，然后对于那种疾病获取丁香园数据中的该疾病类型的各个问题的平均embedding值，随后求所问问题与各个问题的embedding的余弦距离，返回类别代号和list(其中存储各个问题的余弦距离)

#sys.argv[1]代表存储分好词的各个丁香园问题的路径，sys.argv[2]代表训练好的word2vec模型路径

import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import os
import jieba
import numpy as np
import gensim

def get_segement_words(catalog_file_path,sentence):
    #输入为一个string的句子，输出为这个句子的分解的单词
    #print 'sentence : ' + str(sentence)
    jieba.load_userdict(catalog_file_path)
    sentence_words_list = jieba.lcut(sentence,cut_all = False)
    return sentence_words_list

def get_disease_dict(catalog_path):
    disease_dict = {}
    disease_list = []
    for line in open(catalog_path,'rb').readlines():
        line_list = line.strip().split()
        disease_name = line_list[1]
        disease_dict[disease_name] = (line_list[0],line_list[2])
        disease_list.append(disease_name)
    return disease_dict,disease_list

def get_category(user_question,disease_list):
    for item in disease_list:
        if user_question.find(str(item)) >= 0:
            return item
        else:
            continue
    return 'other'
    
def get_vector(word,model):
    vector = model[word]
    return vector
    
def get_mean_vector(question_line_list,model):
    #求问题与答案的平均向量
    question_vector_list = []
    question_vector = np.zeros(128)
    question_word_num = 0
    for word in question_line_list:
        word = word.decode('utf-8')
        try:
            word_vector = get_vector(word,model)
            question_word_num = question_word_num + 1
            question_vector = question_vector + word_vector
        except KeyError:
            continue
    question_mean_vector = (question_vector/question_word_num).tolist()
    return question_mean_vector
    
def calu_cosine_distance(question_vector,answer_temp_vector):
    dot = np.dot(question_vector,answer_temp_vector)
    question_length = np.sqrt(np.sum(np.square(question_vector)))
    answer_length = np.sqrt(np.sum(np.square(answer_temp_vector)))
    cosine_distance = dot/(float(question_length)*float(answer_length))
    return cosine_distance
    
def get_embedding(category,file_path,disease_dict,model,user_question):
    disease_dir_index = disease_dict[category][0]
    disease_dir_question_num = int(disease_dict[category][1])
    #下面加上对于用户提出的问题的分词及求输入问题及对应类别内所有问题的平均embedding及相互余弦距离
    #求用户提出的问题的embedding
    catalog_file_path = '/usr/mlt/dingxiangyuan/dingxiangyuan_data/dingxiangyuan_segment_new/userdict_jieba_test.txt'
    sentence_words_list = get_segement_words(catalog_file_path,user_question)
    if sentence_words_list[0] == 'Error':
        print ('所输入的问题无法分析')
        return []
    user_question_mean_embedding = get_mean_vector(sentence_words_list,model)
    cosine_similarity_list = []
    for question_index in range(disease_dir_question_num):
        question_file_index = question_index + 1
        question_file_temp_path = os.path.join(file_path,str(disease_dir_index),str(question_file_index) + '_q.txt')
        question_temp_line = open(question_file_temp_path,'rb').readline()
        question_temp_list = question_temp_line.strip().split('\t')
        question_temp_embedding = get_mean_vector(question_temp_list,model)
        cosine_similarity_user_question_question_temp = calu_cosine_distance(user_question_mean_embedding,question_temp_embedding)
        cosine_similarity_list.append(cosine_similarity_user_question_question_temp)
    cosine_similarity_sum = np.sum(np.array(cosine_similarity_list))
    return cosine_similarity_list/cosine_similarity_sum
    
def get_embedding_main(file_path,user_question,gensim_model):
    #file_path = sys.argv[1]
    catalog_path = os.path.join(file_path,'catalog.txt')
    disease_dict,disease_list = get_disease_dict(catalog_path)
    #gensim_model = sys.argv[2]
    model = gensim.models.Word2Vec.load(gensim_model)
    category = get_category(str(user_question),disease_list)
    if category == 'other':
        #print '找不到所找疾病信息'
        return category,[]
    else:
        embedding_list = get_embedding(category,file_path,disease_dict,model,user_question)
        if embedding_list == []:
            return category,[]
        else:
            #print 'category : ',category
            #print 'embedding_list : ',str(embedding_list)
            return category,embedding_list
    