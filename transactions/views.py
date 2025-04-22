from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm
from django.shortcuts import get_object_or_404

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
