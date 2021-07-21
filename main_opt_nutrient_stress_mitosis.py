# This optimization routine calibrates chemotactic Lagrange multiplier according to a specified chemotaxing speed

import multiprocessing
from os.path import dirname, join
from re import A
import numpy as np
import pandas as pd
import scipy
from scipy.optimize import shgo
from scipy.optimize import basinhopping
from scipy.signal import savgol_filter
from scipy.interpolate import interp1d
from cc3d import CompuCellSetup
from cc3d.CompuCellSetup.CC3DCaller import CC3DCaller
from cc3d.CompuCellSetup.CC3DCaller import CC3DCallerWorker
import time

# General setup

# Specify location of simulation file
simulation_fname ='/media/sourabh/SSD32/424_auto/Demos/CallableCC3D/cc3d-scipyOptimize/nutrient_stress_mitosis.cc3d'
# Specify root directory of results
res_output_root = 'CC3DCallerOutput'
# Specify number of workers
num_workers = 4

#ratio_val=[10,20,11,14,41] # red to green ratio
ratio_val=[10,20,11,14,41] # red to green ratio

numiter=600

def getSmoothData(xl_sheet, numratio):
    # get_ipython().run_line_magic('matplotlib', 'widget')
    # ratio=[0.0,1.0,4.0,0.25]
    # print(np.shape(xl_sheet))
    datacols = np.shape(xl_sheet)[1]
    cols_per_ratio = int(datacols/numratio)
    smd = np.zeros((np.shape(xl_sheet)[0], numratio))
    for i in range(1, numratio+1):
        cols = range(cols_per_ratio*(i-1), cols_per_ratio*(i))
        smd[:, i-1] = xl_sheet[:, cols].mean(axis=1)

    smd = savgol_filter(smd, 15, 5, axis=0)
    # smd=savgol_filter(xl_sheet, 23, 3,axis=0)
    # span=1
    # for i in range(0, (smd.shape)[1]):
    #     smd[:,i]=np.convolve(smd[:,i], np.ones(span * 2 + 1) / (span * 2 + 1), mode="same")
    x = np.linspace(0, 164, smd.shape[0])
    xnew = np.linspace(0, 164, numiter+1)
    ynew = np.zeros((np.shape(xnew)[0], (smd.shape)[1]))
    ynew = interp1d(x, smd, kind='cubic', axis=0)(xnew)
    # for i in range(0, (smd.shape)[1]):
    #     ynew[:,i]=UnivariateSpline(x,smd[:,i],k=5)(xnew)
    smd = ynew
    x = xnew
    return x, smd


