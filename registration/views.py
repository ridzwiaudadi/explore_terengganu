from django.shortcuts import render,redirect
#from django.http import HttpResponseRedirect
#from django.urls import reverse
from django.contrib.auth import logout
from registration.models import Register,Review,Event,User


# Create your views here.

def index(request):
    return render (request,"index.html")

def aboutus(request):
    return render (request,"aboutus.html")

def registeracc(request):  
    if request.method == 'POST':
        c_username=request.POST['username']
        c_password=request.POST['password']
        c_userphonenum=request.POST['userphonenum']
        c_email= request.POST['useremail']

        find_data=User.objects.filter(username=c_username).values()

        if find_data.count()==0:
            data= User(username=c_username, password=c_password, userphonenum=c_userphonenum, useremail=c_email)
            data.save()
            dict={
                'message':"Your data has been saved and registered."
            }
            return redirect('loginacc')
        else:
            dict={
                'message': "User" + find_data[0]['username'] + "already exists"
            }
    else:
        dict={
            'message':''
        }
    return render (request, "registeracc.html",dict)

def loginacc (request):
    if request.method =='POST':
        u_name=request.POST['username']
        u_password=request.POST['password']
        find=User.objects.filter(username=u_name).values()
        if find.exists(): 
            if (find[0]['password'] == u_password):
                request.session['user'] = u_name
                dict={ "user":find[0]['username']}
                #return render (request, redirect('homepage'),dict)
                return redirect('index2')
            else:
                dict={ "message":"wrong password"}
                return render (request, 'loginacc.html',dict)
        else:
            dict={ "message":"wrong username"}
            return render (request, 'loginacc.html',dict)        
    else:
        return render (request, 'loginacc.html')

def index2(request):
    return render (request,"index2.html")

def aboutus2(request):
    return render (request,"aboutus2.html")
 
def bookevent(request):
    event = Event.objects.all()
    if request.method == 'GET':
        search_term = request.GET.get("search_event")
        if search_term :
            data = Event.objects.filter(eventname__icontains = search_term)
        else: 
            data = Event.objects.none()
        dict={
                'data' : data,
                'event':event
            }      
        return render (request,"bookevent.html",dict)  
    else:
        dict={
                'event':event
            } 
        return render (request,"bookevent.html",dict)

def bookevent2(request):
    event= Event.objects.all()
    if request.method == 'GET':
        search_term = request.GET.get("search_event")
        if search_term:
            data = Event.objects.filter(eventname__icontains = search_term)
        else: 
            data = Event.objects.none()
        dict={
                'data' : data,
                'event':event
            }      
        return render (request,"bookevent2.html",dict)  
    else:
        dict={
                'event':event
            } 
        return render (request,"bookevent2.html",dict)

def registerevent(request):
    if 'user' in request.session:
        s_username = request.session['user']
        user = User.objects.get(username=s_username)
        all_event = Event.objects.all().values()
        userregister= Register.objects.filter(userID=user)

        if request.method == 'POST':
            if 'cancel_register' in request.POST:
                registerID = request.POST.get('registerID')
                try:
                    register = Register.objects.get(registerID=registerID)
                    if register.userID.username == s_username:
                        register.delete()
                except Register.DoesNotExist:
                    return render(request, "registerevent.html", {
                        'all_event': all_event,
                        'userregister': userregister,
                        'error': "Booking not found."
                    })
                return redirect('registerevent')
            s_eventID = request.POST.get('all_event')
            s_numofticket = request.POST.get('numofticket')
            s_paymentmethod = request.POST.get('paymentmethod')
            s_registerdate = request.POST.get('registerdate')

            if not s_eventID or not s_numofticket or not s_paymentmethod or not s_registerdate:
                return render(request, "registerevent.html", {'all_event': all_event,'userregister':userregister,'error': "All fields are required."})
            c_eventID = Event.objects.get(eventID=s_eventID)
            totalPrice = c_eventID.eventprice * int(s_numofticket)
            data = Register(userID=user,eventID=c_eventID,numofticket=s_numofticket,paymentmethod=s_paymentmethod,registerdate=s_registerdate,registerstatus="Booked",totalprice=totalPrice)
            data.save()            
            return redirect('registerevent')
        return render(request, "registerevent.html", {'all_event': all_event, 's_username': s_username, 'userregister':userregister})
    else:
        return redirect('registeracc')




def userdashboard(request):
    if 'user' in request.session:
        username = request.session['user']
        user = User.objects.get(username=username)
        return render(request, "userdashboard.html", {'user': user})
    else:
        return redirect('loginacc')

def userdashboard_update(request,userID):
    user = User.objects.get(userID= userID)
    if request.method =='POST':
        #new_username=request.POST['username']
        new_phonenum = request.POST['userphonenum']
        new_email = request.POST['useremail']
        #user.username= new_username
        user.userphonenum=new_phonenum
        user.useremail= new_email
        user.save()
        return redirect('userdashboard')
    else : 
        dict = {
            'user': user
        }
        return render(request, "userdashboard_update.html", dict)


def sign_out(request):
    logout(request)
    return redirect('index')

def review(request):
    if 'user' in request.session:
        s_username = request.session['user']
        user = User.objects.get(username=s_username) 

        if request.method =='POST':
            review_comment=request.POST['reviewcomment']

            review= Review(userID=user, reviewcomment=review_comment)
            review.save()

            return redirect('review')
        review_user= Review.objects.filter(userID=user)
        return render(request,'review.html',{'review_user': review_user})
    return redirect('loginacc')

def delete_review(request, review_id):
    try:
        review = Review.objects.get(reviewID=review_id)
        review.delete()  
    except Review.DoesNotExist:
        pass
    return redirect('review')  

def edit_review(request, review_id):
    try:
        review = Review.objects.get(reviewID=review_id)
    except Review.DoesNotExist:
        return redirect('review')  

    if request.method == 'POST':
        review_comment = request.POST['reviewcomment']
        review.reviewcomment = review_comment  
        review.save()  
        return redirect('review')  
    return render(request, 'edit_review.html', {'review': review}) 

def display_review(request):
    review= Review.objects.all().values('reviewcomment')
    if review.count()!=0:
        dict={
            'review':review,
        }
    else:
        dict={
        }
    return render (request,"display_review.html",dict)