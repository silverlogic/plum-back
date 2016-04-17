'''
isort:skip_file
'''

from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

# Login / Register
from .login.views import LoginViewSet  # noqa
from .register.views import RegisterViewSet  # noqa

router.register('login', LoginViewSet, base_name='login')
router.register(r'register', RegisterViewSet, base_name='register')

# Users
from .users.views import UsersViewSet  # noqa

router.register(r'users', UsersViewSet, base_name='users')

# Cards
from .cards.views import CardsViewSet, RulesViewSet, TransfersViewSet  # noqa

router.register(r'cards', CardsViewSet, base_name='cards')
router.register(r'rules', RulesViewSet, base_name='rules')
router.register(r'transfers', TransfersViewSet, base_name='transfers')

# Family
from .kids.views import KidsViewSet  # noqa

router.register(r'kids', KidsViewSet, base_name='kids')
