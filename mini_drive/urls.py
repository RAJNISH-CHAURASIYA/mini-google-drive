from django.contrib import admin
from django.urls import path, include
from files.views import (
    home,
    dashboard,
    my_files,
    delete_file,
    share_file,
    shared_download,
    trash,
    restore_file,
    permanent_delete_file,
    activity_log,
    create_folder,
    open_folder
)

from django.conf import settings
from django.conf.urls.static import static
from files.views import restore_file, permanent_delete_file
from files.views import trash
from files.views import activity_log
from files.views import create_folder
from files.views import delete_folder
from files.views import rename_folder
from files.views import move_file_to_folder
from files import views






   

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('files.urls')),   
    path('', include('accounts.urls')),

    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
   

    path('my-files/', my_files, name='my_files'),
    path('delete/<int:file_id>/', delete_file, name='delete_file'),

    path('trash/', trash, name='trash'),
    path('restore/<int:file_id>/', restore_file, name='restore_file'),
    path('permanent-delete/<int:file_id>/', permanent_delete_file, name='permanent_delete'),

    path('share/<int:file_id>/', share_file, name='share_file'),
    path('share/<uuid:token>/', shared_download, name='shared_download'),

    path('activity/', activity_log, name='activity'),

    path('create-folder/', create_folder, name='create_folder'),
    path('folder/<int:folder_id>/', open_folder, name='open_folder'),

    path('accounts/', include('accounts.urls')),
    
    path('folder-delete/<int:folder_id>/', delete_folder, name='delete_folder'),
    path('folder-rename/<int:folder_id>/', rename_folder, name='rename_folder'),

    
    path('move-file/<int:file_id>/', move_file_to_folder, name='move_file_to_folder'),  
    path('activity-delete/<int:log_id>/', views.delete_activity, name='delete_activity'),

]

# MEDIA files (uploads) serve karne ke liye
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
