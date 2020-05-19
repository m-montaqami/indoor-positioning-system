import numpy as np
import pandas as pd
from mydb import db
from get import getinfo
import math


t=getinfo()
db=db()
db.connect()
predict_result=[]
#--------------------------------------------------------
class REPORT:
    def __init__(self):
        pass
    def base_form(self,all_purp):
        text1='\ncreated by m_montaqami\n\n'
        text1+='Linear Regression is used to predict\n:'
        text1+="\nfor this current point we've found the following results: \n"
        def reload(text1,mac_addr,ave_bases,cho_bases,coor,coor_est):
            text1+='\nmac_address     :      %s\n'%(mac_addr)
            text1+='\nthe avalible RPs for this mac_address are    :    %s\n'%ave_bases
            text1+='\nthe three choosed RPs for this mac_address are    :    %s\n'%cho_bases
            text1+='\nthe coordinates of these three RPs are     :     %s\n'%coor
            text1+='\nthe estimated  coordinates based on selected RPs are      :       %s'%coor_est
            return text1
        for i in all_purp:
            coor=[i[4],i[5],i[6]]
            text1=reload(text1,i[0],i[1],i[2],coor,i[7])
        
        file=open('reslt_estimated.txt','w')
        file.write(text1)
        file.close()
        return text1
        
#----------------------------------------------------------
class LR:
    def ml(self):
        t.nlp()
        #position=t.offline_mode()
        #position_mac=list(position.keys())
        #position_rss=list(position.values())
        position_mac=[' ac:67:06:4c:e3:48','f0:9f:c2:7a:e2:9b']
        position_rss=[20,90]
        if position_mac==[]:
            print("There is bo RP in the Database")
            return -1
        for ii in position_mac:
            temp_header=[]
            temp_header.append(ii)
            data=db.export_x_y_rss1(ii)
            if data == [[], [] ,[]]:
                print("this point is not listed of this mac \n ")
                continue
            coordinates=data[0];rss=data[1];point_num=data[2]
            if(len(coordinates)<3):
                print("not enogh points for current position")
                continue
            base_RP=input('We have found the following RP for this Mac_Addr please select three of them as bases [input format: x;x;x] :\n%s : '%(point_num))
            avalible_bases=point_num
            temp_header.append(avalible_bases)
            base_RP=base_RP.split(';');chosed_bases=base_RP
            base_RP=list(point_num.index(int(es)) for es in base_RP)
            temp_header.append(chosed_bases)
            base_RP_coordinate=list(coordinates[es] for es in base_RP)
            temp_header.append(base_RP_coordinate)
            base_RP_rss=list(rss[es] for es in base_RP)
            for (Xenum1,Xenum2,Xenum3) in zip(base_RP_coordinate,base_RP_rss,base_RP):                
                train_x=[]  #train_x is equal to distance from base
                train_y=[]  #train_y is equal to diff of RSS
                for enum in coordinates:
                    train_x.append(math.sqrt(math.pow((enum[0]-Xenum1[0]),2)+math.pow((enum[1]-Xenum1[1]),2)))
                for enum in rss:
                    train_y.append(abs(Xenum2 - enum))
                if 0.0 in train_x:
                    index=train_x.index(0.0)
                    train_x.remove(train_x[index])
                    train_y.remove(train_y[index])
                if train_y==[]:
                    continue
                q=[];ones=[]
                for a in train_x:
                    ones.append(1.)
                q.append(ones)
                q.append(train_x)
                q=np.matrix(q,dtype=float).T
                train_y=np.matrix(train_y,dtype=float).T
                param=np.matrix(np.array([0,0],dtype=float))
#---------------------------------------------------------      
                def cost_function(x, y, param):
                    compute1 = np.power((np.dot(x, param.T) - y), 2)
                    return np.sum(compute1) / (2 * len(y))
#------------------------------------------------
                def gradientdescent(x, y, param, alpha=0.0001):
                    comp = np.dot((np.dot(x, param.T) - y).T, x)
                    param -= (alpha * 1.0 / len(y)) * comp
                iteration = 10000
                cost_values = []
                for i in range(iteration):
                    cost_values.append(cost_function(q, train_y, param))
                    gradientdescent(q,train_y, param)
#------------------------------------------------
                def predict(x1, param):
                    return param[0, 0]+param[0,1]*x1
                ff=predict(position_rss[position_mac.index(ii)],param)
                temp_header.append({Xenum3:ff})
            predict_result.append(temp_header)
#-------------------------------------------------
    def intersection(self,x0, y0, r0, x1, y1, r1):
        d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
        if(d > r0 + r1) :
            return -1
        if(d < abs(r0-r1)):
            return -1
        if(d == 0 and r0 == r1):
            return -1
        else:
            a=(r0**2-r1**2+d**2)/(2*d)
            h=math.sqrt(r0**2-a**2)
            x2=x0+a*(x1-x0)/d   
            y2=y0+a*(y1-y0)/d   
            x3=x2+h*(y1-y0)/d     
            y3=y2-h*(x1-x0)/d 
            x4=x2-h*(y1-y0)/d
            y4=y2+h*(x1-x0)/d
            return (x3, y3, x4, y4)
#------------------------------------------------------------
    def final_result(self,inp):
        res_f=inp;
        for i in inp:
            buff2=[]
            index1=inp.index(i)
            coor=i[3]
            x1=i[4];x1=list(x1.values())[0]
            x2=i[5];x2=list(x2.values())[0]
            x3=i[6];x3=list(x3.values())[0]
            intersect1=LR.intersection(coor[0][0],coor[0][1],x1,coor[1][0],coor[1][1],x2)
            intersect2=LR.intersection(coor[1][0],coor[1][1],x2,coor[2][0],coor[2][1],x3)
            if(intersect1==-1 or intersect2==-1):
                print('can not intersect')
                res_f[index1].append(['can not intersect'])
                continue
            buff=[];rel=[(intersect1[0],intersect1[1]),(intersect1[2],intersect1[3]),(intersect1[0],intersect1[1]),(intersect1[2],intersect1[3])]
            buff.append(math.sqrt(math.pow((intersect1[0]-intersect2[0]),2)+math.pow((intersect1[1]-intersect2[1]),2)))
            buff.append(math.sqrt(math.pow((intersect1[0]-intersect2[2]),2)+math.pow((intersect1[1]-intersect2[3]),2)))
            buff.append(math.sqrt(math.pow((intersect1[2]-intersect2[0]),2)+math.pow((intersect1[3]-intersect2[1]),2)))
            buff.append(math.sqrt(math.pow((intersect1[2]-intersect2[2]),2)+math.pow((intersect1[3]-intersect2[3]),2)))
            buff_min=min(buff);ind=buff.index(buff_min)
            res=rel[ind];buff2.append(res)
            res_f[index1].append(buff2)
        return res_f

    
LR=LR()
LR.ml()
result=LR.final_result(predict_result)
RE=REPORT()
TEXT=RE.base_form(result)

