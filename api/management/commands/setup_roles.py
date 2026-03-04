from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand
from django.contrib.auth import get_user_model

from api.models import Order
from dotenv import load_dotenv
from pathlib import Path
import os

BASE_DIR=Path(__file__).resolve().parent.parent.parent.parent

load_dotenv(BASE_DIR / ".env")


class Command(BaseCommand):
    help = 'create default roles and assign permissions'
    def handle(self, *args, **options):
        User = get_user_model()

        order_ct = ContentType.objects.get_for_model(Order)
        user_ct = ContentType.objects.get_for_model(User)
        perms = {
            "Order.view": Permission.objects.get(codename="view_order", content_type=order_ct),
            "Order.change": Permission.objects.get(codename="change_order", content_type=order_ct),
            "Order.delete": Permission.objects.get(codename="delete_order", content_type=order_ct),
            "Order.add": Permission.objects.get(codename="add_order", content_type=order_ct),
            "User.change": Permission.objects.get(codename="change_user", content_type=user_ct),
        }

        role_map={
            "Admin": list(perms.values()),
            "Manager": [
                perms["Order.view"],
                perms["Order.change"],
                perms["Order.add"],
                perms["User.change"],
            ],
            "User":[
                perms["Order.view"],
                perms["Order.add"]
            ],
            "Guest":[
                perms["Order.view"],
            ]
        }

        for role_name, permissions in role_map.items():
            group, _ = Group.objects.get_or_create(name=role_name)
            group.permissions.add(*permissions)
            group.save()
            self.stdout.write(self.style.SUCCESS(f"Role '{role_name}' created"))

        admin_username="admin"
        admin_email="admin@example.com"
        admin_password=os.getenv("PASSWORD")
        self.stdout.write(self.style.SUCCESS(f"password: {admin_password}"))

        admin_user, created = User.objects.get_or_create(username=admin_username, email=admin_email)

        if created:
            admin_user.set_password(admin_password)
            # admin_user.is_staff = True
            # admin_user.is_superuser = True
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"Admin user '{admin_username}' created"))

        admin_group = Group.objects.get(name="Admin")
        admin_user.groups.add(admin_group)
        self.stdout.write(self.style.SUCCESS(f"Admin user assigned to Admin group"))