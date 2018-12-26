import datetime
from main.models import UserDetail
from .forms import EventUploadForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Event

#
# def event (request,pk):
#     event = get_object_or_404(Event , pk=pk)
#     context = {
#         'event' : event ,
#     }
#
#     return render(request, ,context)

def eventUpload (request):
    if request.method == 'POST':
        if request.session.has_key('eid'):
            emailID = request.session['eid']
            user = UserDetail.objects.get(emailID = emailID)
            event_form = EventUploadForm(request.POST , request.FILES)
            # title=request.POST['title']
            # image=request.FILES['image']
            # venue=request.POST['venue']
            # organizingClub=request.POST['associatedClub']
            # description=request.POST['description']
            # date=request.POST['date']

            if event_form.is_valid():
                title=event_form.cleaned_data['title']
                image=event_form.cleaned_data['image']
                venue=event_form.cleaned_data['venue']
                organizingClub=event_form.cleaned_data['associatedClub']
                description=event_form.cleaned_data['description']
                date=event_form.cleaned_data['date']
                Event.objects.create(
                    postedBy=user.name,
                    title=title,
                    image=image,
                    venue=venue,
                    organizingClub=organizingClub,
                    description=description,
                    date=date,
                )

                return HttpResponse('Event upload success')
        else:
            return HttpResponseRedirect(reverse('main:login'))

    else:
        event_form=EventUploadForm()

    context = {
        'form' : event_form,
    }

    return render(request, 'events/eventupload.html' ,context)

def eventlive(request,pk):
    event=get_object_or_404(Event, pk=pk)

    if request.session.has_key('eid'):
        emailID=request.session['eid']
        user=UserDetail.objects.get(emailID__exact=emailID)
        if user.isAdmin:
            event.isLive = True
            event.approvedBy=user.name
            event.save()
            return HttpResponseRedirect(reverse('blogs:pendingpost'))
        else:
            return HttpResponseRedirect(reverse('main:permissiondenied'))
    else:
        return HttpResponseRedirect(reverse('main:login'))

def eventblock(request,pk):
    event=get_object_or_404(Event, pk=pk)

    if request.session.has_key('eid'):
        emailID=request.session['eid']
        user=UserDetail.objects.get(emailID__exact=emailID)
        if user.isAdmin:
            event.isLive = False
            event.approvedBy=user.name
            event.save()
            return HttpResponseRedirect(reverse('blogs:pendingpost'))
        else:
            return HttpResponseRedirect(reverse('main:permissiondenied'))
    else:
        return HttpResponseRedirect(reverse('main:login'))

def admindashevents (request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		events = Event.objects.all()
		page_title = 'ALL EVENTS'
		context = {
			'user' : user ,
			'events' : events ,
			'page_title' : page_title,
		}

		return render(request , 'events/admindashevents.html' , context)

	return HttpResponseRedirect(reverse('main:login'))

def pendingevent(request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		events = Event.objects.filter(approvedBy=None)

		page_title='PENDING EVENTS'
		context = {
			'user' : user ,
			'events' : events ,
			'page_title' : page_title,
		}
		return render(request , 'events/admindashevents.html' , context)

def newevent(request):
	if request.session.has_key('eid'):
		emailID = request.session['eid']
		user = UserDetail.objects.get(emailID = emailID)
		if not user.isAdmin:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		if user.isBlocked:
			return HttpResponseRedirect(reverse('main:permissiondenied'))
		page_title='NEW EVENTS'
		events = Event.objects.all().order_by('-date')
		context = {
			'user' : user ,
			'events' : events ,
			'page_title' : page_title,
		}

		return render(request , 'events/admindashevents.html' , context)

	return HttpResponseRedirect(reverse('main:login'))
