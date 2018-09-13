import numpy as np
import pandas as pd
from knn import knn
from mydb import db
from get import getinfo
t=getinfo()
db=db()
db.connect()
knn=knn()
best_rp=knn.find()[0]

class lr:
    def ml(self):

        t.nlp()
        position=t.offline_mode()
        position_mac=list(position.keys())
        position_rss=list(position.values())
        # print(position_mac,position_rss)
        i=0
        for mac in position_mac:
            q=[]
            train_x=db.export_x_y(mac,best_rp).values()
            # print(train_x)
            # x=train_x.copy()
            train_x=list(train_x)

            point_rss=db.export_rss(best_rp,mac)
            # print(point_rss)
            train_y=list(db.export_x_y(mac,best_rp).keys())
            # print(train_y)
            if 0.0 in train_x:
                index=train_x.index(0.0)
                train_x.remove(train_x[index])
                train_y.remove(train_y[index])
            # print(train_y)
            if train_y==[]:
                continue
            ones=[]
            for a in train_x:
                ones.append(1.)
            q.append(ones)
            q.append(train_x)
            q=np.matrix(q,dtype=float).T
            train_y=np.matrix(train_y,dtype=float).T
            param=np.matrix(np.array([0,0],dtype=float))
            # print(q,train_y)
            # print(np.shape(q),np.shape(train_y),np.shape(param))
            # param=np.matrix(np.array(np.shape((train_y)),dtype=float))
            # print(param)

            # ///This is where the machine learning starts...

            # print(np.dot(q,param.T))
            def cost_function(x, y, param):
                compute1 = np.power((np.dot(x, param.T) - y), 2)
                return np.sum(compute1) / (2 * len(y))
            # print(cost_function(q,train_y,param))
            def gradientdescent(x, y, param, alpha=0.0001):
                comp = np.dot((np.dot(x, param.T) - y).T, x)
                param -= (alpha * 1.0 / len(y)) * comp

            iteration = 10000
            cost_values = []
            for i in range(iteration):
                cost_values.append(cost_function(q, train_y, param))
                gradientdescent(q,train_y, param)

            def predict(x1, param):
                return param[0, 0]+param[0,1]*x1
            print(predict(2,param))

            # final_result.append(predict(best_rp,param_devide))
            # print(predict(best_rp,param_devide))
            # print(cost_values)







lr=lr()
lr.ml()


