from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpResponse
import datetime 
from django.contrib.auth.decorators import login_required
from .models import UserAdmin,AddUser,Document
from .forms import CustomerForm,AddUserForm,SearchUserForm,AddDocument



#Create an error message function
def get_error_message(request):
    password1=request.POST['password1']
    password2=request.POST['password2']
    email=request.POST['email']
    if password1!=password2:
        return "The Passwords didn't match"
    if UserAdmin.objects.filter(email=email).exists():
        return "Email already exists"

# Create your views here.
def register_request(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method=="POST":
            form=CustomerForm(request.POST)
            if form.is_valid():
                user=form.save()
                login(request,user)
                print("register successful")
                messages.success(request,"Register successful")
                return redirect('homepage')
            print("unsucessful")
            messages.error(request,get_error_message(request))
            return render(request=request,template_name='register.html',context={'register_form':form})
        else:
            form=CustomerForm()
            return render(request=request,template_name='register.html',context={'register_form':form})
    else:
        return render(request=request,template_name='notallowed.html')
    


def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                print('loggged')
                messages.info(request,f"You are logged as {username}")
                return redirect('homepage')
            else:
                print("Invalid username and password!")
                messages.error(request,"invalid username and password")
        else:
            print("not valid form")
            messages.error(request,"not valid form")

    form=AuthenticationForm()
    return render(request=request,template_name='login.html',context={'login_form':form})
    now = datetime.datetime.now()
    return HttpResponse("html")
def logout_request(request):
    logout(request)
    messages.info(request,"You have sucessfully logged out")
    return redirect("login")


@login_required(login_url='/login/')
def add_user(request):
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = AddUserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            
            #img = request.FILES['image']
            
         
            return render(request, 'add_user.html', {'form': form,'img_obj': img_obj})
        return render(request, 'add_user.html', {'form': form})
        
    else:
        form = AddUserForm()
        return render(request, 'add_user.html', {'form': form})



@login_required(login_url='/login') 
def home_page(request):
    return render(request,'home.html')


@login_required(login_url='/login/')
def search_user(request):
    if request.method == 'POST':
        form=SearchUserForm(request.POST)
        print(request.POST['jobnumber'])
        print(type(request.POST['jobnumber']))
        jobnumber=(request.POST['jobnumber'])
        print(type(jobnumber))
        print("user")
        users=AddUser.objects.filter(jobnumber=jobnumber)
        user=AddUser.objects.get(jobnumber=jobnumber)
        print(user)
        print("user")
        documents=Document.objects.filter(user=jobnumber)
        print("documents")
        if user!=None: 
            context={'form':form,'users':users,'user':user,'documents':documents}
            return render(request,'history.html',context)
        else:
            return HttpResponse("No user found")
    
    form=SearchUserForm()
    return render(request,'historyform.html',{'form':form})


@login_required(login_url='/login/')
def add_document(request,pk):
    if request.method == 'POST':
        documentForm=AddDocument(request.POST)
        recipient=[]   #receiver of mail must be a list
        recipient.append(request.user)
        if documentForm.is_valid:
            #documentForm.cleaned_data['name']
            usertable=AddUser.objects.get(jobnumber=pk)
            #usertable=12345
            #documentForm=AddDocument(request.POST)
            print(usertable)
            #documentForm.save(commit=False)
            #documentForm.user=usertable
            print("Data")
            print(usertable)
            #documentForm.save()
            form_obj = documentForm.instance
            #image=(request.POST.get('image'))
            #print(image)
            title=(request.POST.get('title'))
            img = request.FILES['image']
            print(img)
            print(form_obj.image)
            d = Document.objects.create(user=usertable,title=title,image=img)
            print(d)
            context={'documentForm':documentForm,'form_obj':form_obj}
            return render(request,'add_document.html',context)
    documentForm=AddDocument()
    context={'documentForm':documentForm}
    return render(request,'add_document.html',context)  