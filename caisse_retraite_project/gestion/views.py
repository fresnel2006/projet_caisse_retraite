from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Adherent, Cotisation
from .forms import AdherentForm, CotisationForm

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@login_required
@superuser_required
def home(request):
    return redirect('gestion:adherent_list')

@require_http_methods(["GET", "POST", "HEAD"])
def custom_login(request):
    if request.user.is_authenticated:
        return redirect('gestion:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('gestion:home')
        else:
            messages.error(request, 'Seuls les superutilisateurs peuvent se connecter.')
    return render(request, 'login.html')

# Vue pour lister tous les adhérents
@login_required
@superuser_required
def adherent_list(request):
    adherents = Adherent.objects.all()
    return render(request, 'gestion/liste_adherents.html', {'adherents': adherents})

# Vue pour afficher le détail d'un adhérent
@login_required
@superuser_required
def adherent_detail(request, pk):
    adherent = get_object_or_404(Adherent, pk=pk)
    cotisations = adherent.cotisations.all()
    return render(request, 'gestion/detail_adherent.html', {'adherent': adherent, 'cotisations': cotisations})

# Vue pour créer un nouvel adhérent
@login_required
@superuser_required
def adherent_create(request):
    if request.method == 'POST':
        form = AdherentForm(request.POST)
        if form.is_valid():
            adherent = form.save()
            return redirect('gestion:adherent_detail', pk=adherent.pk)
    else:
        form = AdherentForm()
    return render(request, 'gestion/adherent_form.html', {'form': form})

# Vue pour modifier un adhérent existant
@login_required
@superuser_required
def adherent_update(request, pk):
    adherent = get_object_or_404(Adherent, pk=pk)
    if request.method == 'POST':
        form = AdherentForm(request.POST, instance=adherent)
        if form.is_valid():
            form.save()
            return redirect('gestion:adherent_detail', pk=adherent.pk)
    else:
        form = AdherentForm(instance=adherent)
    return render(request, 'gestion/adherent_form.html', {'form': form})

# Vue pour ajouter une cotisation à un adhérent
@login_required
@superuser_required
def cotisation_create(request, pk):
    adherent = get_object_or_404(Adherent, pk=pk)
    if request.method == 'POST':
        form = CotisationForm(request.POST)
        if form.is_valid():
            cotisation = form.save(commit=False)
            cotisation.adherent = adherent
            cotisation.save()
            return redirect('gestion:adherent_detail', pk=adherent.pk)
    else:
        form = CotisationForm()
    return render(request, 'gestion/cotisation_form.html', {'form': form, 'adherent': adherent})

# Vue pour supprimer un adhérent
@login_required
@superuser_required
def adherent_delete(request, pk):
    adherent = get_object_or_404(Adherent, pk=pk)
    if request.method == 'POST':
        adherent.delete()
        return redirect('gestion:adherent_list')
    return render(request, 'gestion/adherent_confirm_delete.html', {'adherent': adherent})

# Vue pour lister tous les adhérents avec leurs cotisations
@login_required
@superuser_required
def cotisation_list(request):
    adherents = Adherent.objects.filter(cotisations__isnull=False).distinct().prefetch_related('cotisations')
    adherents_with_totals = []
    for adherent in adherents:
        total = sum(cotisation.montant for cotisation in adherent.cotisations.all())
        adherents_with_totals.append({
            'adherent': adherent,
            'total': total
        })
    return render(request, 'gestion/cotisation_list.html', {'adherents_with_totals': adherents_with_totals})
