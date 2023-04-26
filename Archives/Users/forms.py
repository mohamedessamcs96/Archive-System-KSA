from fractions import Fraction
from camera_imagefield import CameraImageField
from django import forms
from .models import *



class DateInput(forms.DateInput):
    input_type = 'date'

class CustomerForm(forms.ModelForm):

    class Meta:
        model = UserAdmin
        fields =('fname','lname','username','email','birthdate','gender','is_admin','is_superuser','is_staff','password1','password2')
        widgets={
                'fname':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":"fname"}),
                'lname':forms.TextInput(attrs={'class':'form-control','style':'max-width: 20em',"id":"","placeholder":"lname"}),
                'email':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":"email"}),
                'username':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":"Username"}),
                'password1':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":"password1"}),
                'password2':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":"password2"}),
                'gender': forms.Select(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":"is_admin"}),
                'is_admin': forms.CheckboxInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":"is_superuser"}),
                'is_superuser': forms.CheckboxInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":"fname"}),
                'is_staff': forms.CheckboxInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":"is_staff"}),
                'birthdate':DateInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":"29/09/1996"})
               
                
     }

class AddUserForm(forms.ModelForm):
    class Meta:
            model = AddUser
            fields = ('name','job','jobnumber','birthdate','image','notes','contract')
            widgets={
                'name':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'job':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'jobnumber':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'birthdate':forms.DateTimeInput(attrs={'class':'form-control','style':'width:70%'}),
                'notes':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'image':forms.FileInput(attrs={'class':'form-control','style':'width:70%'}),
                'contract':forms.FileInput(attrs={'class':'form-control','style':'width:70%'})
                
     }

class AddDocument(forms.ModelForm):
     class Meta:
          model=Document
          fields=('title','image')
          widgets={
                'title':forms.TextInput(attrs={'class':'form-control'}),
                #'image':CameraImageField()
                'image':forms.FileInput(attrs={'class':'form-control'})
                
     }


class SearchUserForm(forms.Form):
     jobnumber=forms.IntegerField()
     fields=('jobnumber')
     widgets={
        'jobnumber':forms.TextInput(attrs={'class':'form-control'})
            
     }

     #fields = '__all__'