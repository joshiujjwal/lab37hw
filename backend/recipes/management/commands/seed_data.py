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

        # --- Create More Ingredients ---
        i_garlic, _ = Ingredient.objects.get_or_create(name='Garlic')
        i_parmesan, _ = Ingredient.objects.get_or_create(name='Parmesan Cheese')
        i_chicken, _ = Ingredient.objects.get_or_create(name='Chicken Breast')
        i_bbq_sauce, _ = Ingredient.objects.get_or_create(name='BBQ Sauce')
        i_pepper, _ = Ingredient.objects.get_or_create(name='Black Pepper')
        i_pasta, _ = Ingredient.objects.get_or_create(name='Spaghetti Pasta')
        i_butter, _ = Ingredient.objects.get_or_create(name='Butter')
        self.stdout.write("Created additional ingredients.")

        # --- More Recipes for Nonna's Pizzeria ---
        pasta = Recipe.objects.create(
            title="Garlic Parmesan Spaghetti",
            instructions="1. Cook spaghetti until al dente.\n2. Sauté garlic in butter, toss with pasta, and top with parmesan and black pepper.",
            yield_amount="2 servings",
            restaurant=r1
        )
        RecipeIngredient.objects.create(recipe=pasta, ingredient=i_pasta, quantity=200, unit='g')
        RecipeIngredient.objects.create(recipe=pasta, ingredient=i_garlic, quantity=2, unit='cloves')
        RecipeIngredient.objects.create(recipe=pasta, ingredient=i_butter, quantity=30, unit='g')
        RecipeIngredient.objects.create(recipe=pasta, ingredient=i_parmesan, quantity=40, unit='g')
        RecipeIngredient.objects.create(recipe=pasta, ingredient=i_pepper, quantity=2, unit='g')
        RecipeIngredient.objects.create(recipe=pasta, ingredient=i_salt, quantity=3, unit='g')

        # --- More Recipes for The Sizzling Grill ---
        bbq_chicken = Recipe.objects.create(
            title="BBQ Grilled Chicken",
            instructions="1. Marinate chicken in BBQ sauce.\n2. Grill chicken until cooked through.\n3. Serve with extra BBQ sauce.",
            yield_amount="1 serving",
            restaurant=r2
        )
        RecipeIngredient.objects.create(recipe=bbq_chicken, ingredient=i_chicken, quantity=1, unit='breast')
        RecipeIngredient.objects.create(recipe=bbq_chicken, ingredient=i_bbq_sauce, quantity=50, unit='ml')
        RecipeIngredient.objects.create(recipe=bbq_chicken, ingredient=i_salt, quantity=2, unit='g')
        RecipeIngredient.objects.create(recipe=bbq_chicken, ingredient=i_pepper, quantity=1, unit='g')

        # --- More Recipes for Nonna's Pizzeria ---
        # 1. Garlic Parmesan Spaghetti (already added above)
        # 2. Eggplant Parmigiana
        eggplant_parm = Recipe.objects.create(
            title="Eggplant Parmigiana",
            instructions="1. Slice and salt eggplant, let sit 30 min.\n2. Bread and fry slices.\n3. Layer with tomato sauce and mozzarella, bake until golden.",
            yield_amount="2 servings",
            restaurant=r1
        )
        i_eggplant, _ = Ingredient.objects.get_or_create(name='Eggplant')
        i_breadcrumbs, _ = Ingredient.objects.get_or_create(name='Breadcrumbs')
        RecipeIngredient.objects.create(recipe=eggplant_parm, ingredient=i_eggplant, quantity=1, unit='large')
        RecipeIngredient.objects.create(recipe=eggplant_parm, ingredient=i_tomato, quantity=150, unit='g')
        RecipeIngredient.objects.create(recipe=eggplant_parm, ingredient=i_mozzarella, quantity=100, unit='g')
        RecipeIngredient.objects.create(recipe=eggplant_parm, ingredient=i_breadcrumbs, quantity=50, unit='g')
        RecipeIngredient.objects.create(recipe=eggplant_parm, ingredient=i_olive_oil, quantity=20, unit='ml')
        RecipeIngredient.objects.create(recipe=eggplant_parm, ingredient=i_salt, quantity=3, unit='g')

        # 3. Chicken Alfredo Pizza
        chicken_alfredo_pizza = Recipe.objects.create(
            title="Chicken Alfredo Pizza",
            instructions="1. Stretch dough, spread with Alfredo sauce.\n2. Top with cooked chicken, mozzarella, and parmesan.\n3. Bake until crust is golden.",
            yield_amount="1 12-inch pizza",
            restaurant=r1
        )
        i_alfredo_sauce, _ = Ingredient.objects.get_or_create(name='Alfredo Sauce')
        RecipeIngredient.objects.create(recipe=chicken_alfredo_pizza, ingredient=i_flour, quantity=250, unit='g')
        RecipeIngredient.objects.create(recipe=chicken_alfredo_pizza, ingredient=i_chicken, quantity=100, unit='g')
        RecipeIngredient.objects.create(recipe=chicken_alfredo_pizza, ingredient=i_mozzarella, quantity=100, unit='g')
        RecipeIngredient.objects.create(recipe=chicken_alfredo_pizza, ingredient=i_parmesan, quantity=30, unit='g')
        RecipeIngredient.objects.create(recipe=chicken_alfredo_pizza, ingredient=i_alfredo_sauce, quantity=60, unit='g')
        RecipeIngredient.objects.create(recipe=chicken_alfredo_pizza, ingredient=i_olive_oil, quantity=10, unit='ml')

        # 4. Caprese Salad
        caprese = Recipe.objects.create(
            title="Caprese Salad",
            instructions="1. Slice tomatoes and mozzarella.\n2. Layer with basil leaves.\n3. Drizzle with olive oil and sprinkle with salt.",
            yield_amount="2 servings",
            restaurant=r1
        )
        RecipeIngredient.objects.create(recipe=caprese, ingredient=i_tomato, quantity=150, unit='g')
        RecipeIngredient.objects.create(recipe=caprese, ingredient=i_mozzarella, quantity=100, unit='g')
        RecipeIngredient.objects.create(recipe=caprese, ingredient=i_basil, quantity=10, unit='g')
        RecipeIngredient.objects.create(recipe=caprese, ingredient=i_olive_oil, quantity=10, unit='ml')
        RecipeIngredient.objects.create(recipe=caprese, ingredient=i_salt, quantity=2, unit='g')

        # --- More Recipes for The Sizzling Grill ---
        # 1. BBQ Grilled Chicken (already added above)
        # 2. Spicy Buffalo Wings
        buffalo_wings = Recipe.objects.create(
            title="Spicy Buffalo Wings",
            instructions="1. Fry chicken wings until crispy.\n2. Toss with buffalo sauce.\n3. Serve with celery and blue cheese dip.",
            yield_amount="8 wings",
            restaurant=r2
        )
        i_chicken_wings, _ = Ingredient.objects.get_or_create(name='Chicken Wings')
        i_buffalo_sauce, _ = Ingredient.objects.get_or_create(name='Buffalo Sauce')
        i_celery, _ = Ingredient.objects.get_or_create(name='Celery')
        i_blue_cheese, _ = Ingredient.objects.get_or_create(name='Blue Cheese')
        RecipeIngredient.objects.create(recipe=buffalo_wings, ingredient=i_chicken_wings, quantity=8, unit='count')
        RecipeIngredient.objects.create(recipe=buffalo_wings, ingredient=i_buffalo_sauce, quantity=50, unit='ml')
        RecipeIngredient.objects.create(recipe=buffalo_wings, ingredient=i_celery, quantity=2, unit='sticks')
        RecipeIngredient.objects.create(recipe=buffalo_wings, ingredient=i_blue_cheese, quantity=30, unit='g')

        # 3. Grilled Veggie Skewers
        veggie_skewers = Recipe.objects.create(
            title="Grilled Veggie Skewers",
            instructions="1. Skewer chopped veggies.\n2. Brush with olive oil, season with salt and pepper.\n3. Grill until tender.",
            yield_amount="2 skewers",
            restaurant=r2
        )
        i_bell_pepper, _ = Ingredient.objects.get_or_create(name='Bell Pepper')
        i_zucchini, _ = Ingredient.objects.get_or_create(name='Zucchini')
        i_mushroom, _ = Ingredient.objects.get_or_create(name='Mushroom')
        RecipeIngredient.objects.create(recipe=veggie_skewers, ingredient=i_bell_pepper, quantity=1, unit='count')
        RecipeIngredient.objects.create(recipe=veggie_skewers, ingredient=i_zucchini, quantity=1, unit='count')
        RecipeIngredient.objects.create(recipe=veggie_skewers, ingredient=i_mushroom, quantity=4, unit='count')
        RecipeIngredient.objects.create(recipe=veggie_skewers, ingredient=i_olive_oil, quantity=10, unit='ml')
        RecipeIngredient.objects.create(recipe=veggie_skewers, ingredient=i_salt, quantity=2, unit='g')
        RecipeIngredient.objects.create(recipe=veggie_skewers, ingredient=i_pepper, quantity=1, unit='g')

        # 4. Pulled Pork Sandwich
        pulled_pork = Recipe.objects.create(
            title="Pulled Pork Sandwich",
            instructions="1. Slow cook pork shoulder with BBQ sauce.\n2. Shred and serve on a bun with pickles and onions.",
            yield_amount="1 sandwich",
            restaurant=r2
        )
        i_pork_shoulder, _ = Ingredient.objects.get_or_create(name='Pork Shoulder')
        RecipeIngredient.objects.create(recipe=pulled_pork, ingredient=i_pork_shoulder, quantity=150, unit='g')
        RecipeIngredient.objects.create(recipe=pulled_pork, ingredient=i_bbq_sauce, quantity=40, unit='ml')
        RecipeIngredient.objects.create(recipe=pulled_pork, ingredient=i_bun, quantity=1, unit='count')
        RecipeIngredient.objects.create(recipe=pulled_pork, ingredient=i_pickle, quantity=3, unit='slices')
        RecipeIngredient.objects.create(recipe=pulled_pork, ingredient=i_onion, quantity=2, unit='rings')

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))