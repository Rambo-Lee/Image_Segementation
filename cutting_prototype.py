


from skimage import io, color
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


#setting up horizontal analysis function


def horizontal_analysis(array, row, raw_data, end_point, percentage, color_channel):
    for z in range(0, end_point, 1):
        array.append(raw_data[row][z][color_channel])
    
    
    array=np.array(array)
    threshold=(max(array)-min(array))*percentage+min(array)
    
    return threshold

def vertical_analysis(array, column, raw_data, end_point, percentage, color_channel):
    for z in range(0, end_point, 1):
        array.append(raw_data[z][column][color_channel])
    
    
    array=np.array(array)
    threshold=(max(array)-min(array))*percentage+min(array)
    
    return threshold

def border_fixer(array, threshold):
    #start fixing border

    temp_flag=int(0)
    temp_border=0
    temp_indice=int(0)
    temp_distance=int(0)
    temp_slope=int(0)
    temp_initial_indice=int(0)

    for i in range(0, len(array)-1, 1):
        
        if (array[i+1]-array[i]) > int(threshold):
            for j in range(i+1, len(array), 1):
                if temp_flag == int(0):
                    if abs(array[i]-array[j]) < int(threshold):
                        temp_border=array[j]
                        temp_indice=int(j)
                        temp_initial_indice=int(i)
                        temp_flag=int(1)
                        temp_distance=int(j-i)
                        temp_slope=int((temp_border-array[i])/temp_distance)
        
                
        if i < temp_indice:
            array[i]=int(array[temp_initial_indice]+int(temp_slope*int(i-temp_initial_indice)))
        
        if i >= temp_indice:
            temp_flag=int(0)
            temp_border=0
            temp_indice=int(0)
            temp_distance=int(0)
            temp_slope=int(0)
            temp_initial_indice=int(0)

    plt.plot(array)
    plt.show()        
    
    return array

def fine_tuning_times(array, loop, threshold):
    for i in range(0, int(loop), 1):
        array=border_fixer(array, threshold)
        
    return array
    
#finish intergrating the r2l threshold cutting

def thresholdcutting_right2left(x_end, y_end, path, threshold_analysis, border_fixing, fixing_times):
    #taking the grid at the location where x=1, y=8

    x_start=x_end-1
    y_start=y_end-1


    #inputting data

    Brain_Image= io.imread(path)

    (m,n,o) = Brain_Image.shape

    redChannel=Brain_Image[:,:,0]
    BlueChannel=Brain_Image[:,:,1]
    GreenChannel=Brain_Image[:,:,2]

    allBlack = np.zeros((m,n), dtype=np.uint8)

    justRed = np.stack((redChannel, allBlack, allBlack), axis=2)
    justGreen = np.stack((allBlack, GreenChannel, allBlack),axis=2)
    justBlue = np.stack((allBlack, allBlack, BlueChannel),axis=2)



    #extract the grid picture

    new=[[[0 for k in range(3)] for j in range(int(n/8))] for i in range(int(m/8))]
    new=np.array(new)
    (m1,n1,o1)=new.shape
    for k in range(int(m*int(x_start)/8),int((m*int(x_end))/8) ,1):
        for i in range(int(n*int(y_start)/8),int((n*int(y_end))/8),1):
           for j in range(0,3,1):
               new[k-int(m*int(x_start)/8)][i-int(n*int(y_start)/8)][j]= Brain_Image[k][i][j]
                      
    #setting up parameters for threshold cutting

    flag_g=int(0)
    flag_r=int(0)
    flag_b=int(0)


    R_threshold=0
    G_threshold=0
    B_threshold=0
    
    

    border_r=[]
    border_g=[]
    border_b=[]

    R_border=int(n/8)
    G_border=int(n/8)
    B_border=int(n/8)
    
    temp_r=R_border
    temp_g=G_border
    temp_b=B_border



    #for loop to loop through row

    for i in range( 0, int(m/8), 1):
        
        flag_g=int(0)
        flag_r=int(0)
        flag_b=int(0)
        
        skipper_r=0
        skipper_g=0
        skipper_b=0
        
        R_border=int(n/8)
        G_border=int(n/8)
        B_border=int(n/8)
        
        new_R=[]
        new_G=[]
        new_B=[]

        
        R_threshold=horizontal_analysis(new_R, i, new, int(n/8),threshold_analysis, 0)
        G_threshold=horizontal_analysis(new_G, i, new, int(n/8),threshold_analysis, 1)
        B_threshold=horizontal_analysis(new_B, i, new, int(n/8),threshold_analysis, 2)
        
        
        #for loop to loop through column
        for k in range(int(n/8)-1, 0 , -1 ):
            
            
            
            if skipper_r == int(0):
                if  new[i][k][0]<(int(R_threshold)): 
                    flag_r=1
                    skipper_r=1
                    
            if flag_r == 0: 
                new[i][k][0]=0
                if R_border>k:
                    R_border=k
                
                
                
            if skipper_g ==int(0):
                if  new[i][k][1]<(int(G_threshold)): 
                    flag_g=1
                    skipper_g=1
                    
            if flag_g == 0: 
                new[i][k][1]=0
                if G_border>k:
                    G_border=k
                
            if skipper_b == int(0):
                if  new[i][k][2]<(int(B_threshold)): 
                    flag_b=1
                    skipper_b=1
            
            if flag_b == 0: 
                new[i][k][2]=0
                if B_border>k:
                    B_border=k
                
                
        border_r.append(R_border)
        border_g.append(G_border)
        border_b.append(B_border)
        
        temp_r=R_border    #might be able to delete the temp_* variable?
        temp_g=G_border
        temp_b=B_border     
        
    #border fixing
    border_r=fine_tuning_times(border_r, int(fixing_times), border_fixing)
    border_g=fine_tuning_times(border_g, int(fixing_times), border_fixing)
    border_b=fine_tuning_times(border_b, int(fixing_times), border_fixing)
    
    #applying the second threshold cutting

    for i in range( 0, int(m/8), 1):
        
        #for loop to loop through column
        for k in range(int(n/8)-1, 0 , -1 ):
            if k>border_r[i]:
                new[i][k][0]=0
            if k>border_g[i]:
                new[i][k][1]=0
            if k>border_b[i]:
                new[i][k][2]=0
                
    
    return new


    #finish
