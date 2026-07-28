"""Shared context builder for all routers."""
import os
from fastapi import Request

ADSENSE_PUB_ID = os.getenv("ADSENSE_PUB_ID", "")


def ctx(request: Request, **extra):
    """Build template context with user, ads, and subdomain info."""
    user = request.session.get("user") or {}
    show_ads = bool(ADSENSE_PUB_ID) and not user.get("is_pro", False)
    return {
        "request": request,
        "subdomain": request.state.subdomain,
        "user": user if request.session.get("user") else None,
        "show_ads": show_ads,
        "adsense_pub_id": ADSENSE_PUB_ID,
        **extra,
    }
