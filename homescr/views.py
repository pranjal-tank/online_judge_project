from django.shortcuts import render
from .models import *

def index(request):
    question_list=Problems.objects.all()
    context={'question':question_list,}
    return render(request,'homescr/index.html',context)

def SearchProblem(request):

    if request.method=="POST":
        pc=request.POST['pc']
        question=Problems.objects.filter(problem_code=str(pc)).values()
        sort_by_diff=request.POST['sort_by_diff']
        if sort_by_diff == 'easy':
            question=Problems.objects.filter(problem_diff='easy').values()
        if sort_by_diff == 'medium':
            question=Problems.objects.filter(problem_diff='medium').values()
        if sort_by_diff == 'hard':
            question=Problems.objects.filter(problem_diff='hard').values()
        context={'question':question,}
        return render(request,'homescr/index.html',context)



    

