from django.shortcuts import render

from django.shortcuts import render

from django.shortcuts import render
import pandas as pd

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Show your home page
def chart_topPerson(request):
    return render(request, 'app_top_person/home.html')

# load data
# The loading processes are difined in this function:
def load_data_topPerson():
    # read df
    df_topPerson = pd.read_csv(
        'dataset/news_top_person_by_category_via_ner.csv')
    # load or refresh data
    global data
    data = {}
    for idx, row in df_topPerson.iterrows():
        data[row['category']] = eval(row['top_keys'])

# Invoke this function to load data when starting server.
load_data_topPerson()

# csrf_exempt is used for POST
@csrf_exempt
def api_get_topPerson(request):
    # chart_data, wf_pairs = get_category_topPerson("all", 10) # Make a test
    cate = request.POST.get('news_category')
    topk = request.POST.get('topk')
    topk = int(topk)
    #print(cate, topk)

    chart_data, wf_pairs = get_category_topPerson(cate, topk)

    # print(chart_data)
    response = {'chart_data':  chart_data,
                'wf_pairs': wf_pairs,
                }
    return JsonResponse(response)

def get_category_topPerson(cate, topk):
    wf_pairs = data[cate][0:topk]
    words = [w for w, f in wf_pairs]
    freqs = [f for w, f in wf_pairs]
    chart_data = {
        "category": cate,
        "labels": words,
        "values": freqs}
    return chart_data, wf_pairs  # chart_data is used for charting

print("app_top_person was loaded!")

