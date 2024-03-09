from django.shortcuts import redirect


class SiteWidePasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Paths that don't require the site-wide password
        allowed_paths = ['/login/', '/static/']  # Include any other paths as needed
        if request.path in allowed_paths or request.session.get('authenticated', False):
            response = self.get_response(request)
        else:
            return redirect('site_wide_login')
        return response
