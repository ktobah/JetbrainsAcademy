class Painting:
    museum = "Louvre"
    def __init__(self, title, painter, year):
        self.title = title
        self.painter = painter
        self.year = year

title_sub = input()
painter_name = input()
year_created = int(input())
paint = Painting(title_sub, painter_name, year_created)
print(f'"{paint.title}" by {paint.painter} ({paint.year}) hangs in the Louvre.')