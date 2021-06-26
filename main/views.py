from django.http.response import Http404, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, ListView, DetailView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from main.models import Product, Category, Type, UserData, CartItem, Order, Message

import socket
import random


def error_404(request, exception):
    data = {}
    return render(request, 'main/404.html', data)

def get_user(request):
    if 'user' in request.session:
        try:
            user = UserData.objects.get(pk=request.session['user'])
            user.save()
            return user
        except UserData.DoesNotExist:
            pass
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    try:
        socket.inet_aton(ip)
        ip_valid = True
    except socket.error:
        ip_valid = False
    if ip_valid:
        try:
            user = UserData.objects.get(ip=ip)
        except UserData.DoesNotExist:
            user = UserData.objects.create(ip=ip)
    else:
        user = UserData.objects.create(ip=random.randint(1, 9000000))
    request.session['user'] = f'{user.pk}'
    return user

class HomeView(TemplateView):
    template_name = "main/home.html"

    def get_context_data(self, **kwargs):
        user = get_user(self.request)
        kwargs = super().get_context_data(**kwargs)
        products = list(Product.objects.all().order_by('-id').filter(category='WOMEN'))[:6]
        products += list(Product.objects.all().order_by('-id').filter(category='MEN'))[:6]
        products += list(Product.objects.all().order_by('-id').filter(category='KIDS'))[:6]
        if len(products) > 20:
            products = products[:20]
        kwargs.update({
            'products' : products,
            'three': [1, 2, 3],
            'user_cart_number': len(user.cart.all()),
            'path': self.request.path,
            'show_order_taken': user.display_order_taken_notification
        })
        user.display_order_taken_notification = False
        user.save()
        return kwargs

class ShopView(ListView):
    model = Product
    template_name = "main/shop.html"
    context_object_name = "products"
    paginate_by = 9

    def get_queryset(self):
        if 'category' in self.request.GET:
            category = self.request.GET.get('category')
            if category.upper() in [cate[0] for cate in Category.choices]:
                return Product.objects.filter(category=category.upper())
        if 'type' in self.request.GET:
            type = self.request.GET.get('type')
            if type.upper() in [cate[0] for cate in Type.choices]:
                return Product.objects.filter(productType=type.upper())
        return Product.objects.all()

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            'path': self.request.path,
            'user_cart_number': len(get_user(self.request).cart.all())
        })
        return kwargs

class ProductDetailView(DetailView):
    model = Product
    template_name = "main/product-details.html"

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        category = self.kwargs.get('category')
        queryset = self.model.objects.all()
        if pk is not None:
            queryset = queryset.filter(category=category.upper()).filter(pk=pk)

        if pk is None:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        category = self.kwargs.get('category')
        queryset = list(self.model.objects.filter(category=category.upper()))
        queryset.remove(self.get_object())
        if len(queryset) > 4:
            queryset = queryset[:4]
        kwargs.update({
            'similiar_products': queryset,
            'path': self.request.path,
            'user_cart_number': len(get_user(self.request).cart.all()),
            'domain': self.request._current_scheme_host,
        })
        return kwargs

class ShopCartView(TemplateView):
    template_name = "main/shop-cart.html"

    def get(self, request, *args, **kwargs):
        self.kwargs['cart'] = get_user(request).cart.all()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        if 'cart' in self.kwargs:
            kwargs.update({
                'cart_items': self.kwargs['cart'],
                'user_cart_number': len(get_user(self.request).cart.all()),
                'user': get_user(self.request),
                'path': self.request.path,
            })
        return kwargs

class CheckoutView(TemplateView):
    template_name = "main/checkout.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = get_user(request)
        if user.totalCost != 0:
            order = Order.objects.create(user=user, totalCost=user.totalCost)
            for item in user.cart.all():
                item.order = order
                item.save()
                order.cart.add(item)
                order.save()
            user.firstname = request.POST.get('firstName')
            user.lastname = request.POST.get('lastName')
            user.save()
            if 'save' in request.POST:
                user.city = request.POST.get('city')
                user.state = request.POST.get('state')
                user.phone = request.POST.get('phone')
                if 'address' in request.POST:
                    user.address = request.POST.get('address')
                if 'apartment' in request.POST:
                    user.apartment = request.POST.get('apartment')
                if 'email' in request.POST:
                    user.email = request.POST.get('email')
                user.save()
            order.city = request.POST.get('city')
            order.state = request.POST.get('state')
            order.phone = request.POST.get('phone')
            if 'address' in request.POST:
                order.address = request.POST.get('address')
            if 'apartment' in request.POST:
                order.apartment = request.POST.get('apartment')
            if 'email' in request.POST:
                order.email = request.POST.get('email')
            if 'notes' in request.POST:
                order.notes = request.POST.get('notes')
                order.save()
            for item in user.cart.all():
                user.cart.remove(item)
                user.save()
            user.display_order_taken_notification = True
            user.save()
        return HttpResponseRedirect(reverse('home'))

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            'path': self.request.path,
            'user_cart_number': len(get_user(self.request).cart.all()),
            'user': get_user(self.request)
        })
        return kwargs

class ContactView(TemplateView):
    template_name = "main/contact.html"

    def post(self, request, *args, **kwargs):
        message = Message.objects.create(
            name = request.POST.get('name'),
            phone = request.POST.get('phone'),
            content = request.POST.get('message')
        )
        if 'email' in request.POST:
            message.email = request.POST.get('email')
            message.save()
        messages.add_message(request, messages.SUCCESS, "Your message has been sent. Expect a reply soon")
        return HttpResponseRedirect(request.path)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            'path': self.request.path,
            'user_cart_number': len(get_user(self.request).cart.all()),
            'user': get_user(self.request)
        })
        return kwargs

class PrivacyPolicyView(TemplateView):
    template_name = 'main/privacy-policy.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            'path': self.request.path,
            'user_cart_number': len(get_user(self.request).cart.all()),
            'user': get_user(self.request)
        })
        return kwargs


class RemoveFromCart(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk',0)
        product = CartItem.objects.get(pk=pk).product
        user = get_user(request)
        for cartItem in user.cart.all():
            if cartItem.product == product:
                cartItem.delete()
        messages.add_message(request, messages.WARNING, 'Item has been removed from cart')
        return HttpResponseRedirect(request.GET.get('path', '/'))

class AddToCart(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 0)
        product = Product.objects.get(pk=pk)
        user = get_user(request)
        duplicate = False
        if user.cart.all():
            for cartItem in user.cart.all():
                if cartItem.product == product:
                    duplicate = True
        if not duplicate:
            cartItem = CartItem.objects.create(product=product, qty=1, user=user)
            user.cart.add(cartItem)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Item has been added to cart')
        return HttpResponseRedirect(request.GET.get('path', '/'))

@method_decorator(csrf_exempt, name='dispatch')
class SetAmount(View):
    def post(self, request, *args, **kwargs):
        user = get_user(request)
        user.totalCost = int(request.POST.get('total'))
        user.save()
        cartQty = request.POST.get('qty')
        for item, qty in zip(user.cart.all(), cartQty.split()):
            item.qty = int(qty)
            item.save()
        user.save()
        return JsonResponse({'response': 'amount set'})