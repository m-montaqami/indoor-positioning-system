import os,winwifi
import time

class getinfo:
    
    def __init__(self):
        winwifi.WinWiFi.scan()
        a=os.system("netsh wlan show networks mode=Bssid>1.txt")
        b=open('1.txt')
        self.b=list(b)
        self.name=[]
        self.signal=[]
        self.d={}
        self.namef=[]
        self.signalf=[]
    #------------------------------------------------------------------------------
    def nlp(self):
        for i in range(0,len(self.b)-1):
            if 'SSID' in self.b[i]:
                self.name.append(self.b[i])
            if 'Signal' in self.b[i]:
                self.signal.append(self.b[i])
        for i in range(len(self.signal)):
            if '\n' in self.signal[i]:
                self.signal[i]=self.signal[i].replace('\n','')
        for i in range(len(self.name)):
            if '\n' in self.name[i]:
                self.name[i]=self.name[i].replace('\n','')
        for i in range(len(self.name)):
            if 'BSSID 1' in self.name[i]:
                q=self.name[i].find(':')
                self.namef.append(self.name[i][q+1:])
        for i in range(len(self.signal)):
            w=self.signal[i].find(':')
            self.signalf.append(self.signal[i][w+1:])
        for i in range(len(self.signalf)):
            if '%' in self.signalf[i]:
                self.signalf[i]=self.signalf[i].replace('%','')
        for i in range(len(self.namef)):
            self.d[self.namef[i]]=self.signalf[i]
        return self.d    
    #------------------------------------------------------------------------------
    def intodb(self,data):
        from mydb import db
        m = db()
        ins_index=input("please insert the point id: ")
        for key,value in data.items():
            print(key,value)
            m.ins(str(key),str(value) , ins_index)
        return ins_index
    #------------------------------------------------------------------------------
    def offline_mode(self):
        c={}
        for key,value in self.d.items():
            c[ key]=value
        return c
    #------------------------------------------------------------------------------
    def counter(self,lis,dic={}):
         for enum in lis:
             for dd,kk in zip(enum.keys(),enum.values()):
                 if dd in dic.keys():
                     v=dic[dd];v=str(v)
                     if(')') in v:
                         v=v.replace(')','')
                     if('(') in v:
                         v=v.replace('(','')
                     if('[') in v:
                         v=v.replace('[','')
                     if(']') in v:
                         v=v.replace(']','')
                     if('"') in v:
                         v=v.replace('"','')
                     if('\n') in v:
                         v=v.replace('\n','')
                     if("'") in v:
                         v=v.replace("'",'')
                     v=v.split(',');v=list(int(i) for i in v)
                     v.append(kk)
                     dic[dd]=v
                     continue
                 dic[dd]=kk
         return dic
    #-----------------------------------------------------------------------------
def online_mode():
    data=[]
    for enum in range(20):
        try:
            t=getinfo()
            d=t.nlp()
            d=dict((i,int(j)) for (i,j) in d.items())
            data.append(d)
            print("%s is passed"%(str(enum+1)))
        except:
            print("%s is failed"%(str(enum+1)))

    f=open('data.txt','a+')
    for i in data:    
        f.write(str(i))
    f.close()
    print('Do you want to apply the data to database?')
    inp=input("y)yes n)no: ")
    if(inp=="Y" or inp=="y"):
        data=[]
        f=open('data.txt');f=list(f);
        for enum3 in f:
            enum3=enum3.split('}')
            for enum4 in enum3:
                if('{') in enum4:
                    enum4=enum4.replace('{','')
                if('}') in enum4:
                    enum4=enum4.replace('}','')
                enum4=enum4.split(',')
                for enum5 in enum4:
                    enum5=enum5.split(': ')
                    try:
                        dict_s={};dict_s[enum5[0]]=int(enum5[1])
                        data.append(dict_s)
                    except:
                        print('')
                    
        f=open('data.txt','w');f.close()
        r1=t.counter(data)
        data_main={}
        for k,v in r1.items():
            if(str(type(v))=="<class 'int'>"):
                continue
            if (len(v))<30:
                continue
            data_main[k[2:-1]]=round(sum(v)/len(v))
        ins_index=t.intodb(data_main)
        file=open('export.txt','a+')
        file.write('\nid=%s=====>>\n'%(ins_index))
        file.write(str(r1))
        file.close()

