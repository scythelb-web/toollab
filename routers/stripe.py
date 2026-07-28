"""Stripe checkout and webhook for ToolLab Pro subscriptions."""
import json
import os
import stripe
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from context import ctx

router = APIRouter()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PRICE_ID = os.getenv("STRIPE_PRICE_ID", "price_1TyKpfIh3bqeW0wSKEH0pjlp")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")


@router.post("/create-checkout")
async def create_checkout(request: Request):
    """Create a Stripe Checkout session for Pro subscription."""
    user = request.session.get("user") or {}
    email = user.get("email", "")

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                "price": STRIPE_PRICE_ID,
                "quantity": 1,
            }],
            mode="subscription",
            success_url="https://toollab.ca/stripe/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="https://toollab.ca/pricing",
            customer_email=email if email else None,
            metadata={"user_email": email},
        )
        if checkout_session.url:
            return RedirectResponse(url=str(checkout_session.url), status_code=303)
        return HTMLResponse("<h2>Could not create checkout session</h2>", status_code=500)
    except Exception as e:
        return HTMLResponse(f"<h2>Checkout error</h2><p>{e}</p>", status_code=500)


@router.get("/success")
async def checkout_success(request: Request, session_id: str = ""):
    """Handle successful checkout return. Verify and mark user as Pro."""
    if not session_id:
        return RedirectResponse("/pricing", status_code=303)

    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        if checkout_session.payment_status == "paid":
            user = request.session.get("user") or {}
            user["is_pro"] = True
            request.session["user"] = user
            return request.app.state.templates.TemplateResponse(
                "success.html", ctx(request))
    except Exception:
        pass

    return RedirectResponse("/pricing", status_code=303)


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Receive Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if STRIPE_WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        except Exception:
            return {"error": "Invalid signature"}, 400
    else:
        # No webhook secret set — parse raw body for dev/testing
        try:
            event = json.loads(payload)
        except Exception:
            return {"error": "Invalid payload"}, 400

    if event.get("type") == "checkout.session.completed":
        session = event["data"]["object"]
        _email = session.get("customer_email") or session.get("metadata", {}).get("user_email", "")
        # In production: look up user by email and persist is_pro in DB
        # For now, the success URL redirect handles marking the session

    return {"status": "ok"}
