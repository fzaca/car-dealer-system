from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import (
    ChoicesDropdownFilter,
    RelatedDropdownFilter,
    DropdownFilter,
    RangeNumericListFilter,
    RangeNumericFilter,
    SingleNumericFilter,
    SliderNumericFilter,
)


class GenericChoicesDropdownFilter(ChoicesDropdownFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field
        super().__init__(field, request, params, model, model_admin, field_path)


class GenericRelatedDropdownFilter(RelatedDropdownFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field
        super().__init__(field, request, params, model, model_admin, field_path)


class GenericCustomDropdownFilter(DropdownFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field
        self.title = _(f"Custom dropdown filter for {field}")
        self.parameter_name = f"custom_{field}"
        super().__init__(field, request, params, model, model_admin, field_path)

    def lookups(self, request, model_admin):
        return [
            ["option_1", _("Option 1")],
            ["option_2", _("Option 2")],
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(**{self.field_name: self.value()})
        return queryset


class GenericSingleNumericFilter(SingleNumericFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field
        super().__init__(field, request, params, model, model_admin, field_path)


class GenericRangeNumericFilter(RangeNumericFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field
        super().__init__(field, request, params, model, model_admin, field_path)


class GenericSliderNumericFilter(SliderNumericFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field
        super().__init__(field, request, params, model, model_admin, field_path)


class GenericRangeNumericListFilter(RangeNumericListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field
        self.parameter_name = f"{field}_count"
        self.title = _(f"{field} count")
        super().__init__(field, request, params, model, model_admin, field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            validated_data = dict(self.form.cleaned_data.items())
            if validated_data:
                return queryset.annotate(**{self.parameter_name: Count(self.field_name, distinct=True)}).filter(
                    **{f"{self.parameter_name}__range": (validated_data.get("from"), validated_data.get("to"))}
                )
        return queryset
