import subprocess
import json
import requests
import hashlib
from decouple import config
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate , get_user_model , login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect


API_BASE_URL = config('API_BASE_URL')


def token_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.session.get('token')
        if not token:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper  

@token_required
def home(request):
    if not request.session.get('token'):
        return redirect('login')
    
    user_data = get_user_data(request)
    if user_data:
        users = user_data.get('users')
        user = user_data.get('user') 
        for user in users:
            if user['id'] == user_data.get('user').get('id'):
                users.remove(user)
                break
        return render(request, 'home.html', {
            'users': users,
            'user': user,
            'followers': user_data.get('followers'),
            'followings': user_data.get('followings'),
            'groupes': user_data.get('groupes')
        })
    else:
        return render(request, 'home.html', {'error': 'Unable to fetch user data'})
    
def feed(request):
    if not request.session.get('token'):
        return redirect('login')
    
    user_data = get_user_data(request)
    if(user_data):
        return render(request, 'feed.html', {
            'users': user_data.get('users'),
            'user': user_data.get('user'),
            'followers': user_data.get('followers'),
            'followings': user_data.get('followings')
        })
    else:
        return render(request, 'feed.html', {'error': 'Unable to fetch user data'})
    
def explorer(request):
    if not request.session.get('token'):
        return redirect('login')
    
    user_data = get_user_data(request)
    if user_data:
        return render(request, 'explorer.html', {
            'users': user_data.get('users'),
            'user': user_data.get('user'),
            'followers': user_data.get('followers'),
            'followings': user_data.get('followings')
        })
    else:
        return render(request, 'explorer.html', {'error': 'Unable to fetch user data'})

@token_required
def userDetail (request , pk):
    response = requests.get(API_BASE_URL + 'users/' + str(pk) + '/')
    user_info = requests.post(API_BASE_URL + 'user/', data={'token': request.session.get('token')})
    if response.status_code == 200 and user_info.status_code == 200:
        user = response.json()
        user_info = user_info.json()        
        return render(request, 'userDetail.html', {'user': user , 'user_info': user_info})
    else:
        redirect('home')
        
@token_required
def userInfos (request , username):
    response = requests.get(API_BASE_URL + 'users/' + username + '/')
    user_info = requests.post(API_BASE_URL + 'user/', data={'token': request.session.get('token')})

    if response.status_code == 200 and  user_info.status_code == 200:
        user = response.json()
        user_info = user_info.json()
        followings = requests.get(API_BASE_URL + 'users/' + user_info.get('id') + '/get-following/').json()
        followings = [following.get('id') for following in followings.get('following')]
        followings_users = requests.get(API_BASE_URL + 'users/' + user.get('id') + '/get-following/').json()
        followings_users = [following.get('id') for following in followings_users.get('following')]
        #user = response.json()
        return render(request, 'userDetail.html', {'user_': user , 'user_info': user_info , 'followings': followings , 'followings_users': followings_users})
    else:
        redirect('home')
        
def get_user_data(request):
    token = request.session.get('token')
    user_response = requests.post(API_BASE_URL + 'user/', data={'token': token})
    response = requests.get(API_BASE_URL + 'users/')
    if user_response.status_code == 200 and response.status_code == 200:
        users = response.json()
        user = user_response.json()
        followers_response = requests.get(API_BASE_URL + 'users/' + str(user['id']) + '/followers/')
        followings_response = requests.get(API_BASE_URL + 'users/' + str(user['id']) + '/followings/')
        groupes = requests.get(API_BASE_URL + 'groupe/')
        if followers_response.status_code == 200 and followings_response.status_code == 200:
            return {
                'users': users,
                'user': user,
                'followers': followers_response.json(),
                'followings': followings_response.json(),
                'groupes': groupes.json()
            }
    return None

        
def login(request):
    if request.session.get('token'):
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')        
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'error': 'username and password are required'}) 

        if username and password:
            
            response = requests.post(API_BASE_URL + 'auth/', data={'username': username, 'password': password})
            
            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    request.session['token'] = token
                    user_data = get_user_data(request)
                    user = user_data.get('user')
                    users = user_data.get('users')
                    for user in users:
                        if user['id'] == user_data.get('user').get('id'):
                            users.remove(user)
                            break
                    return render(request, 'home.html' ,{
                                  'users': users,
                                  'user': user,
                                  'followers': user_data.get('followers') ,
                                  'followings': user_data.get('followings'),
                                  'groupes': user_data.get('groupes')},
                                  )
                    
                else:
                    return render(request, 'login.html', {'error': 'Invalid credentials'})
            else:
                return render(request, 'login.html', {'error': 'error api'})
                        
    return render(request, 'login.html')

