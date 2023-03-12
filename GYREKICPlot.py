#Plots for GYRE KIC Draft LastUpdate 11032023
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")  

class sdBMESAGYRE():
    def __init__(self,Target,ChunkSize=1000, CustomPeriodList = [],HowBad = 150, NModels=1000):
        self.Target = Target
        self.ChunkSize = ChunkSize
        self.CustomPeriodList = CustomPeriodList
        self.HowBad = HowBad
        self.NModels = NModels

    def CheckModels(self):
        pt=pd.read_csv(self.Target['Name']+'_output/'+self.Target['Name']+'_seismicfit.csv')
        print(f'Total number of models : {len(pt)}')
        print(f'Used {len(self.CustomPeriodList)} multiplets')
        print(self.CustomPeriodList)
        totalmerit = np.zeros(1)
        for p in self.CustomPeriodList:
            merit = (pt[f'f{int(np.round(p))}'] - p)**2
            totalmerit = totalmerit + merit
        # Metalicity Fe/H calculations Asplund et al. 2010   
        solar_h1 = 0.7154
        solar_h2 = 1.43e-5
        solar_he3 = 4.49e-5
        solar_he4 = 0.2702551
        solar_x = solar_h1 + solar_h2
        solar_y = solar_he3 + solar_he4
        solar_z = 1.0 - solar_x - solar_y
        pt['FeH'] =  np.log10(pt['z'] / solar_z)

        pt['total_merit'] = totalmerit / len(self.CustomPeriodList)
        pt['since_zaehb'] = (pt.age-pt.zaehbage)/(1.e6)

        tr=pt[(pt['teff']>=self.Target['TeffObs']-(self.Target['Sigma']*self.Target['TeffObsErr']))&(pt['teff']<=self.Target['TeffObs']+(self.Target['Sigma']*self.Target['TeffObsErr']))&(pt['logg']>=self.Target['loggObs']-(self.Target['Sigma']*self.Target['loggObsErr']))&(pt['logg']<=self.Target['loggObs']+(self.Target['Sigma']*self.Target['loggObsErr']))]
        print('Number of models within '+str(self.Target['Sigma'])+' sigma observation : ',len(tr))
        trz = tr.sort_values('total_merit').iloc[:self.NModels] # Only selecting first 1000 models with in the 1 sigma observation limit
        ptz = pt.sort_values('total_merit').iloc[:self.NModels] # Only selecting first 1000 models
        print(f'Merit minimum : {pt.total_merit.min()} Merit maximum : {pt.total_merit.max()} (Over all models.)')

        ptz1 = ptz[['mi', 'menv', 'mass', 'convcorem','radius','z', 'FeH','yc', 'age','since_zaehb','teff','logg','luminosity','total_merit']]
        ptz1.reset_index(drop=True)
        ptz2 = ptz1[ptz1.total_merit<=(self.HowBad/100.)*ptz1.total_merit.min()].reset_index(drop=True) # taking models up to 150% of the minimum merit
        print(' Displaying best models upto 1.5x over all models : ')
        print(ptz2)
        
        trz1 = trz[['mi', 'menv', 'mass', 'convcorem','radius','z', 'FeH','yc', 'age','since_zaehb','teff','logg','luminosity','total_merit']]
        trz1.reset_index(drop=True)
        trz2 = trz1[trz1.total_merit<=(self.HowBad/100.)*trz1.total_merit.min()].reset_index(drop=True) # taking models up to 150% of the minimum merit
        print(' Displaying best models upto 1.5x within the observation limit :')
        print(trz2)
        return pt[:10],ptz2[:10],trz2[:10]

