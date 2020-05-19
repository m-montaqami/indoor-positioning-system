#this file contaions the coordinates of traverse
#this file will Adjust the data for IPS project
#The Adjusting Method is BODIGE
import math
data=[[267506.788,4062907.737],[267484.444,4062879.292],[267485.595,4062865.791],
      [267501.361,4062863.112],[267498.032,4062835.791],[267466.029,4062839.699],
      [267467.340,4062856.746],[267443.616,4062858.635],[267470.916,4062883.747],
      [267506.780,4062907.743]]
relations=[[1,2],[2,3],[3,4],[4,5],[5,6],[6,7],[7,8],[8,9],[9,10]]
def distance(x1,y1,x2,y2):
    return math.sqrt(math.pow((x1-x2),2)+math.pow((y1-y2),2))
def e_max(distances,d_alpha,n):
    AB=(1/4)*sum(distances)*math.sqrt(2)
    return (2.5)*d_alpha*AB*math.sqrt(n/2)
def permission(e_max,x_start,y_start,x_end,y_end):
    e=distance(x_start,y_start,x_end,y_end)
    print('error of traverse is: %s'%(e))
    if(e<=e_max):
        print('this traverse is ok with error')
        return 0
    else:
        return -1
def Adjust(e_x,e_y,station_num,data,distances):
    sum_dists=sum(distances)
    for i in range(len(distances)):
        buff1=(e_x*distances[i])/sum_dists;buff2=(e_y*distances[i])/sum_dists;j=i+1
        data[j][0]+=buff1;data[j][1]+=buff2
def main(data,relations):
    distances=[];d_alpha=5;n=len(relations)-1
    d_alpha=math.radians(d_alpha/3600)
    for i in relations:
        distances.append(distance(data[i[0]-1][0],data[i[0]-1][1],data[i[1]-1][0],data[i[1]-1][1]))
    e_maxs=e_max(distances,d_alpha,n)
    print('the maximum error is : %s'%(e_maxs))
    if (permission(e_maxs,data[0][0],data[0][1],data[len(data)-1][0],data[len(data)-1][1])==0):
        Adjust(data[len(data)-1][0]-data[0][0],data[len(data)-1][1]-data[0][1],len(relations),data,distances)
        accuracy=distance(data[0][0],data[0][1],data[len(data)-1][0],data[len(data)-1][1])/sum(distances)
        print('The accuracy of this Traverse is : %s'%(accuracy))
        print('the Adjusted data:');print(data);print(len(distances))
    else:
        print('can not Adjust the data')
main(data,relations)

