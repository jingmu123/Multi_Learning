#code=utf-8
import re
import os

class dataLoad:
    def __init__(self,stopspath="stops.txt"):
        '''
			:param stopspath: 停用词地址
			:self.stoplist: 存储停用词
			:self.traindata: 存储获取的语料库
        '''
        self.stoplist=[]
        self.traindata=[]
        self.dataOfDir=[]
        self.stopspath=stopspath

    def loadstop(self):
        '''
            加载停用词，开启停用词过滤时有效,该项目提供的停用词位于"./stops.txt"
			:return: void
        '''
        with open(self.stopspath, encoding="utf-8") as f:
            for item in f.readlines():
                self.stoplist.append(item[:-1])

    def loadData(self,filepath,is_stop):
        '''
			:param filepath:   待读取文件的路径
			:param is_stop:    停用词过滤标志
			:return:
        '''
        if is_stop==True:  #开启停用词时加载
            self.loadstop()
        with open(filepath, "r", encoding="utf-8") as f:
            data = f.read()
            con = data.split("\n")  #去除换行符
            for item in con:
                sp_it = re.split("\s", item)  #分离单词与各个标志
                if sp_it[0] not in self.stoplist:  #过滤停用词
                    self.traindata.append(sp_it)
        return self.traindata

    def dataFromDir(self,rootdir,is_key,key,is_stop):
        '''
			对目录中的所有文件进行处理
			:param rootdir: 待遍历的目录
			:param is_key:  是否对文件名做关键词过滤
			:param key:      识别待读取文件的关键词
			:param is_stop:   是否做停用词过滤
			:return:
        '''
        for dirpath, dirnames, filenames in os.walk(rootdir):
            for filepath in filenames:
                path=os.path.join(dirpath, filepath)
                if (is_key==True and (key not in path)) or not(path.endswith("txt") or path.endswith("conll")):
                    continue
                print(path)
                data=self.loadData(path,is_stop)
                self.savedata(data,"./results11",filepath)
                self.dataOfDir.append(data)
        return self.dataFromDir()

    def savedata(self,data,savepath,filename):
        '''
            处理数据保存
			:param data:  待保存的数据
			:param savepath:  待存储文件的路径
			:param filename:  文件名
			:return:
        '''
        if not os.path.exists(savepath):
            os.mkdir(savepath)
        with open(os.path.join(savepath,filename),"w",encoding="utf-8") as f:
            f.write(str(data))


if __name__ == '__main__':
    '''
		使用样例
	'''
    dl=dataLoad("stops.txt")
    '''data=dl.loadData("./dataset/conll03/eng.train",False)
    for item in data:
        print(item)'''
    dl.dataFromDir("./dataset/broadcast",True,"train",True)

