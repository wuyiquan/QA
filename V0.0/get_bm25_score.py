#! /usr/env/bin python
# -*-coding: utf-8 -*-

#本程序用于获取用户提出的问题与某类疾病下的所有问题的BM25分数，并返回归一化后的BM25分数

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
import os
import re
import jieba

def get_disease_dict(catalog_path):
    disease_dict = {}
    disease_list = []
    for line in open(catalog_path,'rb').readlines():
        line_list = line.strip().split()
        disease_name = line_list[1]
        disease_dict[disease_name] = (line_list[0],line_list[2])
        disease_list.append(disease_name)
    return disease_dict,disease_list

def get_category(sentence_words_list,disease_list):
    for item in disease_list:
        for word in sentence_words_list:
            if item.find(str(word)) >= 0:
                print item
                return item
            else:
                continue 
    return 'other'
    
def get_segement_words(catalog_file_path,sentence):
    #输入为一个string的句子，输出为这个句子的分解的单词
    #print 'sentence : ' + str(sentence)
    jieba.load_userdict(catalog_file_path)
    sentence_words_list = jieba.lcut(sentence,cut_all = False)
    return sentence_words_list
    
def calu_avg_answer_length(answer_length):
    length_sum = 0
    for length in answer_length:
        length_sum = length_sum + length
    avg_length = length_sum/len(answer_length)
    return avg_length
    
def score_calu_BM25(avg_answer_length,answer_temp_length,answer_word_num_dict,question_line_list,answer_temp_word_num_dict,answer_num):
    question_word_score_list = [] #question中的各个单词的score值
    k1 = 1.5
    b = 0.75
    answer_word_score_list = []
    for word in question_line_list:
        if word == 'question':
            continue
        else:
            if str(word) in answer_word_num_dict:
                n_qi = int(answer_word_num_dict[str(word)])
            else:
                n_qi = 0
            IDF = np.log((int(answer_num) - n_qi + 0.5)/(n_qi + 0.5))
            if str(word) in answer_temp_word_num_dict:
                f_qi_D = int(answer_temp_word_num_dict[str(word)])
            else:
                f_qi_D = 0
            score_temp = (f_qi_D * (k1 + 1))/(f_qi_D + k1 *(1-b+b*(answer_temp_length/avg_answer_length)))
            score_temp = IDF * score_temp
            answer_word_score_list.append(score_temp)
    answer_score = np.sum(answer_word_score_list)
    return answer_score
    
def get_bm25(category,file_path,disease_dict,user_question):
    #获取用户输入的user_question与对应疾病类中的所有疾病问题的BM25分数
    #首先获取输入的用户问句的分词
    catalog_file_path = './userdict_jieba_test.txt'
    sentence_words_list = get_segement_words(catalog_file_path,user_question)
    if sentence_words_list[0] == 'Error':
        print ('所输入的问题无法分析')
        return []
    #需要获取所有该疾病下面的所有问题的单词出现的次数（即对于该疾病类型下面的所有问题，其中各个词会在多少个问题中出现），所有问题的长度，
    #用户提出的各个词分别在该疾病类型下的每个问题中的出现次数
    question_word_num_dict = {} #存储该疾病类型下的所有问题中的各个词分别在多少个问题中出现（每个问题中某个词出现，则只计一次）
    question_length = [] #存储该疾病类型下的所有问题中的每个问题的单词数目
    for index in range(int(disease_dict[category][1])):
        question_file_path_temp = os.path.join(file_path,str(disease_dict[category][0]),str(index+1)+'_q.txt')
        line_list = open(question_file_path_temp,'rb').readline().strip().split()
        question_length.append(len(line_list))
        question_word_num_dict_list = [] #用来保证该问题中的某个词只被计入question_word_num_dict一次
        for word in line_list:
            if word not in question_word_num_dict_list:
                question_word_num_dict_list.append(word)
                if word not in question_word_num_dict:
                    question_word_num_dict[word] = 1
                else:
                    question_word_num_dict[word] = question_word_num_dict[word] + 1
            else:
                continue
                
    avg_question_length = calu_avg_answer_length(question_length)
    
    BM25_scores_list = []
    #下面针对于该疾病类型下的每一个问题，求出该问题中各个词的出现次数，然后传给score_calu_BM25，得到用户所提问题与该问题的BM25分数
    for index in range(int(disease_dict[category][1])):
        question_file_path_temp = os.path.join(file_path,str(disease_dict[category][0]),str(index+1)+'_q.txt')
        line_list = open(question_file_path_temp,'rb').readline().strip().split()
        question_temp_word_num = {} #该问题中各个词的出现次数
        for word in line_list:
            if word not in question_temp_word_num:
                question_temp_word_num[word] = 1
            else:
                question_temp_word_num[word] = question_temp_word_num[word] + 1
        BM25_score_question_temp_user_question = score_calu_BM25(avg_question_length,question_length[index],question_word_num_dict,sentence_words_list,question_temp_word_num,len(question_length))
        BM25_scores_list.append(BM25_score_question_temp_user_question)
    BM25_score_sum = np.sum(np.array(BM25_scores_list))
    return BM25_scores_list/BM25_score_sum
    
def get_bm25_main(file_path,user_question):
    catalog_path = os.path.join(file_path,'catalog.txt')
    disease_dict,disease_list = get_disease_dict(catalog_path)
    catalog_file_path = './userdict_jieba_test.txt'
    sentence_words_list = get_segement_words(catalog_file_path,user_question)
    #category = get_category(str(user_question),disease_list)
    category = get_category(sentence_words_list,disease_list)
    if category == 'other':
        #print '找不到所找疾病信息'
        return category,[]
    else:
        embedding_list = get_bm25(category,file_path,disease_dict,user_question)
        #max_index = embedding_list.tolist().index(max(embedding_list.tolist()))
        #print str(max_index)
            
        if embedding_list == []:
            return category,[]
        else:
            #print 'category : ',category
            #print 'embedding_list : ',str(embedding_list)
            return category,embedding_list
    
