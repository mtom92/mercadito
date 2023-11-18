from django.http import HttpResponse
import json


def get_for_category(request):
    # json_data = json.loads(request.body)
    # category = json_data.get('category', '')

    response = HttpResponse()
    response.content_type = 'application/json'
    response.status_code = 200
    response.content = json.dumps({
        'checklist': {
            'requirements': [{
                'business_license': {
                    'display_text': 'Business License',
                    'more_info_api_url': 'checklist/step/food?req=business_license',
                }
            }],
            'category': 'food',
        }
    })

    return response
