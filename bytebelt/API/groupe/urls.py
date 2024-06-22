from django.urls import path
from .views import CreateGroupeView ,GetAllGroupeView , GetGroupeByName , GetAllPostForGroupeView ,CreatePostForGroupeViewByGroupeId

urlpatterns = [
    path('', GetAllGroupeView.as_view(), name='get-all-groupe'),
    path('create/', CreateGroupeView.as_view(), name='create-groupe'),
    path('info/<name>/', GetGroupeByName.as_view(), name='get-groupe-by-name'),
    path('publications/<groupe_id>/', GetAllPostForGroupeView.as_view(), name='get-all-publications-for-groupe'),
    path('publications/create/<groupe_id>/', CreatePostForGroupeViewByGroupeId.as_view(), name='create-publication-for-groupe'),
]