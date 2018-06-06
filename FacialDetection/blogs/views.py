import base64
import datetime
import os

import cv2

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .forms import NewPostForm
from django.contrib import messages

from .models import Post


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


@method_decorator(login_required, name='dispatch')
class OwnPostView(PostListView):
    template_name = 'own_blogs.html'


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'body', 'image')
    context_object_name = 'Posts'
    template_name = 'edit_post.html'
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.user == post.created_by:
            post.updated_at = timezone.now()
            post.save()
            return redirect('own_blogs')
        else:
            messages.error(self.request, 'You are not own this post!')
            return redirect('home')


def about(request):
    return render(request, 'about.html')


def stream():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('static/images/img_demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' +
               open('static/images/img_demo.jpg', 'rb').read() + b'\r\n')


def video_feed(request):
    return StreamingHttpResponse(stream(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def detected_face(request):
    return render(request, 'streaming.html')


def error(request):
    return render(request, 'error.html')


@login_required
def new_post(request):
    user = request.user
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


@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('blogs')

    def get_object(self, queryset=None):
        obj = super(PostDeleteView, self).get_object()
        if not obj.created_by == self.request.user:
            raise Http404
        return obj


# TODO: Handle file then send log to template
def send_message(request):

    # Demo for read and execute another python file
    exec(open("./test.py").read())

    temp_str = 'Demo for send message to template'
    messages.success(request, temp_str)
    return redirect('get_data')
