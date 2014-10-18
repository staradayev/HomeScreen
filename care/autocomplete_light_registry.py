import autocomplete_light

from models import Category

class CategoryAutocomplete(autocomplete_light.AutocompleteModelBase):
	search_fields = ['^category_name']
	autocomplete_js_attributes={'placeholder': 'Type category here...',}
	model = Category

autocomplete_light.register(Category, CategoryAutocomplete)