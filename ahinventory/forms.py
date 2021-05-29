from django import forms
from mptt.forms import TreeNodeChoiceField
from .models import Category,StorageLocation,Item
from django.core.exceptions import ValidationError
from .fields import ListTextWidget

class SearchForm(forms.Form):
    namevalue = forms.CharField(max_length=50,required=False)
    category = TreeNodeChoiceField(queryset=Category.objects.all(),required=False)
    #location = forms.ModelChoiceField(queryset=StorageLocation.objects.all(),required=False)
    location = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        namevalue = bool(cleaned_data.get("namevalue",False))
        category = bool(cleaned_data.get("category",False))
        location = bool(cleaned_data.get("location",False))
        if not( namevalue ^ category ^ location) :
            raise ValidationError(
              "Input only one field")
              
    def __init__(self,*args,**kwargs):
        _location_list = kwargs.pop('data_list', None)
        super(SearchForm, self).__init__(*args, **kwargs)

    # the "name" parameter will allow you to use the same widget more than once in the same
    # form, not setting this parameter differently will cuse all inputs display the
    # same list.
        self.fields['location'].widget = ListTextWidget(data_list=_location_list, name='location-list')



# class InputForm(forms.Form):
    # namevalue = forms.CharField(max_length=50,required=False)
    # category = TreeNodeChoiceField(queryset=Category.objects.all(),required=False)
    # location = forms.ModelChoiceField(queryset=StorageLocation.objects.all(),required=False)
    
    # def clean(self):
        # cleaned_data = super().clean()
        # namevalue = bool(cleaned_data.get("namevalue",False))
        # category = bool(cleaned_data.get("category",False))
        # location = bool(cleaned_data.get("location",False))
        # if not( namevalue and category and location) :
            # raise ValidationError(
              # "Input all fields")

class InputForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = "__all__"



