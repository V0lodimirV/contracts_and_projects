from django.utils import timezone
from rest_framework import generics, status, serializers
from rest_framework.response import Response

from .models import Project, Contract
from .serializers import ProjectSerializer, ContractSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContractList(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer


class ContractDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def update_contract_status(self, contract, new_status):
        if contract.status == new_status:
            raise serializers.ValidationError(
                {"error": f"Договор уже имеет статус {new_status}."}
            )
        contract.status = new_status
        contract.signed_date = timezone.now() if new_status == "Active" else None
        contract.save()

    def confirm_contract(self, request, *args, **kwargs):
        contract = self.get_object()
        if contract.status == "Draft":
            self.update_contract_status(contract, "Active")
            return Response({"message": "Договор подтвержден и активирован."})
        else:
            return Response(
                {"error": "Договор уже имеет другой статус."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def complete_contract(self, request, *args, **kwargs):
        contract = self.get_object()
        if contract.status == "Active":
            self.update_contract_status(contract, "Completed")
            return Response({"message": "Договор завершен."})
        else:
            return Response(
                {"error": 'Договор не в статусе "Active".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        project_id = request.data.get("project", None)
        if project_id is not None:
            project = Project.objects.filter(pk=project_id).first()
            if not project:
                return Response(
                    {"error": "Проект с таким ID не найден."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            active_contract = Contract.objects.filter(
                project=project, status="Active"
            ).first()
            if active_contract:
                return Response(
                    {"error": "Проект уже имеет активный договор."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            existing_contract = Contract.objects.filter(
                pk=serializer.validated_data["id"]
            ).first()
            if existing_contract and existing_contract.project != project:
                return Response(
                    {"error": "Договор уже используется в другом проекте."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            contract = Contract.objects.get(pk=serializer.data["id"])
            contract.project = project
            contract.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
