#! /usr/env/bin python
# -*-coding: utf-8 -*-

import os
import io
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
import jieba

def splitques(ques):#利用jieba对问题进行分词
    jieba.load_userdict('./userdict_jieba_test.txt')
    wordlist = jieba.lcut(ques, cut_all = False)
    return wordlist

def get_theme(user_question):
    pass
    #return theme

def get_answer(user_question, theme):
    pass
    #return
def main():
    #获取用户的问题
    #user_question = raw_input('输入所问问题 ： ')
    print sys.getdefaultencoding()
    print "您好"
    #找到相关主题
    #theme = get_theme(user_question)
    #if theme == -1:
    #    print "抱歉，未找到相关问题。"
    #    sys.exit(1)
    #寻找答案
    #answer = get_answer(user_question, theme)
    #输出答案
    #answer_file_path = os.path.join('./data/data/',str(theme),str(answer)+'_a.txt')
    #line = open(answer_file_path,'rb').readline()
    #print line
    
    sys.exit(0)

if __name__ == '__main__':
    main()
    
