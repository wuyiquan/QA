#! /usr/env/bin python
# -*-coding: utf-8 -*-

#本代码用于对于用户上传的文件进行分词，然后进行对于分词之后的文件的问题和答案分别存储下来，随后将用户上传的问题、相似问题、答案分类到相关的类别中
#对于用户上传的问题如果有分类的话，则存储到对应的类别中，如果没有分类，则存储到0号文件夹中，同时，对于所有分类和问题存储到一个txt文件中，来写明每一类的文件夹序号、类名、文件夹中的问题数目

#用户上传的文件的格式为：问题\t答案\t相似问题\t问题类型（其中相似问题与问题类型这两项为可选的，一个文件在上传时会表明是否有这两项）
#对于没有问题类型的问题及答案均存储到0号文件夹中

#每次用户上传的文件进行分类后生成的所有文件夹与之前上传的文件分类后生成的文件夹放在不同的文件夹下，catelog文件放在分类后生成的文件夹的同级目录中
#不用记录之前上传的种类数目，只针对这次的训练文件进行分类

#每次针对新上传的数据进行分词并生成对应的含有question，similar question ,answer的文件夹及catalog文件，之后再对于所有的文件（包含过去上传的与当前上传的）进行分词，生成一份新的分词文件，来进行分词处理（将用户上传的词典导入之后再分词）

#sys.argv[1]代表用户上传的训练文件的路径，sys.argv[2]代表是否有相似问题选项，sys.argv[3]代表是否有问题类型这个项目，sys.argv[4]代表存储的catalog文件和分类后的问题答案文件的路径


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import commands
import os

def write_catelog_file(category_dict,catalog_file_path):
    for category_name in category_dict:
        file_write = open(catalog_file_path,'ab+')
        file_write.write(str(category_dict[category_name][0]) + '\t' + str(category_name) + '\t' + str(category_dict[category_name][1]) + '\n')
        file_write.close()

def get_catalog(file_path,similarity_question_flag,question_category_flag,catalog_file_path):
    #新建一个对于该用户新上传的文件生成其catelog文件（为一个新的文件，不跟在原文件的后面，只是将新的分类后的文件跟原来的文件放在一个大的文件夹下，而catelog文件也与原来的catelog文件放在一个文件夹下）
    file_read = open(file_path,'rb')
    category_index = 1
    if similarity_question_flag == 1 and question_category_flag == 1:
        category_dict = {}
        for line in file_read.readlines():
            line_list = line.strip().split()
            question = line_list[0]
            answer = line_list[1]
            category_name = line_list[3]
            if category_name not in category_dict:
                category_dict[category_name] = [category_index,1] #第一项为category_index，第二项为该类别内部的问题数目
                category_index += 1
            else:
                category_dict[category_name][1] += 1
        write_catelog_file(category_dict,catalog_file_path)
    elif similarity_question_flag == 0 and question_category_flag == 1:
        category_dict = {}
        for line in file_read.readlines():
            line_list = line.strip().split()
            question = line_list[0]
            answer = line_list[1]
            category_name = line_list[2]
            if category_name not in category_dict:
                category_dict[category_name] = [category_index,1] #第一项为category_index，第二项为该类别内部的问题数目
                category_index += 1
            else:
                category_dict[category_name][1] += 1
        write_catelog_file(category_dict,catalog_file_path)
    elif question_category_flag == 0:
        category_index = 0
        category_dict = {}
        for line in file_read.readlines():
            line_list = line.strip().split()
            question = line_list[0]
            answer = line_list[1]
            category_name = 'other'
            if category_name not in category_dict:
                category_dict[category_name] = [category_index,1] #第一项为category_index，第二项为该类别内部的问题数目
                category_index += 1
            else:
                category_dict[category_name][1] += 1
        write_catelog_file(category_dict,catalog_file_path)
    return category_dict

def write_question_answer_similarity_question_file(got_file_path,file_read,category_dict):
    category_index_list = [] #用来存储已经建立好分类文件夹的问题类别的名字
    category_index_dict = {} #用来存储每一个分类中已经存储的问题答案的序号
    for line in file_read.readlines():
        line_list = line.strip().split()
        question = line_list[0]
        answer = line_list[1]
        similarity_question = line_list[2]
        category_name = line_list[3]
        category_index = category_dict[category_name][0]
        dir_path = os.path.join(got_file_path,str(category_index))
        if category_index not in category_index_list:
            commands.getstatusoutput('mkdir ' + dir_path)
            category_index_list.append(category_index)
        if category_index not in category_index_dict:
            category_index_dict[category_index] = 1
        else:
            category_index_dict[category_index] += 1
        question_temp_index = category_index_dict[category_index]
        file_question_write = open(os.path.join(dir_path,str(question_temp_index) + '_q.txt'),'wb')
        file_question_write.write(question + '\n')
        file_question_write.close()
        file_answer_write = open(os.path.join(dir_path,str(question_temp_index) + '_a.txt'),'wb')
        file_answer_write.write(answer + '\n')
        file_answer_write.close()
        file_similarity_question_write = open(os.path.join(dir_path,str(question_temp_index) + '_q_similarity.txt'),'wb')
        file_similarity_question_write.write(similarity_question + '\n')
        file_similarity_question_write.close()
        
