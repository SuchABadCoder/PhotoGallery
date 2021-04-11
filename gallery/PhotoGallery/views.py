from django.shortcuts import render, redirect
from .models import Category, Photo


def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name=category)

    categories = Category.objects.all()

    context = {'categories': categories, 'photos': photos}
    return render(request, 'PhotoGallery/gallery.html', context)


def addPhoto(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['new_category'] != '':
            category, created = Category.objects.get_or_create(name=data['new_category'])
        else:
            category = None

        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image
        )

        return redirect('gallery')
    context = {'categories': categories}
    return render(request, 'PhotoGallery/add.html', context)


def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'PhotoGallery/photo.html', {'photo': photo})