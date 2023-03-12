# Change Log
# Last updated by Sachu on 23022023 
# Update : Included age parameter at ZAEHB (zaehbage)

#sdB grid search
import sys
import glob
import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import timeit
import warnings
warnings.filterwarnings("ignore")    

class sdBGrid():
    def __init__(self,GridDir='',GYREPeriodRange=[2000,10000],zGrid=[0.005,0.035],miGrid=[1.0,2.0],menvGrid=[0.0000, 0.0100],heGrid=[0,0.9],gridId=0):
        self.GYREPeriodRange = GYREPeriodRange
        self.GridDir = GridDir
        self.zGrid = zGrid
        self.miGrid = miGrid
        self.menvGrid = menvGrid
        self.heGrid = heGrid
        self.gridId = gridId
    '''Reading messa models'''
    def messa_read(self,track,coreHe_ab):
        path = str(self.gridId)+'_tempzip/'+track+'/history.data'
        df=pd.read_csv(path,skiprows=5,sep=r"\s+")
        He_data_path=str(self.gridId)+'_tempzip/'+track+'/custom_He'+str(coreHe_ab)+'.data'
        He_data=pd.read_csv(He_data_path,nrows=2,sep=r"\s+")
        He_data_header = He_data.iloc[0] 
        He_data = He_data[1:]
        He_data.columns = He_data_header
        model_number=np.array(He_data['model_number'])[0]
        log_Teff_model=df['log_Teff'][df['model_number']==int(model_number)]
        logg_model=df['log_g'][df['model_number']==int(model_number)]
        starage = df['star_age'][df['model_number']==int(model_number)]
        starmass = df['star_mass'][df['model_number']==int(model_number)]
        starradius = df['radius'][df['model_number']==int(model_number)]
        log_L = df['log_L'][df['model_number']==int(model_number)]  
        massconvcore = df['mass_conv_core'][df['model_number']==int(model_number)]
        luminosity = 10.0 ** log_L    
        Teff_model = (10.0 ** log_Teff_model) / 1000.0
        index_zaehb=df['model_number'].index[df['mass_conv_core'] >0.0][0]-1
        zaehbage=df['star_age'][index_zaehb] # age at ZAEHB
        return Teff_model, logg_model,starage,zaehbage,starmass,starradius,massconvcore,luminosity

    '''Formating GYRE csv tables for matching with oservations'''
    def tableformat(self,df,star):
        table='f,fq,P,l,n'
        for i in range(len(df)):
            l = df['l'][i]
            fq = (df['Re(freq)'][i]/86400.0)*1e6
            P = 86400.0/df['Re(freq)'][i]
            n = -1.0*df['n_pg'][i]
            if (P>=self.GYREPeriodRange[0] and P<self.GYREPeriodRange[1]):
                    table0='f'+str(i)+','+str(fq)+','+str(P)+','+str(l)+','+str(n)
                    table=np.vstack((table,table0))
        np.savetxt(star+'_output/gyre_table_full'+str(self.gridId)+'.csv',table,'%s')

    def unzipy(self,zip_name,folder_name):
        os.system('unzip '+zip_name+' -d '+folder_name)

    def Append(self):
        import glob
        all_files = glob.glob('sdb_grid/logs_*.csv')
        all_files = sorted(all_files)
        print(all_files)
        li = []
        for filename in tqdm(all_files):
            df = pd.read_csv(filename, index_col=None, header=0)
            li.append(df)
        frame = pd.concat(li, axis=0, ignore_index=True)
        frame.to_csv('sdb_grid/sdb_grid_extract.csv')

    def Extract(self):
        gridList = glob.glob(self.GridDir+'/*.zip')
        gridList = sorted(gridList)
        print(gridList)
        print('Total grid length: ', len(gridList))
        os.system('rm -r '+str(self.gridId)+'_tempzip ; mkdir '+str(self.gridId)+'_tempzip')
        a = 'Track,mi,menv,z,y,yc,mass,convcorem,radius,age,zaehbage,teff,logg,luminosity'
        m_log = [a]
        gl = gridList[self.gridId]
        gridZ = float(gl[gl.find('_z')+2:gl.find('_lvl')])
        gridMi = float(gl[gl.find('mi')+2:gl.find('_z')])
        if ((gridZ>=self.zGrid[0]) & (gridZ<=self.zGrid[1]) & (gridMi>=self.miGrid[0]) & (gridMi<=self.miGrid[1])): #grid filtering
            self.unzipy(gridList[self.gridId],str(self.gridId)+'_tempzip')
            gridName=glob.glob(str(self.gridId)+"_tempzip/log*")
            gridPath, gridName = os.path.split(gridName[0])
            #grid update
            allTrack = glob.glob(str(self.gridId)+'_tempzip/'+gridName+'/*')  
            for i in tqdm(range(0,len(allTrack))):
                track=allTrack[i]
                os.system('mkdir -p sdb_grid/'+track[track.find('zip/logs')+4:])
                track=track[track.find('zip/')+4:]
                menv=track[track.find('menv')+4:track.find('_rot')]
                z=track[track.find('_z')+2:track.find('_lvl')]
                y=track[track.find('_y')+2:track.find('_f')]
                mi = track[track.find('mi')+2:track.find('_z')]
                if ((float(menv)>=self.menvGrid[0]) & (float(menv)<=self.menvGrid[1])):
                    He_files = glob.glob(str(self.gridId)+"_tempzip/"+track+"/*summary.txt")
                    for j in tqdm(range(0,len(He_files))):
                        coreHe_ab = He_files[j]
                        coreHe_ab =   coreHe_ab[coreHe_ab.find('He')+2:coreHe_ab.find('sum')-1]
                        coreHe_ab = float(coreHe_ab)
                        if ((float(coreHe_ab)>=self.heGrid[0]) & (float(coreHe_ab)<=self.heGrid[1])):
                            pfile = str(self.gridId)+"_tempzip/"+track+"/custom_He"+str(coreHe_ab)+"_summary.txt"
                            df=pd.read_csv(pfile,skiprows=5,sep=r"\s+")
                            Teff_model, logg_model,starage,zaehbage,starmass,starradius,massconvcore,luminosity = self.messa_read(track,coreHe_ab)
                            starmass = str(np.round(np.min(starmass),6))
                            massconvcore = str(np.round(np.min(massconvcore),6))
                            starradius =str(np.round(np.min(starradius),6))
                            starage = str(np.round(np.min(starage),6))
                            zaehbage = str(np.round(np.min(zaehbage),6))
                            Teff_model =str(np.round(np.min(Teff_model),6))
                            logg_model=str(np.round(np.min(logg_model),6))
                            luminosity = str(np.round(np.min(luminosity),6))
                            table='f,fq,P,l,n'
                            per = 86400.0/df['Re(freq)']
                            for itable in range(len(df)):
                                #print('k',i)
                                l = df['l'][itable]
                                fq = (df['Re(freq)'][itable]/86400.0)*1e6
                                P = 86400.0/df['Re(freq)'][itable]
                                #print(P)
                                n = -1.0*df['n_pg'][itable]
                                if (P>=min(per) and P<max(per)):
                                        table0='f'+str(i)+','+str(fq)+','+str(P)+','+str(l)+','+str(n)
                                        table=np.vstack((table,table0))
                            np.savetxt('sdb_grid/'+track+'/custom_He'+str(coreHe_ab)+'_summary.csv',table,'%s')
                            b = track +','+mi+','+menv+','+z+','+y+','+str(coreHe_ab)+','+starmass+','+massconvcore+','+starradius+','+starage+','+zaehbage+','+Teff_model+','+logg_model+','+luminosity
                            m_log0 = np.array([b])
                            m_log=np.vstack((m_log,m_log0))
            np.savetxt('sdb_grid/logs_mi'+str(mi)+'_z_'+str(z)+'_lvl1.csv',m_log,fmt="%s")
            os.system('rm -r '+str(self.gridId)+'_tempzip')


