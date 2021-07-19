
from cc3d.core.PySteppables import *
from cc3d.CompuCellSetup import persistent_globals as pg




class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):

        for cell in self.cell_list:

            cell.targetVolume = 25
            cell.lambdaVolume = 20.0
            
        
        #self.plot_win = self.add_new_plot_window(title='Tolerant and sensitive cells',
         #                                        x_axis_title='MonteCarlo Step (MCS)',
         #                                        y_axis_title='total population', x_scale_type='linear', y_scale_type='linear',
         #                                        grid=False)
        
        #self.plot_win.add_plot("sen", style='Dots', color='red', size=3)
        #self.plot_win.add_plot("tol", style='Dots', color='green', size=3)
    
#     def step(self,mcs):
#         field=CompuCell.getConcentrationField(self.simulator,"nutrient")
#         comPt=CompuCell.Point3D()
#         for cell in self.cellList:
#             comPt.x=int(round(cell.xCOM))
#             comPt.y=int(round(cell.yCOM))
#             comPt.z=int(round(cell.zCOM))
#              #Condensing cell
#             if cell.type==self.SENCELL:
#                 concentration=field.get(comPt) # get concentration at comPt
#                 cell.targetVolume+=0.1*concentration # increase cell's target volume            

        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)
    
    def start(self):
        
        self.plot_win = self.add_new_plot_window(title='Tolerant and sensitive cells',
                                                 x_axis_title='MonteCarlo Step (MCS)',
                                                 y_axis_title='total population', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        
        #self.plot_win.add_plot("sen", style='Dots', color='red', size=3)
        #self.plot_win.add_plot("tol", style='Dots', color='green', size=3)
        
        self.initnumtolcell=len(self.cell_list_by_type(self.TOLCELL))
        self.initnumsencell=len(self.cell_list_by_type(self.SENCELL))
        numiter=int(pg.input_object[9])
        self.sencellfc=np.zeros((numiter+1))

        self.tolcellfc=np.zeros((numiter+1))
        self.timstp=0
        self.simtype = pg.input_object[0]
        self.senHcoef = pg.input_object[1]
        self.senMinGrwthNut = pg.input_object[2]
        self.senStrsCoef = pg.input_object[3]
        self.tolHcoef = pg.input_object[4]
        self.tolLCoef1 = pg.input_object[5]
        self.tolLCoef2 = pg.input_object[6]
        self.tolLCoef3 = pg.input_object[7]
        self.tolMinGrwthNut = pg.input_object[8]
 
    def step(self, mcs):       

        # # alternatively if you want to make growth a function of chemical concentration uncomment lines below and comment lines above        

        field1 = self.field.NUTRIENT
        field2 = self.field.STRESS
        for cell in self.cell_list:
            ntrntAtCOM = field1[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]
            strssAtCOM = field2[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]
            if cell.type == self.SENCELL:
                #cell.targetVolume += 0.4 * (ntrntAtCOM) -  0.2*strssAtCOM-0.05 #- 0.01*(6-ntrntAtCOM) 
                #cell.targetVolume += 0.13 * (ntrntAtCOM) -  0.025*strssAtCOM-0.05
                #cell.targetVolume += -0.2*np.log((1-ntrntAtCOM/5.51)/(80.5*ntrntAtCOM/5.51))- 0.34*max(0,-np.log((10.0-strssAtCOM)/(50.5*ntrntAtCOM)))
                #cell.targetVolume += -0.12*np.log((1-ntrntAtCOM/5.51)/(80*ntrntAtCOM/5.51))- 0.2*max(0,-np.log((10.0-strssAtCOM)/(40.5*strssAtCOM)))
                #cell.targetVolume += 0.68*ntrntAtCOM/(ntrntAtCOM+2.5)*(ntrntAtCOM-0.15) - 0.08*strssAtCOM/(strssAtCOM+2.5)*(strssAtCOM-0.1) 
                
                #health= 0.14*ntrntAtCOM  # - 1.1/(1+np.exp(np.log(19)*(1-2*((strssAtCOM-0.2)/0.6 ))))    
                #cell.targetVolume += 1*((health))*(ntrntAtCOM-0.1) - 0.17*strssAtCOM*strssAtCOM
                
                health= self.senHcoef*ntrntAtCOM      
                cell.targetVolume += 1*((health))*(ntrntAtCOM-self.senMinGrwthNut) - self.senStrsCoef*strssAtCOM*strssAtCOM
                #health= 0.09*ntrntAtCOM      
                #cell.targetVolume += 1*((health))*(ntrntAtCOM-0.03) - 0.18*strssAtCOM*(strssAtCOM)
                #cell.targetVolume += (0.35-2/(1+np.exp(np.log(19)*(1-2*((strssAtCOM-0.3)/4)))))*(ntrntAtCOM)-0.1
                numsencell=len(self.cell_list_by_type(self.SENCELL))
                self.sencellfc[self.timstp]=numsencell/self.initnumsencell
                #self.plot_win.add_data_point("sen", mcs, numsencell/self.initnumsencell)
                
                #cell.targetVolume += 0.34* 10.0/( 1+70*np.power( 2,-( ntrntAtCOM-3.5 ) ) ) - 0.34* 10.0/( 1+70*np.power( 2,-( strssAtCOM-3.5 ) ) )  
                #cell.targetVolume += -0.32*np.log((1000.0-ntrntAtCOM/strssAtCOM)/(800*ntrntAtCOM/strssAtCOM))
            elif cell.type == self.TOLCELL:
                #cell.targetVolume += 0.2 * (ntrntAtCOM) - 0.22*strssAtCOM- 0.05
                #cell.targetVolume += -0.12*np.log((1-ntrntAtCOM/5.51)/(55*ntrntAtCOM/5.51)) - 0.20*max(0,-np.log((10.0-strssAtCOM)/(40.5*ntrntAtCOM))) 
                #cell.targetVolume += -0.04*np.log((1-ntrntAtCOM/5.51)/(55*ntrntAtCOM/5.51)) - 0.20*max(0,-np.log((10.0-strssAtCOM)/(40.5*strssAtCOM))) 
                #health= 0.22*ntrntAtCOM - 3/(1+np.exp((1-2*((strssAtCOM-1.5)/3.5))))  
                
                #health= 0.175 *ntrntAtCOM - 1.1/(1+np.exp(np.log(19)*(1-2*((strssAtCOM-0.5)/0.4 ))))
                #cell.targetVolume += 1*((health))*(ntrntAtCOM-0.1) #- 0.04*strssAtCOM*strssAtCOM
                
                health= self.tolHcoef *ntrntAtCOM - self.tolLCoef1/(1+np.exp(np.log(19)*(1-2*((strssAtCOM-self.tolLCoef2 )/self.tolLCoef3 ))))
                cell.targetVolume += 1*((health))*(ntrntAtCOM-self.tolMinGrwthNut) #- 0.04*strssAtCOM*strssAtCOM
                #health= 0.072 *ntrntAtCOM - 0.25/(1+np.exp(np.log(19)*(1-2*((strssAtCOM-0.2 )/0.4 ))))#(strssAtCOM**1.5)/(0.3+strssAtCOM**1.5)

                #cell.targetVolume += 1*((health))*(ntrntAtCOM-0.01)
                #cell.targetVolume += (0.26-2/(1+np.exp(np.log(19)*(1-2*((strssAtCOM-1.0)/2.7)))))*(ntrntAtCOM)-0.1
                #cell.targetVolume += -0.1+0.12*25/(1+np.exp(np.log(19)*(1-2*((ntrntAtCOM-0.2)/5.0)))) - 0.035*max(0, 9/(1+np.exp(np.log(19)*(1-2*((strssAtCOM-0.3)/10.4))))) 

                numtolcell=len(self.cell_list_by_type(self.TOLCELL))
                self.tolcellfc[self.timstp]=numtolcell/self.initnumtolcell 
                #self.plot_win.add_data_point("tol", mcs, numtolcell/self.initnumtolcell)

                #cell.targetVolume += -0.4*np.log((1-ntrntAtCOM/5.51)/(55*ntrntAtCOM/5.51)) - 0.38*max(0,-np.log((10.0-strssAtCOM)/(99.5*ntrntAtCOM))) 
        self.timstp+=1   
        #print("timstp = ", self.timstp) 
        # arguments are (name of the data series, x, y)
    def finish(self):
        pg.return_object = [self.tolcellfc, self.sencellfc]
        # if (self.timstp==600):
        #         output = np.column_stack((self.tolcellfc.flatten(),self.sencellfc.flatten()))
        #         np.savetxt("exp.csv", output, delimiter=",")
        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)

    def step(self, mcs):

        cells_to_divide=[]
        for cell in self.cell_list:
#           ntrntAtCOM = field1[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)]
            if cell.volume>50:
                cells_to_divide.append(cell)
#               if ntrntAtCOM > 0.2
#                 ntrntAtCOM -= 0.2
#               field1[int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)] = ntrntAtCOM
                 

        for cell in cells_to_divide:

            self.divide_cell_random_orientation(cell)
            # Other valid options
            # self.divide_cell_orientation_vector_based(cell,1,1,0)
            # self.divide_cell_along_major_axis(cell)
            # self.divide_cell_along_minor_axis(cell)

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0                  

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        if self.parent_cell.type==1:
            self.child_cell.type=1
        elif self.parent_cell.type==2:
            self.child_cell.type=2

        
class DeathSteppable(SteppableBasePy):
    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)

#     def step(self, mcs):
#         if mcs == 1000:
#             for cell in self.cell_list:
#                 if cell.type==1:
#                     cell.targetVolume=0
#                     cell.lambdaVolume=100
        
#         if mcs == 2000:
#             for cell in self.cell_list:
#                 if cell.type==2:
#                     cell.targetVolume=0
#                     cell.lambdaVolume=100        
        

        