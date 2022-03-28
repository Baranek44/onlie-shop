from django.shortcuts import render, redirect
from djagno.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApllyForm

# Create your views here.
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.objects.get['code']
        try:
            coupon = Coupon.objects.get(
                code_iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')
