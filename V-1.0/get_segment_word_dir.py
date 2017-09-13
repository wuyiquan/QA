# /usr/env/bin python
# -*- coding: utf-8 -*-

#本代码用于新建丁香园对应数据的文件夹，来存储分词的结果

import commands
import os
import sys

def main():
     segement_path = sys.argv[1]
     for index in range(4):
        file_index = index
        dir_path = os.path.join(segement_path,str(file_index))
        print dir_path
        commands.getstatusoutput('mkdir ' + dir_path)
    
if __name__ == '__main__':
    main()