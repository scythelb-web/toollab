"""Shared context builder for all routers."""
import os
from fastapi import Request
from limits import get_remaining, FREE_LIMIT

ADSENSE_PUB_ID = os.getenv("ADSENSE_PUB_ID", "")


def ctx(request: Request, **extra):
    """Build template context with user, ads, usage limits, and subdomain info."""
    user = request.session.get("user") or {}
    show_ads = bool(ADSENSE_PUB_ID) and not user.get("is_pro", False)
    return {
        "request": request,
        "subdomain": request.state.subdomain,
        "user": user if request.session.get("user") else None,
        "show_ads": show_ads,
        "adsense_pub_id": ADSENSE_PUB_ID,
        "free_limit": FREE_LIMIT,
        "usage_remaining": {
            "pdf": get_remaining(request, "pdf"),
            "image": get_remaining(request, "image"),
            "voice": get_remaining(request, "voice"),
        },
        **extra,
    }
