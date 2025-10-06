from django.contrib import admin
from .models import (
    Product, Review, Cart, CartItem, Order, OrderItem,
    ProductType, ProductLine, ProductConcern, Category,
    Notice, FaqCategory, Faq, Qna, QnaAnswer
)

# --- Product Related Admin ---
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_featured', 'is_on_sale')
    list_filter = ('category', 'is_featured', 'is_on_sale')
    search_fields = ('name', 'description')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'author__username')

# --- Order Related Admin ---
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

# --- CS Center Related Admin ---

class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'views')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)

class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'category')
    list_filter = ('category',)
    search_fields = ('question', 'answer')

class QnaAnswerInline(admin.StackedInline):
    model = QnaAnswer
    can_delete = False
    verbose_name_plural = 'Answer'

class QnaAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'is_private')
    list_filter = ('status', 'is_private', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    inlines = [QnaAnswerInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Automatically update status if an answer is added/changed via admin
        if hasattr(obj, 'answer') and obj.answer is not None:
             obj.status = 'answered'
        else:
             # This part might need adjustment depending on how answers are deleted.
             # For now, if no answer exists, it's pending.
             obj.status = 'pending'
        obj.save()


# --- Registering Models ---

admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(ProductLine)
admin.site.register(ProductConcern)
admin.site.register(Cart)
admin.site.register(CartItem)

# CS Center
admin.site.register(Notice, NoticeAdmin)
admin.site.register(FaqCategory)
admin.site.register(Faq, FaqAdmin)
admin.site.register(Qna, QnaAdmin)

