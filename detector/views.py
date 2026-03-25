from django.shortcuts import render
from .detect import detect_objects, live_detection
from .models import Detection
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def home(request):
    result = None

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

        alert = None

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