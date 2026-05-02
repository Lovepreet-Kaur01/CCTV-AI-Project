from django.shortcuts import render, redirect
from .detect import detect_objects, live_detection
from .models import Detection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def home(request):
    result = None
    alert = None

    if request.method == "POST":

        if 'video' in request.FILES:
            video = request.FILES['video']
            path = "media/" + video.name

            with open(path, 'wb+') as f:
                for chunk in video.chunks():
                    f.write(chunk)

            result = detect_objects(path)

        elif 'live' in request.POST:
            result = live_detection()

        if result:
            for obj in result:
                if obj == "person":
                    alert = "⚠️ Person Detected!"
                Detection.objects.create(object_name=obj)

    data = Detection.objects.all().order_by('-timestamp')[:10]
    chart_data = Detection.objects.values('object_name').annotate(count=Count('object_name'))

    return render(request, "index.html", {
    "result": result,
    "data": data,
    "alert": alert,
    "chart_data": chart_data
})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.save()
        messages.success(request, 'Account created successfully')

        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')