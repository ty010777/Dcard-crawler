from django.contrib import admin
from .models import CrawledData #, Topic

# Register your models here.
# class CrawledDataInline(admin.StackedInline):
#     model = Topic

class CrawledAdmin(admin.ModelAdmin):
    list_display = ('cTitle', 'cForumAlias', 'cCommentCount','cLikeCount','cExcerpt','link','img')
    list_filter=('cTitle',)
    search_fields=('cTitle',)
    # inlines = [
    #     CrawledDataInline,
    # ]


admin.site.register(CrawledData, CrawledAdmin)