
from haystack import indexes
from shop.models import Shop,Product,Collection




class ShopIndex(indexes.SearchIndex, indexes.Indexable):
    text               = indexes.CharField(document=True, use_template=True)
    name               = indexes.CharField(model_attr='name')
    autocomplete       = indexes.EdgeNgramField(model_attr='name')
    
    @staticmethod
    def prepare_autocomplete(obj):
    	return " ".join((
    		obj.name, obj.keywords
    		)) 
    def get_model(self):
        return Shop
    def index_queryset(self, using=None):
    	'''Used when the entire index for model is updated.'''
        return self.get_model().objects.all()

    def get_model(self):
        return Shop

class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text           = indexes.CharField(document=True, use_template=True)
    name           = indexes.CharField(model_attr='name')
    language       = indexes.CharField(model_attr='language')

    autocomplete = indexes.EdgeNgramField(model_attr='name')

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.name, obj.keywords
            )) 
    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        '''Used when the entire index for model is updated.'''
        return self.get_model().objects.all()

    def get_model(self):
        return Product

class CollectionIndex(indexes.SearchIndex, indexes.Indexable):
    text           = indexes.CharField(document=True, use_template=True)
    name           = indexes.CharField(model_attr='name')
    language       = indexes.CharField(model_attr='language')
    
    autocomplete = indexes.EdgeNgramField(model_attr='name')

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((
            obj.name, obj.keywords
            )) 
    def get_model(self):
        return Collection

    def index_queryset(self, using=None):
        '''Used when the entire index for model is updated.'''
        return self.get_model().objects.all()

    def get_model(self):
        return Collection






