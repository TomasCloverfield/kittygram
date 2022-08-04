# Generated by Django 4.1 on 2022-08-04 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cats', '0005_achievement_achievementcat'),
    ]

    operations = [
        migrations.AddField(
            model_name='cat',
            name='achievements',
            field=models.ManyToManyField(through='cats.AchievementCat', to='cats.achievement'),
        ),
        migrations.AlterField(
            model_name='cat',
            name='color',
            field=models.CharField(choices=[('Gray', 'Серый'), ('Black', 'Чёрный'), ('White', 'Белый'), ('Ginger', 'Рыжий'), ('Mixed', 'Смешанный')], max_length=16),
        ),
    ]
