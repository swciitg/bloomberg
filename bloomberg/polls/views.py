from .models import Question, Choice
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect , HttpResponse
from polls.forms import PollForm
from main.models import UserDetail

# Create your views here.

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        return HttpResponseRedirect(reverse('main:index'))
    else:
        emailID=''
        if request.session.has_key('eid'):
            emailID = request.session['eid']
        string=str(question_id)
        string=string+emailID
        print(string)
        if request.session.has_key(string):
            pass
        else:
            question.totalVotes = F('totalVotes') + 1
            question.save()
            request.session[string]=selected_choice.id
            selected_choice.votes = F('votes') + 1
            selected_choice.save()

        return HttpResponseRedirect(reverse('main:index'))

def polladdform(request):
    if not request.session.has_key('eid'):
        return HttpResponseRedirect(reverse('main:login'))

    if request.method == 'POST':
        polls_form = PollForm(request.POST)
        question = request.POST['question']
        choice1 = request.POST['choice1']
        choice2 = request.POST['choice2']
        choice3 = request.POST['choice3']
        choice4 = request.POST['choice4']

        if polls_form.is_valid():
            email = request.session['eid']
            try:
                user = UserDetail.objects.get(emailID__exact=email)
            except UserDetail.DoesNotExist:
                return HttpResponseRedirect(reverse('main:logout'))
            else:
                if not user.isAdmin:
                    return HttpResponseRedirect(reverse('main:permissiondenied'))
                ques = Question.objects.create(
                    question_text = question,
                    authorID = user.userID,
                    author = user,
                )
                print(ques.id)
                Choice.objects.create(
                    question_id = ques.id,
                    choice_text = choice1,
                )
                Choice.objects.create(
                    question_id = ques.id,
                    choice_text = choice2,
                )
                if choice3 != '':
                    Choice.objects.create(
                        question_id = ques.id,
                        choice_text = choice3,
                    )
                if choice4 != '':
                    Choice.objects.create(
                        question_id = ques.id,
                        choice_text = choice4,
                    )
                return HttpResponse('poll upload success')


        return HttpResponseRedirect(reverse('polls:polladdform'))
    else:
        polls_form = PollForm()
    context = {
        'form' : polls_form
    }

    return render(request , 'polls/pollupload.html' , context)

def polllive(request,pk):
    question=get_object_or_404(Question, pk=pk)

    if request.session.has_key('eid'):
        emailID=request.session['eid']
        user=UserDetail.objects.get(emailID__exact=emailID)
        if user.isAdmin:
            question.isLive = True
            question.approvedBy=user.name
            question.save()
            return HttpResponseRedirect(reverse('polls:pendingpolls'))
        else:
            return HttpResponseRedirect(reverse('main:permissiondenied'))
    else:
        return HttpResponseRedirect(reverse('main:login'))

def pollblock(request,pk):
    question=get_object_or_404(Question, pk=pk)

    if request.session.has_key('eid'):
        emailID=request.session['eid']
        user=UserDetail.objects.get(emailID__exact=emailID)
        if user.isAdmin:
            question.isLive = False
            question.approvedBy=user.name
            question.save()
            return HttpResponseRedirect(reverse('polls:pendingpolls'))
        else:
            return HttpResponseRedirect(reverse('main:permissiondenied'))
    else:
        return HttpResponseRedirect(reverse('main:login'))

def admindashpolls (request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		questions = Question.objects.filter(isLive=True)
		page_title = 'ALL POLLS'
		context = {
			'user' : user ,
			'questions' : questions ,
			'page_title' : page_title,
		}

		return render(request , 'polls/admindashpolls.html' , context)

	return HttpResponseRedirect(reverse('main:login'))

def pendingpolls(request):

	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		questions = Question.objects.filter(isLive=False)

		page_title='PENDING POLLS'
		context = {
			'user' : user ,
			'questions' : questions ,
			'page_title' : page_title,
		}
		return render(request , 'polls/admindashpolls.html' , context)


def newpolls(request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		page_title='NEW POLLS'
		questions = Question.objects.all().order_by('-createdAt')
		context = {
			'user' : user ,
			'questions' : questions ,
			'page_title' : page_title,
		}

		return render(request , 'polls/admindashpolls.html' , context)

	return HttpResponseRedirect(reverse('main:login'))
