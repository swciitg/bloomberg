from .models import Question, Choice, Question_exit_poll, Candidate
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.http import HttpResponseRedirect , HttpResponse
from polls.forms import PollForm, ExitPollForm
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
        if request.session.has_key(string):
            pass
        else:
            question.totalVotes = F('totalVotes') + 1
            question.save()
            request.session[string]=selected_choice.id
            selected_choice.votes = F('votes') + 1
            selected_choice.save()

        return HttpResponseRedirect(reverse('main:index'))

def exitpollvote(request, question_id):
    question = get_object_or_404(Question_exit_poll, pk=question_id)
    try:
        selected_choice = question.candidate_set.get(pk=request.POST['choice'])
        print(selected_choice.name)
    except (KeyError, Candidate.DoesNotExist):
        return HttpResponseRedirect(reverse('main:index'))
    else:
        emailID=''
        if request.session.has_key('eid'):
            emailID=request.session['eid']
        string=str(question_id)
        string=string+emailID
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


def exitpolladdform(request):
    if not request.session.has_key('eid'):
        return HttpResponseRedirect(reverse('main:login'))

    if request.method == 'POST':
        polls_form = ExitPollForm(request.POST)
        question = request.POST['question']
        contestingPost = request.POST['contestingPost']
        candidate_1 = request.POST['candidate_1']
        candidate_2 = request.POST['candidate_2']
        candidate_3 = request.POST['candidate_3']
        candidate_4 = request.POST['candidate_4']
        candidate_5 = request.POST['candidate_5']
        candidate_6 = request.POST['candidate_6']

        if polls_form.is_valid():
            email = request.session['eid']
            try:
                user = UserDetail.objects.get(emailID__exact=email)
            except UserDetail.DoesNotExist:
                return HttpResponseRedirect(reverse('main:logout'))
            else:
                if not user.isAdmin:
                    return HttpResponseRedirect(reverse('main:permissiondenied'))
                ques = Question_exit_poll.objects.create(
                    question_text = question,
                    authorID = user.userID,
                    author = user,
                    contestingPost = contestingPost,
                )
                print(ques.id)
                Candidate.objects.create(
                    question_id = ques.id,
                    name = candidate_1,
                    contestingPost = contestingPost,
                )
                Candidate.objects.create(
                    question_id = ques.id,
                    name = candidate_2,
                    contestingPost = contestingPost,
                )
                if candidate_3 != '':
                    Candidate.objects.create(
                        question_id = ques.id,
                        name = candidate_3,
                        contestingPost = contestingPost,
                    )
                if candidate_4 != '':
                    Candidate.objects.create(
                        question_id = ques.id,
                        name = candidate_4,
                        contestingPost = contestingPost,
                    )
                if candidate_5 != '':
                    Candidate.objects.create(
                        question_id = ques.id,
                        name = candidate_5,
                        contestingPost = contestingPost,
                    )
                if candidate_6 != '':
                    Candidate.objects.create(
                        question_id = ques.id,
                        name = candidate_6,
                        contestingPost = contestingPost,
                    )
                return HttpResponse('exit poll upload success')

        return HttpResponseRedirect(reverse('polls:exitpolladdform'))
    else:
        exit_polls_form = ExitPollForm()
    context = {
        'form' : exit_polls_form
    }

    return render(request , 'polls/exitpollupload.html' , context)
