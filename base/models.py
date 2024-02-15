from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  #on_delete account, if to keep the tasks, then use on_delete=models.SET_NULL else models.CASCADE deletes tasks.
        title = models.CharField(max_length=200)
        description = models.TextField(null=True, blank=True)
        complete = models.BooleanField(default=False)
        created = models.DateTimeField(auto_now_add=True) # auto_now_add automatically adds a timestamp and thus not to be done manually
        
        def __str__(self):
                return self.title
            
        class Meta:
            ordering = ['complete'] # the metadata of the tasks should  be ordered based on the completion status that complete hold. So any tasks completed should be sent to the bottom of the list.
            