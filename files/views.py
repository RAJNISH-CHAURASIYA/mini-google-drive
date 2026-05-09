from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UploadedFile, ShareLink, ActivityLog, Folder


# ---------------- HOME ----------------
def home(request):
    return render(request, 'home.html')


# ---------------- DASHBOARD ----------------
@login_required(login_url='login')
def dashboard(request):
    folders = Folder.objects.filter(user=request.user)
    files = UploadedFile.objects.filter(user=request.user, in_trash=False)

    # Upload from dashboard
    if request.method == 'POST' and request.FILES.get('file'):
        UploadedFile.objects.create(
            user=request.user,
            file=request.FILES['file']
        )

        ActivityLog.objects.create(
            user=request.user,
            action="Uploaded a file"
        )

        return redirect('/dashboard/')

    return render(request, 'dashboard.html', {
        'folders': folders,
        'files': files
    })


# ---------------- CREATE FOLDER ----------------
@login_required(login_url='login')
def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        if folder_name:
            Folder.objects.create(
                user=request.user,
                name=folder_name
            )

            ActivityLog.objects.create(
                user=request.user,
                action=f"Created folder {folder_name}"
            )

    return redirect('/dashboard/')


# ---------------- OPEN FOLDER ----------------
@login_required(login_url='login')
def open_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)
    files = UploadedFile.objects.filter(folder=folder, in_trash=False)

    # upload inside folder
    if request.method == 'POST' and request.FILES.get('file'):
        UploadedFile.objects.create(
            user=request.user,
            folder=folder,
            file=request.FILES['file']
        )

        ActivityLog.objects.create(
            user=request.user,
            action=f"Uploaded file in folder {folder.name}"
        )

        return redirect(request.path)

    return render(request, 'folder.html', {
        'folder': folder,
        'files': files
    })


# ---------------- MY FILES ----------------
@login_required(login_url='login')
def my_files(request):
    files = UploadedFile.objects.filter(user=request.user, in_trash=False)
    return render(request, 'my_files.html', {'files': files})


# ---------------- MOVE TO TRASH ----------------
@login_required(login_url='login')
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    file.in_trash = True
    file.save()

    ActivityLog.objects.create(
        user=request.user,
        action="Moved a file to Trash"
    )

    return redirect('my_files')


# ---------------- SHARE FILE ----------------
@login_required(login_url='login')
def share_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    share, _ = ShareLink.objects.get_or_create(file=file)

    ActivityLog.objects.create(
        user=request.user,
        action="Shared a file"
    )

    share_url = request.build_absolute_uri(f'/share/{share.token}/')
    return render(request, 'share.html', {'share_url': share_url})


# ---------------- SHARED DOWNLOAD ----------------
def shared_download(request, token):
    share = get_object_or_404(ShareLink, token=token)
    return redirect(share.file.file.url)


# ---------------- TRASH ----------------
@login_required(login_url='login')
def trash(request):
    files = UploadedFile.objects.filter(user=request.user, in_trash=True)
    return render(request, 'trash.html', {'files': files})


# ---------------- RESTORE FILE ----------------
@login_required(login_url='login')
def restore_file(request, file_id):
    file = get_object_or_404(
        UploadedFile,
        id=file_id,
        user=request.user,
        in_trash=True
    )
    file.in_trash = False
    file.save()

    ActivityLog.objects.create(
        user=request.user,
        action="Restored file from Trash"
    )

    return redirect('trash')


# ---------------- PERMANENT DELETE ----------------
@login_required(login_url='login')
def permanent_delete_file(request, file_id):
    file = get_object_or_404(
        UploadedFile,
        id=file_id,
        user=request.user,
        in_trash=True
    )
    file.file.delete()
    file.delete()

    ActivityLog.objects.create(
        user=request.user,
        action="Permanently deleted a file"
    )

    return redirect('trash')


# ---------------- ACTIVITY LOG ----------------
@login_required(login_url='login')
def activity_log(request):
    logs = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'activity_log.html', {'logs': logs})
@login_required(login_url='login')
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    # files ko root me move kar do (safe delete)
    UploadedFile.objects.filter(folder=folder).update(folder=None)

    folder_name = folder.name
    folder.delete()

    ActivityLog.objects.create(
        user=request.user,
        action=f"Deleted folder {folder_name}"
    )

    return redirect('/dashboard/')

#---------------- rename folder ----------------
@login_required(login_url='login')
def rename_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            old_name = folder.name
            folder.name = new_name
            folder.save()

            ActivityLog.objects.create(
                user=request.user,
                action=f"Renamed folder from {old_name} to {new_name}"
            )

    return redirect('/dashboard/')
#---------------- rename file ----------------
@login_required(login_url='login')
def rename_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        if new_name:
            folder.name = new_name
            folder.save()

            ActivityLog.objects.create(
                user=request.user,
                action=f"Renamed folder to {new_name}"
            )

            return redirect('/dashboard/')

    return render(request, 'rename_folder.html', {'folder': folder})
#---------------- move file to folder ----------------
@login_required(login_url='login')
def move_file_to_folder(request, file_id, folder_id):
    file = get_object_or_404(UploadedFile, id=file_id, user=request.user)
    folder = get_object_or_404(Folder, id=folder_id, user=request.user)

    file.folder = folder
    file.save()

    ActivityLog.objects.create(
        user=request.user,
        action=f"Moved file to folder {folder.name}"
    )

    return redirect('my_files')
@login_required(login_url='login')
def delete_activity(request, log_id):
    log = get_object_or_404(ActivityLog, id=log_id, user=request.user)
    log.delete()
    return redirect('/activity/')


