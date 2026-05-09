from django.urls import path
from .views import (
    dashboard,
    open_folder,
    create_folder,
    delete_file,
    share_file,
    trash,
    activity_log,
)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),

    # 📁 Folder
    path('create-folder/', create_folder, name='create_folder'),
    path('folder/<int:folder_id>/', open_folder, name='open_folder'),

    # 📄 File actions
    path('delete/<int:file_id>/', delete_file, name='delete_file'),
    path('share/<int:file_id>/', share_file, name='share_file'),

    # 🗑 Trash & Activity
    path('trash/', trash, name='trash'),
    path('activity/', activity_log, name='activity_log'),


]
