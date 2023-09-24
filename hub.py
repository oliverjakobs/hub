import tomllib
from itertools import islice

TEMPLATE = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="css/style.css" />
  <title>{title}</title>
</head>
<body>
  <div class="container">
    {content}
  </div>
</body>
</html>
"""
def batched(iterable, chunk_size):
    iterator = iter(iterable)
    while chunk := tuple(islice(iterator, chunk_size)):
        yield chunk

def build_card(title, data):
    with open(data['icon'], 'r') as f:
        icon = f.read()

    return f"""
      <a class="card" href="{data['link']}">
        <div class="icon">{icon}</div>
        <div class="title">{title}</div>
      </a>
      """

def build_row(cards):
    return f"""
    <div class="row">
      {"".join(cards)}
    </div>
    """

def build_content(path, rows):
    with open(path, 'rb') as f:
        data = tomllib.load(f)
    cards = [build_card(title, data[title]) for title in data]
    return "".join([build_row(row) for row in batched(cards, rows)])

def build_hub(rows):
    config = {
        'title': "{ oliver.jakobs } hub",
        'content': build_content("hub.toml", rows)
    }

    with open("index.html", 'w') as f:
        f.write(TEMPLATE.format(**config))

if __name__ == '__main__':
    build_hub(4)