import mysql.connector as mc
import math
import pandas as pd


class db:
    def __init__(self):
        #connection string
        self.cstring = mc.connect(user='root', password='', host='127.0.0.1', database='proj')
    #-----------------------------------------------------------------------------------------   
    def connect(self):
        try:
            self.cstring
            # WE ARE TRYING TO CONNECT TO THE DATABASE
            print('connection string is working ....')
        except:
            print('it looks something wrong with your connection string or directory')
    #-----------------------------------------------------------------------------------------
    def query(self):
        cursor=self.cstring.cursor()
        cursor.execute("SELECT * FROM ap  ")
        for(id) in cursor:
            print("{}\n".format(id))
    #-----------------------------------------------------------------------------------------
    def ins(self,key,value , ins_index):
        cursor1 = self.cstring.cursor()
        cursor2 = self.cstring.cursor()
        cursor2.execute("SELECT id FROM `ap` ORDER BY id DESC LIMIT 1")
        for id in cursor2:
            i=id
        i=i[0]+1
        cursor1.execute("SELECT point_num FROM `ap` ORDER BY point_num DESC LIMIT 1 ")
        cursor1.fetchall()
        q="INSERT INTO `ap` (`id`, `mac_add`, `rss1`, `x`,`y`,`point_num`) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor1.execute(q,(i,key,value,0,0,ins_index))
        self.cstring.commit()
    #-----------------------------------------------------------------------------------------
    def coordinate(self):
        cursor3=self.cstring.cursor()
        cursor2=self.cstring.cursor()
        k=int(input("please enter the point number "))
        print("please select your coordinate for this point")
        x=float(input("\nx:"))
        y=float(input("\ny:"))
        cursor3.execute("UPDATE `ap` SET x=%s , y='%s' WHERE point_num=%s"%(x,y,k))
        self.cstring.commit()
    #-----------------------------------------------------------------------------------------
    def export(self,mac,pn):
        cursor=self.cstring.cursor()
        q="SELECT x,y,rss1 FROM `ap` WHERE mac_add='%s' AND  point_num NOT LIKE %s"
        cursor.execute(q % (mac,pn))
        result=cursor.fetchall()
        x=[];y=[];rss=[]
        for x1,y1,rss1 in result:
            x.append(x1)
            y.append(y1)
            rss.append(rss1)
        if rss==[]:
            return [[],[],[]]
        return x,y,rss
    #-----------------------------------------------------------------------------------------
    def export_rss_pointnum(self,mac):
        cursor4=self.cstring.cursor()
        answer_rss={}
        k=mac
        q="SELECT point_num,rss1 FROM `ap` WHERE `mac_add`='%s' "
        cursor4.execute(q%(k))
        result=cursor4.fetchall()
        for (point_num ,rss1) in result:
            answer_rss[point_num]=rss1
        return answer_rss
    #------------------------------------------------------------------------------------------
    def export_x_y(self,mac,pnum):
        cursor7=self.cstring.cursor()
        ll={};pq={};rp=[]
        k=mac
        q ="SELECT x,y,rss1 FROM `ap` WHERE `mac_add`='%s' "
        q1="SELECT rss1 FROM `ap` WHERE `mac_add`='%s' and point_num=%s "
        cursor7.execute(q%(k))
        result=cursor7.fetchall()
        cursor8 = self.cstring.cursor()
        cursor8.execute(q1 % (k,pnum))
        result1=cursor8.fetchall()
        for rss1 in result1:
            rp.append(rss1)
        if rp==[]:
            return {}
        for (x,y,rss1) in result:
            pos=math.sqrt((x-1000)**2+(y-1000)**2)
            rs=abs(rss1-list(rp[0])[0])
            ll[pos]=rs
        return ll
    #------------------------------------------------------------------------------------------
    def export_x_y_rss(self,mac,AP_pn):
        cursor=self.cstring.cursor()
        q="SELECT x,y,rss1 FROM `ap` WHERE `mac_add`='%s' AND point_num LIKE %s "
        cursor.execute(q % (mac,AP_pn))
        result=cursor.fetchall()
        x=[];y=[];rss=[]
        for x1,y1,rss1 in result:
            x.append(x1)
            y.append(y1)
            rss.append(rss1)
        if rss==[]:
            return [[],[],[]]
        return x,y,rss
    #------------------------------------------------------------------------------------------
    def export_x_y_rss1(self,mac_addr):
        cursor=self.cstring.cursor()
        q="SELECT x,y,rss1,point_num FROM `ap` WHERE `mac_add`='%s'  "
        cursor.execute(q%(mac_addr))
        result=cursor.fetchall()
        d=[];rss=[];point_num=[]
        for x,y,rss1,pn in result:
            #d[x]=y
            #macs.append(ascii(mac)[12:30])
            d.append([x,y])
            rss.append(rss1)
            point_num.append(pn)
        return (d,rss,point_num)
    #------------------------------------------------------------------------------------------
    def export_rss(self,pn,mac):
        cursor=self.cstring.cursor()
        q="SELECT rss1 FROM `ap` WHERE `mac_add`='%s' and `point_num`=%s  "
        cursor.execute(q%(mac,pn))
        laa=[]
        for a in cursor:
            l=a
            laa.append(a)
        if laa==[]:
            return 0
        return int(l[0])
    #-------------------------------------------------------------------------------------------
    def export_pd_format(self):
        h=pd.read_sql("SELECT * FROM ap ",self.cstring)
        return h
    #-------------------------------------------------------------------------------------------    
    def export_info_algo(self,g):
        q="SELECT rss1,mac_add FROM ap WHERE point_num=%s "
        cursor=self.cstring.cursor()
        cursor.execute(q%(g))
        c={}
        for rss,mac_add in cursor:
            c[mac_add]=rss
        if c=={}:
            return 0
        return c
    #-------------------------------------------------------------------------------------------
    def export_coordinate_algo(self,p):
        q="SELECT x,y FROM ap WHERE point_num=%s LIMIT 1 "
        cursor=self.cstring.cursor()
        cursor.execute(q%(p))
        c=[[],[]]
        for x,y in cursor:
            c.append(x)
            c.append(y)
        if c==[]:
            return 0
        return c
    #-------------------------------------------------------------------------------------------
    def ap_matrix(self,abb,pn):
        query_count="SELECT `rss1` FROM `ap` WHERE `mac_add`='%s' and (point_num=%s OR point_num=%s)   "
        query="SELECT `rss1`,`x`,`y` FROM `ap` WHERE `mac_add`='%s' "
        query2="SELECT `rss1`,`x`,`y` FROM `ap` WHERE `mac_add`='%s' and point_num=%s "
        query3="SELECT point_num FROM `ap` WHERE mac_add='%s' ORDER BY rss1 DESC   "
        cursor0=self.cstring.cursor()
        cursor0.execute("SELECT point_num FROM `ap` ORDER BY point_num DESC LIMIT 1")
        j=[]
        for a in cursor0:
            countor=a
            countor=int(countor[0])
        cursor3=self.cstring.cursor()
        cursor3.execute(query3%(abb))
        for a in cursor3:
            j.append(int(a[0]))
        b=[];b1=[];c=[];index=[]
        from get import getinfo
        g=getinfo()
        g.nlp()
        position=list(g.offline_mode().keys())
        for a in position:
            c.append(a)
        cursor2=self.cstring.cursor()
        cursor2.execute(query2%(abb,pn))
        for a in cursor2:
            f=list(a)
            index.append(f)
        if index==[]:
            print("there is no index")
            return 0
        cursor1=self.cstring.cursor()
        cursor1.execute(query%(abb))
        for a in cursor1:
            f=list(a)
            b.append(f)
        for h in range(len(b)-1):
            dist=math.sqrt((b[h][1]-index[0][1])**2+(b[h][2]-index[0][2])**2)
            rss=abs(int(b[h][0])-int(index[0][0]))
            if rss==0 or int(b[h][0])==0 or int(index[0][0])==0:
                continue
            ac=[]
            ac.append(rss)
            ac.append(dist)
            b1.append(ac)
        return b1


    

#m = db()
#m.connect()
# m.query()
# m.ins('2','3')
# m.ins()
#m.coordinate()
# a=m.export_rss(8," 00:1f:fb:cf:0d:49")
# m.export_pd_format()
# m.export_info_algo(4)
# m.export_coordinate_algo(3)
# a=list(a[0])
# print(a)
# m.ap_matrix(' 18:a6:f7:62:3f:64',15)
# m.export_rss_pointnum(' e8:cc:18:44:e0:e6')
# m.export_x_y( ' 90:8d:78:79:65:d4',0)
# m.export_mac_x_y(1)
# m.export_x_y_rss(' 00:26:75:66:9e:5e',1)
