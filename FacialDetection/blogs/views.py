import base64
import datetime
import os

import cv2

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.http import StreamingHttpResponse, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.views.generic import ListView, DetailView
from .forms import NewPostForm

from .models import Post
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

# Create your views here.

def home(request):
    return render(request, 'home.html')


def list_blog(request):
    data = {'Posts': Post.objects.all().order_by('-created_at')}
    return render(request, 'blog.html', data)


class PostListView(ListView):
    queryset = Post.objects.all().order_by('-created_at')
    template_name = 'blog.html'
    context_object_name = 'Posts'
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'


def about(request):
    return render(request, 'about.html')


def stream():
    with PiCamera() as camera:
        camera.resolution = (640,480)
        camera.brightness = 65
        camera.framerate = 30
        rawCapture = PiRGBArray(camera,size=(640,480))
        
        time.sleep(0.1)

        
        for frame in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):
        
            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            rawCapture.truncate(0)
            cv2.imwrite('/home/pi/KL/FacialDetection/static/images/img_demo.jpg', gray)
            
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
               open('/home/pi/KL/FacialDetection/static/images/img_demo.jpg', 'rb').read() + b'\r\n')


def video_feed(request):
    return StreamingHttpResponse(stream(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def detected_face(request):
    return render(request, 'streaming.html')


def error(request):
    return render(request, 'error.html')


def new_post(request):
    user = User.objects.first()
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = user
            post.image = form.cleaned_data['image']
            post.save()
            return redirect('blogs')
    else:
        form = NewPostForm()
    return render(request, 'new_post.html', {'form': form})


def get_data(request):
    # TODO: Show 20 images from server to client
    # try:
    #     for filename in os.listdir('static/images'):
    #         info = os.stat(filename)
    #         print(info.st_mtime)
    # except OSError as e:
    #     print(e)
    media_dir = settings.MEDIA_ROOT
    img_path = os.path.join(media_dir, "data/" + request.user.username)
    img_list = os.listdir(img_path)
    return render(request, 'get_data.html', {'images': img_list})


@login_required
def resource(request):
    return render(request, 'resource.html')


def save_img(request):
    if request.method == 'POST':
        if request.is_ajax():
            data = request.POST.get('imgBase64')

            # get base64 raw string from data receive by split data string
            # data = "data:image/png;base64,'base64_raw_string'"
            base64_str = data[22:]
            img_data = base64.b64decode(base64_str)
            get_date_time = datetime.datetime.now()
            str_file_name = get_date_time.strftime("%y%m%d_%H%M%S")

            # Get oldest img in path
            media_dir = settings.MEDIA_ROOT
            img_path = os.path.join(media_dir, "data/" + request.user.username)
            img_list = os.listdir(img_path)
            oldest_img = oldest_file_in_tree(img_path)

            # TODO: Capture 20 pics fo train

            # put image into username folder
            with open('media/data/' + request.user.username
                      + '/' + str_file_name + '.png', 'wb') as f:
                if img_list.__len__() > 19:
                    os.remove(oldest_img)
                    f.write(img_data)
                else:
                    f.write(img_data)
            return HttpResponse('')


def oldest_file_in_tree(rootfolder, extension=".png"):
    return min(
        (os.path.join(dirname, filename)
         for dirname, dirnames, filenames in os.walk(rootfolder)
         for filename in filenames
         if filename.endswith(extension)),
        key=lambda fn: os.stat(fn).st_mtime)