def thresholdcutting_down2up(x_end, y_end, path, threshold_analysis, border_fixing, fixing_times):
    #taking the grid at the location where x=1, y=8

    x_start=x_end-1
    y_start=y_end-1


    #inputting data

    Brain_Image= io.imread(path)

    (m,n,o) = Brain_Image.shape

    redChannel=Brain_Image[:,:,0]
    BlueChannel=Brain_Image[:,:,1]
    GreenChannel=Brain_Image[:,:,2]

    allBlack = np.zeros((m,n), dtype=np.uint8)

    justRed = np.stack((redChannel, allBlack, allBlack), axis=2)
    justGreen = np.stack((allBlack, GreenChannel, allBlack),axis=2)
    justBlue = np.stack((allBlack, allBlack, BlueChannel),axis=2)



    #extract the grid picture

    new=[[[0 for k in range(3)] for j in range(int(n/8))] for i in range(int(m/8))]
    new=np.array(new)
    (m1,n1,o1)=new.shape
    for k in range(int(m*int(x_start)/8),int((m*int(x_end))/8) ,1):
        for i in range(int(n*int(y_start)/8),int((n*int(y_end))/8),1):
           for j in range(0,3,1):
               new[k-int(m*int(x_start)/8)][i-int(n*int(y_start)/8)][j]= Brain_Image[k][i][j]
                      
    #setting up parameters for threshold cutting

    flag_g=int(0)
    flag_r=int(0)
    flag_b=int(0)


    R_threshold=0
    G_threshold=0
    B_threshold=0
    
    

    border_r=[]
    border_g=[]
    border_b=[]

    R_border=int(n/8)
    G_border=int(n/8)
    B_border=int(n/8)
    
    temp_r=R_border
    temp_g=G_border
    temp_b=B_border



    #for loop to loop through row

    for i in range( 0, int(n/8), 1):
        
        flag_g=int(0)
        flag_r=int(0)
        flag_b=int(0)
        
        skipper_r=0
        skipper_g=0
        skipper_b=0
        
        R_border=int(n/8)
        G_border=int(n/8)
        B_border=int(n/8)
        
        new_R=[]
        new_G=[]
        new_B=[]

        
        R_threshold=vertical_analysis(new_R, i, new, int(m/8),threshold_analysis, 0)
        G_threshold=vertical_analysis(new_G, i, new, int(m/8),threshold_analysis, 1)
        B_threshold=vertical_analysis(new_B, i, new, int(m/8),threshold_analysis, 2)
        
        
        #for loop to loop through column
        for k in range(int(m/8)-1, 0 , -1 ):
            
            
            
            if skipper_r == int(0):
                if  new[k][i][0]<(int(R_threshold)): 
                    flag_r=1
                    skipper_r=1
                    
            if flag_r == 0: 
                new[k][i][0]=0
                if R_border>k:
                    R_border=k
                
                
                
            if skipper_g ==int(0):
                if  new[k][i][1]<(int(G_threshold)): 
                    flag_g=1
                    skipper_g=1
                    
            if flag_g == 0: 
                new[k][i][1]=0
                if G_border>k:
                    G_border=k
                
            if skipper_b == int(0):
                if  new[k][i][2]<(int(B_threshold)): 
                    flag_b=1
                    skipper_b=1
            
            if flag_b == 0: 
                new[k][i][2]=0
                if B_border>k:
                    B_border=k
                
                
        border_r.append(R_border)
        border_g.append(G_border)
        border_b.append(B_border)
        
        temp_r=R_border    #might be able to delete the temp_* variable?
        temp_g=G_border
        temp_b=B_border     
        
    #border fixing
    border_r=fine_tuning_times(border_r, fixing_times, border_fixing)
    border_g=fine_tuning_times(border_g, fixing_times, border_fixing)
    border_b=fine_tuning_times(border_b, fixing_times, border_fixing)
    



    #applying the second threshold cutting

    for i in range( 0, int(n/8), 1):
        
        #for loop to loop through column
        for k in range(int(m/8)-1, 0 , -1 ):
            if k>border_r[i]:
                new[k][i][0]=0
            if k>border_g[i]:
                new[k][i][1]=0
            if k>border_b[i]:
                new[k][i][2]=0

                
    
    return new 


