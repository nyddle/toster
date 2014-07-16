from haystack import indexes
from django.utils import timezone
from .models import Question

NoteIndex(indexes.SearchIndex, indexes.Indexable):
    #text = indexes.CharField(document=True, use_template=True)
    question = indexes.CharField(model_attr='question')
    details = indexes.CharField(model_attr='details')
    def get_model(self):
        return Question
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(timestamp__lte=timezone.now())