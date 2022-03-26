from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order

"""
Send automatic email to customer including the generated PDF 
"""

@task
def payment_completed(order_id):
    # Task to send an e-mail notification when order is completed
    order = Order.objects.get(id=order_id)

    # Created invoice e-mail
    subject = f'Shop - EE invoice no. {order.id}'
    message = 'Pleace, find attached the invoice for your recent purchase.'
    email = EmailMessage(
        subject,
        message,
        'admin@myshop.com',
        {order.email})
    # Generate PDF
    html = render_to_string('orders/order/pdf.html', {'order':order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(
        out,
        stylesheets=stylesheets)
    # Attach PDF file
    email.attach(f'order_{order.id}.pdf',
        out.getvalues(),
        'application/pdf')
    # Send email
    email.send()

