from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from unfold.contrib.filters.admin import ChoicesDropdownFilter, RelatedDropdownFilter
from unfold.contrib.filters.admin import RangeNumericListFilter, RangeNumericFilter
from unfold.contrib.filters.admin import SingleNumericFilter, SliderNumericFilter


class GenericChoicesDropdownFilter(ChoicesDropdownFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field
        super().__init__(field, request, params, model, model_admin, field_path)


class GenericRelatedDropdownFilter(RelatedDropdownFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.field_name = field
        super().__init__(field, request, params, model, model_admin, field_path)


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