if __name__=="__main__":
    Star = 'KIC11179657'

    if Star=='B3':
        #B3 model dictionary
        ModelDict = {'model1' : [5039.728,4794.415,3283.639,3032.43],
                'model2' : [5282.077,5039.728,4794.415,3283.639,3032.43],
                'model3' : [5039.728,4794.415,4292.176,4047.01,3283.639,3032.43],
                'model4' : [5282.077,5039.728,4794.415,4292.176,4047.01,3283.639,3032.43],
                'model5' : [5282.077,5039.728,4794.415,4519.496,4292.176,4047.01,3283.639,3032.43],
                'model6' : [7683.263,7201.584,5282.077,5039.728,4794.415,4292.176,4047.01,3283.639,3032.43],	
                'model7' : [7201.584,5282.077,5039.728,4794.415,4519.496,4292.176,4047.01,3283.639,3032.43],
                'model8' : [7683.263,7201.584,5282.077,5039.728,4794.415,4519.496,4292.176,4047.01,3283.639,3032.43],
        }
        # calling target
        Target = {   'Name'      : 'B3_280223',
                    'TeffObs'    : 23.54,
                    'TeffObsErr' : 0.21,
                    'loggObs'    : 5.311,
                    'loggObsErr' : 0.035,
                    'Sigma'      : 1.0, 
                    'PeriodList' : [7683.263,7201.584,5282.077,5039.728,4794.415,4519.496,4292.176,4047.01,3283.639,3032.43],
                    'GYREPeriodRange' : [2000,10000] #Gyre period min max range in seconds # The range of observed period to be taken from the GYRE models.
        }

    elif Star=='B4':
        #B3 model dictionary
        ModelDict = {'model1' : [4610.602,3149.775,2914.9386],
                  'model2' : [4610.602,3149.775,2914.9386,2679.08565],
                  'model3' : [4610.602,3149.775,2914.9386,2679.08565,2466.66761],
                  'model4' : [4610.602,3435.5454,2914.9386,2679.08565,2466.66761],
                  'model5' : [4610.602,3435.5289,3149.775,2914.9386,2679.08565,2466.66761],
                  'model6' : [4610.602,4366.771,3435.5289,3149.775,2914.9386,2679.08565,2466.66761],
                  'model7' : [4610.602,4366.771,3435.5289,3149.775,2914.9386,2679.08565,2466.66761,2263.4784]
        }
        #Example B4
        Target = {   'Name'      : 'B4_280223',
                    'TeffObs'    : 25.29,
                    'TeffObsErr' : 0.3,
                    'loggObs'    : 5.510,
                    'loggObsErr' : 0.043,
                    'Sigma'      : 1, 
                    'PeriodList' : [4610.602,4366.771,3435.5289,3149.775,2914.9386,2679.08565,2466.66761,2263.4784],
                    'GYREPeriodRange' : [2000,10000] #Gyre period min max range in seconds # The range of observed period to be taken from the GYRE models.
        }
    elif Star == 'KIC2991403':
        #KIC2991403 dictionary
        ModelDict = { 'model1' : [6362.558,5123.517,3239.084,2986.6839],
                      'model2' : [6362.558,5123.517,3512.240,3239.084,2986.6839],
                      'model3' : [6362.558,5123.517,4337.397,3512.240,3239.084,2986.6839,2709.985],
                      'model4' : [6362.558,5123.517,4337.397,3781.592,3239.084,2986.6839,2709.985],
                      'model5' : [6362.558,5123.517,4337.397,3781.592,3512.240,3239.084,2986.6839],
                      'model6' : [6362.558,5123.517,4337.397,3781.592,3512.240,3239.084,2986.6839,2709.985]
                     }
        #Example KIC2991403
        Target = {   'Name'      : 'KIC2991403_280223',
            'TeffObs'    : 27.3,
            'TeffObsErr' : 0.2,
            'loggObs'    : 5.430,
            'loggObsErr' : 0.03,
            'Sigma'      : 1, 
            'PeriodList' : [6362.558,5123.517,4337.397,3781.592,3512.240,3239.084,2986.6839,2709.985],
            'GYREPeriodRange' : [2000,10000] #Gyre period min max range in seconds # The range of observed period to be taken from the GYRE models.
        }
    elif Star == 'KIC11179657':
        # KIC11179657 dictionary
        ModelDict = { 'model1' : [6835.44, 5109.267, 3513.349, 3239.849],	
                      'model2' : [6835.44, 5109.267, 3777.025, 3513.349, 3239.849],
                      'model3' : [3777.025, 3513.349, 3239.849, 2965.8311, 2709.807],
                      'model4' : [6835.44, 5362.571, 5109.267, 3777.025, 3513.349, 3239.849, 2965.8311],
                      'model5' : [6835.44, 5362.571, 5109.267, 4840.46, 3777.025, 3513.349, 3239.849, 2965.8311],
                      'model6' : [5362.571, 5109.267, 4840.46, 3777.025, 3513.349, 3239.849, 2965.8311, 2709.807],
                      'model7' : [6835.44, 6612.32, 5362.571, 5109.267, 4840.46, 3777.025, 3513.349, 3239.849, 2965.8311],
                      'model8' : [6835.44, 6612.32, 5362.571, 5109.267, 4840.46, 3777.025, 3513.349, 3239.849, 2965.8311, 2709.807]
        }    
        #Example KIC11179657
        Target = {  'Name'       : 'KIC11179657_280223',
                    'TeffObs'    : 26.0,
                    'TeffObsErr' : 0.8,
                    'loggObs'    : 5.14,
                    'loggObsErr' : 0.13,
                    'Sigma'      : 1, 
                    'PeriodList' : [6835.44,6612.32,5362.571, 5109.267, 4840.46,3777.025,3513.349, 3239.849, 2965.8311, 2709.807],
                    'GYREPeriodRange' : [2000,10000] #Gyre period min max range in seconds # The range of observed period to be taken from the GYRE models.
        }

    #Ploting the full grid
    data=pd.read_csv('sdb_grid/sdb_grid_extract.csv')
    teff=data['teff']
    logg=data['logg']

    fig, ax1 = plt.subplots()
    left, bottom, width, height = [0.23, 0.2, 0.2, 0.2]
    ax2 = fig.add_axes([left, bottom, width, height])

    ax1.set_xlabel('T$\mathregular{_{eff}}$ [kK]')
    ax1.set_ylabel('$\log$(g/cm s$^2$)')
    ax1.invert_xaxis()
    ax2.invert_xaxis()
    
    ax1.plot(teff,logg,'.k',markersize=0.1)
    #ax2.plot(teff,logg,'.k',markersize=0.1)
    #ax2.set_xlim([25.692, 24.877])
    #ax2.set_ylim([5.4, 5.6])
    for i in ModelDict:
        CustomPeriod = ModelDict[i]
        sdBObj = sdBMESAGYRE(Target,CustomPeriodList=CustomPeriod,NModels=1000,HowBad=150)
        pt,ptz,trz = sdBObj.CheckModels()
        ax1.plot(trz.teff,trz.logg,'ow',markeredgecolor='black') #unconstrained
        ax2.plot(trz.teff,trz.logg,'ow',markeredgecolor='black') #unconstrained
        
    plt.savefig(f'{Star}ConSoln.png')
    plt.savefig(f'{Star}ConSoln.eps')
    plt.show()
