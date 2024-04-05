from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book
from .forms import BookForm, LoginForm, RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                # Handle case where username already exists
                return render(request, 'library/register.html', {'form': form, 'error_message': 'Username already exists.'})
            else:
                # Create new user
                user = User.objects.create_user(username=username, password=password)
                login(request, user)  # Log in the newly created user
                return redirect('book_list')
        else:
            # Form validation failed, render form with errors
            return render(request, 'library/register.html', {'form': form})
    else:
        form = RegistrationForm()
        # Render registration form
        return render(request, 'library/register.html', {'form': form})
    
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('book_list') 
        else:
            # Login failed
            error_message = 'Invalid username or password'
            form = LoginForm()  # Create form instance to display
            return render(request, 'library/login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'library/login.html', {'form': form})

@login_required
def logout_user(request):
    logout(request)
    form = LoginForm()
    return render(request, 'library/login.html', {'form': form})


@login_required
def book_list(request):
    books = Book.objects.filter(user=request.user)  # Filter by user

    # Handle filtering logic
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET['q']
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))  # Search by title or author

    context = {'books': books}
    return render(request, 'library/book_list.html', context)

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)  # Create form with submitted data
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'library/book_form.html', {'form': form})

@login_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'library/book_form.html', {'form': form, 'book': book})

@login_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'library/book_delete_confirm.html', {'book': book})