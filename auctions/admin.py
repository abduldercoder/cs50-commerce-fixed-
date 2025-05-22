"""Minimal, error‑free admin registration for Auctions app.
Update or extend later once model field names are finalised.
"""

from django.contrib import admin

from .models import Listing, Bid, Comment  # adjust names if different in models.py

# --- Simple registration (avoids field‑name mismatches) ---
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
