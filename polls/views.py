from django.shortcuts import render,get_object_or_404
from .models import Question,Choice
from django.urls import reverse
from django.core.paginator import Paginator
# from django.template import loader
from django.http import HttpResponse,Http404,HttpResponseRedirect
def index(request,pIndex):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # 拿到所有的问题
    latest_question_list = Question.objects.all()
    #每一页显示两条数据
    p = Paginator(latest_question_list,2)
    # print(p)
    if pIndex == '':
        pIndex='1'
    pIndex = int(pIndex)
    # print(pIndex)
    # 当前页
    list2 = p.page(pIndex)
    print(list2)
    # 页码取值范围
    plist = p.page_range
    # print(plist)
    # print(latest_question_list.count())
    # context = {
    #     'latest_question_list':latest_question_list
    # }
    return render(request,'polls/index.html',{'list': list2, 'plist': plist, 'pIndex': pIndex,'latest_question_list':latest_question_list})
def detail(request,question_id):
    # return HttpResponse("you are looking at question %s." %question_id)
    try:
        # question = Question.objects.get(pk= question_id)
        question = Question.objects.get(id = question_id)
        print(question)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request,'polls/detail.html',{'question':question})
def results(request,question_id):

    # question = get_object_or_404(Question,pk = question_id)
    question = Question.objects.get(id=question_id)
    return render(request,'polls/result.html',{'question':question})


def vote(request,question_id):
    print(question_id)
    question = get_object_or_404(Question,pk = question_id)
    try:
        a = request.POST['choice']
        print(a)
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
        print(type(selected_choice))
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message': "You didn't select a choice."})
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
# Create your views here.
