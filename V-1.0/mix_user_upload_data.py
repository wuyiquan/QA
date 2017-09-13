# /usr/env/bin python
# -*- coding: utf-8 -*-

#本程序用于将用户多次上传的数据进行合并，每次用户上传的数据被分类后都被存储在一个命名为category_for_upload_file_k(k代表第几次上传的文件)的文件夹中

#sys.argv[1]代表用户上传的文件被分类后的大的文件夹的位置，其中的各个小文件夹叫做category_for_upload_file_k，
#sys.argv[2]代表一共上传了几次文件
#sys.argv[3]代表最终合成后的总体文件夹的路径


import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import commands

def copy_file_upload_segment_data_1(result_path,segment_dir_path):
    commands.getstatusoutput('cp -r ' + segment_dir_path + '/. ' + result_path)

def get_category_dict(category_file_path):
    disease_total_num = 0
    catalog_file = open(category_file_path,'rb')
    catalog_dict = {} #key为编号，value为（疾病名，对应问题数目）
    for line in catalog_file.readlines():
        line_list = line.strip().split()
        disease_name = line_list[1]
        if disease_name not in catalog_dict:
            catalog_dict[disease_name] = [int(line_list[0]),int(line_list[2])] #catalog_dict的key为disease的name，disease的value为disease的序号，与disease的问题数目
            disease_total_num += 1
    return catalog_dict
    
def copy_same_disease_segment_file_to_result_file(disease_name,segment_dir_path,result_path,result_category_dict,segment_category_dict):
    segment_dir_file_num = segment_category_dict[disease_name][1]
    segement_dir_path_for_disease = os.path.join(segment_dir_path,str(segment_category_dict[disease_name][0]))
    result_dir_path_for_disease = os.path.join(result_path,str(result_category_dict[disease_name][0]))
    result_dir_file_num = result_category_dict[disease_name][1]
    for file_index in range(segment_dir_file_num):
        question_index = str(file_index + 1)
        result_question_index = str(result_dir_file_num + 1)
        print 'question_index : ',question_index
        print 'result_question_index : ',result_question_index
        commands.getstatusoutput('cp ' + segement_dir_path_for_disease + '/'  + question_index + '_q.txt ' + result_dir_path_for_disease + '/' + result_question_index + '_q.txt')
        commands.getstatusoutput('cp ' + segement_dir_path_for_disease + '/'  + question_index + '_a.txt ' + result_dir_path_for_disease + '/' + result_question_index + '_a.txt')
        if os.path.isfile(segement_dir_path_for_disease + '/'  + question_index + '__similarity.txt'):
            commands.getstatusoutput('cp ' + segement_dir_path_for_disease + '/'  + question_index + '__similarity.txt ' + result_dir_path_for_disease + '/' +  + result_question_index + '__similarity.txt')
        result_dir_file_num += 1
    result_category_dict[disease_name][1] = result_dir_file_num
    return result_category_dict
    
def copy_different_disease_segment_file_to_result_file(disease_name,segment_dir_path,result_path,result_category_dict,segment_category_dict):
    segment_dir_file_num = segment_category_dict[disease_name][1]
    segement_dir_path_for_disease = os.path.join(segment_dir_path,str(segment_category_dict[disease_name][0]))
    if disease_name == 'other': #若新添加的疾病为other类型，则将这个疾病的序号设为0
        result_disease_index = 0
    else:
        result_disease_index = len(result_category_dict) + 1
    print 'result_disease_index : ' + str(result_disease_index)
    result_copy_path = os.path.join(result_path,str(result_disease_index))
    commands.getstatusoutput('cp -r ' + segement_dir_path_for_disease + '/. ' + result_copy_path)
    result_category_dict[disease_name] = [result_disease_index,segment_dir_file_num]
    return result_category_dict
    
def write_catalog_file(result_path,result_category_dict):
    catalog_file_path = os.path.join(result_path,'catalog.txt')
    file_write = open(catalog_file_path,'wb')
    for disease_name in result_category_dict:
        file_write.write(str(result_category_dict[disease_name][0]) + '\t' + str(disease_name) + '\t' + str(result_category_dict[disease_name][1]) + '\n')
    file_write.close()
    
def mix_segment_file(segment_dir_path,result_path):
    result_file_catalog_file_path = os.path.join(result_path,'catalog.txt')
    result_category_dict = get_category_dict(result_file_catalog_file_path)
    segment_catalog_file_path = os.path.join(segment_dir_path,'catalog.txt')
    segment_category_dict = get_category_dict(segment_catalog_file_path)
    for disease_name in segment_category_dict:
        if disease_name in result_category_dict:
            #将segment_dir_path与result_path中相同的disease_name内的问题放到同一个文件夹之下，并且更新result_category_dict[disease_name][1]的数目
            result_category_dict = copy_same_disease_segment_file_to_result_file(disease_name,segment_dir_path,result_path,result_category_dict,segment_category_dict)
        else:
            #将segment_dir_path中的相应的disease文件夹下的文件复制到result_path中，并且更新result_category_dict
            result_category_dict = copy_different_disease_segment_file_to_result_file(disease_name,segment_dir_path,result_path,result_category_dict,segment_category_dict)
    os.remove(result_file_catalog_file_path)
    write_catalog_file(result_path,result_category_dict) #将result_path中的catalog.txt更新为添加疾病后的情况
    
def main():
    segment_file_path = sys.argv[1]
    dir_num = int(sys.argv[2])
    result_path = sys.argv[3] #最后的合成结果文件夹
    #首先将upload_segment_data_1中的所有文件复制到result_path中
    segment_dir_path = os.path.join(segment_file_path,'category_for_upload_file_1')
    copy_file_upload_segment_data_1(result_path,segment_dir_path)
    for index in range(dir_num):
        segment_dir_path = os.path.join(segment_file_path,'category_for_upload_file_' + str(index+1))
        mix_segment_file(segment_dir_path,result_path) #将segment_dir_path中的文件与result_path的文件进行合并

    
if __name__ == '__main__':
    main()