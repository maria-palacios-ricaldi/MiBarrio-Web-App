# MiBarrioApp/context_processors.py
def show_user_info(request):
    # List of URL names where user-info should be displayed
    user_info_pages = [
        'home', 'profile', 'newSearch', 'newSearch2', 'newSearch3',
        'viewPastSearches', 'feedback'
    ]
    return {
        'show_user_info': request.resolver_match.url_name in user_info_pages
    }
