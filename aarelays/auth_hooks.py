from django.utils.translation import ugettext_lazy as _

from allianceauth.services.hooks import MenuItemHook, UrlHook
from allianceauth import hooks

from . import urls


class AarelaysMenuItem(MenuItemHook):
    """ This class ensures only authorized users will see the menu entry """
    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _('aarelays'),
            'fa fa-cube fa-fw',
            'aarelays:index',
            navactive=['aarelays:index']
        )

    def render(self, request):
        if request.user.has_perm('aarelays.basic_access'):
            return MenuItemHook.render(self, request)
        return ''


@hooks.register('menu_item_hook')
def register_menu():
    return AarelaysMenuItem()


@hooks.register('url_hook')
def register_urls():
    return UrlHook(urls, 'aarelays', r'^aarelays/')