import lists
import urls

print(lists.todo)

for url in lists.todo:
    try:
        urls.validate(url)
        print(url)
    except Exception as e:
        pass
        print("Exception: "+url+str(e.__class__))

