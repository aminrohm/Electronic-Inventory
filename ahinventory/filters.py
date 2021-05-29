from .models import Item
from mptt.forms import TreeNodeChoiceField
import django_filters

class ItemFilter(django_filters.FilterSet):
    class Meta:
        model = Item
        fields = ['namevalue', 'category', 'storelocation', ]

class TreeNodeChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = TreeNodeChoiceField

    def filter(self, qs, value):
        if value != self.null_value:
            return self.get_method(qs)(**{f'{self.field_name}__in': value.get_descendants(include_self=True)})

        return qs.distinct() if self.distinct else qs