def run_trials(num_runs, iteration_num, x0):
    """
    Runs simulation and store simulation results
    :param num_runs: number of simulation runs
    :param iteration_num: integer label for storing results according to an iteration
    :param x0: chemotactic Lagrange multiplier to simulate
    :return: mean horizontal center of mass over all runs
    """

    root_output_folder = join(res_output_root, f'iteration_{iteration_num}')

    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start workers
    workers = [CC3DCallerWorker(tasks, results) for i in range(num_workers)]
    [w.start() for w in workers]
    # Enqueue jobs
    for i in ratio_val:
        
        cc3d_caller = CC3DCaller(cc3d_sim_fname=simulation_fname,
                                 output_frequency=10,
                                 screenshot_output_frequency=10,
                                 output_dir=join(root_output_folder, f'trial_{i}'),
                                 result_identifier_tag=i,
                                 sim_input=np.concatenate(([i],x0,[numiter]))
                                 )
        tasks.put(cc3d_caller)

    # Add a stop task for each of worker
    for i in range(num_workers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Return mean result
    trial_results = []
    while num_runs:
        result = results.get()
        trial_results.append(result['result'])
        num_runs -= 1

    return (trial_results)


def run_trials_no_store(num_runs, x0):
    """
    Runs simulation without storing simulation results
    :param num_runs: number of simulation runs
    :param x0: chemotactic Lagrange multiplier to simulate
    :return: mean horizontal center of mass over all runs
    """

    root_output_folder = join(res_output_root, f'tmp')

    # def call_cc3d():
    #     for ratio in ratio_val: 
    #         cc3d_caller = CC3DCaller(cc3d_sim_fname=simulation_fname,
    #                             output_dir=join(root_output_folder, f'trial_{i}'),
    #                             result_identifier_tag=i,
    #                             sim_input=[ratio]+x0
    #                             )
    #     return cc3d_caller
     
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    # Start workers
    workers = [CC3DCallerWorker(tasks, results) for i in range(num_workers)]
    [w.start() for w in workers]

     
    # Enqueue jobs
    for i in ratio_val:
        #b=[i]+x0
        #print (type(x0))
        #input("press any key ....")
        cc3d_caller = CC3DCaller(cc3d_sim_fname=simulation_fname,
                                output_dir=join(root_output_folder, f'trial_{i}'),
                                result_identifier_tag=i,
                                sim_input=np.concatenate(([i],x0,[numiter]))
                                )
        #cc3d_caller=call_cc3d()
        tasks.put(cc3d_caller)

    # Add a stop task for each of worker
    for i in range(num_workers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()

    # Return mean result
    tol=[]
    sen=[]
    num_ratio=len(ratio_val)
    for ratio in range(num_ratio):
        result = results.get()
        if ratio_val[ratio]==10:
            tol = np.concatenate((tol,result['result'][0]))
        elif ratio_val[ratio]==20:
            sen = np.concatenate((sen,result['result'][1]))
        else:
            tol = np.concatenate((tol,result['result'][0]))
            sen = np.concatenate((sen,result['result'][1]))
#    print(tol.shape)
#    print(sen.shape)
#    input('press any key....!!!')
    simdata=np.concatenate(( sen.reshape(sen.size,1), tol.reshape(tol.size,1) ))
    return  simdata

def run_trials_no_store_serial(num_runs, x0):
    """
    Runs simulation without storing simulation results       tasks.put(cc3d_caller)

    # Add a stop task for each of worker
    for i in range(num_workers):
        tasks.put(None)

    # Wait for all of the tasks to finish
    tasks.join()
    :return: mean horizontal center of mass over all runs
    """

    root_output_folder = join(res_output_root, f'tmp')

    # def call_cc3d():
    #     for ratio in ratio_val: 
    #         cc3d_caller = CC3DCaller(cc3d_sim_fname=simulation_fname,
    #                             output_dir=join(root_output_folder, f'trial_{i}'),
    #                             result_identifier_tag=i,
    #                             sim_input=[ratio]+x0
    #                             )
    #     return cc3d_caller
     

     
    # Enqueue jobs
    for i in ratio_val:
        #b=[i]+x0
        #print (type(x0))
        #input("press any key ....")
        cc3d_caller = CC3DCaller(cc3d_sim_fname=simulation_fname,
                                output_dir=join(root_output_folder, f'trial_{i}'),
                                result_identifier_tag=i,
                                sim_input=np.concatenate(([i],x0,[numiter]))
                                )
        result=cc3d_caller.run()

        if i==10:
            tol = result['result'][0]
        elif i==20:
            sen = result['result'][1]
        else:
            tol = np.concatenate((tol,result['result'][0]))
            sen = np.concatenate((sen,result['result'][1]))
            
    
    # num_ratio=len(ratio_val)
    # while num_ratio-2:
    #     result = results.get()
    #     tol = np.concatenate((tol,result['result'][0]))
    #     sen = np.concatenate((sen,result['result'][1]))
    #     num_ratio -= 1
#    print(tol.shape)
#    print(sen.shape)
#    input('press any key....!!!')
    if len(ratio_val)==1:
        simdata = tol.reshape(tol.size,1)
    else:
        simdata=np.concatenate(( sen.reshape(sen.size,1), tol.reshape(tol.size,1) ))
    
    return  simdata

def main():
    # Number of simulation runs per evaluation
    num_runs = len(ratio_val)
    # Maximum number of optimization iterations
    num_iterations = 10
    
    # Target horizontal center of mass after 1k MCS
    xl_sheet=pd.read_excel('VId1066coculturespheroid.xlsx',sheet_name=[0,1])
    xl_sheet[0] = xl_sheet[0].dropna(axis='columns', how='all') # drop all null columns
    xl_sheet[1] = xl_sheet[1].dropna(axis='columns', how='all')
    #time0 = xl_sheet[0].iloc[:, 0].to_numpy()
    #time1 = xl_sheet[1].iloc[:, 0].to_numpy()
    # print(np.shape((xl_sheet[1].iloc[1:,1:25]).to_numpy()))
    x0, smd0 = getSmoothData(xl_sheet[0].iloc[:, 1:25].to_numpy(), 4)
    x1, smd1 = getSmoothData(xl_sheet[1].iloc[:, 1:25].to_numpy(), 4)
    smd0=smd0/smd0[0,:]
    smd1=smd1/smd1[0,:]
    # avgdta0=avgdta0/avgdta0[0,:]
    # avgdta1=avgdta1/avgdta1[0,:]
    if num_runs==1:
        smd= (smd1[:,0]).reshape(smd1[:,0].size,1)
    elif num_runs==2:
        smd= np.concatenate(( (smd0[:,0]).reshape(smd0[:,0].size,1),
             (smd1[:,0]).reshape(smd1[:,0].size,1) ))      
    else:
        smd=np.concatenate(( (smd0[:,0:num_runs-1].T).reshape(smd0[:,0:num_runs-1].size,1),
                            (smd1[:,0:num_runs-1].T).reshape(smd1[:,0:num_runs-1].size,1) ))
    
    # print(type(data))
    # smd=savgol_filter(xl_sheet[1].iloc[1:,25:32], 23, 3,axis=0)

    # Cost function of optimization
    def cost_fun(x):
        res = run_trials_no_store(num_runs, x)
        return np.sqrt(np.sum((res - smd) ** 2))

    iter_out = 'opt_iter.dat'
    with open(iter_out, 'w') as fout:
        fout.write('Optimization iterations: \n')
    fout.close()

    def print_fun(x, f, accepted):
        with open(iter_out, 'a') as fout:
            fout.write("at minimum %.4f accepted %d\n" % (f, int(accepted)))
            fout.writelines(["with parmeters: ",str(x),"\n"] )
            fout.close()

    # Bounds for chemotactic Lagrange multiplier
    mins = [0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001,0.0001]
    maxs = [0.5,0.5,1.0,0.5,1.8,1.2,1.0,0.5]
    initguess=np.array([0.095,0.1,0.6,0.08,0.9,0.6,0.4,0.06])

    # Solve!
    kwargs = {"method":"SLSQP", "bounds":list(zip(mins, maxs)),
            "options":{'maxiter': 10, 'ftol': 1e-02}}
    solve_time = time.time()

    # opt_res = shgo(cost_fun,bounds=list(zip(mins,maxs)),
    #                options={'maxiter': num_iterations, 'disp': True})
    # opt_res = basinhopping(cost_fun,initguess,
    opt_res = basinhopping(cost_fun,initguess,minimizer_kwargs=kwargs,
            niter=num_iterations,stepsize=0.05,callback=print_fun,disp=True)
    solve_time = time.time() - solve_time

    # Output results with optimal solution
    run_trials(num_runs, 0, opt_res.x)

    # Print and store optimization results summary
    print(opt_res)
    print(solve_time)

    res_out_summ = join(res_output_root, 'opt_summary.dat')
    with open(res_out_summ, 'w') as fout:
        fout.write(str(opt_res))
        fout.write('\n\n')
        fout.write('Solution time: {} s'.format(solve_time))


if __name__ == '__main__':
    main()
