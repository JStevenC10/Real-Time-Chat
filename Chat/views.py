from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.conf import settings

from .models import Room, Message, Profile
from .forms import UserRegisterForm
from .utils import join_name
# Create your views here.

class InfoView(TemplateView):
    template_name = 'info.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = """
            Welcome to chat me, you can meet people and message with them about fun topics, join now!
        """
        return context
    

# REGISTER USERS
class CreateUserView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        messages.success(request, 'Login with new credentials!')
        return super().post(request, *args, **kwargs)


@login_required
def home(request, *args, **kwargs):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms':rooms})

@login_required
def delete_room(request, *args, **kwargs):
    current_user = request.user
    chat_room = Room.objects.filter(pk=kwargs['pk']).first()
    if chat_room and (chat_room.user_create == current_user):
        chat_room.delete()
        return redirect(to=home)
    else:
        return redirect(to=home)

@login_required
def logout_user(request):
    logout(request)
    messages.info(request, 'see you later!')
    return redirect(settings.LOGOUT_REDIRECT_URL)

@login_required
def view_profile(request, *args, **kwargs):
    user = request.user
    user_profile = Profile.objects.filter(user=user).first()
    context = {
        'user': user,
        'profile': user_profile,
    }
    return render(request, 'profile.html', context)

@login_required
def new_room(request, *args, **kwargs):
    if request.method == 'POST':
        name = request.POST['room_name']
        if ' ' in name:
            name = join_name(name)
        new_room = Room.objects.create(
            name=name,
            picture=None,
            user_create=request.user
        )
        try:
            new_room.picture = request.FILES['picture']
        except:
            pass
        new_room.save()
        return redirect('home')
    return render(request, 'newroom.html')

def chatroom(request, *args, **kwargs):
    context = {}
    room = Room.objects.filter(name=kwargs['room_name']).first()
    messages = Message.objects.filter(room=room)
    if room:
        context['room'] = room
        context['username'] = request.user.username
        context['room_name'] = room.name
        context['messages'] = messages
        return render(request, 'chatroom.html', context)
    else:
        return redirect(to=home)

