from django.db import models

# create profile post user create
from django.db.models.signals import post_save

from django.contrib.auth.models import User


# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    picture = models.ImageField(upload_to='rooms', null=True, blank=True)
    user_create = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'room'
        verbose_name_plural = 'rooms'
    
    @property
    def created_by(self):
        return self.user_create.username
    
class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} message"

    class Meta:
        db_table = 'message'
        verbose_name_plural = 'messages' 
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user.username}'profiles"

    @property
    def rooms_created(self):
        numbers_rooms = Room.objects.filter(user_create=self.user).count()
        return numbers_rooms
    
    @property
    def names_rooms_created(self):
        rooms = Room.objects.filter(user_create=self.user).all()
        names_list = []
        for i in rooms:
            names_list.append(i.name)
        return names_list

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_profile, User)
