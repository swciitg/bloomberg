from .models import Question, Choice
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect

# Create your views here.

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        return HttpResponseRedirect(reverse('main:index'))
    else:
        emailID = request.session['eid']
        string=str(question_id)
        string=string+emailID
        print(string)
        if request.session.has_key(string):
            pass
        else:
            request.session[string]=selected_choice.id
            selected_choice.votes = F('votes') + 1
            selected_choice.save()

        return HttpResponseRedirect(reverse('main:index'))
