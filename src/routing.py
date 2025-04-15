import flet_route
from flet_route.params import Params
from flet_route.routing import route_str
from repath import match


class Routing(flet_route.Routing):
    def change_route(self, route):
        notfound = True
        for url in self.app_routes:
            path_match = match(url[0], self.page.route)
            if path_match:
                self.__params = Params(path_match.groupdict())
                if self.__middleware != None:
                    self.__middleware(page=self.page, params=self.__params, basket=self.__basket)
                # if chnge route using main midellware recall change route
                if self.page.route != route_str(route=route):
                    self.page.go(self.page.route)
                    return

                if url[3] != None:
                    url[3](page=self.page, params=self.__params, basket=self.__basket)

                # if chnge route using url midellware recall change route
                if self.page.route != route_str(route=route):
                    self.page.go(self.page.route)
                    return

                if url[1]:
                    self.page.views.clear()
                view = url[2](
                    page=self.page,
                    params=self.__params,
                    basket=self.__basket
                )
                if not hasattr(view, 'appbar'):
                    view.appbar = self.appbar
                if not hasattr(view, 'navigation_bar'):
                    view.navigation_bar = self.navigation_bar
                self.page.views.append(view)
                notfound = False
                break
        if notfound:
            self.__params = Params({"url": self.page.route})
            self.page.views.append(self.not_found_view(page=self.page, params=self.__params, basket=self.__basket))
        self.page.update()
