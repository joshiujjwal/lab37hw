from django.contrib import admin
from .models import Restaurant, UserProfile, Ingredient, Recipe, RecipeIngredient

# This allows managing models from the Django admin interface.
admin.site.register(Restaurant)
admin.site.register(UserProfile)
admin.site.register(Ingredient)

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1 # Show one extra blank ingredient form

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)
    list_display = ('title', 'restaurant', 'updated_at')
    list_filter = ('restaurant',)