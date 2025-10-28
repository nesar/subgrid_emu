import numpy as np
import matplotlib.pylab as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib

font = {'family' : 'normal',
        'size'   : 28}

matplotlib.rc('font', **font)

matplotlib.rc('xtick',labelsize=15)
matplotlib.rc('ytick',labelsize=15)

import pandas as pd
import glob




def plot_scatter_matrix(df, colors): 
    
    f, a = plt.subplots(1,1, figsize = (10, 10))
    scatter_matrix = pd.plotting.scatter_matrix(df, 
                                                color=colors,  
                                                figsize=(10,10), 
                                                alpha=1.0, 
                                                ax=a, 
                                                grid=False, 
                                                diagonal='hist',
                                                range_padding=0.1,
                                                s=80);

    for ax in scatter_matrix.ravel():
        ax.set_xlabel(ax.get_xlabel(), fontsize = 14, rotation = 0)
        ax.set_ylabel(ax.get_ylabel(), fontsize = 14, rotation = 90)
        
    return f