#left2right now
def thresholdcutting_left2right(x_end, y_end, path, threshold_analysis, border_fixing, fixing_times):
    #taking the grid at the location where x=1, y=8

    x_start=x_end-1
    y_start=y_end-1


    #inputting data

    Brain_Image= io.imread(path)

    (m,n,o) = Brain_Image.shape

    redChannel=Brain_Image[:,:,0]
    BlueChannel=Brain_Image[:,:,1]
    GreenChannel=Brain_Image[:,:,2]

    allBlack = np.zeros((m,n), dtype=np.uint8)

    justRed = np.stack((redChannel, allBlack, allBlack), axis=2)
    justGreen = np.stack((allBlack, GreenChannel, allBlack),axis=2)
    justBlue = np.stack((allBlack, allBlack, BlueChannel),axis=2)



    #extract the grid picture

    new=[[[0 for k in range(3)] for j in range(int(n/8))] for i in range(int(m/8))]
    new=np.array(new)
    (m1,n1,o1)=new.shape
    for k in range(int(m*int(x_start)/8),int((m*int(x_end))/8) ,1):
        for i in range(int(n*int(y_start)/8),int((n*int(y_end))/8),1):
           for j in range(0,3,1):
               new[k-int(m*int(x_start)/8)][i-int(n*int(y_start)/8)][j]= Brain_Image[k][i][j]
                      
    #setting up parameters for threshold cutting

    flag_g=int(0)
    flag_r=int(0)
    flag_b=int(0)


    R_threshold=0
    G_threshold=0
    B_threshold=0
    
    

    border_r=[]
    border_g=[]
    border_b=[]

    R_border=int(n/8)
    G_border=int(n/8)
    B_border=int(n/8)
    
    temp_r=R_border
    temp_g=G_border
    temp_b=B_border



    #for loop to loop through row

    for i in range( 0, int(m/8), 1):
        
        flag_g=int(0)
        flag_r=int(0)
        flag_b=int(0)
        
        skipper_r=0
        skipper_g=0
        skipper_b=0
        
        R_border=int(n/8)
        G_border=int(n/8)
        B_border=int(n/8)
        
        new_R=[]
        new_G=[]
        new_B=[]

        
        R_threshold=horizontal_analysis(new_R, i, new, int(n/8),threshold_analysis, 0)
        G_threshold=horizontal_analysis(new_G, i, new, int(n/8),threshold_analysis, 1)
        B_threshold=horizontal_analysis(new_B, i, new, int(n/8),threshold_analysis, 2)
        
        
        #for loop to loop through column
        for k in range(0, int(n/8), 1 ):
            
            
            
            if skipper_r == int(0):
                if  new[i][k][0]>(int(R_threshold)):
                    flag_r=1
                    skipper_r=1
                    
            if flag_r == 0: 
                new[i][k][0]=0
                if R_border>k:
                    R_border=k
                
                
                
            if skipper_g ==int(0):
                if  new[i][k][1]>(int(G_threshold)): 
                    flag_g=1
                    skipper_g=1
                    
            if flag_g == 0: 
                new[i][k][1]=0
                if G_border>k:
                    G_border=k
                
            if skipper_b == int(0):
                if  new[i][k][2]>(int(B_threshold)):
                    flag_b=1
                    skipper_b=1
            
            if flag_b == 0: 
                new[i][k][2]=0
                if B_border>k:
                    B_border=k
                
                
        border_r.append(R_border)
        border_g.append(G_border)
        border_b.append(B_border)
        
        temp_r=R_border    #might be able to delete the temp_* variable?
        temp_g=G_border
        temp_b=B_border     
        
    #border fixing
    border_r=fine_tuning_times(border_r, fixing_times, border_fixing)
    border_g=fine_tuning_times(border_g, fixing_times, border_fixing)
    border_b=fine_tuning_times(border_b, fixing_times, border_fixing)
    


    for i in range( 0, int(m/8), 1):
        
        #for loop to loop through column
        for k in range(0, int(n/8)-1 ,  1 ):
            if k<border_r[i]:
                new[i][k][0]=0
            if k<border_g[i]:
                new[i][k][1]=0
            if k<border_b[i]:
                new[i][k][2]=0


                
    
    return new 

    