def readARG():
 try:
  gridid = sys.argv[1]
  if gridid == 'makego': gridid = -2
  elif gridid =='makecsv' : gridid = -1
  else : gridid = int(sys.argv[1])
  return gridid
 except:
  print(r'''
    All you have to do is 
    i) Update the directory name inside the if __name__=='__main__'
        Grid.GridDir = '/mnt/e/ssd1_july/sdb_grid/' #Add path to jakubs grid directory 
    ii) Run the script "python3 GridExtract.py makego"
        It will create a "run.go" file and execute it with ".\run.go"  
        it will extract all the grids and copy necessary parameters to a folder sdb_grid
    iii) run the script "python3 GridExtract.py makecsv"
        It will create a merged csv file with all the necessary parameters from the grid.
    All we need is the "sdb_grid" folder and "sdb_gridextract.csv" file''') 
  exit()



if __name__ == "__main__":
    gridid = readARG()
    if not os.path.exists('sdb_grid'):
        os.system('mkdir sdb_grid')
       
    Grid = sdBGrid()
    Grid.gridId = gridid
    Grid.GridDir = '/mnt/e/ssd1_july/sdb_grid/' #Add path to jakubs grid directory 
    Grid.miGrid = [1.0,2.0]
    Grid.menvGrid = [0.0000, 0.0100]
    Grid.heGrid = [0,0.9]
    Grid.zGrid = [0.005,0.035]
    Grid.GYREPeriodRange=[2000,10000]
    if gridid >= 0:
        start = timeit.default_timer() 
        Grid.Extract()
        stop = timeit.default_timer()
        print('Run Time: ', stop - start)
    elif gridid == -1 :
        Grid.Append()
    elif gridid == -2:
        gridList = glob.glob(Grid.GridDir+'/*.zip')
        run = np.zeros(1)
        for num,i in enumerate(gridList):
            run0 = "python3 GridExtract.py "+str(num)+" "
            run = np.vstack((run,run0))
            np.savetxt('run.go',run[1:],fmt="%s")
