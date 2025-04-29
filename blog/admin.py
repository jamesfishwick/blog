from django.contrib import admin
from .models import Tag, Entry, Authorship, Blogmark

class AuthorshipInline(admin.TabularInline):
    model = Authorship
    extra = 1

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'is_draft')
    list_filter = ('is_draft', 'created', 'tags')
    search_fields = ('title', 'summary', 'body')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    inlines = [AuthorshipInline]
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'summary', 'body', 'created')
        }),
        ('Publishing', {
            'fields': ('is_draft', 'tags', 'card_image')
        }),
    )

@admin.register(Blogmark)
class BlogmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created', 'is_draft')
    list_filter = ('is_draft', 'created', 'tags')
    search_fields = ('title', 'commentary', 'url')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created'
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'url', 'commentary', 'created')
        }),
        ('Publishing', {
            'fields': ('is_draft', 'tags')
        }),
        ('Via', {
            'fields': ('via', 'via_title'),
            'classes': ('collapse',)
        }),
    )
