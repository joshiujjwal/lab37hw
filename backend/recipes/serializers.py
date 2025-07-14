from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient, Restaurant, UserProfile
from django.contrib.auth.models import User
from django.db import transaction

# Serializer for the Ingredient model
class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

# Serializer for the RecipeIngredient "through" model
class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name')

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'quantity', 'unit']

# Serializer for the main Recipe model (for detail view)
class RecipeDetailSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'instructions', 'yield_amount', 'ingredients', 'updated_at']
    
    # We need to handle the creation of nested ingredients
    @transaction.atomic
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            ingredient_name = ingredient_data['ingredient']['name']
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=ingredient_data['quantity'],
                unit=ingredient_data['unit']
            )
        return recipe

    # We also need to handle updates for nested ingredients
    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients', None)
        
        # Update the recipe instance fields
        instance.title = validated_data.get('title', instance.title)
        instance.instructions = validated_data.get('instructions', instance.instructions)
        instance.yield_amount = validated_data.get('yield_amount', instance.yield_amount)
        instance.save()

        # Handle nested ingredients update
        if ingredients_data is not None:
            # Clear old ingredients
            instance.ingredients.all().delete()
            # Create new ones
            for ingredient_data in ingredients_data:
                ingredient_name = ingredient_data['ingredient']['name']
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
                RecipeIngredient.objects.create(
                    recipe=instance,
                    ingredient=ingredient,
                    quantity=ingredient_data['quantity'],
                    unit=ingredient_data['unit']
                )
        return instance


# A simpler serializer for list view
class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'yield_amount']