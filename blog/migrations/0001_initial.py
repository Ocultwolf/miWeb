from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=160)),
                ('slug', models.SlugField(unique=True)),
                ('excerpt', models.CharField(max_length=260)),
                ('content', models.TextField()),
                ('cover_label', models.CharField(blank=True, max_length=80)),
                ('published_at', models.DateTimeField()),
                ('published', models.BooleanField(default=True)),
            ],
            options={'ordering': ['-published_at']},
        ),
    ]
