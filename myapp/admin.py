from .models import *
from django import forms
from django.contrib import admin
from .models import Notification
from .forms import NotificationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

# @admin.register(Consumer)
# class ConsumerAdmin(admin.ModelAdmin):
#     list_display = ["id", "name", "email", "image", "content"]

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "message"]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["id", "consumer", "comment", "rating"]

class NotificationForm(forms.ModelForm):
    send_to_all = forms.BooleanField(required=False, label='Send to all users', initial=False)

    class Meta:
        model = Notification
        fields = ['user', 'message', 'send_to_all']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "message", "created_at"]
    form = NotificationForm

    def add_view(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = NotificationForm(request.POST)
            if form.is_valid():
                user_id = form.cleaned_data['user'].id  # Extracting the user ID
                message = form.cleaned_data['message']
                send_to_all = form.cleaned_data['send_to_all']

                if send_to_all:
                    users = User.objects.all()
                    for user in users:
                        Notification.objects.create(user=user, message=message)
                    messages.success(request, 'Notification sent to all users.')
                else:
                    user = User.objects.get(id=user_id)
                    Notification.objects.create(user=user, message=message)
                    messages.success(request, 'Notification sent successfully.')
                    
                return HttpResponseRedirect(request.path)  # Redirect after processing the form

        return super().add_view(request, *args, **kwargs)

from django.contrib import admin
admin.site.disable_action('delete_selected')