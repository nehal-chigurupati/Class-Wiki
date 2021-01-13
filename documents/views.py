from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import DocumentForm


def document_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.uploaded_by = request.user
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'document_upload_form.html', {'form': form})