def write_question_answer_file(got_file_path,file_read,category_dict):
    category_index_list = [] #用来存储已经建立好分类文件夹的问题类别的名字
    category_index_dict = {} #用来存储每一个分类中已经存储的问题答案的序号
    for line in file_read.readlines():
        line_list = line.strip().split()
        question = line_list[0]
        answer = line_list[1]
        category_name = line_list[2]
        category_index = category_dict[category_name][0]
        dir_path = os.path.join(got_file_path,str(category_index))
        if category_index not in category_index_list:
            commands.getstatusoutput('mkdir ' + dir_path)
            category_index_list.append(category_index)
        if category_index not in category_index_dict:
            category_index_dict[category_index] = 1
        else:
            category_index_dict[category_index] += 1
        question_temp_index = category_index_dict[category_index]
        file_question_write = open(os.path.join(dir_path,str(question_temp_index) + '_q.txt'),'wb')
        file_question_write.write(question + '\n')
        file_question_write.close()
        file_answer_write = open(os.path.join(dir_path,str(question_temp_index) + '_a.txt'),'wb')
        file_answer_write.write(answer + '\n')
        file_answer_write.close()
        
def write_question_answer_similarity_question_file_other_category(got_file_path,file_read,category_dict):
    category_index_list = [] #用来存储已经建立好分类文件夹的问题类别的名字
    category_index_dict = {} #用来存储每一个分类中已经存储的问题答案的序号
    for line in file_read.readlines():
        line_list = line.strip().split()
        question = line_list[0]
        answer = line_list[1]
        similarity_question = line_list[2]
        category_name = 'other'
        category_index = category_dict[category_name][0]
        dir_path = os.path.join(got_file_path,str(category_index))
        if category_index not in category_index_list:
            commands.getstatusoutput('mkdir ' + dir_path)
            category_index_list.append(category_index)
        if category_index not in category_index_dict:
            category_index_dict[category_index] = 1
        else:
            category_index_dict[category_index] += 1
        question_temp_index = category_index_dict[category_index]
        file_question_write = open(os.path.join(dir_path,str(question_temp_index) + '_q.txt'),'wb')
        file_question_write.write(question + '\n')
        file_question_write.close()
        file_answer_write = open(os.path.join(dir_path,str(question_temp_index) + '_a.txt'),'wb')
        file_answer_write.write(answer + '\n')
        file_answer_write.close()
        file_similarity_question_write = open(os.path.join(dir_path,str(question_temp_index) + '_q_similarity.txt'),'wb')
        file_similarity_question_write.write(similarity_question + '\n')
        file_similarity_question_write.close()
        
def write_question_answer_file_other_category(got_file_path,file_read,category_dict):
    category_index_list = [] #用来存储已经建立好分类文件夹的问题类别的名字
    category_index_dict = {} #用来存储每一个分类中已经存储的问题答案的序号
    for line in file_read.readlines():
        line_list = line.strip().split()
        question = line_list[0]
        answer = line_list[1]
        category_name = 'other'
        category_index = category_dict[category_name][0]
        dir_path = os.path.join(got_file_path,str(category_index))
        if category_index not in category_index_list:
            commands.getstatusoutput('mkdir ' + dir_path)
            category_index_list.append(category_index)
        if category_index not in category_index_dict:
            category_index_dict[category_index] = 1
        else:
            category_index_dict[category_index] += 1
        question_temp_index = category_index_dict[category_index]
        file_question_write = open(os.path.join(dir_path,str(question_temp_index) + '_q.txt'),'wb')
        file_question_write.write(question + '\n')
        file_question_write.close()
        file_answer_write = open(os.path.join(dir_path,str(question_temp_index) + '_a.txt'),'wb')
        file_answer_write.write(answer + '\n')
        file_answer_write.close()
            
def get_category(file_path,similarity_question_flag,question_category_flag,got_file_path,category_dict):
    file_read = open(file_path,'rb')
    category_index = 1
    if similarity_question_flag == 1 and question_category_flag == 1:
        write_question_answer_similarity_question_file(got_file_path,file_read,category_dict)
    elif similarity_question_flag == 0 and question_category_flag == 1:
        write_question_answer_file(got_file_path,file_read,category_dict)
    elif similarity_question_flag == 1 and question_category_flag == 0:
        write_question_answer_similarity_question_file_other_category(got_file_path,file_read,category_dict)
    elif similarity_question_flag == 0 and question_category_flag == 0:
        write_question_answer_file_other_category(got_file_path,file_read,category_dict)

def main():
    file_path = sys.argv[1]
    similarity_question_flag = int(sys.argv[2])
    question_category_flag = int(sys.argv[3])
    got_file_path = sys.argv[4]
    catalog_file_path = os.path.join(got_file_path,'catalog.txt')
    category_dict = get_catalog(file_path,similarity_question_flag,question_category_flag,catalog_file_path)
    get_category(file_path,similarity_question_flag,question_category_flag,got_file_path,category_dict)
    
if __name__ == '__main__':
    main()