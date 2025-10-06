from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import (
    Product, Review, Cart, CartItem, Order, OrderItem,
    ProductType, ProductLine, ProductConcern,
    Notice, FaqCategory, Faq, Qna
)
from .forms import QnaForm

# Main pages
def home(request):
    featured_products = Product.objects.filter(is_featured=True)[:4]
    latest_reviews = Review.objects.order_by('-created_at')[:3]
    return render(request, 'products/home.html', {
        'featured_products': featured_products,
        'latest_reviews': latest_reviews
    })

def shop(request):
    # This can be expanded with filtering and sorting
    products = Product.objects.all()
    return render(request, 'products/shop.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

# --- CS Center Views ---

def notice(request):
    notice_list = Notice.objects.all()
    paginator = Paginator(notice_list, 10) # Show 10 notices per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/notice.html', {'page_obj': page_obj})

def notice_detail(request, notice_id):
    notice_item = get_object_or_404(Notice, pk=notice_id)
    # Increase view count
    notice_item.views += 1
    notice_item.save()
    return render(request, 'products/notice_detail.html', {'notice': notice_item})

def faq(request):
    categories = FaqCategory.objects.all()
    active_category_name = request.GET.get('category')
    
    if active_category_name:
        faqs = Faq.objects.filter(category__name=active_category_name)
    else:
        faqs = Faq.objects.all()
        
    return render(request, 'products/faq.html', {
        'categories': categories,
        'faqs': faqs,
        'active_category': active_category_name
    })

def qna(request):
    qna_list = Qna.objects.all()
    paginator = Paginator(qna_list, 10) # Show 10 Q&As per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products/qna.html', {'page_obj': page_obj})

def qna_detail(request, qna_id):
    qna_item = get_object_or_404(Qna, pk=qna_id)

    # Check for private posts
    if qna_item.is_private:
        if not request.user.is_authenticated or (request.user != qna_item.author and not request.user.is_staff):
            messages.error(request, '이 글을 볼 권한이 없습니다.')
            return redirect('qna')

    return render(request, 'products/qna_detail.html', {'qna': qna_item})

@login_required
def qna_write(request):
    if request.method == 'POST':
        form = QnaForm(request.POST)
        if form.is_valid():
            qna_item = form.save(commit=False)
            qna_item.author = request.user
            qna_item.save()
            return redirect('qna_detail', qna_id=qna_item.id)
    else:
        form = QnaForm()
    return render(request, 'products/qna_write.html', {'form': form})


# --- Placeholder Views for other pages ---

def about(request):
    return render(request, 'products/about.html')

def story(request):
    return render(request, 'products/story.html')

def reviews(request):
    return render(request, 'products/reviews.html')

def articles(request):
    return render(request, 'products/articles.html')

def suggestions(request):
    return render(request, 'products/suggestions.html')

# --- Cart Views ---

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'products/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def update_cart(request, item_id):
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.quantity = int(quantity)
        cart_item.save()
    return redirect('cart')

# --- Order Views ---

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return redirect('cart')

    order = Order.objects.create(user=request.user, total_amount=cart.get_total_price())
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.get_display_price()
        )
    cart.items.all().delete()
    return redirect('order_complete')

@login_required
def order_complete(request):
    return render(request, 'products/order_complete.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'products/order_detail.html', {'order': order})

