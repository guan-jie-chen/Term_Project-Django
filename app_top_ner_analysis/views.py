from django.shortcuts import render
import pandas as pd

from django.http import  JsonResponse
from django.views.decorators.csrf import csrf_exempt

'''
{'CARDINAL': {'政治': [('2020', 249),
   ('10', 170),
   ('15', 113),
   ('13', 105),
  ...
  }
'''

# ne names
ne_name =['EVENT','FAC','GPE','LANGUAGE','LAW','LOC','NORP','ORG','PERSON','PRODUCT','WORK_OF_ART']
idx2nename = { str(i) : item for i, item in enumerate(ne_name)}

# category names
news_categories = ['八卦','棒球','車子','手機通訊','軟工','NBA','PlayStation','LoL','Steam','NSwitch','全部']
idx2cate = { str(i) : item for i, item in enumerate(news_categories)}

def load_data_topNer():
    # read data
    df_topNer = pd.read_csv('dataset/news_topkey_by_ne_and_category.csv')

    global data
    data = {}
    for idx, row in df_topNer.iterrows():
        ne_row = eval(row['top_keys'])
        cate_wf={}
        for cate_wf_row in ne_row:
            cate_wf[ cate_wf_row[0] ] = cate_wf_row[1]
        data[row['ne_name']]= cate_wf
    return

# We should call load_data() at first.
load_data_topNer()

def home(request):
    return render(request,'app_top_ner_analysis/home.html')


# When Post is used, the csrf of this function should be ignored
@csrf_exempt
def api_get_cate_topkey(request):

    # Get the news category
    cate_idx = request.POST.get('news_category')
    cate = idx2cate[cate_idx]

    # Get the number of keywords
    topk = int(request.POST.get('topk'))

    # Get ner value
    ner_value = request.POST.get('ner_value')
    ner_value = idx2nename[ner_value]

    print(ner_value, cate, topk)

    content = get_category_topkey(ner_value, cate, topk)
    response = {'data': content }
    print(response)
    return JsonResponse(response)


def get_category_topkey(ner_value, cate, topk):

    wf_pairs = data[ner_value][cate][0:topk]

    if wf_pairs == []:
        return []

    words = [w for w, f in wf_pairs]
    freqs = [f for w, f in wf_pairs]


    # the minimum and maximum frequency of top words
    min_ = wf_pairs[-1][1]  # the last line is smaller
    max_ = wf_pairs[0][1]

    textSizeMin = 10
    textSizeMax = 90

    if (min_ != max_):
        max_min_range = max_ - min_

    else:
        max_min_range = len(wf_pairs)
        min_ = min_ - 1

    # cloud chart data
    # using proportional scaling
    clouddata = [{'text':w, 'size':int(textSizeMin+(f - min_)/max_min_range*(textSizeMax-textSizeMin))} for w, f in wf_pairs]

    content = {
        "wf_pairs": wf_pairs,
        "data_barchart":{
                        "category": cate,
                        "labels": words,
                        "values": freqs
                        },
        "data_cloud": clouddata}
    return content



def get_category_topkey_v1(ner_value, cate, topk):

    wf_pairs = data[ner_value][cate][0:topk]
    words = [w for w, f in wf_pairs]
    freqs = [f for w, f in wf_pairs]
    clouddata=[{
      'text': 'javascript',
      'size': 40
    },
    {
      'text': 'D3.js',
      'size': 15
    },
    {
      'text': 'coffeescript',
      'size': 25
    }]
    content = {
        "category": cate,
        "labels": words,
        "values": freqs,
        "clouddata": clouddata}
    return content, wf_pairs # content is for chartting

def get_category_topkey_v0(ner_value, cate, topk):

    wf_pairs = data[ner_value][cate][0:topk]
    words = [w for w, f in wf_pairs]
    freqs = [f for w, f in wf_pairs]
    content = {
        "category": cate,
        "labels": words,
        "values": freqs}
    return content, wf_pairs # content is for chartting

print("app_news_analysis was loaded!")