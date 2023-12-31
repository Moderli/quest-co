from django.urls import path
from .views import index, signup, activate, login_view, profile_view, question_view, add_comment, add_answer, logout_view, error_view
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [ 
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('accounts/login/', login_view, name='login'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'), 
    path('profile/', profile_view, name="profile"),
    path('logout/', logout_view, name='logout_view'),
    path('questions/', question_view, name='question_view'),
    path('add_comment/<int:question_id>/', add_comment, name='add_comment'),
    path('add_answer/<int:question_id>/', add_answer, name='add_answer'),
    path('error/', error_view, name='error_view'),  # For handling specific error codes
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
