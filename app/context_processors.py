from.forms import TweetSearchForm

def search_form(request):
    return {'serch_form': TweetSearchForm()}