def subscribe(request):
    if request.session.get('token'):
            return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if not username or not email or not password or not password2:
            return render(request, 'register.html', {'error': 'All fields are required'})
        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        try:
            response = requests.post(API_BASE_URL + 'register/', data={'username': username, 'email': email, 'password': password})
            if response.status_code == 201:
                request.session['token'] = response.json().get('token')
                user_data = get_user_data(request)
                user = user_data.get('user')
                users  = user_data.get('users')
                for user in users:
                    if user['id'] == user_data.get('user').get('id'):
                        users.remove(user)
                        break
                return render(request, 'home.html' ,{
                                    'users': users,
                                    'user': user,
                                    'followers': user_data.get('followers') ,
                                    'followings': user_data.get('followings'),
                                    'groupes': user_data.get('groupes')
  
                })
            else:
                error = response.json().get('error', 'Error registering user via API')
                return render(request, 'register.html', {'error': error})
        except requests.RequestException:
            return render(request, 'register.html', {'error': 'Error connecting to API'})
    
    return render(request, 'register.html')

def get_user_data(request):
    token = request.session.get('token')
    user_response = requests.post(API_BASE_URL + 'user/', data={'token': token})
    if user_response.status_code == 200:
        user = user_response.json()
        users = requests.get(API_BASE_URL + 'users/')
        followers_response = requests.get(API_BASE_URL + 'users/' + str(user['id']) + '/followers/')
        followings_response = requests.get(API_BASE_URL + 'users/' + str(user['id']) + '/followings/')
        groupes = requests.get(API_BASE_URL + 'groupe/')
        if followers_response.status_code == 200 and followings_response.status_code == 200 and users.status_code == 200 and groupes.status_code == 200:
            return {
                'users': users.json(),
                'user': user,
                'followers': followers_response.json(),
                'followings': followings_response.json(),
                'groupes': groupes.json()
            }
    return None

def get_all_users_view(request):
    user_get_data = get_user_data(request)
    if user_get_data:
        users = user_get_data.get('users')
        user = user_get_data.get('user') 
        for user in users:
            if user['id'] == user_get_data.get('user').get('id'):
                users.remove(user)
                break
        return render(request, 'users_.html', {'users': users, 'user': user})
    
    
def resetPassword(request):
    return render(request, 'resetPassword.html')


def logout(request):
    del request.session['token']
    return redirect('login')

@token_required
def profile(request):
    #get user info by token in session
    user_data = get_user_data(request)
    if user_data:
        return render(request, 'profile.html', {
            'users': user_data.get('users'),
            'user': user_data.get('user'),
            'followers': user_data.get('followers'),
            'followings': user_data.get('followings')
        })
    else:
        return render(request, 'profile.html', {'error': 'Unable to fetch user info'})
    
        
    
def updateProfile(request):
    user_data = get_user_data(request)

    if request.method == 'POST':
        token = request.session.get('token')
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic') if 'profile_pic' in request.FILES else None

        data = {
            'username': username,
            'email': email,
        }
        files = {'profile_pic': profile_pic} if profile_pic else None

        headers = {'Authorization': 'Token ' + token}
        if files:
            response = requests.post(API_BASE_URL + 'updateuser/', headers=headers, data=data, files=files)
        else:
            response = requests.post(API_BASE_URL + 'updateuser/', headers=headers, data=data)

        if response.status_code == 200:
            return redirect('profile')
        else:
            messages.error(request, 'Error updating user')
            return render(request, 'profile.html', {
                'users': user_data.get('users'),
                'user': user_data.get('user'),
                'followers': user_data.get('followers'),
                'followings': user_data.get('followings')
            })

    return render(request, 'updatProfile.html', {
        'users': user_data.get('users'),
        'user': user_data.get('user'),
        'followers': user_data.get('followers'),
        'followings': user_data.get('followings')
    })


def updatePassword(request):
    user_data = get_user_data(request)
    
    if request.method == 'POST':
        password = request.POST.get('password')
        if password and len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return render(request, 'updatePassword.html', {
                'user': user_data.get('user'),
            })     
        if password:
            token = request.session.get('token')
            headers = {'Authorization': 'Token ' + token}
            data = {'password': password}
            response = requests.post(API_BASE_URL + 'updateuser/', headers=headers, data=data)

            if response.status_code == 200:
                messages.success(request, 'Password updated successfully')
                return redirect('profile')
            else:
                messages.error(request, 'Error updating password')
                return render(request, 'updatePassword.html', {
                    'user': user_data.get('user'),
                })
        else:
            messages.error(request, 'Password is required')
            return render(request, 'updatePassword.html', {
                'user': user_data.get('user'),
            })
      
    return render(request, 'updatePassword.html', {
        'user': user_data.get('user'),
    })
    

    
def groupInfo(request , name):
    response = requests.get(API_BASE_URL + 'groupe/info/' + name + '/')
    groupe_id = response.json().get('id')
    posts = requests.get(API_BASE_URL + 'groupe/publications/' + str(groupe_id) + '/')
    token = request.session.get('token')
    user_id = requests.post(API_BASE_URL + 'user/', data={'token': token}).json().get('id')
    users_response = requests.get(API_BASE_URL + 'users/')
    if response.status_code == 200 and posts.status_code == 200:
        groupe = response.json()
        posts = posts.json()
        users = users_response.json()
        user_id_to_username = {user['id']: user['username'] for user in users}
        for post in posts:
            if post['author'] in user_id_to_username:
                post['author'] = user_id_to_username[post['author']]

        user_id = requests.post(API_BASE_URL + 'user/', data={'token': token}).json().get('id')
        return render(request, 'groupInfo.html', {'groupe': groupe, 'posts': posts, 'user_id': user_id})
    else:
        return render(request, 'groupInfo.html', {'error': 'Unable to fetch group info'})

