from rest_framework import viewsets, permissions
from .models import Recipe
from .serializers import RecipeDetailSerializer, RecipeListSerializer

# Custom permission to only allow users to see recipes from their own restaurant.
class IsOwnerOfRecipe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # A user's profile must be linked to the same restaurant as the recipe.
        # Handle cases where profile might not exist for a user.
        if hasattr(request.user, 'profile'):
            return obj.restaurant == request.user.profile.restaurant
        return False

class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfRecipe]

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeListSerializer
        return RecipeDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all the recipes
        for the currently authenticated user's restaurant.
        """
        user = self.request.user
        if hasattr(user, 'profile'):
            restaurant = user.profile.restaurant
            return Recipe.objects.filter(restaurant=restaurant).order_by('-updated_at')
        # Return an empty queryset if the user has no profile/restaurant
        return Recipe.objects.none()

    def perform_create(self, serializer):
        """
        Assign the user's restaurant to the recipe when it's created.
        """
        restaurant = self.request.user.profile.restaurant
        serializer.save(restaurant=restaurant)