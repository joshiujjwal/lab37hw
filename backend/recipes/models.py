from django.db import models
from django.contrib.auth.models import User

# A simple model for multi-tenancy. Each user belongs to a restaurant.
class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# We can extend the default User model if needed, but for now, we'll just link it.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} at {self.restaurant.name}"

# Represents a single ingredient that can be used across many recipes.
class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# The main Recipe model.
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    yield_amount = models.CharField(max_length=100, help_text="e.g., '4 servings' or '1 large pizza'")
    # Each recipe is owned by a restaurant to enforce data separation.
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# This is a "through" model to link Recipes and Ingredients with extra data.
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT) # Don't delete ingredient if used in recipe
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, help_text="e.g., 'grams', 'cups', 'tbsp'")

    class Meta:
        unique_together = ('recipe', 'ingredient') # Can't have the same ingredient twice in one recipe

    def __str__(self):
        return f"{self.quantity} {self.unit} of {self.ingredient.name}"

