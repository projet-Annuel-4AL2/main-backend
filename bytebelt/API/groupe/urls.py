from django.urls import path
from .views import CreateGroupeView ,GetAllGroupeView , GetGroupeByName , GetAllPostForGroupeView ,CreatePostForGroupeViewByGroupeId ,LikePublicationView , CommentPublicationView , GetPublicationGroupeById

urlpatterns = [
    path('', GetAllGroupeView.as_view(), name='get-all-groupe'),
    path('create/', CreateGroupeView.as_view(), name='create-groupe'),
    path('info/<name>/', GetGroupeByName.as_view(), name='get-groupe-by-name'),
    path('publications/<groupe_id>/', GetAllPostForGroupeView.as_view(), name='get-all-publications-for-groupe'),
    path('publications/create/<groupe_id>/', CreatePostForGroupeViewByGroupeId.as_view(), name='create-publication-for-groupe'),
    path('publications/<int:publication_id>/like/', LikePublicationView.as_view(), name='like-publication'),
    path('publications/<int:publication_id>/comment/', CommentPublicationView.as_view(), name='comment-publication'),
    path('publications/<str:groupe_name>/<int:publication_id>/', GetPublicationGroupeById.as_view(), name='get-publication-by-id')
]