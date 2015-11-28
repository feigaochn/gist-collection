# http://jugad2.blogspot.sg/2014/12/tortilla-python-api-wrapper.html

import tortilla

github = tortilla.wrap('https://api.github.com')
user = github.users.get('feigaochn')

for key in user:
    print(key, ":", user[key])
