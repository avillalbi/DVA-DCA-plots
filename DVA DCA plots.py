# -*- coding: utf-8 -*-
"""
Created on Mon May 19 13:50:33 2025

@author: Arno
"""
Caca

"""

Plot the DVA and DCA curves

"""

import matplotlib.pyplot as plt
from scipy import signal

def abs_derivative(x_axis: str, y_axis: str, pts_range: int):

    slope = []
    x = []

    i = 0
    while i < len(x_axis) - pts_range:

        delta_x = (x_axis[i + pts_range] - x_axis[i])
        delta_y = (y_axis[i + pts_range] - y_axis[i])

        if delta_x != 0:
            slope.append(abs(delta_y / delta_x))
            x.append((x_axis[i + pts_range] + x_axis[i]) / 2)

        i += 1

    return x, slope

def extraction_Q_E_BT_Lab(File_Name):

    import glob
    import os
    
    k=0  # compteur pour détecter quand on change de fichier
    
    folder = glob.glob('C:/Users/Arno/Nextcloud/Thèse/Piles/BT-Lab/'+str(File_Name)+'/**/*.txt', 
                       recursive = True)  
    # folder = glob.glob('C:/Users/Arno/Desktop/Piles/BT-Lab exports/**/*.txt', 
                       # recursive = True)                # Returns a list of names in list folder.
    
    for path,dirs,files in os.walk('C:/Users/Arno/Nextcloud/Thèse/Piles/BT-Lab/'+str(File_Name)):
        nb_cells=(len(dirs))
        # print(dirs)
        # nb_export2=len(files)
        break
    print('number of cells = ' + str(nb_cells) )
    # print(nb_export2) 
    # print(dirs)
    print('Cell  '+str(dirs[k]))
     
    
    X_glob3=[]# list contenant une list par coin cell elle meme contenant une list par expérience (C-rate par exemple) elle même contenant une list par step (SOC or SOD)
    Y_glob3=[]# pareil pour les capacités (au lieu des pot)
    
    X_glob2=[] 
    Y_glob2=[]
    
    c=0 #simple compteur aide
    
    for files in folder:
        
        c+=1
        filename=os.path.splitext(os.path.basename(files))[0]   #=nom du fichier"""
        folder_1=os.path.basename(os.path.dirname(files))  #nom du dossier dont les fichiers doivent être concaténés (après le plot pour avoir le bon title)
        
        if str(folder_1)!=dirs[k]:      # quand on change de dossier, equivalent a changer de piles
            print()
            print('Cell  '+ str(folder_1))
            k+=1
            X_glob3.append(X_glob2)
            Y_glob3.append(Y_glob2)
            X_glob2=[]
            Y_glob2=[] 
            
        X_glob1=[]
        Y_glob1=[] 
          
        print('file number : '+str(c)+' / '+str(filename))
        
        with open(files,'r',encoding= 'ISO-8859-1') as file:    #[ ISO permet de lire le symbole mu]
            # print(file)
      
            file1=file.readline()     
            # print(file1)
            first_line=file1.split('\t')
            first_line.pop()    #to remove the last elt of the list (which is '\n')
            # print(first_line)   #permet de savoir dans qeulle colonne sont les données que l'on veut et aussi de copier coller la str de la colonne si on veut la retrouver apres avec un if ==
            
            for i in range(len(first_line)):   #on trouve les deux colonne choisies en arg de la func
            
                if first_line[i] == 'Ecell/V':  
                    col1=i
                    
                if first_line[i] == 'Capacity/mA.h':
                    col2=i
                
            X=[]
            Y=[]
            
            for line in file:
                
                n=line.split()
                
                if len(n)>0:   # to avoid working on empty lines
                    
                    for i in range(len(n)):
                        n[i]=n[i].replace(',','.')
                    
                    if round(float(n[col2]),6)!=0:      # tant que la capa est différente de 0, on remplis les list 
                        X.append(round(float(n[col2]),6))
                        Y.append(round(float(n[col1]) ,6))
                        
                    if round(float(n[col2]),6)==0 and len(X)>1:    #  un peu foireux comme détection de changement de SOD à SOC (capa =0) , c>1 pour ne éviter le tout premier fichier
                       
                        X_glob1.append(X)
                        Y_glob1.append(Y)
                        X=[]
                        Y=[]
                            
            X_glob1.append(X)
            Y_glob1.append(Y)
            
            X_glob2.append(X_glob1)
            Y_glob2.append(Y_glob1)
            
    X_glob3.append(X_glob2)
    Y_glob3.append(Y_glob2)
    
    print()
    print('youhou')
    
    """ Vérifications"""
    
    print()
    print('nombre de cells traitées : '+ str(len(X_glob3)))
    print("nombre d'exp dans la cell 1 : "+ str(len(X_glob3[0])))
    print("nombre de step (SOC+SOD) dans l'exp 1 de la cell 1 : "+ str(len(X_glob3[0][0])))
    print("nombre d'exp dans la denrière cell : "+ str(len(X_glob3[-1])))
    print("nombre de step (SOC+SOD) dans la dernière exp de la dernière cell 1 : "+ str(len(X_glob3[-1][-1])))
    
    return(dirs,X_glob3,Y_glob3)

