from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(unique=True)),
                ('short_description', models.CharField(max_length=220)),
                ('description', models.TextField()),
                ('technologies', models.CharField(max_length=220)),
                ('link', models.URLField(blank=True)),
                ('impact', models.CharField(blank=True, max_length=160)),
                ('featured', models.BooleanField(default=False)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['order', '-created_at']},
        ),
    ]
