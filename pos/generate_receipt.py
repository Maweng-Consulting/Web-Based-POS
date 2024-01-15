# views.py
import os

import pdfkit
from django.conf import settings
from django.template.loader import render_to_string

from pos.models import Order


def render_to_pdf(order_id):
    order = Order.objects.get(id=order_id)

    # Render HTML template with data
    html = render_to_string(
        "receipts/order.html", {"order": order, "order_items": order.items}
    )

    # Generate PDF and save it locally
    pdf_path = os.path.join(
        settings.MEDIA_ROOT, f"receipts/invoice_{order_id}.pdf"
    )  # Adjust path as needed
    pdfkit.from_string(html, pdf_path)

    order.order_receipt = f"/receipts/invoice_{order_id}.pdf"
    order.save()
