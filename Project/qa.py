__author__ = 'Anirudh'


import sys
import nltk
from nltk.corpus import stopwords
import QP
import WM


################ Getting the input file from the command line arguments ###########################

if len(sys.argv) > 1:
    input_file=sys.argv[1]
else:
    print 'Please provide an input file as an argument to this qa system !'

######################### Reading the input file #########################################

with open(input_file, 'r') as input:
    data=input.readlines()

for i in range(0, len(data)):
    data[i]=data[i].replace("\n","")

#print 'Data is :', data


######################## Getting the question and story from the given input story ID ##############################

directory_path=data[0]
#print 'Directory path is :', directory_path

#######################  Computing the full directory path from the storyID for story and question  #######################

for i in range(1, len(data)):
    story_id=data[i]
    question_path=directory_path + '/' + story_id + '.questions'
    story_path=directory_path + '/' + story_id + '.story'
    #print 'Question file is :', question_path
    #print 'Story file is :', story_path

    ################## Reading the corresponding story file for the given story id ###################
    with open(story_path, 'r') as storyFile:
        story=storyFile.readlines()

    for i in range(0,len(story)):
        story[i]=story[i].replace("\n","")

    #print 'Story is :', story

    deleted_index=[]
    for i in range(6,len(story)):
        if story[i]=='':
            #print 'story[i] is:',story[i]
            deleted_index.append(i)

    #print 'Deleted indexes is :', deleted_index

    '''for i in range(0, len(deleted_index)):
        print 'Element to be deleted is :', story[deleted_index[i]]
        print deleted_index[i],i
        del story[deleted_index[i]]'''

    #print 'Story is :', story
    sentences_list=QP.story_parser(story)


    # Removing the stop words from  each sentence using NLTK's stopwords and then creating a final sentence list
    # where each sentence is free of stop words
    stops = set(stopwords.words('english'))

    print 'Number of stop words in NLTK library is :',len(stops)

    non_stop_words=[]
    stopwords_free_sentences_list=[]
    for sent in sentences_list:
        for w in sent.split():
            if w.lower() not in stops:
                non_stop_words.append(w)
        temp=' '.join(non_stop_words)
        stopwords_free_sentences_list.append(temp)
        non_stop_words=[]

    #print 'After stop words removal the sentences list is:', stopwords_free_sentences_list
    #print len(stopwords_free_sentences_list)

    ################## Reading the corresponding question file for the given story id ###################
    with open(question_path, 'r') as questionFile:
        question=questionFile.readlines()

    for i in range(0,len(question)):
        question[i]=question[i].replace("\n","")

    #print 'Question is :', question

    qIDList, qList,cleansedqList = QP.question_parser(question)

    #print 'QuestionID List is :', qIDList
    #print 'Question list is :', qList
    #print 'Cleansed question list is :',cleansedqList


    #print len(qList)

    # Removing the stop words from  each question using NLTK's stopwords and then creating a final question list
    # where each question is free of stop words  --- Actually need not do this for the questions

    response_sent_candidates=[]

    #Calling WordMatch function to compute the number of words that appear in both question and sentence being considered
    for i in range(0, len(cleansedqList)):
        for j in range(0, len(stopwords_free_sentences_list)):
            result_count = WM.wordMatch(cleansedqList[i],stopwords_free_sentences_list[j])
            if result_count > 0:
                response_sent_candidates.append(stopwords_free_sentences_list[j])
        print 'Question is :', cleansedqList[i]
        print 'Candidate responses are:',response_sent_candidates
        response_sent_candidates=[]










    ####################### Building the response file #############################################

    with open ("AnswerResponse","a") as f:
	    for i in range(0, len(qIDList)):
                f.write(qIDList[i])
                f.write("\n")
                f.write("Answer:")
                f.write("\n\n")



