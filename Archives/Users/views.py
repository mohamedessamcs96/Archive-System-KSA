from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpResponse
import datetime 
# Import these methods
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.platypus import Frame
from reportlab.lib.pagesizes import A4, landscape
from django.contrib.auth.decorators import login_required
from .models import UserAdmin,AddUser,Document
from .forms import CustomerForm,AddUserForm,SearchUserForm,AddDocument
# importing required libraries
import cv2  # OpenCV library 
import time # time library
import numpy as np
from threading import Thread # library for multi-threading

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
    # In django views
    TakeImage=False
    UploadImage=False
    if request.GET.get('UploadImage') == 'UploadImage':
        UploadImage=not(UploadImage) 
        TakeImage=False     
        print('user clicked UploadImage')
        print(UploadImage)
    if request.GET.get('TakeImage') == 'TakeImage':
        print('user clicked TakeImage')
        TakeImage=not TakeImage 
        UploadImage=False
        video = cv2.VideoCapture(0)
        if video.isOpened():
            frames=[]
            while len(frames)<20:
                time.sleep(0.1) 
                check, frame = video.read()
                if check:
                    cv2.imshow('Color Frame', frame)
                    frames.append(frame)
                    lastframe=frames[len(frames)-1]
                    """                    mask = np.zeros(lastframe.shape[:2],np.uint8)
                    bgdModel = np.zeros((1,65),np.float64)
                    fgdModel = np.zeros((1,65),np.float64)
                    rect = (20,20,lastframe.shape[1]-20,lastframe.shape[0]-20)
                    cv2.grabCut(lastframe,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
                    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
                    lastframe = lastframe*mask2[:,:,np.newaxis]
                    """
                    """
                    gray=cv2.cvtColor(lastframe,cv2.COLOR_BGR2GRAY)

                    # Set the threshold and maxValue
                    thresh= 120
                    maxValue = 255

                    gray=cv2.cvtColor(lastframe,cv2.COLOR_BGR2GRAY)
                    # Basic threshold example
                    th, dst= cv2.threshold(gray, thresh, maxValue, cv2. THRESH_BINARY)
                    lastframe[np.where(dst==0)] = 255
                    #use -1 as the 3rd parameter to draw all the contours
                    #cv2.drawContours(lastframe,contours,-1,(0,255,0),3)
                    #gray=cv2.cvtColor(lastframe,cv2.COLOR_BGR2GRAY)
                    #edged=cv2.Canny(gray,30,200)
                    #we have to add _, before the contours as an empty argument due to upgrade of the OpenCV version
                    #contours, hierarchy=cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
                    #_, contours,hierarchy=cv2.findContours(edged,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
                    #cv2.drawContours(lastframe, contours, -1, (0, 255, 0), -1) #---set the last parameter to -1
                    """
                    cv2.imwrite('./media/images/newdocument.jpg' , lastframe)
                    document=cv2.imread('document.jpg')
                    print(document)
                    key = cv2.waitKey(10)
                    if key == ord('q'):
                        break
                else:
                    print('Frame not available')
                    print(video.isOpened())
    document=cv2.imread('document.jpg')
    import os
    print(os.getcwd())
    documentpath=os.path.join(os.getcwd(),'document.jpg')
    print(documentpath)
    documentForm=AddDocument()
    context={'documentForm':documentForm,'document':documentpath,'UploadImage':UploadImage,'TakeImage':TakeImage}
    return render(request,'add_document.html',context)  


def create_report(request,pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="EmplyeeReport.pdf"'

    usertable=AddUser.objects.get(jobnumber=pk)
    

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    p.setPageSize((800, 800)) 
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(400,700, f"Hello {usertable.name}")
    p.drawString(400,680, f"job number {usertable.jobnumber}")
    

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response