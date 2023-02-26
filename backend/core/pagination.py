# -*- coding: utf-8 -*-
from rest_framework import pagination
from rest_framework.response import Response


class PageNumberPagination(pagination.PageNumberPagination):
    """
    Custom pagination
    """

    def get_paginated_response(self, data):
        """
        Return custom paginated response
        """
        return Response(
            {
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "page": int(
                    self.get_page_number(self.request, self.django_paginator_class)
                ),
                "page_size": int(self.page_size),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
