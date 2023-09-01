"""
URL configuration for contract_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views
from .yasg import urlpatterns as doc_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("projects/", views.ProjectList.as_view(), name="project-list"),
    path("projects/<int:pk>/", views.ProjectDetail.as_view(), name="project-detail"),
    path("contracts/", views.ContractList.as_view(), name="contract-list"),
    path("contracts/<int:pk>/", views.ContractDetail.as_view(), name="contract-detail"),
    path(
        "contracts/<int:pk>/confirm/",
        views.ContractDetail.confirm_contract,
        name="confirm-contract",
    ),
    path(
        "contracts/<int:pk>/complete/",
        views.ContractDetail.complete_contract,
        name="complete-contract",
    ),
]


admin.site.site_header = "iCode ADMIN"
admin.site.site_title = "contracts and projects"
admin.site.index_title = "Добро Пожаловать в админку iCode"


urlpatterns += doc_urls
