






from django.utils.deprecation import MiddlewareMixin
from basket.models import Basket
from django.contrib.sessions.models import Session
from blog.models import Category, Article
#from newsletter.forms import SubscribersForm
#from .forms import LoginForm , RegisterForm
#from .forms import SearchForm


class BasketMiddleware(MiddlewareMixin):

    def process_request(self, request):

        #loginForm=LoginForm()
        #subscribersForm = SubscribersForm()
        #searchForm = SearchForm()
        
        request.notificati= Article.objects.get(notification='True')

        if not request.user.is_authenticated:
            request.user.is_vendor = False

        if not request.session.session_key:
            request.session.create()
            session = Session.objects.get(pk=request.session.session_key)
            request.basket = Basket.objects.create(session=session)
            request.basket_size = request.basket.order_set.filter(finished=False).count()
        else:
            session = Session.objects.get(pk=request.session.session_key)
            request.basket = Basket.objects.get(session=session)
            request.basket_size = request.basket.order_set.filter(finished=False).count()

        #return request
    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie or delete
        the session cookie if the session has been emptied.
        """

        return response