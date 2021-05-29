from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import StorageLocation,Item,Category
from django.urls import reverse_lazy
from .filters import ItemFilter,TreeNodeChoiceFilter
from django.shortcuts import render
from .forms import SearchForm,InputForm
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.http import HttpResponse


class StorageLocationList(ListView):
    model = StorageLocation


class StorageLocationCreate(CreateView):
    model = StorageLocation
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ahinventory:storagelocation-list')
    
    
    def get_success_url(self):
        print("get success url ",self.request.POST)
        if "another" in self.request.POST:
            print("ini self request..",self.request.POST)
            return reverse_lazy('ahinventory:storagelocation-add')
        return  super().get_success_url()
        
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        print("ini context",context)
        context['storage'] = StorageLocation.objects.all()
        return context
        
        
class StorageLocationUpdate(UpdateView):
    model = StorageLocation
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ahinventory:storagelocation-list')
    
class StorageLocationDelete(DeleteView):
    model = StorageLocation
    success_url = reverse_lazy('ahinventory:storagelocation-list')


class ItemList(ListView):
    model = Item

class ItemCreate(CreateView):
    model = Item
    fields = '__all__'
    template_name_suffix = '_create_form'
    success_url = reverse_lazy('ahinventory:item-add')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['storage'] = StorageLocation.objects.all()
        return context
    
class ItemUpdate(UpdateView):
    model = Item
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ahinventory:home')

class ItemDelete(DeleteView):
    model = Item
    success_url = reverse_lazy('ahinventory:home')
    


class CategoryList(ListView):
    model = Category
    
class CategoryCreate(CreateView):
    model = Category
    template_name_suffix = '_create_form'
    fields = '__all__'
    success_url = reverse_lazy('ahinventory:category-list')
    
    def get_success_url(self):
        if "another" in self.request.POST:
            return reverse_lazy('ahinventory:category-add')
        return  super().get_success_url()
        
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class CategoryUpdate(UpdateView):
    model = Category
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('ahinventory:category-list')

class CategoryDelete(DeleteView):
    model = Category
    success_url = reverse_lazy('ahinventory:category-list')


class HomeView(TemplateView):
    template_name = 'ahinventoryhome.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['search_form'] = SearchForm()
        context['input_form'] = InputForm()
        context['storage'] = StorageLocation.objects.all()
        return context
        
    def get(self,request,*args,**kwargs):
        item_filter=[]
        location_list = StorageLocation.objects.all()
        search_form = SearchForm(data_list=location_list)
        input_form = InputForm()
        category =False
        item = False
        location=False
        search_flag = False
        search_form=SearchForm()
        query_category = request.GET.get('category',None)
        query_name = request.GET.get('namevalue',None)
        query_location = request.GET.get('location',None)
        if query_category and not query_name and not query_location:
            item_filter = Category.objects.get(pk=query_category).get_descendants(include_self=True)
            search_form = SearchForm(request.GET or None)
            category = True
            search_flag = True
            return render(request,self.template_name, {'filter': item_filter,'search_form':search_form,'input_form':input_form,'category':category})
        elif query_name and not query_category and not query_location:
            item_filter = Item.objects.filter(namevalue__contains=query_name)
            search_form = SearchForm(request.GET or None)
            item = True
            search_flag = True
            return render(request, self.template_name, {'filter': item_filter,'search_form':search_form,'input_form':input_form,'item':item,'search_flag':search_flag})
        elif query_location and not query_name and not query_category:
            item_filter =StorageLocation.objects.filter(location=query_location)    # This need to be changed
            search_form = SearchForm(request.GET or None,data_list=location_list)
            location = True
            search_flag = True
            return render(request,self.template_name, {'filter': item_filter,'search_form':search_form,'input_form':input_form,'location':location,'search_flag':search_flag})
        else:
            search_form = SearchForm()
            search_warning = True
            return render(request,self.template_name,{'search_form':search_form,'input_form':input_form,'search_warning':search_warning})
        

    def post(self,request,*args,**kwargs):
        set_category = request.POST.get('category',None)
        set_namevalue = request.POST.get('namevalue',None)
        set_location = request.POST.get('storelocation',None)
        set_quantity = request.POST.get('quantity',None)
        input_form = InputForm(request.POST or None)
        search_form = SearchForm()
        input_flag = False
        input_warning = False
        storage = StorageLocation.objects.all()
        if set_category and set_namevalue and set_location and set_quantity:
            set_item = Item.objects.create(namevalue=set_namevalue,category=Category.objects.get(pk=set_category),storelocation=StorageLocation.objects.get(pk=set_location),quantity=set_quantity)
            input_flag = True
            return render(request, self.template_name, {'input_form':input_form,'search_form':search_form,'storage':storage,'input_flag':input_flag})
        else:
            input_form = InputForm()
            input_warning = True
            return render(request,self.template_name,{'input_form':input_form,'search_form':search_form,'input_warning':input_warning})


    
