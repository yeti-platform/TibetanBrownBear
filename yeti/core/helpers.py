import re

def refang(url):

    def http(match):
        return "http{}".format(match.group('real'))

    substitutes = ('me[o0]w', 'h..p')
    schema_re = re.compile(
        "^(?P<fake>{})(?P<real>s?://)".format("|".join(substitutes)))
    domain_re = re.compile(r"(\[\.\]|,)")
    url = schema_re.sub(http, url)
    url = domain_re.sub(".", url)
    return url
