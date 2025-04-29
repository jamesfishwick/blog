from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags
import markdown
from django.utils.html import mark_safe
from django.urls import reverse

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})

class BaseEntry(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique_for_date='created')
    tags = models.ManyToManyField(Tag, blank=True)
    is_draft = models.BooleanField(
        default=False,
        help_text="Draft entries do not show in index pages but can be visited directly if you know the URL",
    )

    class Meta:
        abstract = True
        ordering = ['-created']

    def __str__(self):
        return self.title

class Entry(BaseEntry):
    summary = models.TextField()
    body = models.TextField()
    card_image = models.URLField(
        blank=True, null=True, help_text="URL to image for social media cards"
    )
    authors = models.ManyToManyField(User, through="Authorship", blank=True)

    class Meta:
        verbose_name_plural = "entries"
        ordering = ['-created']

    @property
    def summary_rendered(self):
        return mark_safe(markdown.markdown(self.summary, output_format="html5"))

    @property
    def summary_text(self):
        return strip_tags(markdown.markdown(self.summary, output_format="html5"))

    @property
    def body_rendered(self):
        return mark_safe(markdown.markdown(self.body, output_format="html5"))

    def get_absolute_url(self):
        return reverse('blog:entry', kwargs={
            'year': self.created.year,
            'month': self.created.strftime('%b').lower(),
            'day': self.created.day,
            'slug': self.slug
        })

class Authorship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "authorships"

class Blogmark(BaseEntry):
    """Link blog implementation similar to Simon's 'blogmarks'"""
    url = models.URLField()
    commentary = models.TextField()
    via = models.URLField(blank=True, null=True, help_text="URL of where you found the link")
    via_title = models.CharField(max_length=200, blank=True, null=True, help_text="Title of where you found the link")

    @property
    def commentary_rendered(self):
        return mark_safe(markdown.markdown(self.commentary, output_format="html5"))

    def get_absolute_url(self):
        return reverse('blog:blogmark', kwargs={
            'year': self.created.year,
            'month': self.created.strftime('%b').lower(),
            'day': self.created.day,
            'slug': self.slug
        })
