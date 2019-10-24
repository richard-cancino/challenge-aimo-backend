from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from account.api.serializers import CreateNoteSerializer, RetrieveNoteSerializer
from account.models import Note
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


def log_in(request):
    if request.user.is_authenticated:
        return redirect(reverse('index:home'))

    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(reverse('index:home'))

    return render(request, 'login.html', {'form': form})


def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse('index:login'))

    return render(request, 'index.html')
