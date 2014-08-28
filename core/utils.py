from django.core.files.base import ContentFile
from requests import request, HTTPError


def save_user_profile(strategy, user, response, details, is_new, *args, **kwargs):
    """
    Save user avatar using python-social-auth
    """
    print("getting social avatar...")
    url = None
    full_name = ''
    if strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
        full_name = response["first_name"] + " " + response["last_name"]
        print(full_name)

    elif strategy.backend.name == 'google-oauth2':
        url = response["image"]["url"]
        full_name = response["displayName"]
        pass
    elif strategy.backend.name == 'twitter':
        url = response["profile_image_url"]
        full_name = response["name"]

    if url:
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            user.profile_picture.save('{0}_social.jpg'.format(user.username), ContentFile(response.content))
            user.full_name = full_name
            user.save()

def avatar_file_name(instance, filename):
    return '/'.join(['avatar', instance.username, filename])