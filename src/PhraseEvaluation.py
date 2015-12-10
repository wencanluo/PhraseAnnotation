from annotation import *
import os
import fio
import numpy
import Survey

'''
Evaluate the phrase summarization
'''
class PhraseEvalator:
    def __init__(self):
        pass
    
    def get_phrase_performance_task_summary_semantic_match(self, task, system_phrases, prompt):
        #get phrase annotation
        phrase_annotation = task.get_phrase_annotation(prompt)
        
        #get precision, recall, f-measure
        tp = 0. #truth positive
        
        for _, phrases in phrase_annotation.items():
            for phrasedict in phrases:
                if phrasedict['phrase'] in system_phrases:
                    tp += 1.
                    break
         
        p = tp/len(system_phrases)
        r = tp/len(phrase_annotation)
        
        if p+r == 0.0:
            f = 0
        else:
            f = 2*p*r/(p+r)
             
        return p, r, f
    
    def get_phrase_performance_task_summary_semantic_weight_match(self, task, system_phrases, prompt):
        #get phrase annotation
        phrase_annotation = task.get_phrase_annotation(prompt)
        
        #get precision, recall, f-measure
        tp = 0. #truth positive
        
        ranks = []
        
        for rank, phrases in phrase_annotation.items():
            for phrasedict in phrases:
                if phrasedict['phrase'] in system_phrases:
                    tp += 1.
                    ranks.append(rank)
                    break
         
        p = tp/len(system_phrases)
        r = tp/len(phrase_annotation)
        
        if p+r == 0.0:
            f = 0
        else:
            f = 2*p*r/(p+r)
             
        return p, r, f, ranks
        
    def get_phrase_performance_task_summary_exact_match(self, task, system_phrases, prompt):
        human_summaries = task.get_phrase_summary(prompt)
        human_summary_phrases = [row[1].lower() for row in human_summaries]
        
        print human_summary_phrases
        print system_phrases
        
        tp = 0. #truth positive
        
        for phrase in system_phrases:
            if phrase in human_summary_phrases:
                tp += 1.
        
        p = tp/len(system_phrases)
        r = tp/len(human_summary_phrases)
        
        if p+r == 0.0:
            f = 0
        else:
            f = 2*p*r/(p+r)
            
        return p, r, f
    
    def get_phrase_performance_task_summary_exact_weight_match(self, task, system_phrases, prompt):
        human_summaries = task.get_phrase_summary(prompt)
        human_summary_phrases = [row[1].lower() for row in human_summaries]
        
        #print human_summary_phrases
        #print system_phrases
        
        tp = 0. #truth positive
        
        rank = []
        
        for phrase in system_phrases:
            for i, human_phrase in enumerate(human_summary_phrases):
                if phrase == human_phrase:
                    tp += 1.
                    rank.append(i+1)
                    break
        
        p = tp/len(system_phrases)
        r = tp/len(human_summary_phrases)
        
        if p+r == 0.0:
            f = 0
        else:
            f = 2*p*r/(p+r)
            
        return p, r, f, rank
    
    def get_phrase_performance_task_summary(self, task, system_phrases, prompt, match="exact"):
        if match == 'exact':
            return self.get_phrase_performance_task_summary_exact_match(task, system_phrases, prompt)
        elif match == 'exact_weight':
            return self.get_phrase_performance_task_summary_exact_weight_match(task, system_phrases, prompt)
        elif match == 'semantic':
            return self.get_phrase_performance_task_summary_semantic_match(task, system_phrases, prompt)
        elif match == 'semantic_weight':
            return self.get_phrase_performance_task_summary_semantic_weight_match(task, system_phrases, prompt)
        
    def get_phrase_performance(self, dir_annotation, extension, annotators, summarization_dir, output, match="exact"):
        '''
        get the recall for each prompt and lectures
        '''
        print dir_annotation, extension, annotators
        print summarization_dir, match
        
        body = []
        head = ['annotator', 'lecture', 'prompt', 'precision', 'recall', 'f-measure']
        for doc, lec, annotator in generate_all_files(dir_annotation + 'json/', '.json', anotators = ['Youngmin', 'Trevor'], lectures=Lectures):
            print doc
            
            #load task
            task = Task()
            task.loadjson(doc)
            
            for prompt in ['POI', 'MP']:
                #load summaries
                summary_file = os.path.join(summarization_dir, str(lec), prompt + '.summary')
                
                system_phrases = [Survey.NormalizeMeadSummary(summary) for summary in fio.LoadList(summary_file)]
                
                p, r, f, _ = self.get_phrase_performance_task_summary(task, system_phrases, prompt, match)
                
                print p, r, f, _
                
                row = [annotator, lec, prompt, p, r, f, _]
                
                body.append(row)
        
        row = ['average', 'All', 'All']
        for i in range(-4, -1):
            scores = [float(xx[i]) for xx in body]
            row.append(numpy.mean(scores))
        body.append(row)
        
        fio.WriteMatrix(output, body, head)

def Combine(models, outputdir):
    Header = ['annotator', 'lecture', 'prompt', 'precision', 'recall', 'f-measure']
    newbody = []
    
    for model in models: 
        filename = outputdir + model + ".txt"
        head, body = fio.ReadMatrix(filename, hasHead=True)
        
        row = []
        row.append(model)
        row = row + body[-1][1:]
        
        newbody.append(row)
            
    #get the max
    row = []
    row.append("max")
    for i in range(-3, 0):
        scores = [float(xx[i]) for xx in newbody]
        row.append(numpy.max(scores))
    newbody.append(row)
    
    newname = outputdir + "_".join(models) + ".txt"
    if len(newname) > 50:
        newname = newname[:50] + "_50.txt"
    fio.WriteMatrix(newname, newbody, Header)
    
if __name__ == '__main__':
    mead_datadir = "../../Fall2014/summarization/mead/data/"
    
    models = [
                #'IE256_keyphrase',
                #'IE256_Mead',
                #'IE256_PhraseMead',
                #'IE256_PhraseMeadMMR',
                'IE256_PhraseLexRank',
                #'IE256_PhraseLexRankMMR',
                'IE256_ClusterARank',
                ]
    
    for model in models:
        
        for match in ['semantic_weight']:
            summaries_dir = mead_datadir + model
            
            print model
            
            eval = PhraseEvalator()
            
            output = '../data/evaluation/phrase_semantic_'+model+'.txt'
            eval.get_phrase_performance(datadir, '.json', anotators, summaries_dir, output, match=match)
    
    Combine(models, '../data/evaluation/phrase_exact_')
    #Combine(models, '../data/evaluation/phrase_semantic_')
    