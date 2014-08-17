import datetime
from haystack import indexes
from bands.models import Band


class BandIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document = True, use_template = True)
    name = indexes.CharField(model_attr = 'name')
    description = indexes.CharField(model_attr = 'description')
    content_auto = indexes.EdgeNgramField(model_attr = 'name')
    
    def get_model(self):
        return Band
    def index_queryset(self, using= None):
        return self.get_model().objects.all()
    