""" Extraction of the data using extraction_Q_E_BT_Lab"""

file = 'LTO,TiS2,LFP vs Li(m)'
list_cell,Q,E=extraction_Q_E_BT_Lab(file)

list_mass=[]
list_cell_name=[]
for i in range(len(list_cell)):
    list_mass.append(float(list_cell[i].split('=').pop(1)))
    list_cell_name.append(str(list_cell[i].split('me').pop(0)))
    
print('\nTreated coin cells')
print(list_cell_name)
print('\nMasses of active materials (mg)')
print(list_mass)


""" Plots des DVA et DCA : E,dV/dQ=f(Q)  and  Q,dQ/dV=f(E), spécific capacities if Boo1==True and saving plot if Bool2==True"""


def deriv_plots(nb_cell,nb_exp,nb_step,pts_deriv,Bool1,Bool2):
    
    """ To have the list of specific capacities"""
    
    Q_spe=[[[[k/(float(list_mass[nb_cell])*10**(-3)) for k in k1] for k1 in k2] for k2 in k3] for k3 in Q]       # create a list where evry elt of the list of list of list (thrice) is divided by the mass
    
    """ Smoothing data with Savitzky-Golay Filtering"""
    
    SavGol_E=signal.savgol_filter(E[nb_cell][nb_exp][nb_step],int(len(E[nb_cell][nb_exp][nb_step])/50),3)
    
    """To verify that the smoothing works , at least visually"""
    
    plt.plot(Q[nb_cell][nb_exp][nb_step],E[nb_cell][nb_exp][nb_step],label='original')
    plt.plot(Q[nb_cell][nb_exp][nb_step],SavGol_E,label='SavGol')
    plt.grid()
    plt.legend()
    plt.show()
    
    """ Applying the derivative functiun on the smoothed list, and the original one to see the difference"""
    
    Q1,dV_dQ1=abs_derivative(Q[nb_cell][nb_exp][nb_step],E[nb_cell][nb_exp][nb_step],pts_deriv)
    Q2,dV_dQ2=abs_derivative(Q[nb_cell][nb_exp][nb_step],SavGol_E,pts_deriv)
    
    E1,dQ_dV1=abs_derivative(E[nb_cell][nb_exp][nb_step],Q[nb_cell][nb_exp][nb_step],pts_deriv)
    E2,dQ_dV2=abs_derivative(SavGol_E,Q[nb_cell][nb_exp][nb_step],pts_deriv)
    
    
    """DCA : Tracer dQ/dV = f(V) en parallèle de Q=f(E)"""  # using the smoothed data E2 and dQ/dV2
    
    fig,ax1=plt.subplots()
    
    ax1.set_xlabel('Ecell / V',fontweight='bold',fontsize=18)
    
    if Bool1==True:
        ax1.plot(E[nb_cell][nb_exp][nb_step],Q_spe[nb_cell][nb_exp][nb_step],color='tab:red')
        ax1.set_ylabel(r'$\bf{Spécific~capacity~/~mAh.g^{-1}}$',color='tab:red',fontweight='bold',fontsize=18)
    else:
        ax1.plot(E[nb_cell][nb_exp][nb_step],Q[nb_cell][nb_exp][nb_step],color='tab:red')
        ax1.set_ylabel('Capacity / mA.h',color='tab:red',fontweight='bold',fontsize=18) 
   
    ax1.tick_params(axis='y',labelcolor='tab:red',labelsize=15,direction='inout')
    
    plt.grid()
    ax2=ax1.twinx()
    ax2.set_ylabel('|dQ/dV|',color='tab:blue',fontweight='bold',fontsize=18)
    ax2.plot(E2,dQ_dV2,color='tab:blue')
    
    # ax2.set_yscale('log')           # putting the dQ/dV in log could allow us to see more precisely the variation but it's ugly
    ax2.yaxis.set_ticks([],[])      # remove the ticks and graduation for the dQ/dV curve
    
    ax1.set_zorder(ax2.get_zorder()+1)      # to put the dV/dQ at the back
    ax1.patch.set_visible(False)
    filename='DCA of '+str(list_cell_name[nb_cell])+' - Exp'+str(int(nb_exp)+1)+' - Step'+str(int(nb_step)+1)
    plt.title(filename,fontweight='bold',fontsize=18)
    if Bool2==True:
        plt.savefig('C:/Users/Arno/Nextcloud/Thèse/Piles/BT-Lab/'+str(file)+'/' +str(filename) + '.svg',transparent=True,format='svg',dpi=1200,bbox_inches='tight',pad_inches=0)
    plt.show()
    
    
    """DVA : Tracer dV/dQ = f(Q) en parallèle de E=f(Q)"""   # using the smoothed data Q2 and dV/dQ2
    
    fig,ax1=plt.subplots()
    
    if Bool1==True:
        ax1.set_xlabel(r'$\bf{Spécific~capacity~/~mAh.g^{-1}}$',fontweight='bold',fontsize=18)
        ax1.plot(Q_spe[nb_cell][nb_exp][nb_step],E[nb_cell][nb_exp][nb_step],color='tab:red')
    else:
        ax1.set_xlabel('Capacity / mA.h',fontweight='bold',fontsize=18)
        ax1.plot(Q[nb_cell][nb_exp][nb_step],E[nb_cell][nb_exp][nb_step],color='tab:red')
        
    
    ax1.set_ylabel('Ecell / V',color='tab:red',fontweight='bold',fontsize=18)
    ax1.tick_params(axis='y',labelcolor='tab:red', labelsize=15,direction='inout')
    
    plt.grid()
    ax2=ax1.twinx()
    ax2.set_ylabel('|dV/dQ|',color='tab:blue',fontweight='bold',fontsize=18)
   
    if Bool1==True:
        Q2_spe=[k/(float(list_mass[nb_cell])*10**(-3)) for k in Q2] 
        ax2.plot(Q2_spe,dV_dQ2,color='tab:blue')
    else:
        ax2.plot(Q2,dV_dQ2,color='tab:blue')
        
    
    #ax2.set_yscale('log')           # putting the dQ/dV in log allow us to see more precisely the variation, but it's ugly
    ax2.yaxis.set_ticks([],[])      # remove the ticks and graduation for the dQ/dV curve
    
    ax1.set_zorder(ax2.get_zorder()+1)      #to put the dV/dQ at the back
    ax1.patch.set_visible(False)
    filename='DVA of '+str(list_cell_name[nb_cell])+' - Exp'+str(int(nb_exp)+1)+' - Step'+str(int(nb_step)+1)

    plt.title(filename,fontweight='bold',fontsize=18)
    if Bool2==True:
        plt.savefig('C:/Users/Arno/Nextcloud/Thèse/Piles/BT-Lab/'+str(file)+'/' +str(filename) + '.svg',transparent=True,format='svg',dpi=1200,bbox_inches='tight',pad_inches=0)


    plt.show()