#up2down now
def thresholdcutting_up2down(x_end, y_end, path, threshold_analysis, border_fixing, fixing_times):
    
    #recommend parameter setting:
    #threshold_analysis = 0.8
    #border_fixing = 20
    #fixing_times = int(2)
    
    
    #taking the grid at the location where x=1, y=8

    x_start=x_end-1
    y_start=y_end-1


    #inputting data

    Brain_Image= io.imread(path)

    (m,n,o) = Brain_Image.shape

    redChannel=Brain_Image[:,:,0]
    BlueChannel=Brain_Image[:,:,1]
    GreenChannel=Brain_Image[:,:,2]

    allBlack = np.zeros((m,n), dtype=np.uint8)

    justRed = np.stack((redChannel, allBlack, allBlack), axis=2)
    justGreen = np.stack((allBlack, GreenChannel, allBlack),axis=2)
    justBlue = np.stack((allBlack, allBlack, BlueChannel),axis=2)



    #extract the grid picture

    new=[[[0 for k in range(3)] for j in range(int(n/8))] for i in range(int(m/8))]
    new=np.array(new)
    (m1,n1,o1)=new.shape
    for k in range(int(m*int(x_start)/8),int((m*int(x_end))/8) ,1):
        for i in range(int(n*int(y_start)/8),int((n*int(y_end))/8),1):
           for j in range(0,3,1):
               new[k-int(m*int(x_start)/8)][i-int(n*int(y_start)/8)][j]= Brain_Image[k][i][j]
                      
    #setting up parameters for threshold cutting

    flag_g=int(0)
    flag_r=int(0)
    flag_b=int(0)


    R_threshold=0
    G_threshold=0
    B_threshold=0
    
    

    border_r=[]
    border_g=[]
    border_b=[]

    R_border=int(n/8)
    G_border=int(n/8)
    B_border=int(n/8)
    
    temp_r=R_border
    temp_g=G_border
    temp_b=B_border



    #for loop to loop through row

    for i in range( 0, int(n/8), 1):
        
        flag_g=int(0)
        flag_r=int(0)
        flag_b=int(0)
        
        skipper_r=0
        skipper_g=0
        skipper_b=0
        
        R_border=int(n/8)
        G_border=int(n/8)
        B_border=int(n/8)
        
        new_R=[]
        new_G=[]
        new_B=[]

        
        R_threshold=vertical_analysis(new_R, i, new, int(m/8),threshold_analysis, 0)
        G_threshold=vertical_analysis(new_G, i, new, int(m/8),threshold_analysis, 1)
        B_threshold=vertical_analysis(new_B, i, new, int(m/8),threshold_analysis, 2)
        
        
        #for loop to loop through column
        for k in range(0,  int(m/8), 1 ):
            
            
            
            if skipper_r == int(0):
                if  new[k][i][0]<(int(R_threshold)):
                    flag_r=1
                    skipper_r=1
                    
            if flag_r == 0: 
                new[k][i][0]=0
                if R_border>k:
                    R_border=k
                
                
                
            if skipper_g ==int(0):
                if  new[k][i][1]<(int(G_threshold)): 
                    flag_g=1
                    skipper_g=1
                    
            if flag_g == 0: 
                new[k][i][1]=0
                if G_border>k:
                    G_border=k
                
            if skipper_b == int(0):
                if  new[k][i][2]<(int(B_threshold)):
                    flag_b=1
                    skipper_b=1
            
            if flag_b == 0: 
                new[k][i][2]=0
                if B_border>k:
                    B_border=k
                
                
        border_r.append(R_border)
        border_g.append(G_border)
        border_b.append(B_border)
        
        temp_r=R_border    #might be able to delete the temp_* variable?
        temp_g=G_border
        temp_b=B_border     
        
    #border fixing
    border_r=fine_tuning_times(border_r, fixing_times, border_fixing)
    border_g=fine_tuning_times(border_g, fixing_times, border_fixing)
    border_b=fine_tuning_times(border_b, fixing_times, border_fixing)
    


    for i in range( 0, int(n/8), 1):
        
        #for loop to loop through column
        for k in range(0, int(m/8)-1 , 1 ):
            if k<border_r[i]:
                new[k][i][0]=0
            if k<border_g[i]:
                new[k][i][1]=0
            if k<border_b[i]:
                new[k][i][2]=0


    
    return new 


