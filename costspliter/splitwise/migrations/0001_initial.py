# Generated by Django 4.2.5 on 2023-09-30 07:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "user_id",
                    models.CharField(
                        default=uuid.UUID("bc72fb5e-f85a-407c-b06e-7dd9b6e1b254"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField()),
                ("email", models.EmailField(max_length=254)),
                ("mobile", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Expense",
            fields=[
                (
                    "expense_id",
                    models.CharField(
                        default=uuid.UUID("4d53b9a2-c1b3-482b-812a-0590920e1bc5"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.IntegerField()),
                ("expense_type", models.CharField()),
                ("expense_name", models.CharField()),
                ("notes", models.CharField(blank=True, null=True)),
                ("images", models.CharField(blank=True, null=True)),
                (
                    "payer_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="splitwise.user"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Balance",
            fields=[
                (
                    "balance_id",
                    models.CharField(
                        default=uuid.UUID("118cf470-a9d8-46c6-b2d5-cfa875a2fe1a"),
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.FloatField()),
                (
                    "creditor_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="u2",
                        to="splitwise.user",
                    ),
                ),
                (
                    "debtor_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="u1",
                        to="splitwise.user",
                    ),
                ),
            ],
        ),
    ]