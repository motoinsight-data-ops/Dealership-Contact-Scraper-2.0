from collections import Counter

l = ['c','a','a','c','','c', 'b', 'b', 'c']

c = Counter(l)

g = c.most_common(1)[0][0]

print(g)

STAFF_TILE_CONTENT_WHITELIST = ['yui','staff', 'member', 'employee', 'col-', 'team']

STAFF_TILE_CONTENT_BLACKLIST = ['wrapper', 'title', 'name', 'img', 'image', 'link']

txt = '''card l5 departmentCard-employees-19b16282-233d-47d3-97a5-9bb1738d6615_eec962b2-e1e6-4965-836c-5b8fce9e84fa default-motif bg-light media-bleed-none deck-bleed-full deck-listing col link-clickable no aspect-unknown insight cards-none title-one copy-one media-one links-few leafy'''


for keyword in STAFF_TILE_CONTENT_BLACKLIST:
    if keyword in txt:
        print(keyword)

print('----------')

for keyword in STAFF_TILE_CONTENT_WHITELIST:
    if keyword in txt:
        print(keyword)


print(("john smith").isalpha())