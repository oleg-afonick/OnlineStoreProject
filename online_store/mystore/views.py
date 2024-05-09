from django.views.generic import *

from mystore.forms import ProductForm
from mystore.models import Product


class ProductList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'


class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'


class ProductCreate(CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_create.html'
    context_object_name = 'product'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.method == 'POST':
            post.name = f'Новое имя: {form.get_name()}'
        return super().form_valid(form)
