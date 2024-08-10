from rest_framework import pagination


class NoPagination(pagination.PageNumberPagination):
    """Disables pagination, returns all objects."""

    def paginate_queryset(self, queryset, request, view=None):
        return None