def density_seer(path, x_start, x_end, y_start, y_end, d_c_th):
    Brain_Image= io.imread(path)

    (m,n,o) = Brain_Image.shape

    redChannel=Brain_Image[:,:,0]
    BlueChannel=Brain_Image[:,:,1]
    GreenChannel=Brain_Image[:,:,2]

    allBlack = np.zeros((m,n), dtype=np.uint8)

    justRed = np.stack((redChannel, allBlack, allBlack), axis=2)
    justGreen = np.stack((allBlack, GreenChannel, allBlack),axis=2)
    justBlue = np.stack((allBlack, allBlack, BlueChannel),axis=2)

    count1=int(0)
    new=[[[0 for k in range(3)] for j in range(int(n/8))] for i in range(int(m/8))]
    new=np.array(new)
    (m1,n1,o1)=new.shape
    for k in range(int(m*int(x_start)/8),int((m*int(x_end))/8) ,1):
        for i in range(int(n*int(y_start)/8),int((n*int(y_end))/8),1):
           for j in range(0,3,1):
               if Brain_Image[k][i][j] <  d_c_th:
                  new[k-int(m*int(x_start)/8)][i-int(n*int(y_start)/8)][j]= 255
                  count1=count1+int(1)
               else:
                   new[k-int(m*int(x_start)/8)][i-int(n*int(y_start)/8)][j]=0
              
               

    for k in range(int(m*int(x_start)/8), int((m*int(x_end))/8),1):
        for i in range(int(n*int(y_start)/8),int((n*int(y_end))/8),1):
           for j in range(0,3,1):
                   new[k-int(m*int(x_start)/8)][i-int(n*int(y_start)/8)][j]=Brain_Image[k][i][j]
              

    density=float(float(count1)/float(m1*n1*o1))
    return density

# main program starts

#setting parameters


#parameter for right to left orientation threshold cutting
r2l_th_ana = 0.8
r2l_th_bf = 20
r2l_ft = int(2)

#parameter for down to up orientation threshold cutting
d2u_th_ana = 0.8
d2u_th_bf = 20
d2u_ft = int(2)

#parameter for up to down orientation threshold cutting
u2d_th_ana = 0.8
u2d_th_bf = 20
u2d_ft = int(2)

#parameter for left to right orientation threshold cutting
l2r_th_ana = 0.99
l2r_th_bf = 20
l2r_ft = int(2)

#parameter for density_seer subprogram
#threshold 119
density_highthres=0.199
density_lowthres=0
d_c_th= 119

#centering parameter
r2l_center=int(6)
l2r_center=int(1)
u2d_center=int(6)
d2u_center=int(6)

#activation key for orientation
r2l_key=0
l2r_key=0
d2u_key=0
u2d_key=0





#picture that needs to be processed
data_path= 'C:\\Users\\user\Desktop\Alouatta_seniculus\Alouatta_seniculus_1184_left_entorhinal_930_0.tif'

#starting main program
Brain_Image= io.imread(data_path)
(m,n,o)=Brain_Image.shape
print("Brain Image shape: ", (m,n,o))
print("Before: ")
plt.imshow(Brain_Image)
plt.show()

grid_x=[]
grid_y=[]
new=[]

