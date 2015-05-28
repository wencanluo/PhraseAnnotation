import fio
import os
from annotation import *
import numpy as np
import matplotlib.pyplot as plt

anotators = ['Youngmin', 'Trevor']

def get_length_distribution():
    anotators = ['Youngmin']
    
    N = [[], []]
    for doc, lec, annotator in generate_all_files(datadir + 'json/', '.json', anotators):
        task = Task()
        task.loadjson(doc)
        
        task.get_number_of_words()
        
        for i, responses in enumerate(task.raw_response):
            for dict in responses:
                N[i].append(dict['number_of_words'])
    
    width1 = np.max(N[0]) - np.min(N[0])
    width2 = np.max(N[1]) - np.min(N[1])
    
    width = max(width1, width2)
    
    fig = plt.figure(figsize=(12, 5))
         
    fig.subplots_adjust(left=0.1, bottom=0.2, right=0.9)
    
    #plt.title("Length distribution of the responses")
    
    ax = fig.add_subplot(121)
    ax.grid(True)
    
    ax.hist(N[0], bins=width, color='#fec44f', alpha=0.9,label='POI')
    #ax.xaxis.set_ticks(numpy.arange(0, 80, 5))
    ax.set_ylabel('Count', fontsize=15)
    ax.set_xlabel('# of words', fontsize=15)
    
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.legend(prop={'size':15})
    
    #plt.legend()

    ax1 = fig.add_subplot(122)
    ax1.grid(True)
    ax1.hist(N[1], bins=width, color='#7fcdbb', alpha=0.5, label='MP')
    ax1.set_ylabel('Count', fontsize=15)
    ax1.set_xlabel('# of words', fontsize=15)
    
    plt.tick_params(axis='both', which='major', labelsize=15)
    plt.legend(prop={'size':15})
    
    plt.show()
    
def get_statistics():
    #print "total lectures:", len(AllLectures)
    #print "total lectures that have phrase annotation:", len(Lectures)
    
    anotators = ['Youngmin']
    
    N = np.array([0, 0])
    for doc, lec, annotator in generate_all_files(datadir + 'json/', '.json', anotators):
        task = Task()
        task.loadjson(doc)
        
        N += np.array(task.get_number_of_sentences())
        #N += np.array(task.get_number_of_words())
    print N
    
    
if __name__ == '__main__':
    get_length_distribution()