from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
import calendar
from collections import OrderedDict
from .models import Transaction
from .forms import TransactionForm

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transactions/add_transaction.html', {'form': form})

@login_required
def transaction_list(request):
    selected_categories = request.GET.getlist('category')
    if selected_categories:
        transactions = Transaction.objects.filter(category__in=selected_categories)
    else:
        transactions = Transaction.objects.all()

    context = {
        'transactions': transactions,
        'category_choices': [
            ('FOOD', 'Food'),
            ('RENT', 'Rent'),
            ('UTIL', 'Utilities'),
            ('TRAN', 'Transport'),
            ('ENTR', 'Entertainment'),
            ('HEAL', 'Healthcare'),
            ('MISC', 'Miscellaneous'),
        ],
        'selected_categories': selected_categories
    }
    return render(request, 'transactions/transaction_list.html', context)

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transactions/edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'transactions/delete_transaction.html', {'transaction': transaction})

@login_required
def user_report_page(request):
    return render(request, 'transactions/report.html')

@login_required
def user_report_data(request):
    user = request.user
    time_range = request.GET.get('range', 'all')

    today = now()

    if time_range == '3months':
        start_date = today - timedelta(days=90)
        transactions = Transaction.objects.filter(user=user, date__gte=start_date)

        # Create monthly buckets for the past 3 months
        monthly_data = OrderedDict()
        for i in range(2, -1, -1):
            month_date = today - timedelta(days=30 * i)
            label = month_date.strftime('%B %Y')
            monthly_data[label] = 0

        for t in transactions:
            if t.date:
                label = t.date.strftime('%B %Y')
                if label in monthly_data:
                    monthly_data[label] += t.amount

    else:  # all time
        transactions = Transaction.objects.filter(user=user)

        # Create monthly buckets for the past 12 months
        monthly_data = OrderedDict()
        for i in range(11, -1, -1):
            month_date = today - timedelta(days=30 * i)
            label = month_date.strftime('%B %Y')
            monthly_data[label] = 0

        for t in transactions:
            if t.date:
                label = t.date.strftime('%B %Y')
                if label in monthly_data:
                    monthly_data[label] += t.amount

    category_data = (
        transactions.values('category')
        .annotate(total=Sum('amount'))
    )

    return JsonResponse({
        'category_data': list(category_data),
        'monthly_data': monthly_data,
    })