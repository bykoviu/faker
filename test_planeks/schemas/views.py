from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from faker import Faker
import csv



from .forms import LoginUserForm, RegisterUserForm, CreateSchemaForm, CreateColumnForm
from .utils import *
from .models import Schema, Column


def home(request):
    return render(request, 'home.html')
@login_required
def schemas(request):

    schemas = Schema.objects.all().filter(owner=request.user.id)
    return render(request, 'all_schemas.html', {'schemas': schemas})

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Main page")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="РђРІС‚РѕСЂРёР·Р°С†РёСЏ")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def create_schema(request, *args):
    form = CreateSchemaForm(request.GET)
    if request.method == 'POST':

        form = CreateSchemaForm(request.POST)


        if form.is_valid():

            title = form.cleaned_data['title']
            owner = request.user
            schema = Schema(title=title, owner=owner)

            if schema:
                schema.save()
            # Переход по адресу 'all-borrowed':
            return redirect('/schemas/')
    #shemas_column =
    return render(request, 'new_schema.html', {'form': form})

def single_schema(request, id=None):
    try:
        schema = Schema.objects.get(id=id)
    except Exception as e:
        raise e

    try:
        columns = Column.objects.filter(schema_id=schema.id)
    except Exception as e:
        raise e

    form = CreateColumnForm(request.GET)



    if request.method == 'POST':
        print('form is suka valid')
        form = CreateColumnForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data['title']
            # schema = request.schema
            order = form.cleaned_data['order']
            order_right = order + schema.id
            type = form.cleaned_data['type']
            new_column = Column(title=title, schema=schema, type=type, order=order_right)
            if new_column:
                new_column.save()

                    # return redirect('single-schema')
    sort_columns = sorted(columns, key=lambda x: x.order)
    print(sort_columns)
    list_order = []
    # for x in columns:
    #     list_order.append(x.title)
    #
    # print(list_order)


    fake = Faker()
    fake_data_by_schema = []


    for x in sort_columns:
        if x.type == 'n':
            fake_data_by_schema.append(fake.name())
        elif x.type == 'c':
            fake_data_by_schema.append(fake.company())
        elif x.type == 'a':
            fake_data_by_schema.append(fake.address())
        elif x.type == 'e':
            fake_data_by_schema.append(fake.safe_email())
    print(fake_data_by_schema )

    return render(request, 'single_schema.html', {'schema': schema, 'form': form, 'columns': columns})


class UpdateColumnView(UpdateView):
    model = Column
    template_name = 'update_column.html'


    form_class = CreateColumnForm


class DeleteColumnView(DeleteView):
    model = Column
    template_name = 'delete_column.html'
    schema_id = model.schema_id
    success_url = '/schema/{schema_id}'

def create_csv(request, id=None):
    try:
        schema = Schema.objects.get(id=id)
    except Exception as e:
        raise e

    try:
        columns = Column.objects.filter(schema_id=schema.id)
    except Exception as e:
        raise e

    sort_columns = sorted(columns, key=lambda x: x.order)
    print(sort_columns)
    list_order = []
    # for x in columns:
    #     list_order.append(x.title)
    #
    # print(list_order)

    fake = Faker()
    # fake_data_by_schema = []
    columns_names = []
    for x in columns:
        columns_names.append(x.title)

    last_fake = []
    for i in range(3):

        fake_data_by_schema = []

        for x in sort_columns:

            if x.type == 'n':
                fake_data_by_schema.append(fake.name())
            elif x.type == 'c':
                fake_data_by_schema.append(fake.company())
            elif x.type == 'a':
                fake_data_by_schema.append(fake.address())
            elif x.type == 'e':
                fake_data_by_schema.append(fake.safe_email())
        last_fake.append(fake_data_by_schema)




    with open('media/' + schema.title + 'new.csv', mode='w') as w_file:
        file_writer = csv.writer(w_file, delimiter=",")
        file_writer.writerow(columns_names)
        for x in last_fake:
            file_writer.writerow(x)

    print(last_fake)
    return render(request, 'create_csv.html', {'schema': schema, 'column': columns})

# title = form.cleaned_data['title']
#             schema = request.schema
#             type = form.cleaned_data['type']
#             order = form.cleaned_data['order']


# class LoginView(View):
#     def get(self, request, *args, **kwargs):
#         form = LoginForm(request.POST or None)
#         context = {'form': form,}
#         return render(request, 'login.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = LoginForm(request.POST or None)
#         if form.is_valid():
#             print(form.cleaned_data)
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 return HttpResponseRedirect('/')
#         return render(request, 'login.html', {'form': form})
#
# def reg(request):
#     form = RegisterForm(request.GET or None)
#     if request.method == 'POST':
#         form = RegisterForm(request.POST or None)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             user = User.objects.create_user(username, email, password)
#             if user:
#                 user.save()
#         # if request.method == 'POST':
#         #     print(str(request))
#         #     username = request.name
#         #     email = request.email
#         #     password = request.password
#         #     user = User.objects.create_user(username, email, password)
#         # #u = User.objects.get(username='bykoviu')
#         # #     # user_name = u.username
#         # #     # user_email = u.email
#         #
#         #
#         #     # request.username, request.email, request.password
#         #     if user:
#         #
#         #
#         #         # user.password = request.password1
#         #     #     user_name = user.username
#         #     #     user_last_name = user.last_name
#         #         user.save()
#         # #     print(user.username, user.email)
#                 return render(request, 'home.html')
#     return render(request, 'test.html', {'form': form})
# def log(request):
#
#     if request.method == 'POST':
#         form = LoginForm(request.POST or None)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             # user = User.objects.filter(username=username).get()
#             user = authenticate(username=username, password=password)
#
#             if user:
#                 if user.password == password:
#                     login(request, user)
#                     return render(request, 'home.html')
#             else:
#                 return render(request, 'register.html')
#     else:
#         form = LoginForm(request.GET or None)
#         return render(request, 'login.html', {'form': form})
#     return HttpResponseRedirect('/')
#                 # if request.method == 'POST':
#                 #     print(str(request))
#                 #     username = request.name
#                 #     email = request.email
#                 #     password = request.password
#                 #     user = User.objects.create_user(username, email, password)
#                 # #u = User.objects.get(username='bykoviu')
#                 # #     # user_name = u.username
#                 # #     # user_email = u.email
#                 #
#                 #
#                 #     # request.username, request.email, request.password
#                 #     if user:
#                 #
#                 #
#                 #         # user.password = request.password1
#                 #     #     user_name = user.username
#                 #     #     user_last_name = user.last_name
#                 #         user.save()
#                 # #     print(user.username, user.email)
