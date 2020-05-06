from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Application, AcceptedUser, RejectedUser, BlackList
from .choices import RESPONSE_CHOICES
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class ApplicationForm(forms.ModelForm):
    reference = forms.ModelChoiceField(queryset=AcceptedUser.objects.all().filter(is_SU=False))
    class Meta:
        model = Application
        fields = [
            'email',
            'firstName',
            'lastName',
            'interest',
            'credential',
            'reference',
        ]

    def checkBlackList(self):
        '''This function checks if email is black listed'''
        data = self.cleaned_data
        try:
            BlackList.objects.get(email=data['email'])
        except ObjectDoesNotExist:
            return False
        return True

    def checkApplicationExist(self):
        '''This function checks if the email has already applied and is waitng for response'''
        data = self.cleaned_data
        try:
            Application.objects.get(email=data['email'])
        except ObjectDoesNotExist:
            return False
        return True


class AcceptRejectForm(forms.Form):
    application = forms.ModelChoiceField(queryset=Application.objects.all())
    response = forms.ChoiceField(choices=RESPONSE_CHOICES)
    username = forms.CharField(label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
       fields = [
           'application',
           'response',
           'username',
           'password'
       ]
    
    def getChoice(self):
        data = self.cleaned_data
        application = data['application']
        email = application.getEmail()

        if data['response'] == "1":
            self.acceptApplication(data['username'], data['password'], email)
        else:
            self.rejectApplication(email)

    def acceptApplication(self, username, password, email):
        '''Will email username and password also create user and accepteduser'''
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User already exists!")  #ouput to page that the user already exists

        else:
            user = User.objects.create_user(username, password=password, email=email)
            user.save()
            AcceptedUser.objects.create(user=user)
            status = 'new user was created'

            #send out email if accepted
            html_message = render_to_string('AcceptEmail.html', {'username': username, 'password':password})
            plain_message = strip_tags(html_message)
            
            send_mail('Welcome to TeamUp', plain_message, 'sender@example.com', [email], html_message=html_message) #action of sending email
     
        
    def rejectApplication(self, email):
        '''Function will handle rejection of application
        if it is first time it will be added to rejected DB
        otherwise added to Blacklist DB'''
        if(self.checkRejected(email)):
            #adds to blacklist only if it was rejected before
            BlackList.objects.create(email=email)
        else:
            RejectedUser.objects.create(email=email)

        

    def checkRejected(self, email):
        '''This function checks if Application has been rejected before'''
        try:
            RejectedUser.objects.get(email=email)
        except ObjectDoesNotExist:
            return False
        return True