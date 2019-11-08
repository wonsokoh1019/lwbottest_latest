# Table of Contents

  * [calendar\_bot.calendar\_bot](#calendar_bot.calendar_bot)
    * [sig\_handler](#calendar_bot.calendar_bot.sig_handler)
    * [kill\_server](#calendar_bot.calendar_bot.kill_server)
    * [init\_logger](#calendar_bot.calendar_bot.init_logger)
    * [check\_init\_bot](#calendar_bot.calendar_bot.check_init_bot)
    * [init\_rich\_menu\_first](#calendar_bot.calendar_bot.init_rich_menu_first)
    * [init\_calendar\_first](#calendar_bot.calendar_bot.init_calendar_first)
    * [start\_calendar\_bot](#calendar_bot.calendar_bot.start_calendar_bot)
  * [calendar\_bot.router](#calendar_bot.router)
    * [getRouter](#calendar_bot.router.getRouter)

# `calendar_bot.calendar_bot`

launch calendar_bot

## `sig_handler()`

```python
def sig_handler(sig, _)
```

signal handler

## `kill_server()`

```python
def kill_server()
```

stop the ioloop

## `init_logger()`

```python
def init_logger()
```

Initializes the logger settings.

## `check_init_bot()`

```python
def check_init_bot()
```

Initialize bot no, check if the bot is initialized.
If this function gets an exception, it is probably like script/registerBot.py.
This is not executed or the execution failed.
ref: https://developers.worksmobile.com/jp/document/3005001?lang=en

## `init_rich_menu_first()`

```python
def init_rich_menu_first()
```

Initialize rich menu API. Check also: calendar_bot/externals/richmenu.py
ref: https://developers.worksmobile.com/jp/document/1005040?lang=en

## `init_calendar_first()`

```python
def init_calendar_first()
```

Initialize calendar API.

## `start_calendar_bot()`

```python
def start_calendar_bot()
```

the calendar_bot launch code

tornado.httpserver a non-blocking, single-threaded HTTP server
ref: https://www.tornadoweb.org/en/stable/httpserver.html

tornado.routing flexible routing implementation.
ref: https://www.tornadoweb.org/en/stable/routing.html

If you use the event loop that comes with tornado, many third-party
packages based on asyncio may not be used, such as aioredis.

# `calendar_bot.router`

the url to handler route

## `getRouter()`

```python
def getRouter()
```

get the app with route info
ref:https://www.tornadoweb.org/en/stable/web.html

StaticFileHandler is a simple handler that can serve static content
from a directory.
ref: https://www.tornadoweb.org/en/stable/web.html#tornado.web.StaticFileHandler

