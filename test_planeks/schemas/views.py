from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth import login, logout
from faker import Faker
import csv
import os
import datetime
import random

from .forms import LoginUserForm, RegisterUserForm, CreateSchemaForm, CreateColumnForm
from .utils import *
from .models import Schema, Column


def home(request):

    return render(request, 'home.html')



def schemas(request):
    col_exist = []
    if request.user.is_authenticated:
        schemas = Schema.objects.all().filter(owner=request.user.id)

        for x in schemas:
            print(x.id, x.all_column)
            columns = Column.objects.all().filter(schema_id=x.id)
            if columns:
                col_exist.append(x.title)

                x.save()

            if not os.path.exists('/media/' + x.file_name):
                x.file_exists = False
                x.save()


        for x in schemas:

            file_name = x.file_name
            path = 'media/' + file_name

            if os.path.exists(path):
                x.file_exists = True
                x.save()


        return render(request, 'all_schemas.html', {'schemas': schemas, 'col_exist': col_exist})
    else:
        return redirect('home')

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
            delimiter = form.cleaned_data['delimiter']
            schema = Schema(title=title, owner=owner, delimiter=delimiter)


            if schema:
                schema.save()

            return redirect('/schemas/')

    return render(request, 'new_schema.html', {'form': form})


class UpdateSchemaView(UpdateView):
    model = Schema
    template_name = 'update_schema.html'

    form_class = CreateSchemaForm
    success_url = '/schemas'

class DeleteSchemaView(DeleteView):
    model = Schema
    template_name = 'delete_schema.html'
    success_url = '/schemas'


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
        form = CreateColumnForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data['title']
            order = form.cleaned_data['order']
            order_right = order + schema.id
            type = form.cleaned_data['type']
            new_column = Column(title=title, schema=schema, type=type, order=order_right)
            if new_column:
                new_column.save()
                schema.all_column = True


    return render(request, 'single_schema.html', {'schema': schema, 'form': form, 'columns': columns})


class UpdateColumnView(UpdateView):
    model = Column
    template_name = 'update_column.html'

    form_class = CreateColumnForm


class DeleteColumnView(DeleteView):
    model = Column
    template_name = 'delete_column.html'
    schema_id = model.schema_id
    # schema = Schema.objects.filter(id=schema_id)
    # schema.all_column.pop()
    # schema.save()
    success_url = '/schema/{schema_id}'


def make_csv(request, id=None):
    try:
        schema = Schema.objects.get(id=id)
    except Exception as e:
        raise e

    try:
        columns = Column.objects.filter(schema_id=schema.id)
    except Exception as e:
        raise e

    if request.POST:
        sort_columns = sorted(columns, key=lambda x: x.order)
        fake = Faker()
        columns_names = []
        count_rows = int(request.POST.get('count'))

        for x in columns:
            columns_names.append(x.title)

        last_fake = []
        for i in range(count_rows):

            fake_data_by_schema = []

            for x in sort_columns:

                if x.type == 'Name':
                    fake_data_by_schema.append(fake.name())
                elif x.type == 'Company':
                    fake_data_by_schema.append(fake.company())
                elif x.type == 'Address':
                    fake_data_by_schema.append(fake.address())
                elif x.type == 'E-mail':
                    fake_data_by_schema.append(fake.safe_email())
                elif x.type == 'Age':
                    fake_data_by_schema.append(random.randint(18, 64))
                elif x.type == 'Phone number':
                    fake_data_by_schema.append(fake.phone_number())
            last_fake.append(fake_data_by_schema)

        date_title_file = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = 'media/' + schema.title + '_' + date_title_file + '.csv'
        file_name = schema.title + '_' + date_title_file + '.csv'
        schema.file_name = file_name
        schema.save()
        print(path)
        print(schema.file_name)
        with open(path, mode='w') as w_file:
            delimiter = schema.delimiter
            file_writer = csv.writer(w_file, delimiter=delimiter)
            file_writer.writerow(columns_names)
            file_writer.writerows(last_fake)



        return redirect('/schemas/')
    return render(request, 'create_csv.html', {'schema': schema, 'column': columns})

def downloadFile(request, pk=None):
    schema = Schema.objects.get(id=pk)
    print(schema.id)
    path = 'media/' + schema.file_name
    print(path)
    response = FileResponse(open(path,'rb'))
    return response

