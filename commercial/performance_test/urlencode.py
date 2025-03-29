import re

def urlencode(query):
    encodes = {
        '{': '%7B',
        '}': '%7D',
        '[': '%5B',
        ']': '%5D',
        ',': '%2C'
    }

    for k,v in encodes.items():
        query = query.replace(k, v)
    return(query)

def main():
    pattern = 'params=\{(.*)\}$'
    repatter = re.compile(pattern)

    with open('solr.log') as f:
        for l in f.readlines():
            if "/select" in l:
                for content in l.split():
                    if "params" in content and not "shard.url" in content:
                        result = repatter.findall(content)
                        print(urlencode(result[0]))

if __name__ == '__main__':
    main()