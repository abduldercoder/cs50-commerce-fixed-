from .models import Listing

def category_choices(request):
    categories = Listing.CATEGORY_CHOICES
    return {"category_choices": categories}
