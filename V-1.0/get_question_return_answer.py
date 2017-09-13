#! /usr/env/bin python
# -*-coding: utf-8 -*-

#本代码用于利用word_embedding及bm25的代码来获取最大余弦距离的问题的编号，然后返回相应的答案

import get_question_embedding
import get_bm25_score
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
import os
import math

def get_disease_dict(catalog_path):
    disease_dict = {}
    for line in open(catalog_path,'rb').readlines():
        line_list = line.strip().split()
        disease_name = line_list[1]
        disease_dict[disease_name] = (line_list[0],line_list[2])
    return disease_dict

def judge_user_question(user_question,disease_dict,embedding_category,file_path_1):
    same_question_flag = False  # 标记是否输入的问题与丁香园数据中的一个问题相同
    for question_index in range(int(disease_dict[embedding_category][1])):
        question_file_name = os.path.join(file_path_1, str(disease_dict[embedding_category][0]),
                                          str(question_index + 1) + '_q.txt')
        question_line = open(question_file_name, 'rb').readline()
        if str(question_line) == user_question:
            same_question_flag = True
            break
        else:
            continue
    return same_question_flag

def main():
    #user_question = raw_input('输入所问问题 ： ')
    user_question = sys.argv[1]
    #print user_question
    file_path = '/usr/mlt/user_upload_test/user_upload_test_data/mix_result_data_segment/'
    file_path_1 = '/usr/mlt/user_upload_test/user_upload_test_data/mix_result_data/'
    gensim_model = '/usr/mlt/user_upload_test/code_jieba/word2vec.model'
    catalog_path = os.path.join(file_path_1,'catalog.txt')
    embedding_category,embedding_similarity = get_question_embedding.get_embedding_main(file_path,user_question,gensim_model)
    #print 'embedding_category : ' , str(embedding_category)
    #下面是给出bm25的相关的近似值
    bm25_category,bm25_similarity = get_bm25_score.get_bm25_main(file_path,user_question)
    disease_dict = get_disease_dict(catalog_path)
    if embedding_category == bm25_category:
        if embedding_category == 'other':
            print u'找不到所找疾病信息'
            sys.exit(0)
        same_question_flag = judge_user_question(user_question,disease_dict,embedding_category,file_path_1)
        if same_question_flag == True:
            similarity_array = np.array(embedding_similarity)
        else:
            similarity_array = np.array(embedding_similarity) + np.array(bm25_similarity)
        #print repr(similarity_array.tolist())
        for item_similarity_array in similarity_array:
            if math.isnan(item_similarity_array):
                print u'找不到所找疾病信息'
                sys.exit(0)
        question_index = similarity_array.tolist().index(np.max(similarity_array))
        category_index = disease_dict[embedding_category][0]
        answer_file_path = os.path.join('/usr/mlt/user_upload_test/user_upload_test_data/mix_result_data/',str(category_index),str(question_index+1)+'_a.txt')
        line = open(answer_file_path,'rb').readline()
        print line
        sys.exit(0)
    else:
        print 'word_embedding与bm25的结果不同，有错'
        sys.exit(1)
    
    
if __name__ == '__main__':
    main()