for i_1 in range(0,8,1):
    for j_1 in range(0,8,1):
        temp=density_seer(data_path, int(i_1),int(i_1+1),int(j_1),int(j_1+1), d_c_th)
        if temp > density_lowthres:
            if temp < density_highthres: 
                grid_x.append(i_1)
                grid_y.append(j_1)
            
        

#print out the patch we are to modified
grid_x=np.array(grid_x)
grid_y=np.array(grid_y)
print("grid_x: ", grid_x, "\n grid_y: ", grid_y)
print("size: ", len(grid_x))



for i in range(0, len(grid_x), 1):
        j=i
        skipper_main= int(0)
        print(i,"th loop: ")
        if skipper_main ==int(0):
            if grid_y[i] < l2r_center: 
                skipper_main =int(1)
                print("1st one executed. ")
                if l2r_key == 0:
                    new=thresholdcutting_left2right(int(grid_x[i]+1), int(grid_y[j]+1), data_path, l2r_th_ana, l2r_th_bf, l2r_ft)
                    (m2,n2,o2)=new.shape
                    for k_alpha in range(int(m*int(int(grid_x[i]))/8),int((m*int(int(grid_x[i]+1)))/8) ,1):
                        for i_alpha in range(int(n*int(int(grid_y[j]))/8),int((n*int(int(grid_y[j]+1))/8)),1):
                           for j_alpha in range(0,3,1):
                               Brain_Image[k_alpha][i_alpha][j_alpha]=new[int(k_alpha-int(m*int(int(grid_x[i]))/8))][int(i_alpha-int(n*int(int(grid_y[j]))/8))][j_alpha]                  
        if skipper_main == int(0):
            if grid_x[j] > d2u_center: 
                skipper_main =int(1)
                print("2nd one executed. ")
                if d2u_key == 0:
                    new=thresholdcutting_down2up(int(grid_x[i]+1), int(grid_y[j]+1), data_path, d2u_th_ana, d2u_th_bf, d2u_ft)
                    (m2,n2,o2)=new.shape
                    for k_alpha in range(int(m*int(int(grid_x[i]))/8),int((m*int(int(grid_x[i]+1)))/8) ,1):
                        for i_alpha in range(int(n*int(int(grid_y[j]))/8),int((n*int(int(grid_y[j]+1))/8)),1):
                           for j_alpha in range(0,3,1):
                               Brain_Image[k_alpha][i_alpha][j_alpha]=new[int(k_alpha-int(m*int(int(grid_x[i]))/8))][int(i_alpha-int(n*int(int(grid_y[j]))/8))][j_alpha]
        if skipper_main == int(0):
            if grid_y[i] > r2l_center:
                skipper_main =int(1)
                print("3rd one executed. ")
                if r2l_key ==0:
                    new=thresholdcutting_right2left(int(grid_x[i]+1), int(grid_y[j]+1), data_path, r2l_th_ana, r2l_th_bf, r2l_ft)
                    (m2,n2,o2)=new.shape
                    for k_alpha in range(int(m*int(int(grid_x[i]))/8),int((m*int(int(grid_x[i]+1)))/8) ,1):
                        for i_alpha in range(int(n*int(int(grid_y[j]))/8),int((n*int(int(grid_y[j]+1))/8)),1):
                           for j_alpha in range(0,3,1):
                               Brain_Image[k_alpha][i_alpha][j_alpha]=new[int(k_alpha-int(m*int(int(grid_x[i]))/8))][int(i_alpha-int(n*int(int(grid_y[j]))/8))][j_alpha]
                               
        if skipper_main == int(0):
            if grid_x[j] < u2d_center: 
                skipper_main =int(1)
                print("4th one executed. ")
                if u2d_key == 0:
                    new=thresholdcutting_up2down(int(grid_x[i]+1), int(grid_y[j]+1), data_path, u2d_th_ana, u2d_th_bf, u2d_ft)
                    (m2,n2,o2)=new.shape
                    for k_alpha in range(int(m*int(int(grid_x[i]))/8),int((m*int(int(grid_x[i]+1)))/8) ,1):
                        for i_alpha in range(int(n*int(int(grid_y[j]))/8),int((n*int(int(grid_y[j]+1))/8)),1):
                           for j_alpha in range(0,3,1):
                               Brain_Image[k_alpha][i_alpha][j_alpha]=new[int(k_alpha-int(m*int(int(grid_x[i]))/8))][int(i_alpha-int(n*int(int(grid_y[j]))/8))][j_alpha]                       
        
        
        print("\n\nend\n\n")
        
            




print("After: ")
plt.imshow(Brain_Image)
plt.show()