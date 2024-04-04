from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Book
from .forms import BookForm, LoginForm, RegistrationForm

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        return redirect('library/login')
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
  else:
    form = LoginForm()
  return render(request, 'library/login.html', {'form': form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('library/login')

def home(request):
    return render(request, 'library/home.html')

@login_required
def book_list(request):
    books = Book.objects.filter(user=request.user)  # Filter by user

    # Handle filtering logic
    if request.method == 'GET' and 'q' in request.GET:
        query = request.GET['q']
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))  # Search by title or author

    context = {'books': books}
    print("this is the print statement")
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