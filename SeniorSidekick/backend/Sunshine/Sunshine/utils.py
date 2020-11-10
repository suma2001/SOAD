from api.serializers import ProfileSerializer, ElderProfileSerializer


def my_jwt_profile_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': ProfileSerializer(user, context={'request': request}).data
    }

def my_jwt_elder_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': ElderProfileSerializer(user, context={'request': request}).data
    }