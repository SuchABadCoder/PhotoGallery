from django.shortcuts import render, redirect
from .models import Category, Photo, User
from django.db.models import Count

def gallery(request):
    global category
    category = request.GET.get('category')

    if category == None:
        photos = Photo.objects.all()
    elif category == "Rate":
        photos = Photo.objects.all().annotate(num_likes=Count('likes')).order_by('-num_likes')
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

        Photo.objects.create(
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


def likePhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    liked = 'Like'
    print(User.id)
    if request.user.is_authenticated:
        if photo.likes.filter(id=request.user.id).exists():
            photo.likes.remove(request.user)
            liked = 'Like'
        else:
            liked = 'Unlike'
            photo.likes.add(request.user)
    try:
        if category == None:
            photos = Photo.objects.all()
        elif category == "Rate":
            photos = Photo.objects.all().annotate(num_likes=Count('likes')).order_by('-num_likes')
        else:
            photos = Photo.objects.filter(category__name=category)
    except NameError:
        photos = Photo.objects.all()

    categories = Category.objects.all()

    context = {'categories': categories, 'photos': photos, 'liked': liked}

    return render(request, 'PhotoGallery/gallery.html', context)
