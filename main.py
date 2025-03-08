import numpy as np
from scipy import signal

from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox

plt.style.use('dracula.mplstyle')
#plt.style.use('seaborn')



PDK = "GPDK45"
global Lmin0
Lmin0 = 45e-9
global Lmax0
Lmax0 = 100e-9

L_tar = 500e-9
N0 = 8 #Number of initial grphs per plot (Más de 8 se repiten colores)
N = N0

def interpolate(arr1, arr2, alfa):
        arr_out = []
        if len(arr1) == len(arr2):
            for i in range(len(arr1)):
                arr_out.append( (arr1[i]*alfa) + (arr2[i]*(1-alfa)))
        else:
            print("Error in interpolation: Arrays are not the same length")
        return arr_out

def str2float(inputString):
    if (type(inputString) == str):
        if "n" in inputString: # Nanometers
            decimal_part = inputString.split("n")[0]
            exponent_part = -9
        if "u" in inputString: # Micrometers
            decimal_part = inputString.split("u")[0]
            exponent_part = -6
        FinalValue = float(decimal_part)*(10**(exponent_part))
        return FinalValue
    else: 
        quit()

def main_gmId(L_target):
    
    # Array with all the simulated L (Length) Values
    Sim_L = []

    gmIdVgs_Data = pd.read_csv('C:/Users/Usuario/Desktop/Proyectos/gm_Id_Plotter/GPDK45/GPDK45_nmos1V_Results/GPDK_45_gmIDvsVgs.csv')
    Ft_Data = pd.read_csv('C:/Users/Usuario/Desktop/Proyectos/gm_Id_Plotter/GPDK45/GPDK45_nmos1V_Results/GPDK_45_Ft.csv')
    gmRo = pd.read_csv('C:/Users/Usuario/Desktop/Proyectos/gm_Id_Plotter/GPDK45/GPDK45_nmos1V_Results/GPDK_45_gm_gds.csv')
    gmW = pd.read_csv('C:/Users/Usuario/Desktop/Proyectos/gm_Id_Plotter/GPDK45/GPDK45_nmos1V_Results/GPDK_45_gm_W.csv')
    IdW = pd.read_csv('C:/Users/Usuario/Desktop/Proyectos/gm_Id_Plotter/GPDK45/GPDK45_nmos1V_Results/GPDK_45_Id_W.csv')

    CSV_DataSets = []
    CSV_DataSets.append(gmIdVgs_Data)
    CSV_DataSets.append(Ft_Data)
    CSV_DataSets.append(gmRo)
    CSV_DataSets.append(gmW)
    CSV_DataSets.append(IdW)

    # Paso el Header a un array de strings para poder leer los valores de L simulados
    Header_String_Array = gmIdVgs_Data.columns.values.tolist()
    # Extraigo los valores de Vgs simulados de la primera columna
    Vgs = gmIdVgs_Data[Header_String_Array[0]]

    for i in range( int(len(Header_String_Array)/2) ):     
        # Como los valores de Vgs se repiten todo el rato [0, 2, 4...] para acceder a L necesito masajear el índice:
        i = 1+(2*i)
        work_string = Header_String_Array[i].split("=")[1]
        work_string = work_string.split(")")[0]
        decimal_part = work_string.split("e")[0]
        exponent_part = work_string.split("e")[1]
        Value2Append = float(decimal_part)*(10**(int(exponent_part)))
        Sim_L.append(Value2Append)

    if (L_target > Sim_L[len(Sim_L)-1]):
        print("Error: L_target is too large and is out of bounds")
        quit()

    if (L_target < Sim_L[0]):
        print("Error: L_target is too small and is out of bounds")
        quit()

    HeaderName_Upper = []
    HeaderName_Lower = []
    alfa = 0
    for i in range(len(Sim_L)):
        #print("Sim L: "+str(Sim_L[i]))
        if (Sim_L[i] >= L_target):
            alfa = (L_target-Sim_L[i-1])/(Sim_L[i]-Sim_L[i-1])
            HeaderName_Upper = Header_String_Array[1+(2*i)]
            HeaderName_Lower = Header_String_Array[1+(2*(i-1))]
            
            break

    Results = []
    for Dataset in CSV_DataSets:
        #print("Debug: " + str(Dataset.columns.values.tolist()[0]))
        if not ("gm/Id" in Dataset.columns.values.tolist()[0]):
            #print("Debug: gm/Id not found: Doing Ft")
            #print(HeaderName_Upper)
            HeaderStringArray_SpecificDataset = Dataset.columns.values.tolist()
            coreString = HeaderStringArray_SpecificDataset[0].split()[0]

            HeaderName_Upper = coreString + " " + HeaderName_Upper.split()[1] + " Y"
            HeaderName_Lower = coreString + " " + HeaderName_Lower.split()[1] + " Y"
            #print(HeaderName_Upper)

        Upper_Data = Dataset[HeaderName_Upper]
        #print("Upper_Data: " + str(Upper_Data))
        Lower_Data = Dataset[HeaderName_Lower]
        #print("Alpha: " + str(alfa))
        #print("Length: " + str(len(Sim_L)))
        Interpolated_Data = interpolate(Upper_Data, Lower_Data, alfa)
        if ("Ft" in Dataset.columns.values.tolist()[0]):
            for i in range(len(Interpolated_Data)):
                Interpolated_Data[i] = Interpolated_Data[i]*1e-9

        Results.append(Interpolated_Data)

    #print("Result lenghs: " + str(len(Results)))
    return_list = []
    return_list.append(list(Vgs))
    return_list = return_list + Results
    return return_list


fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(13, 7))
fig.subplots_adjust(right=0.97, left=0.2)

fig.suptitle("Analog Design Tool (By Adrián Ramos Bardin)", font = "Cambria", fontsize = 22)

Debug = main_gmId(L_tar)
#print(Debug)
#print("Debug Dim: "+ str(len(Debug)))
# Instanciation of X axis:
Vgs = Debug[0]
#print("Vgs: " +str(Vgs))
gmIdData0 = Debug[1]

def ResetGraphs(Lmin, Lmax):

    for i in range(3):
        for j in range(2):
            ax[j,i].cla()
            ax[j,i].grid(True, alpha = 0.4)
            ax[j,i].patch.set_edgecolor(color=(0,0,0))
            ax[j,i].set_facecolor(color = (0.1,0.1,0.14))
    
    ax[0,0].set_xlabel("Vgs", font= "Cambria")
    ax[0,1].set_xlabel("gm/Id", font= "Cambria")
    ax[0,2].set_xlabel("gm/Id", font= "Cambria")
    ax[1,0].set_xlabel("gm/Id", font= "Cambria")
    ax[1,1].set_xlabel("gm/Id", font= "Cambria")
    ax[1,2].set_xlabel("gm/Id", font= "Cambria")

    ax[0,0].set_ylabel("gm/Id [1/V]", font= "Cambria")
    ax[0,1].set_ylabel("Ft [GHz]", font= "Cambria")
    ax[0,2].set_ylabel("gm/gds [V/V]", font= "Cambria")
    ax[1,0].set_ylabel("gm/W", font= "Cambria")
    ax[1,1].set_ylabel("Id/W", font= "Cambria")

    ax[1,1].patch.set_linewidth(1)
    Legend_Ls = []
    Ls = np.geomspace(Lmin, Lmax, N)

    def format_float(num):
        return f"{num:.2f}"

    for i in range(N):
        if (Ls[i] > 1e-6):
            appendString = format_float(Ls[i]*1e6) + "u"
        else:
            appendString = format_float(Ls[i]*1e9) + "n"

        Legend_Ls.append(appendString)
    return(Legend_Ls)
    



legend = ResetGraphs(Lmin0, Lmax0)

ax[0,0].plot(Vgs,gmIdData0, label ='Inline label')
ax[0,1].plot(gmIdData0,Debug[2])
ax[0,2].plot(gmIdData0,Debug[3])
ax[1,0].plot(gmIdData0,Debug[4])
ax[1,1].plot(gmIdData0,Debug[5])

ax[0,0].legend(legend)



## Lmin Text Box:
Lmin_TxBox_ax = plt.axes([0.05, 0.8, 0.1, 0.032])
Lmin_TxBox = TextBox(Lmin_TxBox_ax, 'Lmin: ', initial="45n", color=(0.2,0.2,0.22))

def Lmin_on_sliders_on_changed(Lmin_inpt):
    global Lmin0
    Lmin0 = str2float(Lmin_inpt) # Update Lmin
    Ls = np.geomspace(Lmin0, Lmax0, N)
    
    # Clear Plots
    legend = ResetGraphs(Lmin0, Lmax0)

    for i in range(N):
        AllData = main_gmId(Ls[i])
        gmId_data = AllData[1]
        Ft_data = AllData[2]
        gmRo_data = AllData[3]
        gmW_data = AllData[4]
        IdW_data = AllData[5]


        ax[0,0].plot(Vgs,gmId_data, label ='Inline label')
        ax[0,0].legend(legend)
        ax[0,1].plot(gmId_data,Ft_data)
        ax[0,2].plot(gmId_data,gmRo_data)
        ax[1,0].plot(gmId_data,gmW_data)
        ax[1,1].plot(gmId_data,IdW_data)

    fig.canvas.draw_idle()
    print("Lmin_Global: " + str(Lmin0))
    print("Lmax_Global: " + str(Lmax0))

