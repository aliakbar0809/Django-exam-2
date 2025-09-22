from django.shortcuts import render, redirect,get_object_or_404
from .models import * 
from .forms import *
from django.views.generic  import *
from django.urls import reverse_lazy


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'profile/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email, password=password)
            if user:
                request.session['user_id'] = user.id
                return redirect('profile_view')
        except:
            return render(request, 'profile/login.html', {'context': 'Ваш email или пароль введены неправильно'})
    return render(request, 'profile/login.html')

def logout(request):
    request.session.flush()
    return redirect('login')

# Profile card

class ProfileView(DetailView):

    model = Profile
    template_name = 'profile/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        user_id = self.request.session.get('user_id')
        return get_object_or_404(Profile, user_id=user_id)
    

class ProfileUpdateView(UpdateView):

    model = Profile
    form_class = ProfileForm
    template_name = 'profile/profile_update.html'
    success_url = reverse_lazy('profile_view')

    def get_object(self):
        user_id = self.request.session.get('user_id')
        return get_object_or_404(Profile, user_id=user_id)


class ProfileDeleteView(DeleteView):

    model = Profile
    success_url = 'register/'

    def get_object(self):
        user_id = self.request.session.get('user_id')
        return get_object_or_404(Profile, user_id=user_id)



# Product card



class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_create.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
    

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)



class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/product_update.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product/product_delete.html'
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)
    

# Cart CARD
class CreateToCartView(CreateView):
    model = Cart
    success_url = reverse_lazy('cart_detail')

    def post(self, request):
        if not request.session.get('user_id'):
            return redirect('login')
        
        user_id = request.session.get('user_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)

        if product.quantity < quantity or quantity < 1:
            return redirect('product_detail', pk=product.id)

        # Если товар уже в корзине — увеличиваем количество
        cart_item = Cart.objects.filter(user_id=user_id, product=product).first()
        if cart_item:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.quantity:
                new_quantity = product.quantity
            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            Cart.objects.create(user_id=user_id, product=product, quantity=quantity)

        return redirect('cart_detail')




class CartListView(ListView):
    model = Cart
    template_name = 'cart/cart_list.html'
    context_object_name = 'carts'

    def get_queryset(self):
        user_id = self.request.session.get('user_id')
        return Cart.objects.filter(user_id=user_id)
    


class CartDeleteView(DeleteView):
    model = Cart
    template_name = 'cart/cart_delete.html'
    success_url = reverse_lazy('cart_detail')

    def get_queryset(self):
        user_id = self.request.session.get('user_id')
        return Cart.objects.filter(user_id=user_id)
    

# Order CARD

class OrderCreateView(CreateView):
    model = Order
    success_url = reverse_lazy('cart/order_list')

    def post(self, request):
        if not request.session.get('user_id'):
            return redirect('login')
        
        user_id = request.session.get('user_id')
        cart_items = Cart.objects.filter(user_id=user_id)

        if not cart_items:
            return redirect('cart_list')

        cnt = 0

        for item in cart_items:
            if item.quantity > item.product.quantity:
                return render(request,'cart/cart_list.html',{'context':'На складе нет такого количества товара'})
            
            cnt += item.quantity * item.product.price


        order = Order.objects.create(user_id=user_id, total_amount=cnt)

        for item in cart_items:
            product = item.product
            product.quantity -= item.quantity
            product.save()


        cart_items.delete()

        return redirect('order_list')
    

class OrderListView(ListView):
    model = Order
    template_name = 'cart/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        user_id = self.request.session.get('user_id')
        return Order.objects.filter(user_id=user_id)