def groupPost(request, name):
    response = requests.get(API_BASE_URL + 'groupe/info/' + name + '/')
    groupe_id = response.json().get('id')
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')  # Use FILES to get the uploaded image

        if content:
            token = request.session.get('token')
            user_response = requests.post(API_BASE_URL + 'user/', data={'token': token})
            if user_response.status_code == 200:
                user_id = user_response.json().get('id')
                if user_id:
                    data = {
                        'content': content,
                        'author': str(user_id),
                        'groupe': str(groupe_id)
                    }
                    files = {'image': image} if image else None
                    response = requests.post(API_BASE_URL + f'groupe/publications/create/{groupe_id}/', data=data, files=files)
                    if response.status_code == 201:
                        return redirect('group', name=name)
                    else:
                        messages.error(request, f'Error creating post: {response.text}')
                        return redirect('group', name=name)
                else:
                    messages.error(request, 'User ID not found')
                    return redirect('group', name=name)
            else:
                messages.error(request, 'Invalid token')
                return redirect('group', name=name)
        else:
            messages.error(request, 'Content is required')
            return redirect('group', name=name)

    return render(request, 'groupPost.html', {'groupe': response.json()})

  
def groupPostInfo(request, name, id):
    token = request.session.get('token')
    user = requests.post(API_BASE_URL + 'user/', data={'token': token}).json()
    response = requests.get(API_BASE_URL + 'groupe/info/' + name + '/')
    post = requests.get(API_BASE_URL + 'groupe/publications/' + name + '/' + str(id) + '/')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            user_id = user.get('id')
            publication_id = post.json().get('id')
            response_comment = requests.post(API_BASE_URL + 'groupe/publications/' + str(publication_id) + '/comment/', data={'content': content, 'author': str(user_id), 'groupe': str(id)})
            if response_comment.status_code != 201:
                messages.error(request, 'Error adding comment')
        else:
            messages.error(request, 'Content is required')

    if post.status_code == 200:
        post = post.json()
        comments = requests.get(API_BASE_URL + 'groupe/publication/' + str(id) + '/comment/').json()
        users = requests.get(API_BASE_URL + 'users/')
        user_id_to_username = {user['id']: user['username'] for user in users.json()}
        for comment in comments:
            if comment['author'] in user_id_to_username:
                comment['author'] = user_id_to_username[comment['author']]
        if post['author'] in user_id_to_username:
            post['author'] = user_id_to_username[post['author']]
        return render(request, 'postGroupInfo.html', {'groupe': response.json(), 'post': post, 'user': user , 'comments': comments})
    else:
        return render(request, 'postGroupInfo.html', {'error': 'Unable to fetch post info'})   
    


def followers(request ):
    token = request.session.get('token')
    user = requests.post(API_BASE_URL + 'user/', data={'token': token}).json()
    user_id = user.get('id')
    response = requests.get(API_BASE_URL + 'users/' + user_id + '/followers/')
    if response.status_code == 200:
        followers = response.json()
        return render(request, 'followers.html', {'followers': followers.get('followers')})
    else:
        return render(request, 'followers.html', {'error': 'Unable to fetch followers'})
    
    
def createGroupe(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        token = request.session.get('token')
        image = request.FILES.get('image')

        if name and description and token and image:
            user_response = requests.post(API_BASE_URL + 'user/', data={'token': token})
            if user_response.status_code == 200:
                user_id = user_response.json().get('id')
                if user_id:
                    files = {'group_pic': image}
                    data = {
                        'name': name,
                        'description': description,
                        'author': user_id
                    }
                    response = requests.post(API_BASE_URL + 'groupe/create/', data=data, files=files)
                    if response.status_code == 201:
                        return redirect('home')
                    else:
                        messages.error(request, 'Error creating group: {}'.format(response.text))
                        return render(request, 'createGroupe.html')
                else:
                    messages.error(request, 'User ID not found')
                    return render(request, 'createGroupe.html')
            else:
                messages.error(request, 'Invalid token')
                return render(request, 'createGroupe.html')
        else:
            messages.error(request, 'All fields are required')
            return render(request, 'createGroupe.html')

    return render(request, 'createGroupe.html')



def userSettings(request , name):
    user_data = get_user_data(request)
    if user_data:
        return render(request, 'userSettings.html', {
            'users': user_data.get('users'),
            'user': user_data.get('user'),
            'followers': user_data.get('followers'),
            'followings': user_data.get('followings')
        })
    else:
        return render(request, 'userSettings.html', {'error': 'Unable to fetch user data'})
    

def deleteUser(request , name):
    response = requests.delete(API_BASE_URL + 'users/' + name + '/')
    if response.status_code == 204:
        del request.session['token']
        return redirect('login')  
    else:
        return render(request, 'userSettings.html', {'error': 'Unable to delete account'})