Lmin_TxBox.on_submit(Lmin_on_sliders_on_changed)

## Lmax Text Box:
Lmax_TxBox_ax = plt.axes([0.05, 0.75, 0.1, 0.032])
Lmax_TxBox = TextBox(Lmax_TxBox_ax, 'Lmax: ', initial="100n", color=(0.2,0.2,0.22))

def Lmax_on_sliders_on_changed(Lmax_inpt):
    global Lmax0
    Lmax0 = str2float(Lmax_inpt) # Update Lmax
    Ls = np.geomspace(Lmin0, Lmax0, N)

    # Clear Plots
    legend = ResetGraphs(Lmin0, Lmax0)

    for i in range(N):
        AllData = main_gmId(Ls[i])
        gmId_data = AllData[1]
        Ft_data = AllData[2]
        gmRo_data = AllData[3]
        gmW_data = AllData[4]
        IdW_data = AllData[5]


        ax[0,0].plot(Vgs,gmId_data, label ='Inline label')
        ax[0,0].legend(legend)
        ax[0,1].plot(gmId_data,Ft_data)
        ax[0,2].plot(gmId_data,gmRo_data)
        ax[1,0].plot(gmId_data,gmW_data)
        ax[1,1].plot(gmId_data,IdW_data)
    fig.canvas.draw_idle()
    print("Lmin_Global: " + str(Lmin0))
    print("Lmax_Global: " + str(Lmax0))

Lmax_TxBox.on_submit(Lmax_on_sliders_on_changed)

## Vds Slider:
Vds_slider_ax = fig.add_axes([0.05, 0.6, 0.1, 0.03], facecolor='grey')
Vds_slider = Slider(Vds_slider_ax, 'Vds', 0, max(Vgs), valinit=max(Vgs)/2)


# Define an action for modifying the line when any slider's value changes
def sliders_on_changed(val):
    #line.set_ydata(signal(amp_slider.val, freq_slider.val))
    fig.canvas.draw_idle()
Vds_slider.on_changed(sliders_on_changed)

## NMOS & PMOS Botones

def NMOS_button_click(event):
   print("NMOS Button Clicked!")  # Perform actions or call functions here

NMOS_Button_ax = plt.axes([0.04, 0.67, 0.05, 0.04])  # [left, bottom, width, height]
NMOS_Button = Button(NMOS_Button_ax, 'NMOS', color=(0.1,0.1,0.14))  # Create a button object
NMOS_Button.on_clicked(NMOS_button_click)

def PMOS_button_click(event):
   print("PMOS Button Clicked!")  # Perform actions or call functions here

PMOS_Button_ax = plt.axes([0.11, 0.67, 0.05, 0.04])  # [left, bottom, width, height]
PMOS_Button = Button(PMOS_Button_ax, 'PMOS', color=(0.1,0.1,0.14))  # Create a button object
PMOS_Button.on_clicked(PMOS_button_click)

## LVT | STD | HVT Botones

def LVT_button_click(event):
   print("LVT Button Clicked!")  # Perform actions or call functions here

LVT_Button_ax = plt.axes([0.02, 0.5, 0.04, 0.03])  # [left, bottom, width, height]
LVT_Button = Button(LVT_Button_ax, 'LVT', color=(0.1,0.1,0.14))  # Create a button object
LVT_Button.on_clicked(LVT_button_click)

def STD_button_click(event):
   print("STD Button Clicked!")  # Perform actions or call functions here

STD_Button_ax = plt.axes([0.08, 0.5, 0.04, 0.03])  # [left, bottom, width, height]
STD_Button = Button(STD_Button_ax, 'STD', color=(0.1,0.1,0.14))  # Create a button object
STD_Button.on_clicked(STD_button_click)

def HVT_button_click(event):
   print("HVT Button Clicked!")  # Perform actions or call functions here

HVT_Button_ax = plt.axes([0.14, 0.5, 0.04, 0.03])  # [left, bottom, width, height]
HVT_Button = Button(HVT_Button_ax, 'HVT', color=(0.1,0.1,0.14))  # Create a button object
HVT_Button.on_clicked(HVT_button_click)


plt.show()


