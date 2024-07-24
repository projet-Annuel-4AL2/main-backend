from django.urls import path
from .views import CreateGroupeView ,GetAllGroupeView , GetGroupeByName , GetAllPostForGroupeView ,CreatePostForGroupeViewByGroupeId ,LikePublicationView , CommentPublicationView , GetPublicationGroupeById , GetCommentGroupeById , DeletePostForGroupeView  ,GetGroupeById , GetPostInfoView , EditPostForGroupeView , EditGroupeView

urlpatterns = [
    path('', GetAllGroupeView.as_view(), name='get-all-groupe'),
    path('update/<int:groupe_id>/', EditGroupeView.as_view(), name='update-groupe'),
    path('create/', CreateGroupeView.as_view(), name='create-groupe'),
    path('info/<name>/', GetGroupeByName.as_view(), name='get-groupe-by-name'),
    path('inf/<int:groupe_id>/', GetGroupeById.as_view(), name='get-groupe-by-id'),
    path('publications/<groupe_id>/', GetAllPostForGroupeView.as_view(), name='get-all-publications-for-groupe'),
    path('publications/info/<int:publication_id>/', GetPostInfoView.as_view(), name='get-publication-info'),
    path('publications/create/<groupe_id>/', CreatePostForGroupeViewByGroupeId.as_view(), name='create-publication-for-groupe'),
    path('publications/delete/<int:publication_id>/', DeletePostForGroupeView.as_view(), name='delete-publication'),
    path('publications/edit/<int:publication_id>/', EditPostForGroupeView.as_view(), name='edit-publication'),
    path('publications/<int:publication_id>/like/', LikePublicationView.as_view(), name='like-publication'),
    path('publications/<int:publication_id>/comment/', CommentPublicationView.as_view(), name='comment-publication'),
    path('publications/<str:groupe_name>/<int:publication_id>/', GetPublicationGroupeById.as_view(), name='get-publication-by-id'),
    path('publication/<int:publication_id>/comment/', GetCommentGroupeById.as_view(), name='get-comment-by-id')
]