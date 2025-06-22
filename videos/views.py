from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .forms import VideoCreateForm
from .models import Video


class VideoDetailView(DetailView):
    model = Video
    template_name = "video_detail.html"
    context_object_name = "video"


class VideoCreateView(CreateView):
    model = Video
    form_class = VideoCreateForm
    template_name = "video_create.html"


class VideoListView(ListView):
    model = Video
    template_name = "video_list.html"
    context_object_name = "videos"
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        if not q:
            return Video.objects.all()
        return Video.objects.search(q)
