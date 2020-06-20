from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from keras.models import load_model
from keras.preprocessing import sequence
import pickle
import jieba

jieba.set_dictionary('app_news_classify/jieba_big_chinese_dict/dict.txt.big')

# We don't use GPU
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

#keras==2.2.5  tensorflow==1.14

# (Problem 1) Sometimes exception arises when we use tensorflow in Django
# We should run K.clear_session() to avoid the problem
# K.clear_session() should be used before all the deep learning models are loaded.   
# Usually we apply clear_session() only once, and then the problem will not happen again. 
# Then we comma and disable the K.clear_session()

from keras import backend as K
#K.clear_session()

# tensorflow graph
# raise ValueError("Tensor %s is not an element of this graph." % obj)
# ValueError: Tensor Tensor("dense_9/Softmax:0", shape=(?, 2), dtype=float32) is not an element of this graph.

from tensorflow.python.keras.backend import set_session
import tensorflow as tf

graph = tf.get_default_graph()
sess = tf.Session()

# Load tensorflow model
# (Problem 2) Sometimes exception arises when we use tensorflow in Django
# We should apply set_session() before load_model() to avoid the problem
set_session(sess)
model = load_model('app_news_classify/news_classify_model/news_cnn.hdf5')

# Load tokenizer 
tokenizer = pickle.load(open('app_news_classify/news_classify_model/news_classify_tokenizer.pickle', 'rb'))

# category index
news_categories = ['八卦','棒球','車子','手機通訊','軟工','NBA','PlayStation','LoL','Steam','NSwitch']
idx2cate = { i : item for i, item in enumerate(news_categories)}

# home
def home(request):
    return render(request, "app_news_classify/home.html")

from django.http import JsonResponse
import json

# import sentiment 
from app_sentiment.views import api_get_sentiment
from app_sentiment.views import get_sentiment_proba

# api: get news class given user input text
@csrf_exempt
def api_get_news_cate(request):
    
    new_text = request.POST.get('input_text')
    #print(new_text)

    news_cate = get_cate_proba(new_text)

    # Get sentiment: call sentiment app  
    # (1) method 1: call sentiment api, 
    senti = api_get_sentiment(request)
    # The format of return data is json format
    # we should use json.loads()
    sentiment = json.loads(senti.content)
    
    # print return data 
    #print(senti.content)
    #print(senti.items()) # doesn't work

    # (2) method 2: easy way
    # sentiment = get_sentiment_proba(new_text)

    response = {
        'news_cate': news_cate,
        'news_sentiment': sentiment
    }

    return JsonResponse(response)


# get category probability
def get_cate_proba(new_text):
    tokens = jieba.lcut(new_text, cut_all=False)
    tokens = [tokens]
    # print(tokens)
    new_text_seq = tokenizer.texts_to_sequences(tokens)
    new_text_pad = sequence.pad_sequences(new_text_seq, maxlen=250)

  
    # tensorflow graph
    # (Problem 3) Exception will arise when we use predict() in Django
    # We should apply graph.as_default() and set_session() to avoid the problem
    # error message: .... is not an element of this graph.
    # set_session(sess) is necessary, otherwise, the following errors may arise:
    # tensorflow.python.framework.errors_impl.FailedPreconditionError:
    # Error while reading resource variable dense_2/kernel from Container
    with graph.as_default():
        set_session(sess)
        result = model.predict(new_text_pad)
        result_label = model.predict_classes(new_text_pad)

    label = idx2cate[result_label[0]]
    proba = round(float(max(result[0])), 2)
    # Note that result is numpy format and it should be convert to float

    return {'label': label, 'proba': proba}

print("app news classification was loaded!")
