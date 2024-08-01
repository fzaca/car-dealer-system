from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class AutocompleteDropdownFilter(admin.SimpleListFilter):
    template = 'admin/filter_autocomplete.html'  # Asegúrate de tener esta plantilla

    def __init__(self, request, params, model, model_admin, field_name, title=None):
        self.parameter_name = field_name
        self.title = title or _(f"{field_name} Autocomplete Filter")
        self.field_name = field_name
        super().__init__(request, params, model, model_admin)

    def lookups(self, request, model_admin):
        return (
            (str(value), str(value))
            for value in model_admin.model.objects.values_list(self.field_name, flat=True).distinct()
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.field_name: self.value()})
        return queryset


def create_autocomplete_filter(field_name, title=None):
    """
    Factory function to create a specific autocomplete filter for a given field name.
    """
    class SpecificAutocompleteDropdownFilter(AutocompleteDropdownFilter):
        def __init__(self, request, params, model, model_admin):
            super().__init__(request, params, model, model_admin, field_name, title)

    return SpecificAutocompleteDropdownFilter
