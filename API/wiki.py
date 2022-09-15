import wikipedia
import re

wikipedia.set_lang("uk")

def get_wiki(s):
    text = wikipedia.page(s)
    content = text.content[:1000]
    content = content.split('.')
    content = content[:-1]
    wikitext = ''

    for x in content:
        if not('==' in x):
            if(len((x.strip()))>3):
                wikitext+=(x+'.')
        else:
            break

    wikitext=re.sub('\\([^()]*\\)', '', wikitext)
    wikitext=re.sub('\\([^()]*\\)', '', wikitext)
    wikitext=re.sub('\\{[^\\{\\}]*\\}', '', wikitext)

    return wikitext