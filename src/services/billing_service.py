from __future__ import annotations

from io import BytesIO


def generate_bill_number(order) -> str:
    return f"HB-{order.business_id:03d}-{order.id:05d}"


def build_bill_pdf(order) -> BytesIO:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    from reportlab.pdfgen import canvas

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 20 * mm

    pdf.setTitle(f"Bill-{generate_bill_number(order)}")
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(20 * mm, y, order.table.business.name)

    y -= 8 * mm
    pdf.setFont("Helvetica", 10)
    pdf.drawString(20 * mm, y, order.table.business.address or "Address not set")

    y -= 12 * mm
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(20 * mm, y, f"Bill No: {generate_bill_number(order)}")
    pdf.drawRightString(width - 20 * mm, y, order.created_at.strftime("%Y-%m-%d %H:%M"))

    y -= 8 * mm
    pdf.setFont("Helvetica", 11)
    pdf.drawString(20 * mm, y, f"Table: {order.table.name}")
    pdf.drawRightString(width - 20 * mm, y, f"Payment: {order.payment_status}")

    y -= 12 * mm
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(20 * mm, y, "Item")
    pdf.drawRightString(width - 70 * mm, y, "Qty")
    pdf.drawRightString(width - 45 * mm, y, "Rate")
    pdf.drawRightString(width - 20 * mm, y, "Amount")

    y -= 4 * mm
    pdf.line(20 * mm, y, width - 20 * mm, y)
    y -= 8 * mm

    pdf.setFont("Helvetica", 10)
    for item in order.items:
        amount = item.quantity * item.price_at_order
        pdf.drawString(20 * mm, y, item.menu_item.name)
        pdf.drawRightString(width - 70 * mm, y, str(item.quantity))
        pdf.drawRightString(width - 45 * mm, y, f"{item.price_at_order:.2f}")
        pdf.drawRightString(width - 20 * mm, y, f"{amount:.2f}")
        y -= 7 * mm
        if y < 40 * mm:
            pdf.showPage()
            y = height - 20 * mm
            pdf.setFont("Helvetica", 10)

    y -= 3 * mm
    pdf.line(20 * mm, y, width - 20 * mm, y)
    y -= 10 * mm

    pdf.setFont("Helvetica", 11)
    pdf.drawRightString(width - 45 * mm, y, "Subtotal:")
    pdf.drawRightString(width - 20 * mm, y, f"{order.total_amount:.2f}")
    y -= 7 * mm
    pdf.drawRightString(width - 45 * mm, y, "GST:")
    pdf.drawRightString(width - 20 * mm, y, f"{order.gst_amount:.2f}")
    y -= 7 * mm
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawRightString(width - 45 * mm, y, "Total:")
    pdf.drawRightString(width - 20 * mm, y, f"{order.final_amount:.2f}")

    y -= 15 * mm
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(20 * mm, y, "Thank you for using HBuddy.")
    pdf.save()

    buffer.seek(0)
    return buffer
