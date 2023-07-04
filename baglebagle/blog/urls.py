
# 현재 폴더의 views를 사용한다.
from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('post_update/<int:pk>', views.PostUpdate.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),
    path('<int:pk>/add_comment', views.add_comment),
    path('<int:pk>/add_aggression', views.add_aggression),
    path('tag/<str:slug>/', views.tag_page),
    path('search/<str:q>/', views.PostSearch.as_view()),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment),
    path('mim/<int:pk>/',views.mim_explanation),
    path('original_me/', views.get_original_content_me),
    path('step22_me/', views.get_step22_results_me),
    path('step33_me/',views.get_step33_results_me),
    path('step44_me/',views.get_step44_results_me),
    path('original_other/', views.get_original_content_other),
    path('step22_other/', views.get_step22_results_other),
    path('step33_other/', views.get_step33_results_other),
    path('step44_other/', views.get_step44_results_other),
]