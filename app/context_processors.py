from.forms import TweetSearchForm

def search_form(request):
    return {'search_form': TweetSearchForm()}