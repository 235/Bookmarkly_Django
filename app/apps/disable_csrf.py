""" Disables CSRF for the whole project to simplify prototyping, unsecure in production """


class DisableCSRF(object):
    #def process_view(self, request, callback, callback_args, callback_kwargs):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)
