from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views
from .views import ProductListView, ProductDetailView, AddReviewView, EditReviewView, ConfirmDeleteReviewView, \
    DeleteReviewView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('', ProductListView.as_view(), name='index'),
    path('product/list', ProductListView.as_view(), name='product_list'),
    path('product/<int:id>', ProductDetailView.as_view(), name='detail'),
    path('product/kurtka', ProductListView.as_view(), name='kurtka'),
    path('product/rubashka', ProductListView.as_view(), name='rubashka'),
    path('korzina', views.cart_detail, name='order_detail'),
    path('korzina/add/<int:product_id>/', views.cart_add, name='order_add'),
    path('korzina/remove/<int:item_id>/', views.cart_remove, name='order_remove'),
    path('product/<int:id>/review', AddReviewView.as_view(), name='reviews'),
    path('product/<int:product_id>/review/<int:review_id>/edit', EditReviewView.as_view(), name='review-edit'),
    path('product/<int:product_id>/reviews/<int:review_id>/delete/confirm/', ConfirmDeleteReviewView.as_view(), name='confirm-delete-review'),
    path('product/<int:product_id>/reviews/<int:review_id>/delete/', DeleteReviewView.as_view(), name='delete-review'),
    path('add-to-favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove-from-favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('favorites/share/', views.share_favorites, name='share_favorites'),
    path('favorites/shared/', views.shared_favorites_view, name='shared_favorites_view'),
    path('analytics/report/', views.analytics_report, name='analytics_report'),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #media file lardi taba aliwi ushin