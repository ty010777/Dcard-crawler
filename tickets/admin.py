from django.contrib import admin
from .models import CrawledData #, Topic

# Register your models here.
# class CrawledDataInline(admin.StackedInline):
#     model = Topic

class CrawledAdmin(admin.ModelAdmin):
    list_display = ('num','cTitle', 'cForumAlias','cForumName', 'cCommentCount','cLikeCount','cExcerpt',"cTag",'link','img')
    list_filter=('num',)
    search_fields=('cTitle','cTag')
    # inlines = [
    #     CrawledDataInline,
    # ]
    ordering=('cLikeCount',)


admin.site.register(CrawledData, CrawledAdmin)