from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import PostViewSet, GroupViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'groups', GroupViewSet, basename='group')

# Роутер для комментариев (вложенный в посты)
# Комментарии регистрируем отдельно с динамическим постом
urlpatterns = [
    path('api-token-auth/', obtain_auth_token),  # получение токена
    path('', include(router.urls)),  # posts/ и groups/

    # Комментарии: вложенный роутинг через posts/{post_id}/comments/
    path('posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('posts/<int:post_id>/comments/<int:pk>/',
         CommentViewSet.as_view({
             'get': 'retrieve',
             'put': 'update',
             'patch': 'partial_update',
             'delete': 'destroy'
         })),
]
