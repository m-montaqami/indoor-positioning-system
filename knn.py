from mynewdb import db
from get import getinfo
g=getinfo()
d=db()
best_rss=[]

class knn:
    def find(self):
        g.nlp()
        position_signal=list(g.offline_mode().values())
        position_mac=list(g.offline_mode().keys())
        ii=0
        # print(position_signal,position_mac)
        for i in position_mac:
            point_num=list(d.export_rss_pointnum(i).keys())
            point_signal=list(d.export_rss_pointnum(i).values())
            # print(point_signal)
            signal_first=[]
            num_first=[]
            cc=0
            for o in point_signal:
                # print(int(point_signal[ii]),o)
                p= abs(int(point_signal[ii]) - o)
                # print(p)
                if (o!=0 and position_signal[ii]!=0) :
                    signal_first.append(p)
                    num_first.append(point_num[cc])

                # print(cc)
                cc=cc+1

            # print(signal_first,num_first)
            # print(ii)
            # ii=ii+1
            if signal_first==[] :
                continue
            minz = min(signal_first)

            uu=[]
            for u in range(len(signal_first)):
                if signal_first[u]==minz:
                    uu.append(u)
                # if u != minz:
                #     uu.append(0)
            for r in uu:
                best_rss.append(num_first[r])
            # print(best_rss)
        kl=[]
        for t in range(max(best_rss)+1):
            kl.append(best_rss.count(t))
        # print(kl)
        maxt=max(kl)
        # t=kl.index(maxt)
        final_RP=[]
        for t in range(len(kl)):
            if kl[t]==maxt:
                final_RP.append(t)
        print("as we computed based on knn algorithm,the nearest RP is : %s"%final_RP)
        return final_RP
# k=knn()
# k.find()
# print(best_rss)
