# /usr/env/bin python
# -*- coding: utf-8 -*-

#本代码用于对于用户上传的数据进行数据清洗及分词，字符串的分词的结果存储到一个单独的文件夹中
#sys.argv[1]代表丁香园数据的位置，sys.argv[2]代表丁香园数据中的病的种类数目(不包括0类)，sys.argv[3]代表分好词的丁香园的数据位置，分词的结果也是按照病的种类编号存储在对应文件夹中
#sys.argv[4]代表存储无法分词的文件的地址的路径, sys.argv[5]为分词时分词文件的路径, sys.argv[6]为分完词后存储分词的文件为word2vec做准备的文件的路径
#sys.argv[7]代表用户是否上传了分词文件，sys.argv[8]代表用户上传的分词文件的路径

import sys
import pynlpir
import os
import codecs
import commands

import jieba

def get_segement_words(catalog_file_path,sentence,query_id):
    #输入为一个string的句子，输出为这个句子的分解的单词
    print 'sentence : ' + str(sentence)
    try:
        jieba.load_userdict(catalog_file_path)
        sentence_words_list = jieba.lcut(sentence,cut_all = False)
        return sentence_words_list
    except BaseException:
        return ['ERROR',str(query_id)]
        
def write_sentence_word(write_file_name,sentence_list):
    file_write = codecs.open(write_file_name,'ab+','utf-8')
    for word in sentence_list:
        file_write.write(word+'\t')
    file_write.write('\n')
    print str(sentence_list) + 'done'

def get_user_dict(catalog_file_path,user_dict_file_path):
    file_write = open(user_dict_file_path,'wb')
    for line in open(catalog_file_path,'rb').readlines():
        line_list = line.strip().split()
        disease_name = line_list[1]
        file_write.write(str(disease_name)+'\n')
    file_write.close()
        
def get_segmentation_dir(word_path,data_path):
    catalog_file_path = os.path.join(data_path,'catalog.txt')
    catalog_file = open(catalog_file_path,'rb')
    catalog_dict = {} #key为编号，value为（疾病名，对应问题数目）
    for line in catalog_file.readlines():
        line_list = line.strip().split()
        disease_index = int(line_list[0])
        if disease_index not in catalog_dict:
            catalog_dict[disease_index] = (line_list[1],int(line_list[2]))
    for disease_index in catalog_dict:
        dir_path = os.path.join(word_path,str(disease_index))
        commands.getstatusoutput('mkdir ' + dir_path)
        
    
def get_words(data_path,category_num,word_path,error_file_path,user_dict_file_path,word2vec_path,if_upload_category_file,upload_file_path):
    catalog_file_path = os.path.join(data_path,'catalog.txt')
    catalog_file = open(catalog_file_path,'rb')
    catalog_dict = {} #key为编号，value为（疾病名，对应问题数目）
    for line in catalog_file.readlines():
        line_list = line.strip().split()
        disease_index = int(line_list[0])
        if disease_index not in catalog_dict:
            catalog_dict[disease_index] = (line_list[1],int(line_list[2]))
    get_user_dict(catalog_file_path,user_dict_file_path) #获取用户上传的字典，利用catalog.txt中的病名作为字典的内容，存储到一个text文档中
    jieba.load_userdict(user_dict_file_path)
    if if_upload_category_file == 'yes':
        jieba.load_userdict(upload_file_path)
    if os.path.exists(os.path.join(data_path,str(0))):
        file_num = catalog_dict[0][1]
        for file_index in range(file_num):
            file_index_temp = file_index + 1
            file_index_path = str(file_index_temp) + '_q.txt'
            question_file = open(os.path.join(data_path,str(0),file_index_path),'rb')
            question_line = question_file.readline()
            query_word_list = get_segement_words(user_dict_file_path,question_line,str(0)+ '/' + file_index_path)
            if query_word_list[0] == 'ERROR':
                error_file = open(error_file_path,'ab+')
                error_file.write(str(query_word_list[1]) + '\n')
                error_file.close()
                continue
            write_file_name = os.path.join(word_path,str(0),file_index_path)
            write_sentence_word(write_file_name,query_word_list)
            write_sentence_word(word2vec_path,query_word_list)
            
    for index in range(category_num):
        category_index = index + 1
        file_num = catalog_dict[category_index][1]
        for file_index in range(file_num):
            file_index_temp = file_index + 1
            file_index_path = str(file_index_temp) + '_q.txt'
            question_file = open(os.path.join(data_path,str(category_index),file_index_path),'rb')
            question_line = question_file.readline()
            query_word_list = get_segement_words(user_dict_file_path,question_line,str(category_index)+ '/' + file_index_path)
            if query_word_list[0] == 'ERROR':
                error_file = open(error_file_path,'ab+')
                error_file.write(str(query_word_list[1]) + '\n')
                error_file.close()
                continue
            write_file_name = os.path.join(word_path,str(category_index),file_index_path)
            write_sentence_word(write_file_name,query_word_list)
            write_sentence_word(word2vec_path,query_word_list)
            
    commands.getstatusoutput('cp ' + os.path.join(data_path,'catalog.txt') + ' ' + os.path.join(word_path,'catalog.txt'))
            

def main():
    data_path = sys.argv[1]
    word_path = sys.argv[3]
    category_num = int(sys.argv[2])
    error_file_path = sys.argv[4]
    user_dict_file_path = sys.argv[5]
    word2vec_path = sys.argv[6]
    if_upload_category_file = sys.argv[7]
    upload_file_path = sys.argv[8]
    get_segmentation_dir(word_path,data_path)
    get_words(data_path,category_num,word_path,error_file_path,user_dict_file_path,word2vec_path,if_upload_category_file,upload_file_path)

if __name__ == '__main__':
    main()