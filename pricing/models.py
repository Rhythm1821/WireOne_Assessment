from django.db import models
from django.db.models.signals import post_save,pre_save,pre_delete
from django.dispatch import receiver

# Create your models here.
class PricingConfig(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    base_distance_price = models.DecimalField(max_digits=6, decimal_places=2)
    base_distance_limit = models.DecimalField(max_digits=4, decimal_places=1)
    additional_price_per_km = models.DecimalField(max_digits=4, decimal_places=2)
    time_multiplier_factor = models.DecimalField(max_digits=3, decimal_places=2)
    waiting_charge_per_minute = models.DecimalField(max_digits=3, decimal_places=2)
    enabled = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.day_of_week} - Base Price: {self.base_distance_price}'
    
class PricingConfigLog(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.SET_NULL,null=True)
    modified_by = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
    changes = models.TextField(max_length=255)

    config_day_of_week = models.CharField(max_length=3, null=True, blank=True)
    config_base_distance_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f'{self.config_day_of_week} - {self.action} at {self.timestamp}'
    
@receiver(post_save, sender=PricingConfig)
def log_pricing_config_changes(sender, instance, created, **kwargs):
    if created:
        action = "Created"
        changes = "Instance Created"
    else:
        action = "Updated"
        old_data = instance._old_data
        changes = {}

        if old_data:
            for field in instance._meta.fields:
                field_name = field.name
                old_value = old_data.get(field_name)
                new_value = getattr(instance, field_name)

                if old_value != new_value:
                    changes[field_name] = {'old_value': old_value, 'new_value': new_value}

    modified_by = "System"
    
    PricingConfigLog.objects.create(
        config=instance,
        modified_by=modified_by,
        action=action,
        changes=changes if changes else "No Changes",
        config_day_of_week=instance.day_of_week,
        config_base_distance_price=instance.base_distance_price,
    )

@receiver(pre_delete, sender=PricingConfig)
def log_pricing_config_delete(sender, instance, **kwargs):
    modified_by = "System"  # Replace with actual user if available

    PricingConfigLog.objects.create(
        config=instance,
        modified_by=modified_by,
        action='Deleted',
        changes="Instance Deleted",
        config_day_of_week=instance.day_of_week,
        config_base_distance_price=instance.base_distance_price,
    )