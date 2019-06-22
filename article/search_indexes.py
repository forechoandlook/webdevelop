from haystack import indexes
from .models import ArticlePost
# 对指定的某些类数据建立索引

class ArticleIndex(indexes.SearchIndex,indexes.Indexable):
	text = indexes.CharField(document=True,use_template=True)
	# 注意模板文件

#这一行用来干啥的？
	def get_model(self):
		return ArticlePost

	def index_queryset(self,using=None):
		return self.get_model().objects.all()
# 	
	def prepare_likeuser(self,obj):
		return [likeuser.name for likeuser in obj.likeuser.all()]

	def prepare_articletag(self,obj):
		return [articletag.tag for articletag in obj.articletags.all()]