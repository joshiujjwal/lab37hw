from rest_framework import viewsets, permissions
from rest_framework.filters import SearchFilter
from .models import Recipe
from .serializers import RecipeDetailSerializer, RecipeListSerializer

# Custom permission to only allow users to see recipes from their own restaurant.
class IsOwnerOfRecipe(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'profile'):
            return obj.restaurant == request.user.profile.restaurant
        return False

class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows recipes to be viewed or edited.
    Includes search functionality on title and ingredients.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfRecipe]
    
    # --- SEARCH CONFIGURATION ---
    filter_backends = [SearchFilter]
    search_fields = ['title', 'ingredients__ingredient__name'] # Search by recipe title or ingredient name

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
            # The queryset is now automatically filtered by SearchFilter if a 'search' query param is present
            return Recipe.objects.filter(restaurant=restaurant).order_by('-updated_at').distinct()
        return Recipe.objects.none()

    def perform_create(self, serializer):
        """
        Assign the user's restaurant to the recipe when it's created.
        """
        restaurant = self.request.user.profile.restaurant
        serializer.save(restaurant=restaurant)
