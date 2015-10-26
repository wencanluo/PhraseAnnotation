from annotation import *
import os
import fio

def get_phrase_reference_summary(outputs = None):
    for output in outputs:
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
                    
                    fio.SaveList(summaries, summary_filename)
                    

if __name__ == '__main__':
    mead_datadir = "../../Fall2014/summarization/mead/data/"
    outputs =  [
                mead_datadir + 'IE256_Mead',
                mead_datadir + 'IE256_PhraseMead',
                mead_datadir + 'IE256_PhraseMeadMMR',
                mead_datadir + 'IE256_PhraseLexRank',
                mead_datadir + 'IE256_PhraseLexRankMMR',
                mead_datadir + 'IE256_keyphrase',
                mead_datadir + 'IE256_ClusterARank',
               ]
    
    get_phrase_reference_summary(outputs)
    