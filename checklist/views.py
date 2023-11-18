from django.http import HttpResponse
import json

from django.shortcuts import render


class RequirementItem:
    def __init__(self, name, display_text, description, more_info):
        self.name = name
        self.display_text = display_text
        self.description = description
        self.more_info = more_info


food_items = [
    RequirementItem(
        'business_license',
        'Business License',
        'Business license required by the WA govt',
        'checklist/step/food?req=business_license',
    ),
    RequirementItem(
        'revenue_license',
        'Revenue License',
        'License required by the IRS',
        'checklist/step/food?req=business_license',
    ),
]

construction_items = [
    RequirementItem(
        'business_license',
        'Business License',
        'Business license required by the WA govt',
        'checklist/step/food?req=business_license',
    ),
]

items_per_category = {
    'food': food_items,
    'construction': construction_items,
}


def get_for_category(request):
    content = {}
    if request.body:
        content = json.loads(request.body)
    category = content.get('category', 'food')
    
    checklist = {
        'requirements':
            [{
                'name': req.name,
                'display_text': req.display_text,
                'description': req.description,
                'more_info_api_url': req.more_info,
            } for req in items_per_category.get(category, '')],
        'category': category,
    }

    return render(request, 'checklist.html', {'checklist': checklist})
