from django.contrib import admin
from .models import PricingConfig, PricingConfigLog

# Register your models here.
@admin.register(PricingConfig)
class PricingConfigAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'base_distance_price', 'additional_price_per_km','time_multiplier_factor', 'enabled')
    list_filter = ('day_of_week', 'enabled')
    search_fields = ('day_of_week', )

    def save_model(self,request,obj,form,change):
        super().save_model(request,obj,form,change)

        PricingConfigLog.objects.create(
            config=obj,
            modified_by=request.user.username,
            action='Updated' if change else 'Created'
        )
    
    def delete_model(self,request,obj):
        PricingConfigLog.objects.create(
            config=obj,
            modified_by=request.user.username,
            action='Deleted'
        )

        super().delete_model(request,obj)


@admin.register(PricingConfigLog)
class PricingConfigLogAdmin(admin.ModelAdmin):
    list_display = ('config', 'timestamp', 'action', 'modified_by')
    readonly_fields = ('timestamp', )
    search_fields = ('modified_by', )