from django import forms
from .models import *


class CustomerForm(forms.ModelForm):

    class Meta:
        model = UserAdmin
        fields =('fname','lname','username','email','birthdate','gender','is_admin','is_superuser','is_staff','password1','password2')
    

class AddUserForm(forms.ModelForm):
    class Meta:
            model = AddUser
            fields = ('name','job','jobnumber','birthdate','image','notes','contract')


class AddDocument(forms.ModelForm):
     class Meta:
          model=Document
          fields=('title','image')

class SearchUserForm(forms.Form):
     jobnumber=forms.IntegerField()
     fields=('jobnumber')
     #fields = '__all__'