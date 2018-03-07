"""blog admin settings"""
from django.contrib import admin
from .models import (Article,
                     Author)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('publication_date',
                    'title')
    fields = ('publication_date',
              'title',
              'content',
              'author',
              'expiration_date')

    def queryset(self,
                 request):
        qs = super().queryset(request)
        qs.author.queryset = Author.objects.filter(user=request.user)
        return qs


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Article,
                    ArticleAdmin)
admin.site.register(Author,
                    AuthorAdmin)
