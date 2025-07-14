from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Restaurant, UserProfile, Recipe, Ingredient, RecipeIngredient

class RecipeAPITests(APITestCase):
    """
    Test suite for the Recipe API.
    """

    def setUp(self):
        """
        Set up the necessary objects for the tests.
        This runs before every single test method.
        """
        # Create two separate restaurants and users
        self.restaurant1 = Restaurant.objects.create(name="Pizza Palace")
        self.user1 = User.objects.create_user(username='user1', password='password123')
        UserProfile.objects.create(user=self.user1, restaurant=self.restaurant1)

        self.restaurant2 = Restaurant.objects.create(name="Burger Barn")
        self.user2 = User.objects.create_user(username='user2', password='password123')
        UserProfile.objects.create(user=self.user2, restaurant=self.restaurant2)

        # Create a recipe for the first restaurant
        self.recipe1 = Recipe.objects.create(
            title="Margherita Pizza",
            instructions="1. Add sauce. 2. Add cheese.",
            yield_amount="1 pizza",
            restaurant=self.restaurant1
        )
        # Add ingredients to the recipe
        self.flour = Ingredient.objects.create(name="Flour")
        self.cheese = Ingredient.objects.create(name="Cheese")
        RecipeIngredient.objects.create(recipe=self.recipe1, ingredient=self.flour, quantity=500, unit="grams")
        RecipeIngredient.objects.create(recipe=self.recipe1, ingredient=self.cheese, quantity=200, unit="grams")

        # Authenticate the client for user1
        self.client.force_authenticate(user=self.user1)

    def test_unauthenticated_access(self):
        """
        Ensure unauthenticated users cannot access any recipe endpoint.
        """
        self.client.force_authenticate(user=None) # Log out
        response = self.client.get('/api/recipes/', format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_recipes(self):
        """
        Ensure a user can list recipes from their own restaurant.
        """
        response = self.client.get('/api/recipes/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Should only see one recipe
        self.assertEqual(response.data[0]['title'], self.recipe1.title)

    def test_retrieve_own_recipe(self):
        """
        Ensure a user can retrieve a specific recipe from their own restaurant.
        """
        response = self.client.get(f'/api/recipes/{self.recipe1.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.recipe1.title)
        self.assertEqual(len(response.data['ingredients']), 2)

    def test_cannot_retrieve_other_restaurant_recipe(self):
        """
        Ensure a user cannot retrieve a recipe from a different restaurant.
        """
        # Create a recipe for the second restaurant
        other_recipe = Recipe.objects.create(
            title="Classic Burger",
            instructions="Cook patty, assemble burger.",
            yield_amount="1 burger",
            restaurant=self.restaurant2
        )
        # User1 (from Pizza Palace) tries to access the recipe from Burger Barn
        response = self.client.get(f'/api/recipes/{other_recipe.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_recipe(self):
        """
        Ensure a user can create a new recipe for their restaurant.
        """
        data = {
            "title": "Garlic Bread",
            "instructions": "Bake it.",
            "yield_amount": "4 pieces",
            "ingredients": [
                {"name": "Bread", "quantity": 1, "unit": "loaf"},
                {"name": "Garlic", "quantity": 2, "unit": "cloves"}
            ]
        }
        response = self.client.post('/api/recipes/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Should be 2: one from setUp and the one created in this test.
        self.assertEqual(Recipe.objects.count(), 2)
        
        # Verify the new recipe is linked to the correct restaurant
        new_recipe = Recipe.objects.get(id=response.data['id'])
        self.assertEqual(new_recipe.restaurant, self.restaurant1)
        self.assertEqual(new_recipe.ingredients.count(), 2)


    def test_update_recipe(self):
        """
        Ensure a user can update their own recipe.
        """
        updated_data = {
            "title": "Super Margherita Pizza",
            "instructions": "1. Add sauce. 2. Add lots of cheese.",
            "yield_amount": "1 large pizza",
            "ingredients": [
                {"name": "Flour", "quantity": 600, "unit": "grams"}
            ]
        }
        response = self.client.put(f'/api/recipes/{self.recipe1.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.recipe1.refresh_from_db()
        self.assertEqual(self.recipe1.title, "Super Margherita Pizza")
        self.assertEqual(self.recipe1.ingredients.count(), 1) # Old ingredients are replaced
        self.assertEqual(self.recipe1.ingredients.first().quantity, 600)
    
    def test_cannot_update_other_restaurant_recipe(self):
        """
        Ensure a user cannot update a recipe from another restaurant.
        """
        other_recipe = Recipe.objects.create(
            title="Burger", restaurant=self.restaurant2
        )
        response = self.client.put(f'/api/recipes/{other_recipe.id}/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_recipe(self):
        """
        Ensure a user can delete their own recipe.
        """
        response = self.client.delete(f'/api/recipes/{self.recipe1.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.recipe1.id).exists())

    def test_cannot_delete_other_restaurant_recipe(self):
        """
        Ensure a user cannot delete a recipe from another restaurant.
        """
        other_recipe = Recipe.objects.create(
            title="Burger", restaurant=self.restaurant2
        )
        response = self.client.delete(f'/api/recipes/{other_recipe.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)