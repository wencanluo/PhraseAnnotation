from annotation import *
import os
import fio
import NLTKWrapper
import numpy

def get_phrase_reference_summary_phrase(outputs = None):
    
    for output in outputs:
        fio.NewPath(output)
        
        counts = []
        for doc, lec, annotator in generate_all_files(datadir + 'json/', '.json', anotators = ['Youngmin', 'Trevor']):
            print doc
            
            task = Task()
            task.loadjson(doc)
            
            sub_tasks = task.get_tasks()
            
            for sub_task in sub_tasks:
                if sub_task["task_name"] == "Phrase":
                    if sub_task['prompt'] == 0: #POI
                        type = 'POI'
                    else: 
                        type = 'MP'
                    
                    summary_filename = os.path.join(output, str(lec), type+'.ref.' + str(anotator_dict[annotator])) 
                    #summary_filename = os.path.join(output, str(lec), type+'.ref.summary') 
                    
                    print summary_filename
                    
                    summaries = [row[1] for row in sub_task["summary"][1:]]
                    
                    count = 0
                    for summary in summaries:
                        count += len(NLTKWrapper.wordtokenizer(summary))
                    
                    counts.append(count)
                    fio.SaveList(summaries, summary_filename)
        
        print counts
        print numpy.mean(counts)
        print numpy.median(counts)
        
def get_phrase_reference_summary_abstract(outputs = None):
    for output in outputs:
        counts = []
        
        for doc, lec, annotator in generate_all_files(datadir + 'json/', '.json', anotators = ['Youngmin', 'Trevor']):
            print doc
            
            task = Task()
            task.loadjson(doc)
            
            sub_tasks = task.get_tasks()
            
            for sub_task in sub_tasks:
                if sub_task["task_name"] == "Abstract":
                    if sub_task['prompt'] == 0: #POI
                        type = 'q1'
                    else: 
                        type = 'q2'
                    
                    summary_filename = os.path.join(output, str(lec), type+'.ref.' + str(anotator_dict[annotator])) 
                    #summary_filename = os.path.join(output, str(lec), type+'.ref.summary') 
                    
                    print summary_filename
                    
                    summaries = NLTKWrapper.splitSentence(sub_task["summary"][0])
                    
                    fio.SaveList(summaries, summary_filename)
                    
                    count = 0
                    for summary in summaries:
                        count += len(NLTKWrapper.wordtokenizer(summary))
                    
                    counts.append(count)
        
        print counts
        print numpy.mean(counts)
        print numpy.median(counts)

def get_phrase_reference_summary_extractive(outputs = None):
    for output in outputs:
        counts = []
        
        for doc, lec, annotator in generate_all_files(datadir + 'json/', '.json', anotators = ['Youngmin', 'Trevor']):
            print doc
            
            task = Task()
            task.loadjson(doc)
            
            sub_tasks = task.get_tasks()
            
            for sub_task in sub_tasks:
                if sub_task["task_name"] == "Extractive":
                    if sub_task['prompt'] == 0: #POI
                        type = 'q1'
                    else: 
                        type = 'q2'
                    
                    summary_filename = os.path.join(output, str(lec), type+'.ref.' + str(anotator_dict[annotator])) 
                    #summary_filename = os.path.join(output, str(lec), type+'.ref.summary') 
                    
                    print summary_filename
                    
                    summaries = task.get_summary_text(sub_task)
                    
                    fio.SaveList(summaries, summary_filename)
                    
                    count = 0
                    for summary in summaries:
                        count += len(NLTKWrapper.wordtokenizer(summary))
                    
                    counts.append(count)
                    
        print counts
        print numpy.mean(counts)
        print numpy.median(counts)      

if __name__ == '__main__':
    #mead_datadir = "../../Fall2014/summarization/mead/data/IE256_C16/"
    IE256_datadir = "../../AbstractPhraseSummarization/data/IE256/"
    
    mead_datadir = "../../Fall2014/summarization/mead/data/IE256_C16/"
    outputs =  [
                #mead_datadir + 'Mead',
                #mead_datadir + 'PhraseMead',
                #mead_datadir + 'PhraseMeadMMR',
                #mead_datadir + 'PhraseLexRank',
                #mead_datadir + 'PhraseLexRankMMR',
                #mead_datadir + 'keyphrase',
                mead_datadir + 'ClusterARank',
                
                #mead_datadir + 'IE256_Mead',
                #mead_datadir + 'IE256_PhraseMead',
                #mead_datadir + 'IE256_PhraseMeadMMR',
                #mead_datadir + 'IE256_PhraseLexRank',
                #mead_datadir + 'IE256_PhraseLexRankMMR',
                #mead_datadir + 'IE256_keyphrase',
                #mead_datadir + 'IE256_ClusterARank',
                #IE256_datadir + 'ILP_Sentence_MC',
                #IE256_datadir + 'ILP_Baseline_Sentence'
               ]
    
    #get_phrase_reference_summary_extractive(outputs)
    
    get_phrase_reference_summary_phrase(outputs)
    
    #get_phrase_reference_summary_abstract(outputs)
    
#     outdirs = ['../../AbstractPhraseSummarization/data/IE256/ILP_Baseline_Sentence/',
#                '../../AbstractPhraseSummarization/data/IE256/ILP_Sentence_MC/',
#                '../../AbstractPhraseSummarization/data/IE256/ILP_Sentence_Supervised_FeatureWeightingAveragePerceptron/',
#                ]
#     get_phrase_reference_summary_abstract(outdirs)
#     