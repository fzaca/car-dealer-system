from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import DropdownFilter


class GearboxDropdownFilter(DropdownFilter):
    title = _("Gearbox")
    parameter_name = "gearbox"

    def lookups(self, request, model_admin):
        gearboxes = model_admin.model.objects.values_list('gearbox', flat=True).distinct()
        return [(gearbox, gearbox) for gearbox in gearboxes]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(gearbox=self.value())
        return queryset


class FuelTypeDropdownFilter(DropdownFilter):
    title = _("Fuel Type")
    parameter_name = "fuel_type"

    def lookups(self, request, model_admin):
        fuel_types = model_admin.model.objects.values_list('fuel_type', flat=True).distinct()
        return [(fuel_type, fuel_type) for fuel_type in fuel_types]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(fuel_type=self.value())
        return queryset
