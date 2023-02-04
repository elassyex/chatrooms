from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import Room,Topic,Message,User
from .forms import RoomForm, UserForm, MyUserCreationForm

# rooms = [
#     {'id':1, 'name':'kosm masr'},
#     {'id':2, 'name':'kosm russia'},
#     {'id':3, 'name':'kosm sisi'},
#     {'id':4, 'name':'kosm puti'}
# ]

def logina(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        usera = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=usera)
        except:
            messages.error(request, "username doesn't exist :( ")
        user = authenticate(request, username=usera, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in :)")
            return redirect('home')
        else:
            messages.error(request, "username or password wrong :( ")
    conte = {'page':page}
    return render(request, 'base/login_register.html', conte)

def register(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something Wrong Just Happened :(')

    cona = {'page':page, 'form':form}
    return render(request, 'base/login_register.html', cona)

def logouta(request):
    logout(request)
    return redirect('home')

def topics(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topicsa.html', {'topics': topics})
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | 
    Q(name__icontains=q)|
    Q(description__icontains=q))
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    con = {'rooms': rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'base/home.html', con)

def room(request,pk):
    room = Room.objects.get(id=pk)
    rmessages = room.message_set.all().order_by('-created')
    members = room.members.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room=room,
            body= request.POST.get('body')
        )
        room.members.add(request.user)
        return redirect('room', pk=room.id)
        
    con = {'room':room, 'messages':rmessages, "members":members}
    return render(request, 'base/room.html', con)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    con = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html',con)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic=topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')
    contex = {'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', contex)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        HttpResponse("You're not allowed here ! :(")
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('home')

    conte = {'form':form, 'topics':topics , 'room':room}
    return render(request, 'base/room_form.html', conte)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        HttpResponse("You're not allowed here ! :(")
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context={'obj':room})

@login_required(login_url='login')
def delmes(request,pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        HttpResponse("You're not allowed here ! :(")
    if request.method == 'POST':
        message.delete()
        # print(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(('home'))
        
    return render(request, 'base/delete.html', context={'obj':message})

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile',pk=user.id)
    con = {'form':form}
    return render(request, 'base/update-user.html', con)

def activity(request):
    room_message = Message.objects.all()
    return render(request, 'base/activitys.html', {'room_message':room_message})