from random import randint
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

from .forms import RegisterForm
from .models import ToolCategory, DueDates, ShoppingCart, History


def getCart():
    cart = ShoppingCart.objects.all()
    return {'cart': cart}


def index(request):
    context = getCart()
    return render(request, 'tools/index.html', context)


def allTools(request):
    context = getCart()
    tools_list = ToolCategory.objects.all()
    context['inCart'] = 0
    for item in context['cart']:
        context['inCart'] += item.quantity
    try:
        filter = request.POST['search']
        filter_list = []
        for tool in tools_list:
            if filter in tool.type:
                filter_list.append(tool)
        context['tools_list'] = filter_list
        context['search'] = filter
    except:
        context['tools_list'] = tools_list
    finally:
        return render(request, 'tools/all_tools.html', context)


def contact(request):
    context = getCart()
    return render(request, 'tools/contact.html', context)


def project(request):
    context = getCart()
    return render(request, 'tools/project.html', context)


def history(request):
    if not request.user.is_authenticated:
        return redirect('index')
    history = History.objects.all()[::-1]
    context = getCart()
    context['history'] = history
    return render(request, 'tools/history.html', context)


def toolpage(request, tool_id):
    if not request.user.is_authenticated:
        return redirect('index')
    tool_category = get_object_or_404(ToolCategory, pk=tool_id)
    context = getCart()
    context['tool'] = tool_category
    return render(request, 'tools/toolpage.html', context)


def delete_tool(request, tool_id):
    if not request.user.is_authenticated:
        return redirect('index')
    tool_category = get_object_or_404(ToolCategory, pk=tool_id)
    tool_category.delete()
    return redirect('index')


def edit_tool(request, tool_id):
    if not request.user.is_authenticated:
        return redirect('index')
    t = get_object_or_404(ToolCategory, pk=tool_id)
    t.type = request.POST['name']
    t.available = request.POST['quantity']
    t.price = request.POST['price']
    t.tool_image = request.POST['img']
    t.save()
    return redirect('index')


def checkedOut(request):
    if not request.user.is_authenticated:
        return redirect('index')
    tools_list = ToolCategory.objects.all()
    list = []
    due = DueDates.objects.order_by('-date_bought')
    for d in due:
        for tool in tools_list:
            if tool == d.toolCategory:
                list.append(d)
    context = getCart()
    context['checkedOut_tools'] = list
    return render(request, 'tools/checked_out.html', context)


def availableTools(request):
    tools_list = ToolCategory.objects.all()
    list = []
    for tool in tools_list:
        if tool.available > 0:
            list.append(tool)
    context = getCart()
    context['available_tools'] = list
    return render(request, 'tools/available.html', context)


def create_category(request):
    if not request.user.is_authenticated:
        return redirect('index')
    context = getCart()
    return render(request, 'tools/create_category.html', context)


def overdue(request):
    if not request.user.is_authenticated:
        return redirect('index')
    due_dates = DueDates.objects.order_by('-date_due')
    list = []
    for tool in reversed(due_dates):
        if tool.date_due < timezone.now():
            list.append(tool)
    context = getCart()
    context['overdue_tools'] = list
    return render(request, 'tools/overdue.html', context)


def create(request):
    if not request.user.is_authenticated:
        return redirect('index')
    t = ToolCategory()
    t.type = request.POST['name']
    t.available = request.POST['quantity']
    t.unavailable = 0
    t.price = request.POST['price']
    t.tool_image = request.POST['img']
    t.save()
    return redirect('index')


def checkin(request, tool_id):
    due = get_object_or_404(DueDates, pk=tool_id)
    due.toolCategory.available += due.quantity
    due.toolCategory.unavailable -= due.quantity
    due.toolCategory.save()

    history = History()
    history.customer = due.buyer
    history.date_bought = due.date_bought
    history.price = 0  # We could put late fees here if we want
    history.tools = due.toolCategory.type
    history.state = history.CHECKIN
    history.save()

    due.delete()
    return redirect('index')


def checkout(request):
    context = getCart()

    history = History()
    for cart in ShoppingCart.objects.all():
        due = DueDates()
        due.toolCategory = cart.toolCategory
        due.quantity = cart.quantity
        due.date_bought = datetime.datetime.now()
        due.date_due = datetime.datetime(2020, randint(1, 12), randint(1, 28))
        # due.date_bought = datetime.datetime.now()
        # due.date_due = datetime.datetime.now()
        due.buyer = "Connor"
        due.save()

        history.customer = due.buyer
        history.date_bought = due.date_bought
        history.price += due.toolCategory.price * due.quantity
        history.tools += due.toolCategory.type + ", "

        cart.delete()

    history.tools = history.tools[:-2]
    history.state = history.CHECKOUT
    history.save()
    return redirect('checkout_confirmed')


def checkout_confirmed(request):
    return render(request, 'tools/checkout.html')


def addToCart(request, category_id):
    tool = get_object_or_404(ToolCategory, pk=category_id)
    tool.available -= 1
    tool.unavailable += 1
    tool.save()

    inCart = False
    for cart in ShoppingCart.objects.all():
        if cart.tool == tool.type:
            cart.quantity += 1
            cart.save()
            inCart = True

    if not inCart:
        cart = ShoppingCart()
        cart.toolCategory = tool
        cart.tool = tool.type
        cart.quantity = 1
        cart.tool_image = tool.tool_image
        cart.save()

    return redirect('all_tools')


def init(request):
    # for now let's not have init be an admin view for simplicity sake
    #    if not request.user.is_authenticated:
    #        return redirect('index')

    nuke(request)
    User.objects.filter(email='admin@example.com').delete()
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    categories = ['hammer', 'wrench', 'screwdriver', 'level', 'drill']
    images = {
        'hammer': '/static/images/hammer.jpg',
        'wrench': '/static/images/wrench.jpg',
        'screwdriver': '/static/images/screwdriver.jpg',
        'level': '/static/images/level.jpg',
        'drill': '/static/images/drill.jpg',
    }

    prices = {'hammer': 2, 'wrench': 2, 'screwdriver': 2, 'level': 2, 'drill': 5}
    for i in range(len(categories)):
        tool = ToolCategory(type=categories[i],
                            available=10,
                            unavailable=randint(1, 5),
                            price=prices.get(categories[i]),
                            tool_image=images.get(categories[i]))
        tool.save()
        for j in range(tool.unavailable):
            due = DueDates()
            due.toolCategory = tool
            due.date_bought = datetime.datetime(2019, randint(1, 12), randint(1, 28))
            due.date_due = datetime.datetime(2020, randint(1, 12), randint(1, 28))
            due.buyer = "Tyler"
            due.save()

    return redirect('index')


def nuke(request):
    for categories in ToolCategory.objects.all():
        categories.delete()


def nuke_it(request):
    if not request.user.is_authenticated:
        return redirect('index')
    nuke(request)
    history = History.objects.all()
    history.delete()
    return redirect('index')
