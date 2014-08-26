from django.core.files.base import ContentFile
from social.pipeline.user import get_username as social_get_username
from requests import request, HTTPError


def get_username(strategy, details, user=None, *args, **kwargs):
    """
    Returns username without hash using python-social-auth
    """
    result = social_get_username(strategy, details, user=user, *args, **kwargs)
    return result


def save_user_avatar(strategy, user, response, details, is_new, *args, **kwargs):
    """
    Save user avatar using python-social-auth
    """
    url = ''
    if strategy.backend.name == 'facebook':
        url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
    #elif strategy.backend.name == 'google':
        #url = response["picture"]
    elif strategy.backend.name == 'twitter':
        url = response["profile_image_url"]

    if url:
        try:
            response = request('GET', url, params={'type': 'large'})
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            user.profile_picture.save('{0}_social.jpg'.format(user.username), ContentFile(response.content))
            user.save()
