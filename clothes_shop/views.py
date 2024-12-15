from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.db.models import Count
from django.utils.timezone import now

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from products.forms import OrderAddForm, ProductReviewForm
from products.models import Product, Order, OrderItem, ProductReview, Favorite, PageView

class ProductDetailView(View):
    def get(self, request, id):
        try:
            product = get_object_or_404(Product, id=id)

        except Product.DoesNotExist:
            return redirect('index')

        form = OrderAddForm()
        return render(request, 'detail.html', {'product':product, 'form':form})


class ProductListView(View):
    def get(self, request):
        # Pre-fetch category products to avoid redundant queries
        kurtkalar = Product.objects.filter(category=1).order_by('-created_at')
        rubashkalar = Product.objects.filter(category=4).order_by('-created_at')

        # Get the required slices for kurtkalar and rubashkalar
        kurtkalar_top = kurtkalar[:3]
        kurtkalar_bottom = kurtkalar.order_by('created_at')[:3]
        rubashkalar_top = rubashkalar[:3]
        rubashkalar_bottom = rubashkalar.order_by('created_at')[:3]
        rubashkalar_all = rubashkalar  # Already ordered by '-created_at'
        kurtkalar_all = kurtkalar  # Already ordered by '-created_at'

        # Template selection based on request path
        path_templates = {
            '/': 'index.html',
            '/product/rubashka': 'rubashka.html',
            '/product/kurtka': 'kurtka.html',
            '/product/list': 'product_list.html'
        }

        # Default to '404.html' if the path is not recognized
        template_name = path_templates.get(request.path, '404.html')

        # Context to pass to the template
        context = {
            'products': Product.objects.order_by('-created_at'),
            'kurtkalar': kurtkalar_top,
            'kurtkalar2': kurtkalar_bottom,
            'rubashkalar': rubashkalar_top,
            'rubashkalar2': rubashkalar_bottom,
            'rubashkalar3': rubashkalar_all,
            'kurtkalar3': kurtkalar_all
        }

        return render(request, template_name, context)

def cart_detail(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    order, _ = Order.objects.get_or_create(user=request.user)
    return render(request, 'order/detail.html', {'order': order})

def cart_add(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        order, _ = Order.objects.get_or_create(user=request.user)
        form = OrderAddForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart_item, created = OrderItem.objects.get_or_create(order=order, product=product)
            if not created:
                cart_item.quantity += quantity
            cart_item.save()
        return redirect('order_detail')
    return redirect('users:login')

def cart_remove(request, item_id):
    cart_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
    cart_item.delete()
    return redirect('order_detail')

@login_required
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Favorite.objects.get_or_create(user=request.user, product=product)
    messages.success(request, f"{product.name} добавлен в избранное.")
    return redirect('favorites')  # Замените 'product_list' на вашу страницу товаров

@login_required
def remove_from_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    favorite = Favorite.objects.filter(user=request.user, product=product).first()
    if favorite:
        favorite.delete()
        messages.success(request, f"{product.name} удален из избранного.")
    else:
        messages.error(request, "Товар не найден в избранном.")
    return redirect('favorites')  # Замените на вашу страницу избранного

@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    return render(request, 'favorites/list.html', {'favorites': favorites})


@login_required
def share_favorites(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    if not favorites:
        return JsonResponse({'error': 'У вас нет избранных товаров'}, status=400)

    # Пример генерации ссылки
    shared_items = [favorite.product.id for favorite in favorites]
    share_url = f"{request.build_absolute_uri('/favorites/shared/')}?items={','.join(map(str, shared_items))}"
    return JsonResponse({'share_url': share_url})

def shared_favorites_view(request):
    items = request.GET.get('items', '')
    product_ids = items.split(',') if items else []
    products = Product.objects.filter(id__in=product_ids)
    return render(request, 'favorites/shared_favorites.html', {'products': products})

class AddReviewView(View):
    def post(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return redirect('detail', id=id)

        review_form = ProductReviewForm(data=request.POST)
        if request.user.is_authenticated:
            if review_form.is_valid():
                ProductReview.objects.create(
                    product_id=product,
                    user_id=request.user,
                    # stars_given=review_form.cleaned_data['stars_given'],
                    comment=review_form.cleaned_data['comment']
                )
                return redirect(reverse("detail", kwargs={"id":product.id}))


            return render(request, 'detail.html', {'product':product, 'review_form':review_form})
        else:
            return redirect('users:login')


class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, product_id, review_id):
        product = get_object_or_404(Product, id=product_id)
        review = get_object_or_404(product.productreview_set, id=review_id)
        review_form = ProductReviewForm(instance=review)
        return render(request, 'review_edit.html', {'product': product, 'review': review, 'review_form': review_form})

    def post(self, request, product_id, review_id):
        product = get_object_or_404(Product, id=product_id)
        review = get_object_or_404(product.productreview_set, id=review_id)
        review_form = ProductReviewForm(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('detail', kwargs={"id": product_id}))
        return render(request, 'review_edit.html', {'product': product, 'review': review, 'review_form': review_form})

class ConfirmDeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, product_id, review_id):
        product = Product.objects.get(id=product_id)
        review = product.productreview_set.get(id=review_id)
        return render(request, 'confirm_delete_review.html', {'product':product, 'review':review})

class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, product_id, review_id):
        product = Product.objects.get(id=product_id)
        review = product.productreview_set.get(id=review_id)

        review.delete()
        messages.success(request, "You have successfully deleted this review")

        return redirect(reverse('detail', kwargs={'id':product_id}))

def view_function(request):
    # Получаем или создаем ключ сессии
    if not request.session.session_key:
        request.session.create()
    session_id = request.session.session_key

    # Создаем запись просмотра страницы с текущим URL
    pageview = PageView(session_id=session_id, url=request.path)
    pageview.save()

@staff_member_required
def analytics_report(request):
    # Фиксируем текущий просмотр
    view_function(request)

    # Генерируем отчет
    data = (
        PageView.objects.values('url')
        .annotate(views=Count('id'))
        .order_by('-views')[:10]
    )
    return render(request, 'analytics/report.html', {'data': data, 'now': now()})