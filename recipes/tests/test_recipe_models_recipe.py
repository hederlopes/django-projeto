from .test_recipe_base import RecipeTestBase
from parameterized import parameterized
from django.core.exceptions import ValidationError
from recipes.models import Recipe



class RecipeModelTest(RecipeTestBase):  
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='Teste Default category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_step='Recipe Preparation Steps',            
          )
        recipe.full_clean()
        recipe.save()
        return recipe
    
   
    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe,field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):            
            self.recipe.full_clean() # aqui ocorre a validação
    
    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.preparation_step_is_html,
            msg='Recipe preparation_step_is_html is not False',
            )
    
    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()
        recipe.full_clean()
        recipe.save()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False',
            )
        
    def test_recipe_string_representation(self):
        needed = 'Testing Representation'
        self.recipe.title = 'Testing Representation'
        self.recipe.full_clean()
        self.recipe.save()
        
        self.assertEquals(
            str(self.recipe), needed,
            msg= f'Recipe string representation must be '\
                  f'"{needed}" but "{str(self.recipe)}" was received')
