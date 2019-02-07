from django.shortcuts import render
from rango.models import Category,Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime

# Templates can be seen as scaffolding

# Create your views here.

def index(request):  # The view itself
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request, 'rango/index.html', context=context_dict)
    return response

def about(request):
    context_dict = {'boldmessage': "Rango says this is the about page!"}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

    response = render(request,'rango/about.html',context_dict)

    return response

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request,'rango/category.html',context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    # HTTP Post?

    if request.method == 'POST':
        form = CategoryForm(request.POST)

    if form.is_valid():
        form.save(commit=True)
        return index(request)

    else:
        print(form.errors)

    return render(request,'rango/add_category.html',{'form':form})

@login_required
def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request,category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form':form,'category':category}
    return render(request,'rango/add_page.html',context_dict)

def register(request):
    # Was registration successful? To start, no!
    registered = False

    if request.method=='POST':
        # Grab RAW information from form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save information
            user = user_form.save()

            # Hash the password, then update user object
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # Did user provide profile picture? If so, get it from input form and put it in the user profile
            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']

            # Save the profile and confirm successful registration
            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
        'rango/register.html',
        {'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered})


def user_login(request):
    # Get user provided information (username and password)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # use django the check if valid
        user = authenticate(username=username, password=password)

        # If user object exists, details are correct
        if user:
            # is the account active?
            if user.is_active:
                # if account is valid and active, log in
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                # if account is disabled, can't login
                return HttpResponse("Your rango account is disabled")

        else:
            # bad login details, can't log user in
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")      

    else:
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request,'rango/restricted.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def get_server_side_cookie(request,cookie, default_val=None):
    val = request.session_get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # get number of visits to site
    # if exists, return the value, else return default value of 1
    visits = int(request.COOKIES.get('visits','1'))

    last_visit_cookie = request.COOKIES.get('last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')

    # if it's been more than a day since last visit
    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update the last cookie with the current count
        request.session['last_visit'] = str(datetime.now())

    else:
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
    # update/set the visits cookie
    request.session['visits'] = visits