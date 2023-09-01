import os
import sys
from django.utils import timezone

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "contract_manager"))
)
os.environ["DJANGO_SETTINGS_MODULE"] = "contract_manager.settings"

import django

django.setup()

from main.models import Project, Contract


def create_project():
    name = input("Введите название проекта: ")
    project = Project.objects.create(name=name)
    print(f"Проект '{project.name}' создан.")


def create_contract():
    name = input("Введите название договора: ")
    contract = Contract.objects.create(name=name)
    print(f"Договор '{contract.name}' создан.")


def confirm_contract():
    contracts = Contract.objects.filter(status="Draft")
    if not contracts.exists():
        print("Нет доступных договоров для подтверждения.")
        return

    print("Доступные договоры для подтверждения:")
    for idx, contract in enumerate(contracts):
        print(f"{idx + 1}. {contract.name}")

    choice = input("Выберите номер договора для подтверждения: ")
    try:
        idx = int(choice) - 1
        contract = contracts[idx]
        contract.status = "Active"
        contract.signed_date = timezone.now()
        contract.save()
        print(f"Договор '{contract.name}' подтвержден.")
    except (ValueError, IndexError):
        print("Некорректный выбор или договор не существует.")


def complete_contract():
    contracts = Contract.objects.filter(status="Active")
    if not contracts.exists():
        print("Нет активных договоров для завершения.")
        return

    print("Активные договоры для завершения:")
    for idx, contract in enumerate(contracts):
        print(f"{idx + 1}. {contract.name}")

    choice = input("Выберите номер договора для завершения: ")
    try:
        idx = int(choice) - 1
        contract = contracts[idx]
        contract.status = "Completed"
        contract.save()
        print(f"Договор '{contract.name}' завершен.")
    except (ValueError, IndexError):
        print("Некорректный выбор или договор не существует.")


def view_projects():
    projects = Project.objects.all()
    if not projects.exists():
        print("Нет проектов.")
        return

    print("Список проектов:")
    for project in projects:
        print(f"{project.name}")


def view_contracts():
    contracts = Contract.objects.all()
    if not contracts.exists():
        print("Нет договоров.")
        return

    print("Список договоров:")
    for contract in contracts:
        print(f"{contract.name}")


def main():
    while True:
        print("1. Создать проект")
        print("2. Создать договор")
        print("3. Подтвердить договор")
        print("4. Завершить договор")
        print("5. Просмотреть список проектов")
        print("6. Просмотреть список договоров")
        print("7. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            create_project()
        elif choice == "2":
            create_contract()
        elif choice == "3":
            confirm_contract()
        elif choice == "4":
            complete_contract()
        elif choice == "5":
            view_projects()
        elif choice == "6":
            view_contracts()
        elif choice == "7":
            break
        else:
            print("Некорректный выбор.")


if __name__ == "__main__":
    main()
