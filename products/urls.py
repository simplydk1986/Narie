from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('story/', views.story, name='story'),
    path('reviews/', views.reviews, name='reviews'),
    path('articles/', views.articles, name='articles'),
    path('suggestions/', views.suggestions, name='suggestions'),
    
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),

    # Order
    path('create_order/', views.create_order, name='create_order'),
    path('order_complete/', views.order_complete, name='order_complete'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),

    # CS Center
    path('cs/notice/', views.notice, name='notice'),
    path('cs/notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('cs/faq/', views.faq, name='faq'),
    path('cs/qna/', views.qna, name='qna'),
    path('cs/qna/<int:qna_id>/', views.qna_detail, name='qna_detail'),
    path('cs/qna/write/', views.qna_write, name='qna_write'),
]

