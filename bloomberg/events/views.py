import datetime
from bloomberg.blogs.models import UserDetail
from .forms import EventUploadForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Event


def event (request,pk):
    event = get_object_or_404(Event , pk=pk)
    context = {
        'event' : event ,
    }

    return render(request, ,context)

def eventUpload (request):
    if request.method == 'POST':
        if request.session.has_key('eid'):
            event_form = EventUploadForm(request.POST , request.FILES)
            title=request.POST['title']
            image=request.FILES['image']
            venue=request.POST['venue']
            associatedClub=request.POST['associatedClub']
            description=request.POST['description']
            date=request.POST['date']

            if event_form.is_valid():
                Event.objects.create(
                    title=title,
                    image=image,
                    venue=venue,
                    associatedClub=associatedClub,
                    description=description,
                    date=date,
                )

                return HttpResponse('Event upload success')
        else:
            return HttpResponseRedirect(reverse('blogs:login'))

    else:
        event_form=EventUploadForm()

    context = {
        'form' = event_form,
    }

    return render(request, ,context)

def eventlive(request,pk):
    event=get_object_or_404(Event, pk=pk)

    if request.session.has_key()'eid'):
        emailID=request.session['eid']
        user=UserDetail.objects.get(emailID__exact=emailID)
        if user.isAdmin:
            event.isLive = True
            event.save()
            return HttpResponseRedirect(reverse('blogs:pendingpost'))
        else:
            return HttpResponseRedirect(reverse('blogs:permissiondenied'))
    else:
        return HttpResponseRedirect(reverse('blogs:login'))

def eventblock(request,pk):
    event=get_object_or_404(Event, pk=pk)

    if request.session.has_key()'eid'):
        emailID=request.session['eid']
        user=UserDetail.objects.get(emailID__exact=emailID)
        if user.isAdmin:
            event.isLive = False
            event.save()
            return HttpResponseRedirect(reverse('blogs:pendingpost'))
        else:
            return HttpResponseRedirect(reverse('blogs:permissiondenied'))
    else:
        return HttpResponseRedirect(reverse('blogs:login'))
