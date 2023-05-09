from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

""" Arquivo feito para conseguir logar com o e-mail """

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            raise ValidationError('O usuário não existe.')

        if user.check_password(password):
            return user
        else:
            raise ValidationError('Senha incorreta.')
