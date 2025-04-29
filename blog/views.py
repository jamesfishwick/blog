from django.contrib.syndication.views import Feed
from django.shortcuts import render, get_object_or_404
from django.utils.feedgenerator import Atom1Feed
from django.db import models
from .models import Entry, Tag, Blogmark
from .utils import paginate_queryset
from .related import get_related_entries

ENTRIES_ON_HOMEPAGE = 5

def index(request):
    entries = list(
        Entry.objects.filter(is_draft=False).order_by("-created")[
            : ENTRIES_ON_HOMEPAGE + 1
        ]
    )
    blogmarks = list(
        Blogmark.objects.filter(is_draft=False).order_by("-created")[
            : ENTRIES_ON_HOMEPAGE
        ]
    )
    has_more = False
    if len(entries) > ENTRIES_ON_HOMEPAGE:
        has_more = True
        entries = entries[:ENTRIES_ON_HOMEPAGE]
    
    # Add reading time to entries
    for entry in entries:
        entry.reading_time = reading_time(entry.body)
    
    return render(
        request, 
        "blog/index.html", 
        {
            "entries": entries, 
            "blogmarks": blogmarks,
            "has_more": has_more
        }
    )

def entry(request, year, month, day, slug):
    entry = get_object_or_404(
        Entry, 
        created__year=year, 
        created__month=get_month_number(month),
        created__day=day,
        slug=slug
    )
    
    # Get related entries
    related_entries = get_related_entries(entry)
    
    return render(
        request,
        "blog/entry.html",
        {
            "entry": entry,
            "related_entries": related_entries
        },
    )

def blogmark(request, year, month, day, slug):
    blogmark = get_object_or_404(
        Blogmark, 
        created__year=year, 
        created__month=get_month_number(month),
        created__day=day,
        slug=slug
    )
    return render(
        request,
        "blog/blogmark.html",
        {"blogmark": blogmark},
    )

def year(request, year):
    entries = Entry.objects.filter(created__year=year, is_draft=False).order_by(
        "-created"
    )
    blogmarks = Blogmark.objects.filter(created__year=year, is_draft=False).order_by(
        "-created"
    )
    
    # Paginate entries
    paginated_entries = paginate_queryset(request, entries)
    
    return render(
        request, 
        "blog/year.html", 
        {
            "entries": paginated_entries,
            "blogmarks": blogmarks,
            "year": year,
            "page_obj": paginated_entries
        }
    )

def month(request, year, month):
    month_number = get_month_number(month)
    entries = Entry.objects.filter(
        created__year=year, 
        created__month=month_number,
        is_draft=False
    ).order_by("-created")
    blogmarks = Blogmark.objects.filter(
        created__year=year, 
        created__month=month_number,
        is_draft=False
    ).order_by("-created")
    
    # Paginate entries
    paginated_entries = paginate_queryset(request, entries)
    
    return render(
        request, 
        "blog/month.html", 
        {
            "entries": paginated_entries,
            "blogmarks": blogmarks,
            "year": year,
            "month": month,
            "month_name": get_month_name(month_number),
            "page_obj": paginated_entries
        }
    )

def archive(request):
    entries = Entry.objects.filter(is_draft=False).order_by("-created")
    blogmarks = Blogmark.objects.filter(is_draft=False).order_by("-created")
    
    # Paginate entries
    paginated_entries = paginate_queryset(request, entries)
    
    return render(
        request, 
        "blog/archive.html", 
        {
            "entries": paginated_entries,
            "blogmarks": blogmarks,
            "page_obj": paginated_entries
        }
    )

def tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    entries = tag.entry_set.filter(is_draft=False).order_by("-created")
    blogmarks = tag.blogmark_set.filter(is_draft=False).order_by("-created")
    
    # Paginate entries
    paginated_entries = paginate_queryset(request, entries)
    
    return render(
        request, 
        "blog/tag.html", 
        {
            "tag": tag, 
            "entries": paginated_entries,
            "blogmarks": blogmarks,
            "page_obj": paginated_entries
        }
    )

def search(request):
    q = request.GET.get("q", "").strip()
    if q:
        # Simple search implementation - can be enhanced later
        entries = Entry.objects.filter(
            is_draft=False
        ).filter(
            models.Q(title__icontains=q) | 
            models.Q(summary__icontains=q) | 
            models.Q(body__icontains=q)
        ).order_by("-created")
        
        blogmarks = Blogmark.objects.filter(
            is_draft=False
        ).filter(
            models.Q(title__icontains=q) | 
            models.Q(commentary__icontains=q)
        ).order_by("-created")
        
        # Paginate entries
        paginated_entries = paginate_queryset(request, entries)
    else:
        entries = []
        blogmarks = []
        paginated_entries = None
    
    return render(
        request,
        "blog/search.html",
        {
            "q": q, 
            "entries": paginated_entries, 
            "blogmarks": blogmarks,
            "page_obj": paginated_entries
        },
    )

class AtomFeed(Feed):
    title = "Minimal Wave Blog"
    link = "/blog/"
    subtitle = "Latest blog posts"
    feed_type = Atom1Feed

    def items(self):
        return Entry.objects.filter(is_draft=False).order_by("-created")[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary_rendered

    def item_pubdate(self, item):
        return item.created

def get_month_number(month_name):
    """Convert month name to number (1-12)"""
    months = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4,
        'may': 5, 'jun': 6, 'jul': 7, 'aug': 8,
        'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    return months.get(month_name.lower()[:3], 1)

def get_month_name(month_number):
    """Convert month number to name"""
    months = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    return months.get(month_number, 'January')

def reading_time(text):
    """
    Estimate reading time for a given text.
    Average reading speed is about 200-250 words per minute.
    """
    import re
    import math
    
    # Strip HTML tags if present
    text = re.sub(r'<[^>]+>', '', text)
    
    # Count words
    words = len(text.split())
    
    # Calculate reading time in minutes (using 200 words per minute)
    minutes = math.ceil(words / 200)
    
    return minutes
