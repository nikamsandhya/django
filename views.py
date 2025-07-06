from django.shortcuts import render
from.models import Tweet
from.forms import Tweetform ,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index(request):
    return render(request,'index.html')

# first functoinality is for list all tweets on on page
def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html',{'tweets':tweets})
# creating tweets
@login_required
def tweet_create(request):
    if request.method =="POST":# CHECKING FOR USER IS FILLING A FORM OR NOT if its fill then post request should be come
      form=Tweetform(request.POST,request.FILES)# WE accepting a form (post data)and files also
      if form.is_valid():# django provide built in security (like CSRF)this method is for checking a form is valid or not
          tweet=form.save(commit=False)# false because ham abhi database mai use save nhi karna chahte only form save karna chahte hai
          tweet.user =request.user #har request ke pass user ata hi ata hai
          tweet.save()
          return redirect('tweet_list')
    else:
        form =Tweetform() #user ko empty form dede
    return render(request,'tweet_form.html',{'form':form})

#how to edit tweet
@login_required
def tweet_edit(request,tweet_id):
    tweet= get_object_or_404(Tweet,pk=tweet_id,user=request.user)# tweet should be edit by only requested user
    if request.method =='POST':
       form = Tweetform(request.POST,request.FILES,instance=tweet)
       if form.is_valid():
           tweet=form.save(commit=False)
           return redirect('tweet_list')

    else:
        form=Tweetform(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})
#tweet delete
@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request)
    if request.method =='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_confirm_delete.html',{'tweet:form'})

def register(request):
    if request.method == "POST":
        form= UserRegistrationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.set_passwordform(form.cleaned_data['password1'])
            user.save()
            login(request.user)
            return redirect('tweet_list')

    else:
        form= UserRegistrationForm()
    return render(request,'registration/register.html',
                  {'form':form})

