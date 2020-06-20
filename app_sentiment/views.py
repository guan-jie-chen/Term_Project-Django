from django.shortcuts import render
from django.http import JsonResponse

import pickle
import jieba

import re
import json

from keras.models import load_model
from keras.preprocessing import sequence
from django.views.decorators.csrf import csrf_exempt


jieba.set_dictionary('app_sentiment/jieba_big_chinese_dict/dict.txt.big')

# We don't use GPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0'



#keras==2.2.5  tensorflow==1.14

# (Problem 1) Sometimes exception arises when we use tensorflow in Django
# We should run K.clear_session() to avoid the problem
# K.clear_session() should be used before all the deep learning models are loaded.   
# Usually we apply clear_session() only once, and then the problem will not happen again. 
# Then we comma and disable the K.clear_session()

from keras import backend as K
K.clear_session()


from tensorflow.python.keras.backend import set_session

import tensorflow as tf
graph = tf.get_default_graph()
sess = tf.Session()

## Read tokenizer
tokenizer = pickle.load(open('app_sentiment/sentiment_model/model_deep/sentiment_tokenizer.pickle', 'rb'))


## Read CNN model
# (Problem 2) Sometimes exception arises when we use tensorflow in Django
# We should apply set_session() before load_model() to avoid the problem 
set_session(sess)
model = load_model('app_sentiment/sentiment_model/model_deep/sentiment_best_model.hdf5')

# home
def home(request):
    return render(request, "app_sentiment/home.html")

# api get sentiment score
@csrf_exempt
def api_get_sentiment_simple(request):

    new_text = request.POST['input_text'] # or get('input_text')
    sentiment_prob = get_sentiment_proba(new_text)

    return JsonResponse(sentiment_prob)

# api get sentiment score
@csrf_exempt
def api_get_sentiment(request):

    # See the content_type and body
    print(request.content_type)
    print(request.body) # byte format
    
    if request.content_type == "application/x-www-form-urlencoded":
        print("Content type: application/x-www-form-urlencoded")
        new_text = request.POST['input_text'] # or get('input_text')
    elif request.content_type in ["application/json","text/plain"]:
        print("Content type: text/plain or application/json")
        # json.load can load data with json format
        request_json = json.loads(request.body)
        new_text = request_json['input_text']

    sentiment_prob = get_sentiment_proba(new_text)

    return JsonResponse(sentiment_prob)


# get sentiment probability
chinese_word_regex = re.compile(r'[\u4e00-\u9fa5]+')
def get_sentiment_proba( new_text ):
    
    tokens = jieba.lcut(new_text, cut_all=False)
    # remove some characters
    tokens = [x for x in tokens if chinese_word_regex.match(x)]
    tokens = [tokens]
    # print(tokens)
    
    # Index the document
    new_text_seq = tokenizer.texts_to_sequences(tokens)
    # Pad the document
    max_document_length = 350
    new_text_pad = sequence.pad_sequences(new_text_seq, maxlen= max_document_length)
    
    # result = model.predict(new_text_pad) # 這樣寫會報錯
    # 報錯訊息: .... is not an element of this graph.
    # set_session(sess) 不可缺少 否則會有以下報錯訊息:
    # tensorflow.python.framework.errors_impl.FailedPreconditionError: Error while reading resource variable dense_2/kernel from Container: localhost. This could mean that the variable was uninitialized. Not found: Container localhost does not exist. (Could not find resource: localhost/dense_2/kernel)

    # tensorflow graph
    # (Problem 3) Exception will arise when we use predict() in Django
    # We should apply graph.as_default() and set_session() to avoid the problem   
    with graph.as_default():
        set_session(sess)
        result = model.predict(new_text_pad)

    response = {'Negative': round(float(result[0, 0]), 2), 'Positive': round(float(result[0, 1]), 2)}
    # Note that result is numpy format and it should be convert to float

    return response

print("app_sentiment was loaded!")
