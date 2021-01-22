
import tornado.web
import tornado.httpserver
import tornado.ioloop
import asyncio
import peewee_async

from RNGfreehub.baseModel import database
from RNGfreehub.settings import settings
from RNGfreehub.urls import page_url


HANDLERS=page_url

def run():
    from tornado.platform.asyncio import AsyncIOMainLoop
    AsyncIOMainLoop().install()
    # 集成json到wtforms
    import wtforms_json
    wtforms_json.init()

    app = tornado.web.Application(
        HANDLERS,
        **settings
        #static_url_prefix='/static/',
    )
    app.listen(port=8888)
    app.objects = peewee_async.Manager(database)

    loop = asyncio.get_event_loop()
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print(" server stopped")


if __name__ == '__main__':
    run()