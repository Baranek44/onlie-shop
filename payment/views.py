from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
import braintree 

"""
Import braintree module & create an instace of the Braintree gateway
"""

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    

    if request.method == 'POST':
        ## When the view is loaded with Post methode, payment_methode_nonce generate a new
        ## trasaction using gateway with 3 parameters
        #retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # Create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            # mark the order as paid
            order.paid = True
            # Store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # Generate token
        client_token = gateway.client_token.generate()
        return render(
            request,
            'payment/process.html',
            {'order': order,
            'client_token': client_token})


def payment_done(request):
    # payment successful done and show user done.html script
    return render(request, 'payment/done.html')

def payment_canceled(request):
    # payment canceled and show user canceled.html script
    return render(request, 'payment/canceled.html')