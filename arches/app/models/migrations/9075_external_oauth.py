# Generated by Django 2.2.24 on 2022-05-12 17:03

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ("models", "8974_rr_load_performance_v2"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExternalOauthToken",
            fields=[
                ("token_id", models.UUIDField(primary_key=True, serialize=False, unique=True)),
                ("user", models.ForeignKey(
                    db_column="userid", null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                )),
                ("id_token", models.TextField()),
                ("access_token", models.TextField()),
                ("access_token_expiration", models.DateTimeField(null=False)),
                ("refresh_token", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "external_oauth_tokens",
                "managed": True,
            },
        )
    ]