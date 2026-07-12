import html.parser

class Checker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
        self.stack = []
        self.void = {'img','br','hr','input','meta','link','area','base','col','embed','source','track','wbr'}
    def handle_starttag(self, tag, attrs):
        if tag not in self.void:
            self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag in self.void: return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            self.errors.append(f'Mismatched </{tag}> at line {self.getpos()[0]}')

for f in ['index.html','news.html','team.html','publications.html','contact.html']:
    c = Checker()
    c.feed(open(f).read())
    if c.errors:
        print(f'{f}: ERRORS')
        for e in c.errors: print(f'  {e}')
    elif c.stack:
        print(f'{f}: Unclosed tags:')
        for t in c.stack: print(f'  <{t[0]}> at line {t[1][0]}')
    else:
        print(f'{f}: OK')