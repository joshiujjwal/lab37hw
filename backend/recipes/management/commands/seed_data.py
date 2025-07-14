from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from recipes.models import Restaurant, UserProfile, Ingredient, Recipe, RecipeIngredient

class Command(BaseCommand):
    help = 'Seeds the database with sample data for restaurants, users, and recipes.'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        # Clear existing data to prevent duplicates
        models = [RecipeIngredient, Recipe, Ingredient, UserProfile, Restaurant, User]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        # --- Create Restaurants ---
        r1 = Restaurant.objects.create(name="Nonna's Pizzeria")
        r2 = Restaurant.objects.create(name="The Sizzling Grill")
        self.stdout.write(f"Created restaurants: {r1.name}, {r2.name}")

        # --- Create Users and Profiles ---
        # User for Nonna's Pizzeria
        user1 = User.objects.create_user(username='chef_tony', password='password123', first_name='Tony', last_name='Soprano')
        UserProfile.objects.create(user=user1, restaurant=r1)
        
        # User for The Sizzling Grill
        user2 = User.objects.create_user(username='grillmaster_glen', password='password123', first_name='Glen', last_name='Garry')
        UserProfile.objects.create(user=user2, restaurant=r2)
        self.stdout.write(f"Created users: {user1.username}, {user2.username}")

        # --- Create Ingredients ---
        i_flour, _ = Ingredient.objects.get_or_create(name='All-Purpose Flour')
        i_tomato, _ = Ingredient.objects.get_or_create(name='San Marzano Tomatoes')
        i_mozzarella, _ = Ingredient.objects.get_or_create(name='Fresh Mozzarella')
        i_basil, _ = Ingredient.objects.get_or_create(name='Fresh Basil')
        i_olive_oil, _ = Ingredient.objects.get_or_create(name='Extra Virgin Olive Oil')
        i_salt, _ = Ingredient.objects.get_or_create(name='Salt')
        i_yeast, _ = Ingredient.objects.get_or_create(name='Active Dry Yeast')
        
        i_beef, _ = Ingredient.objects.get_or_create(name='Ground Beef')
        i_bun, _ = Ingredient.objects.get_or_create(name='Brioche Bun')
        i_cheddar, _ = Ingredient.objects.get_or_create(name='Cheddar Cheese')
        i_lettuce, _ = Ingredient.objects.get_or_create(name='Iceberg Lettuce')
        i_onion, _ = Ingredient.objects.get_or_create(name='Red Onion')
        i_pickle, _ = Ingredient.objects.get_or_create(name='Dill Pickles')
        self.stdout.write("Created common ingredients.")

        # --- Create Recipes ---
        # Recipe 1: Margherita Pizza for Nonna's Pizzeria
        pizza = Recipe.objects.create(
            title="Classic Margherita Pizza",
            instructions="1. Prepare dough and let it rise.\n2. Stretch dough and top with tomatoes, mozzarella, and basil.\n3. Bake at 250°C for 10-12 minutes.\n4. Drizzle with olive oil before serving.",
            yield_amount="1 12-inch pizza",
            restaurant=r1
        )
        RecipeIngredient.objects.create(recipe=pizza, ingredient=i_flour, quantity=250, unit='g')
        RecipeIngredient.objects.create(recipe=pizza, ingredient=i_tomato, quantity=200, unit='g')
        RecipeIngredient.objects.create(recipe=pizza, ingredient=i_mozzarella, quantity=125, unit='g')
        RecipeIngredient.objects.create(recipe=pizza, ingredient=i_basil, quantity=10, unit='g')
        RecipeIngredient.objects.create(recipe=pizza, ingredient=i_olive_oil, quantity=15, unit='ml')
        RecipeIngredient.objects.create(recipe=pizza, ingredient=i_salt, quantity=5, unit='g')
        RecipeIngredient.objects.create(recipe=pizza, ingredient=i_yeast, quantity=7, unit='g')

        # Recipe 2: Classic Cheeseburger for The Sizzling Grill
        burger = Recipe.objects.create(
            title="The Classic Cheeseburger",
            instructions="1. Form ground beef into 1/3-pound patties.\n2. Grill patties for 3-4 minutes per side for medium-rare.\n3. Top with cheddar cheese in the last minute of cooking.\n4. Serve on a toasted brioche bun with lettuce, onion, and pickles.",
            yield_amount="1 burger",
            restaurant=r2
        )
        RecipeIngredient.objects.create(recipe=burger, ingredient=i_beef, quantity=0.33, unit='lb')
        RecipeIngredient.objects.create(recipe=burger, ingredient=i_bun, quantity=1, unit='count')
        RecipeIngredient.objects.create(recipe=burger, ingredient=i_cheddar, quantity=1, unit='slice')
        RecipeIngredient.objects.create(recipe=burger, ingredient=i_lettuce, quantity=2, unit='leaves')
        RecipeIngredient.objects.create(recipe=burger, ingredient=i_onion, quantity=3, unit='rings')
        RecipeIngredient.objects.create(recipe=burger, ingredient=i_pickle, quantity=4, unit='slices')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))