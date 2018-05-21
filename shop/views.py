#!/usr/bin/python
# -*- coding: utf-8 -*-



from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from shop.models import Shop,Product,Collection
from shop.serializers import SearchSerializer
from drf_haystack.viewsets import HaystackViewSet
from drf_haystack.filters import HaystackAutocompleteFilter



#@csrf_exempt
#@permission_classes((AllowAny,))
class ShopSearchView(HaystackViewSet):
    serializer_class = SearchSerializer
    filter_backends = [HaystackAutocompleteFilter]
    index_models = [Shop,Product,Collection]
    #permission_classes = [AllowAny,]

    def __name__(self):
        return "ShopSearchView"





