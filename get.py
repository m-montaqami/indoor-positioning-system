import os
# from mynewdb import db
# m=db()
a=os.system("netsh wlan show networks mode=Bssid>e:/pytest/1.txt")
b=open('e:/pytest/1.txt')
b=list(b)
name=[]
signal=[]
d={}
namef=[]
signalf=[]
class getinfo:
    def __init__(self):
        pass
    def nlp(self):


        for i in range(0,len(b)-1):
            if 'SSID' in b[i]:
                name.append(b[i])
            if 'Signal' in b[i]:
                signal.append(b[i])
        for i in range(len(signal)):
            if '\n' in signal[i]:
                signal[i]=signal[i].replace('\n','')
# print(signal,len(signal))
        for i in range(len(name)):
            if '\n' in name[i]:
                name[i]=name[i].replace('\n','')
        # print(len(name),len(signal))
        for i in range(len(name)):
            if 'BSSID 1' in name[i]:
                q=name[i].find(':')
                namef.append(name[i][q+1:])
        # print(len(name), len(signal))
        for i in range(len(signal)):
            w=signal[i].find(':')
            signalf.append(signal[i][w+1:])
        for i in range(len(signalf)):
            if '%' in signalf[i]:
                signalf[i]=signalf[i].replace('%','')
        # d={}

        for i in range(len(namef)):
            d[namef[i]]=signalf[i]
        # print(len(namef), namef,signalf,len(signalf))
        # print(d)
    def intodb(self):

        from mynewdb import db
        m = db()
        for key,value in d.items():
            print(key,value)
            m.ins(str(key),str(value))
            # print(key,value)
    def offline_mode(self):
        c={}
        for key,value in d.items():
            c[ key]=value
        print(c)
        return c


# t=getinfo()
# t.nlp()
# t.intodb()
# t.offline_mode()









