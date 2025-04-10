#Code to generate the initial condition
import numpy as np
check_list=np.linspace(0,1,21)
initial_list=[]
f5=open("InitialPoints.txt","w+")
for p1 in check_list:
    for p2 in check_list:
        for p3 in check_list:
            for p4 in check_list:
                for p5 in check_list:
                    for p6 in check_list:
                        for p7 in check_list:
                            if p1==1 or p2==1 or p3==1 or p4==1 or p5==1 or p6==1 or p7==1 or (1- p1-p2-p3-p4-p5-p6-p7)==1: 
                                flga=1
                            else:
                                if (p1 + p2 + p3 + p4 + p5 + p6 + p7 ) < 1:
                                    f5.write("%15.9f%15.9f%15.9f%15.9f%15.9f%15.9f%15.9f%15.9f\n"%(p1,p2,p3,p4,p5,p6,p7,1- p1-p2-p3-p4-p5-p6-p7))
        print("p1=",p1,"  p2=",p2)
f5.close()






