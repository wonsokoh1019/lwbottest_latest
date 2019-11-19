# Table of Contents

  * [calendar\_bot](#calendar_bot)
  * [calendar\_bot.contextlog](#calendar_bot.contextlog)
    * [RequestContextData](#calendar_bot.contextlog.RequestContextData)
    * [Metaclass](#calendar_bot.contextlog.Metaclass)
    * [RequestContext](#calendar_bot.contextlog.RequestContext)
    * [RequestContextFilter](#calendar_bot.contextlog.RequestContextFilter)
    * [contextualizedLogging](#calendar_bot.contextlog.contextualizedLogging)
  * [calendar\_bot.check\_and\_handle\_actions](#calendar_bot.check_and_handle_actions)
    * [LOGGER](#calendar_bot.check_and_handle_actions.LOGGER)
    * [cmd\_message](#calendar_bot.check_and_handle_actions.cmd_message)
    * [is\_message\_time](#calendar_bot.check_and_handle_actions.is_message_time)
    * [CheckAndHandleActions](#calendar_bot.check_and_handle_actions.CheckAndHandleActions)
  * [calendar\_bot.callbackHandler](#calendar_bot.callbackHandler)
    * [LOGGER](#calendar_bot.callbackHandler.LOGGER)
    * [CallbackHandler](#calendar_bot.callbackHandler.CallbackHandler)
  * [calendar\_bot.externals](#calendar_bot.externals)
  * [calendar\_bot.externals.send\_message](#calendar_bot.externals.send_message)
    * [LOGGER](#calendar_bot.externals.send_message.LOGGER)
    * [push\_message](#calendar_bot.externals.send_message.push_message)
    * [push\_messages](#calendar_bot.externals.send_message.push_messages)
  * [calendar\_bot.externals.calendar\_req](#calendar_bot.externals.calendar_req)
    * [LOGGER](#calendar_bot.externals.calendar_req.LOGGER)
    * [create\_headers](#calendar_bot.externals.calendar_req.create_headers)
    * [make\_icalendar\_data](#calendar_bot.externals.calendar_req.make_icalendar_data)
    * [create\_calendar](#calendar_bot.externals.calendar_req.create_calendar)
    * [create\_schedule](#calendar_bot.externals.calendar_req.create_schedule)
    * [modify\_schedule](#calendar_bot.externals.calendar_req.modify_schedule)
    * [init\_calendar](#calendar_bot.externals.calendar_req.init_calendar)
  * [calendar\_bot.externals.richmenu](#calendar_bot.externals.richmenu)
    * [LOGGER](#calendar_bot.externals.richmenu.LOGGER)
    * [upload\_content](#calendar_bot.externals.richmenu.upload_content)
    * [make\_add\_rich\_menu\_body](#calendar_bot.externals.richmenu.make_add_rich_menu_body)
    * [set\_rich\_menu\_image](#calendar_bot.externals.richmenu.set_rich_menu_image)
    * [set\_user\_specific\_rich\_menu](#calendar_bot.externals.richmenu.set_user_specific_rich_menu)
    * [get\_rich\_menus](#calendar_bot.externals.richmenu.get_rich_menus)
    * [cancel\_user\_specific\_rich\_menu](#calendar_bot.externals.richmenu.cancel_user_specific_rich_menu)
    * [init\_rich\_menu](#calendar_bot.externals.richmenu.init_rich_menu)
  * [calendar\_bot.calendar\_bot](#calendar_bot.calendar_bot)
    * [sig\_handler](#calendar_bot.calendar_bot.sig_handler)
    * [kill\_server](#calendar_bot.calendar_bot.kill_server)
    * [init\_logger](#calendar_bot.calendar_bot.init_logger)
    * [check\_init\_bot](#calendar_bot.calendar_bot.check_init_bot)
    * [init\_rich\_menu\_first](#calendar_bot.calendar_bot.init_rich_menu_first)
    * [init\_calendar\_first](#calendar_bot.calendar_bot.init_calendar_first)
    * [start\_calendar\_bot](#calendar_bot.calendar_bot.start_calendar_bot)
  * [calendar\_bot.settings](#calendar_bot.settings)
    * [LOG\_PATH](#calendar_bot.settings.LOG_PATH)
    * [CALENDAR\_LOG\_FILE](#calendar_bot.settings.CALENDAR_LOG_FILE)
    * [CALENDAR\_LOG\_ROTATE](#calendar_bot.settings.CALENDAR_LOG_ROTATE)
    * [CALENDAR\_LOG\_FMT](#calendar_bot.settings.CALENDAR_LOG_FMT)
    * [CALENDAR\_LOG\_LEVEL](#calendar_bot.settings.CALENDAR_LOG_LEVEL)
    * [CALENDAR\_PORT](#calendar_bot.settings.CALENDAR_PORT)
    * [CALENDAR\_PID\_FILE](#calendar_bot.settings.CALENDAR_PID_FILE)
  * [calendar\_bot.model](#calendar_bot.model)
  * [calendar\_bot.model.postgreSqlPool](#calendar_bot.model.postgreSqlPool)
    * [PostGreSql](#calendar_bot.model.postgreSqlPool.PostGreSql)
  * [calendar\_bot.model.initStatusDBHandle](#calendar_bot.model.initStatusDBHandle)
    * [insert\_init\_status](#calendar_bot.model.initStatusDBHandle.insert_init_status)
    * [update\_init\_status](#calendar_bot.model.initStatusDBHandle.update_init_status)
    * [get\_init\_status](#calendar_bot.model.initStatusDBHandle.get_init_status)
    * [delete\_init\_status](#calendar_bot.model.initStatusDBHandle.delete_init_status)
  * [calendar\_bot.model.processStatusDBHandle](#calendar_bot.model.processStatusDBHandle)
    * [LOGGER](#calendar_bot.model.processStatusDBHandle.LOGGER)
    * [insert\_replace\_status\_by\_user\_date](#calendar_bot.model.processStatusDBHandle.insert_replace_status_by_user_date)
    * [set\_status\_by\_user\_date](#calendar_bot.model.processStatusDBHandle.set_status_by_user_date)
    * [get\_status\_by\_user](#calendar_bot.model.processStatusDBHandle.get_status_by_user)
    * [delete\_status\_by\_user\_date](#calendar_bot.model.processStatusDBHandle.delete_status_by_user_date)
    * [clean\_status\_by\_user](#calendar_bot.model.processStatusDBHandle.clean_status_by_user)
  * [calendar\_bot.model.calendarDBHandle](#calendar_bot.model.calendarDBHandle)
    * [LOGGER](#calendar_bot.model.calendarDBHandle.LOGGER)
    * [set\_schedule\_by\_user](#calendar_bot.model.calendarDBHandle.set_schedule_by_user)
    * [get\_schedule\_by\_user](#calendar_bot.model.calendarDBHandle.get_schedule_by_user)
    * [modify\_schedule\_by\_user](#calendar_bot.model.calendarDBHandle.modify_schedule_by_user)
    * [clean\_schedule\_by\_user](#calendar_bot.model.calendarDBHandle.clean_schedule_by_user)
  * [calendar\_bot.model.data](#calendar_bot.model.data)
    * [make\_i18n\_label](#calendar_bot.model.data.make_i18n_label)
    * [i18n\_display\_text](#calendar_bot.model.data.i18n_display_text)
    * [make\_postback\_action](#calendar_bot.model.data.make_postback_action)
    * [i18n\_text](#calendar_bot.model.data.i18n_text)
    * [make\_message\_action](#calendar_bot.model.data.make_message_action)
    * [make\_url\_action](#calendar_bot.model.data.make_url_action)
    * [make\_normal\_action](#calendar_bot.model.data.make_normal_action)
    * [make\_i18n\_thumbnail\_image\_url](#calendar_bot.model.data.make_i18n_thumbnail_image_url)
    * [make\_i18n\_image\_resource\_id](#calendar_bot.model.data.make_i18n_image_resource_id)
    * [make\_quick\_reply\_item](#calendar_bot.model.data.make_quick_reply_item)
    * [make\_quick\_reply](#calendar_bot.model.data.make_quick_reply)
    * [make\_text](#calendar_bot.model.data.make_text)
    * [make\_i18n\_image\_url](#calendar_bot.model.data.make_i18n_image_url)
    * [make\_image\_carousel\_column](#calendar_bot.model.data.make_image_carousel_column)
    * [make\_image\_carousel](#calendar_bot.model.data.make_image_carousel)
    * [make\_size](#calendar_bot.model.data.make_size)
    * [make\_bound](#calendar_bot.model.data.make_bound)
    * [make\_area](#calendar_bot.model.data.make_area)
    * [make\_add\_rich\_menu](#calendar_bot.model.data.make_add_rich_menu)
    * [make\_i18n\_content\_texts](#calendar_bot.model.data.make_i18n_content_texts)
    * [make\_button](#calendar_bot.model.data.make_button)
  * [calendar\_bot.constant](#calendar_bot.constant)
    * [ABSDIR\_OF\_SELF](#calendar_bot.constant.ABSDIR_OF_SELF)
    * [ABSDIR\_OF\_PARENT](#calendar_bot.constant.ABSDIR_OF_PARENT)
    * [HEROKU\_SERVER\_ID](#calendar_bot.constant.HEROKU_SERVER_ID)
    * [PRIVATE\_KEY\_PATH](#calendar_bot.constant.PRIVATE_KEY_PATH)
    * [STORAGE\_DOMAIN](#calendar_bot.constant.STORAGE_DOMAIN)
    * [AUTH\_DOMAIN](#calendar_bot.constant.AUTH_DOMAIN)
    * [DEVELOP\_API\_DOMAIN](#calendar_bot.constant.DEVELOP_API_DOMAIN)
    * [RICH\_MENUS](#calendar_bot.constant.RICH_MENUS)
    * [IMAGE\_CAROUSEL](#calendar_bot.constant.IMAGE_CAROUSEL)
    * [API\_BO](#calendar_bot.constant.API_BO)
    * [OPEN\_API](#calendar_bot.constant.OPEN_API)
    * [DB\_CONFIG](#calendar_bot.constant.DB_CONFIG)
    * [FILE\_SYSTEM](#calendar_bot.constant.FILE_SYSTEM)
  * [calendar\_bot.common](#calendar_bot.common)
  * [calendar\_bot.common.local\_timezone](#calendar_bot.common.local_timezone)
    * [LOGGER](#calendar_bot.common.local_timezone.LOGGER)
    * [get\_time\_zone](#calendar_bot.common.local_timezone.get_time_zone)
    * [get\_tz](#calendar_bot.common.local_timezone.get_tz)
    * [set\_tz](#calendar_bot.common.local_timezone.set_tz)
    * [load\_time\_zone](#calendar_bot.common.local_timezone.load_time_zone)
    * [local\_date\_time](#calendar_bot.common.local_timezone.local_date_time)
  * [calendar\_bot.common.utils](#calendar_bot.common.utils)
    * [LOGGER](#calendar_bot.common.utils.LOGGER)
    * [refresh\_token](#calendar_bot.common.utils.refresh_token)
    * [get\_token](#calendar_bot.common.utils.get_token)
    * [replace\_url\_bot\_no](#calendar_bot.common.utils.replace_url_bot_no)
    * [auth\_post](#calendar_bot.common.utils.auth_post)
    * [auth\_get](#calendar_bot.common.utils.auth_get)
    * [auth\_del](#calendar_bot.common.utils.auth_del)
    * [auth\_put](#calendar_bot.common.utils.auth_put)
  * [calendar\_bot.common.global\_data](#calendar_bot.common.global_data)
    * [set\_value](#calendar_bot.common.global_data.set_value)
    * [get\_value](#calendar_bot.common.global_data.get_value)
  * [calendar\_bot.common.local\_external\_ke](#calendar_bot.common.local_external_ke)
    * [LOGGER](#calendar_bot.common.local_external_ke.LOGGER)
    * [get\_external\_key\_from\_remote](#calendar_bot.common.local_external_ke.get_external_key_from_remote)
    * [get\_external\_key](#calendar_bot.common.local_external_ke.get_external_key)
    * [set\_external\_key](#calendar_bot.common.local_external_ke.set_external_key)
    * [load\_external\_key](#calendar_bot.common.local_external_ke.load_external_key)
  * [calendar\_bot.common.token](#calendar_bot.common.token)
    * [create\_tmp\_token](#calendar_bot.common.token.create_tmp_token)
    * [generate\_token](#calendar_bot.common.token.generate_token)
  * [calendar\_bot.router](#calendar_bot.router)
    * [getRouter](#calendar_bot.router.getRouter)
  * [calendar\_bot.actions](#calendar_bot.actions)
  * [calendar\_bot.actions.to\_first](#calendar_bot.actions.to_first)
    * [LOGGER](#calendar_bot.actions.to_first.LOGGER)
    * [to\_first](#calendar_bot.actions.to_first.to_first)
  * [calendar\_bot.actions.confirm\_out](#calendar_bot.actions.confirm_out)
    * [LOGGER](#calendar_bot.actions.confirm_out.LOGGER)
    * [confirm\_out\_message](#calendar_bot.actions.confirm_out.confirm_out_message)
    * [deal\_confirm\_out](#calendar_bot.actions.confirm_out.deal_confirm_out)
    * [confirm\_out](#calendar_bot.actions.confirm_out.confirm_out)
  * [calendar\_bot.actions.message](#calendar_bot.actions.message)
    * [LOGGER](#calendar_bot.actions.message.LOGGER)
    * [TimeStruct](#calendar_bot.actions.message.TimeStruct)
    * [create\_button\_actions](#calendar_bot.actions.message.create_button_actions)
    * [create\_quick\_replay\_items](#calendar_bot.actions.message.create_quick_replay_items)
    * [prompt\_input](#calendar_bot.actions.message.prompt_input)
    * [number\_message](#calendar_bot.actions.message.number_message)
    * [error\_message](#calendar_bot.actions.message.error_message)
    * [invalid\_message](#calendar_bot.actions.message.invalid_message)
    * [reminder\_message](#calendar_bot.actions.message.reminder_message)
  * [calendar\_bot.actions.manual\_sign\_in](#calendar_bot.actions.manual_sign_in)
    * [LOGGER](#calendar_bot.actions.manual_sign_in.LOGGER)
    * [manual\_sign\_in\_message](#calendar_bot.actions.manual_sign_in.manual_sign_in_message)
    * [manual\_sign\_in\_content](#calendar_bot.actions.manual_sign_in.manual_sign_in_content)
    * [manual\_sign\_in](#calendar_bot.actions.manual_sign_in.manual_sign_in)
  * [calendar\_bot.actions.sign\_in](#calendar_bot.actions.sign_in)
    * [LOGGER](#calendar_bot.actions.sign_in.LOGGER)
    * [sign\_in\_message](#calendar_bot.actions.sign_in.sign_in_message)
    * [sign\_in\_content](#calendar_bot.actions.sign_in.sign_in_content)
    * [sign\_in](#calendar_bot.actions.sign_in.sign_in)
  * [calendar\_bot.actions.direct\_sign\_out](#calendar_bot.actions.direct_sign_out)
    * [LOGGER](#calendar_bot.actions.direct_sign_out.LOGGER)
    * [deal\_sign\_out\_message](#calendar_bot.actions.direct_sign_out.deal_sign_out_message)
    * [deal\_sign\_out](#calendar_bot.actions.direct_sign_out.deal_sign_out)
    * [direct\_sign\_out](#calendar_bot.actions.direct_sign_out.direct_sign_out)
  * [calendar\_bot.actions.confirm\_in](#calendar_bot.actions.confirm_in)
    * [LOGGER](#calendar_bot.actions.confirm_in.LOGGER)
    * [deal\_confirm\_in](#calendar_bot.actions.confirm_in.deal_confirm_in)
    * [confirm\_in](#calendar_bot.actions.confirm_in.confirm_in)
  * [calendar\_bot.actions.deal\_message](#calendar_bot.actions.deal_message)
    * [LOGGER](#calendar_bot.actions.deal_message.LOGGER)
    * [deal\_user\_message](#calendar_bot.actions.deal_message.deal_user_message)
    * [deal\_message](#calendar_bot.actions.deal_message.deal_message)
  * [calendar\_bot.actions.manual\_sign\_out](#calendar_bot.actions.manual_sign_out)
    * [LOGGER](#calendar_bot.actions.manual_sign_out.LOGGER)
    * [manual\_sign\_out\_message](#calendar_bot.actions.manual_sign_out.manual_sign_out_message)
    * [manual\_sign\_out\_content](#calendar_bot.actions.manual_sign_out.manual_sign_out_content)
    * [manual\_sign\_out](#calendar_bot.actions.manual_sign_out.manual_sign_out)
  * [calendar\_bot.actions.direct\_sign\_in](#calendar_bot.actions.direct_sign_in)
    * [LOGGER](#calendar_bot.actions.direct_sign_in.LOGGER)
    * [deal\_sign\_in\_message](#calendar_bot.actions.direct_sign_in.deal_sign_in_message)
    * [deal\_sign\_in](#calendar_bot.actions.direct_sign_in.deal_sign_in)
    * [direct\_sign\_in](#calendar_bot.actions.direct_sign_in.direct_sign_in)
  * [calendar\_bot.actions.start](#calendar_bot.actions.start)
    * [LOGGER](#calendar_bot.actions.start.LOGGER)
    * [image\_introduce](#calendar_bot.actions.start.image_introduce)
    * [sign](#calendar_bot.actions.start.sign)
    * [start\_content](#calendar_bot.actions.start.start_content)
    * [start](#calendar_bot.actions.start.start)
  * [calendar\_bot.actions.sign\_out](#calendar_bot.actions.sign_out)
    * [LOGGER](#calendar_bot.actions.sign_out.LOGGER)
    * [sign\_out\_message](#calendar_bot.actions.sign_out.sign_out_message)
    * [sign\_out\_content](#calendar_bot.actions.sign_out.sign_out_content)
    * [sign\_out](#calendar_bot.actions.sign_out.sign_out)

# `calendar_bot`


# `calendar_bot.contextlog`

The context for logging request_id

## `RequestContextData` Objects

```python
def __init__(self, request_id=0)
```

request_id

### `RequestContextData.__init__()`

```python
def __init__(self, request_id=0)
```


### `RequestContextData.__eq__()`

```python
def __eq__(self, other)
```


## `Metaclass` Objects

meta class for RequestContext

### `Metaclass.data()`

```python
@property
def data(cls)
```

data property of RequestContext

## `RequestContext` Objects

```python
def __init__(self, request_id=0)
```

The context class for request_id

### `RequestContext.__init__()`

```python
def __init__(self, request_id=0)
```


### `RequestContext.__enter__()`

```python
def __enter__(self)
```


### `RequestContext.__exit__()`

```python
def __exit__(self, exc_type, exc_value, traceback)
```


## `RequestContextFilter` Objects

logging filter for add request_id to record

### `RequestContextFilter.filter()`

```python
def filter(self, record)
```

add request_id to record

## `contextualizedLogging()`

```python
def contextualizedLogging(handler)
```

This class decorator is contextualizing the HTTP request in logging.

# `calendar_bot.check_and_handle_actions`

Factory used to create handler and execute handler.

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `cmd_message`

```python
cmd_message = ["start", "clean"]
```


## `is_message_time()`

```python
def is_message_time(message)
```

Checks if the message should include time information.
:param message:  User's callback message.
:return: time of user sign in/out.

## `CheckAndHandleActions` Objects

```python
def __init__(self)
```

Factory used to create handler and execute handler.

### `CheckAndHandleActions.__init__()`

```python
def __init__(self)
```


### `CheckAndHandleActions.execute()`

```python
@tornado.gen.coroutine
def execute(self, body)
```

Verify the body parameter and execute handler.
Please refer to the reference link of the function.
[reference](https://developers.worksmobile.com/jp/document/100500901?lang=en)

# `calendar_bot.callbackHandler`

Process requests of users

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `CallbackHandler` Objects

Process business requests of users.

tornado.web.RequestHandler base class for HTTP request handlers.
[reference](https://www.tornadoweb.org/en/stable/web.html)

### `CallbackHandler.post()`

```python
@tornado.gen.coroutine
def post(self)
```

Implement the handle to corresponding HTTP method.
Check also: calendar_bot/router.py

# `calendar_bot.externals`


# `calendar_bot.externals.send_message`

send message to user

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `push_message()`

```python
@tornado.gen.coroutine
def push_message(account_id, content, header=None)
```

Send message to user. the package is the following JSON structure.
[reference](https://developers.worksmobile.com/jp/document/1005008?lang=en)

:param account_id: user account id
:param content: message content
:param header: http header

## `push_messages()`

```python
@tornado.gen.coroutine
def push_messages(account_id, contents)
```

Send multiple messages to users
:param account_id: user account id
:param contents: message content list

# `calendar_bot.externals.calendar_req`

Provides calendar API related functions

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `create_headers()`

```python
def create_headers()
```


## `make_icalendar_data()`

```python
def make_icalendar_data(uid, summary, current, end, begin, account_id, create_flag=False)
```

Generate iCalendar data format message body.
[reference](https://developers.worksmobile.com/jp/document/1007011?lang=en)

## `create_calendar()`

```python
def create_calendar()
```

create calender.
[reference](https://developers.worksmobile.com/kr/document/100702701?lang=ko)
:return: calendar id.

## `create_schedule()`

```python
def create_schedule(current, end, begin, account_id)
```

create schedule.
[reference](https://developers.worksmobile.com/kr/document/100702703?lang=ko)
:return: schedule id.

## `modify_schedule()`

```python
def modify_schedule(calendar_uid, current, end, begin, account_id)
```

modify schedule.
[reference](https://developers.worksmobile.com/kr/document/100702704?lang=ko)
:return: schedule id.

## `init_calendar()`

```python
def init_calendar()
```

init calendar.
The calendar initialization function is called to generate
the calendar id when the system starts.
:return: calendar id

# `calendar_bot.externals.richmenu`

rich menu's api

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `upload_content()`

```python
def upload_content(file_path)
```

Upload rich menu background picture.
[reference](https://developers.worksmobile.com/kr/document/1005025?lang=en)
:param file_path: resource local path
:return: resource id

## `make_add_rich_menu_body()`

```python
def make_add_rich_menu_body(rich_menu_name)
```

add rich menu body
[reference](https://developers.worksmobile.com/kr/document/100504001?lang=en)
:param rich_menu_name: rich menu name
:return: rich menu id

## `set_rich_menu_image()`

```python
def set_rich_menu_image(resource_id, rich_menu_id)
```

Set a rich menu image.
[reference](https://developers.worksmobile.com/kr/document/100504002?lang=en)
:param resource_id: resource id
:param rich_menu_id: rich menu id
:return:

## `set_user_specific_rich_menu()`

```python
def set_user_specific_rich_menu(rich_menu_id, account_id)
```

Set a user-specific rich menu.
[reference](https://developers.worksmobile.com/kr/document/100504010?lang=en)
:param rich_menu_id: rich menu id
:param account_id: user account id

## `get_rich_menus()`

```python
def get_rich_menus()
```

Get rich menus
[reference](https://developers.worksmobile.com/kr/document/100504004?lang=en)
:return: rich menu list

## `cancel_user_specific_rich_menu()`

```python
def cancel_user_specific_rich_menu(account_id)
```

Cancel a user-specific rich menu
[reference](https://developers.worksmobile.com/kr/document/100504012?lang=en)
:param account_id: user account id

## `init_rich_menu()`

```python
def init_rich_menu()
```

init rich menu.
[reference](https://developers.worksmobile.com/kr/document/1005040?lang=en)
:return: rich menu id

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
[reference](https://developers.worksmobile.com/jp/document/3005001?lang=en)

## `init_rich_menu_first()`

```python
def init_rich_menu_first()
```

Initialize rich menu API. Check also: calendar_bot/externals/richmenu.py
[reference](https://developers.worksmobile.com/jp/document/1005040?lang=en)

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
[reference](https://www.tornadoweb.org/en/stable/httpserver.html)

tornado.routing flexible routing implementation.
[reference](https://www.tornadoweb.org/en/stable/routing.html)

If you use the event loop that comes with tornado, many third-party
packages based on asyncio may not be used, such as aioredis.

Message bot API overview.
[reference](https://developers.worksmobile.com/jp/document/3005001?lang=en)

# `calendar_bot.settings`

the global setting for calendar_bot

## `LOG_PATH`

```python
LOG_PATH = ABSDIR_OF_PARENT + "/logs/"
```


## `CALENDAR_LOG_FILE`

```python
CALENDAR_LOG_FILE = LOG_PATH + "calendar_bot.log"
```


## `CALENDAR_LOG_ROTATE`

```python
CALENDAR_LOG_ROTATE = "midnight"
```


## `CALENDAR_LOG_FMT`

```python
CALENDAR_LOG_FMT = '[%(asctime)-15s] [%(levelname)s] ' \
                   '%(filename)s %(funcName)s:%(lineno)d ' \
  ...
```


## `CALENDAR_LOG_LEVEL`

```python
CALENDAR_LOG_LEVEL = "DEBUG"
```


## `CALENDAR_PORT`

```python
CALENDAR_PORT = 8080
```


## `CALENDAR_PID_FILE`

```python
CALENDAR_PID_FILE = LOG_PATH + "calendar_bot.pid"
```


# `calendar_bot.model`


# `calendar_bot.model.postgreSqlPool`

Connection pool for database
[reference](https://cito.github.io/DBUtils/UsersGuide.html#pooleddb)

## `PostGreSql` Objects

```python
def __init__(self)
```


### `PostGreSql.__init__()`

```python
def __init__(self)
```


### `PostGreSql.cursor()`

```python
def cursor(self)
```


### `PostGreSql.commit()`

```python
def commit(self)
```


### `PostGreSql.rollback()`

```python
def rollback(self)
```


### `PostGreSql.execute()`

```python
def execute(self, sql)
```


### `PostGreSql.fetchall()`

```python
def fetchall(self)
```


### `PostGreSql.fetchone()`

```python
def fetchone(self)
```


### `PostGreSql.close()`

```python
def close(self)
```


### `PostGreSql.__enter__()`

```python
def __enter__(self)
```


### `PostGreSql.__exit__()`

```python
def __exit__(self, type, value, tb)
```


# `calendar_bot.model.initStatusDBHandle`

system_init_status table's CRUD operation.
save the system Initialize status。
Check also: scripts/initDB.py

## `insert_init_status()`

```python
def insert_init_status(action, extra)
```

Inserts the initialization status of an item after initialization.
:param action: Initialized item
:param extra: Initialized data or status
:return: no

## `update_init_status()`

```python
def update_init_status(action, extra)
```

Update the initialization status of an item after initialization.
:param action: Initialized item
:param extra: Initialized data or status
:return: no

## `get_init_status()`

```python
def get_init_status(action)
```

Get an item initialized data or status.
:param action: item
:return: initialized data or status

## `delete_init_status()`

```python
def delete_init_status(action)
```

delete an item initialized data or status.
:param action: item
:return: no

# `calendar_bot.model.processStatusDBHandle`

bot_process_status table's CRUD operation.
save the user context.
Check also: scripts/initDB.py

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `insert_replace_status_by_user_date()`

```python
def insert_replace_status_by_user_date(account, date, status, process=None)
```

insert or update user's status.
:param account: user account
:param date: current date by local time.
:param status: user text input status.
:param process: processing progress.
:return: Return false when status is None Else, Return None

## `set_status_by_user_date()`

```python
def set_status_by_user_date(account, date, status=None, process=None)
```

update user's status.
:param account: user account
:param date: current date by local time.
:param status: user text input status.
:param process: processing progress.
:return: no

## `get_status_by_user()`

```python
def get_status_by_user(account, date)
```

select user's status.
:param account: user account
:param date: current date by local time.
:return: no

## `delete_status_by_user_date()`

```python
def delete_status_by_user_date(account, date)
```

delete user's status.
:param account: user account
:param date: current date by local time.
:return: no

## `clean_status_by_user()`

```python
def clean_status_by_user(account, date)
```

delete a item.
:param account: user account
:param date: current date by local time.
:return: no

# `calendar_bot.model.calendarDBHandle`

bot_calendar_record table's CRUD operation.
This table is used to save the time of the user.
Check also: scripts/initDB.py

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `set_schedule_by_user()`

```python
def set_schedule_by_user(schedule_id, account, date, begin, end)
```

insert schedule
:param schedule_id: schedule_id
:param account: user account
:param date: current date by local time.
:param begin: schedule begin time.
:param end: schedule end time.
:return: no

## `get_schedule_by_user()`

```python
def get_schedule_by_user(account, date)
```

get schedule
:param account: user account
:param date: current date by local time.
:return: schedule id, begin time

## `modify_schedule_by_user()`

```python
def modify_schedule_by_user(schedule_id, end)
```

update schedule's end time
:param schedule_id: schedule_id
:param end: schedule end time.
:return: no

## `clean_schedule_by_user()`

```python
def clean_schedule_by_user(account, date)
```

delete a schedule
:param account: user account
:param date: current date by local time.
:return: no

# `calendar_bot.model.data`

create message content

## `make_i18n_label()`

```python
def make_i18n_label(language, label)
```


## `i18n_display_text()`

```python
def i18n_display_text(language, display_text)
```


## `make_postback_action()`

```python
def make_postback_action(data, display_text=None, label=None, i18n_labels=None, i18n_display_texts=None)
```

make post back action.
[reference](https://developers.worksmobile.com/jp/document/1005050?lang=en)
:param data: post back string
:return: actions content

## `i18n_text()`

```python
def i18n_text(language, text)
```


## `make_message_action()`

```python
def make_message_action(label, post_back, text=None, i18n_labels=None, i18n_texts=None)
```

make message action.
[reference](https://developers.worksmobile.com/jp/document/1005050?lang=en)
:param post_back: post back string
:return: actions content

## `make_url_action()`

```python
def make_url_action(label, url, i18n_labels=None)
```

make url action.
[reference](https://developers.worksmobile.com/jp/document/1005050?lang=en)
:param url: User behavior will trigger the client to request this URL.
:return: actions content

## `make_normal_action()`

```python
def make_normal_action(atype, label, i18n_labels=None)
```

Create camera, camera roll, location action.
[reference](https://developers.worksmobile.com/jp/document/1005050?lang=en)
:param atype: action's type
:return: None

## `make_i18n_thumbnail_image_url()`

```python
def make_i18n_thumbnail_image_url(language, thumbnail_image_url)
```


## `make_i18n_image_resource_id()`

```python
def make_i18n_image_resource_id(language, image_resource_id)
```


## `make_quick_reply_item()`

```python
def make_quick_reply_item(action, url=None, image_resource_id=None, i18n_thumbnail_image_urls=None, i18n_image_resource_ids=None)
```

Create quick reply message item.
[reference](https://developers.worksmobile.com/jp/document/100500807?lang=en)
:param action: The user clicks the quick reply button to trigger this action.
:return: quick reply content.

## `make_quick_reply()`

```python
def make_quick_reply(replay_items)
```

Create quick reply message.
[reference](https://developers.worksmobile.com/jp/document/100500807?lang=en)
:param replay_items: Array of return object of make_quick_reply_item function.
:return: quick reply content.

## `make_text()`

```python
def make_text(text, i18n_texts=None)
```

make text.
[reference](https://developers.worksmobile.com/jp/document/100500801?lang=en)
:return: text content.

## `make_i18n_image_url()`

```python
def make_i18n_image_url(language, image_url)
```


## `make_image_carousel_column()`

```python
def make_image_carousel_column(image_url=None, image_resource_id=None, action=None, i18n_image_urls=None, i18n_image_resource_ids=None)
```


## `make_image_carousel()`

```python
def make_image_carousel(columns)
```

Image Carousel:
[reference](https://developers.worksmobile.com/jp/document/100500809?lang=en)

Request URL
https://apis.worksmobile.com/r/{API ID}/message/v1/bot/{botNo}/message/push

POST (Content-Type: application / json; charset = UTF-8)

:param columns: image carousel columns
:return: image carousel content

## `make_size()`

```python
def make_size(w, h)
```


## `make_bound()`

```python
def make_bound(x, y, w, h)
```


## `make_area()`

```python
def make_area(bound, action)
```


## `make_add_rich_menu()`

```python
def make_add_rich_menu(name, size, areas)
```

add rich menu content:
[reference](https://developers.worksmobile.com/jp/document/1005040?lang=en)
    You can create a rich menu for the message bot by following these steps:
    Image uploads: using the "Upload Content" API
    Rich menu generation: using the "Register Message Rich Menu" API
    Rich Menu Image Settings: Use the "Message Rich Menu Image Settings" API

## `make_i18n_content_texts()`

```python
def make_i18n_content_texts(language, content_text)
```


## `make_button()`

```python
def make_button(text, actions, content_texts=None)
```

create button message content
[reference](https://developers.worksmobile.com/jp/document/100500804?lang=en)

# `calendar_bot.constant`

constants.py Defining the constant used for a project.

## `ABSDIR_OF_SELF`

```python
ABSDIR_OF_SELF = os.path.dirname(os.path.abspath(__file__))
```


## `ABSDIR_OF_PARENT`

```python
ABSDIR_OF_PARENT = os.path.dirname(ABSDIR_OF_SELF)
```


## `HEROKU_SERVER_ID`

```python
HEROKU_SERVER_ID = SERVER_ID
```


## `PRIVATE_KEY_PATH`

```python
PRIVATE_KEY_PATH = ABSDIR_OF_PARENT + "/key/" + SECRET_KEY_NAME
```


## `STORAGE_DOMAIN`

```python
STORAGE_DOMAIN = "storage.worksmobile.com"
```


## `AUTH_DOMAIN`

```python
AUTH_DOMAIN = "auth.worksmobile.com"
```


## `DEVELOP_API_DOMAIN`

```python
DEVELOP_API_DOMAIN = "apis.worksmobile.com"
```


## `RICH_MENUS`

```python
RICH_MENUS = {
                "name": "calendar_bot_rich_menu_en",
                "path": ABSDIR_OF_PARENT + "/ ...
```


## `IMAGE_CAROUSEL`

```python
IMAGE_CAROUSEL = {
                    "resource_url":
                    [
                        LOCAL_ADDRESS +  ...
```


## `API_BO`

```python
API_BO = {
            "headers": {
                "content-type": "application/json",
                "char ...
```


## `OPEN_API`

```python
OPEN_API = {
        "_info": "nwetest.com",
        "apiId": API_ID,
        "consumerKey": SERVER_CONSUMER_KE ...
```


## `DB_CONFIG`

```python
DB_CONFIG = {
    "host": DB_HOST,
    "port": DB_PORT,
    "dbname": DB_NAME,
    "user": DB_USER,
    "passwor ...
```


## `FILE_SYSTEM`

```python
FILE_SYSTEM = {
    "image_dir": ABSDIR_OF_PARENT+"/image",
}
```


# `calendar_bot.common`


# `calendar_bot.common.local_timezone`

deal time zone

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `get_time_zone()`

```python
def get_time_zone()
```

Get time zone according to administrator account.
[reference](https://developers.worksmobile.com/kr/document/100300528?lang=en)

## `get_tz()`

```python
def get_tz()
```


## `set_tz()`

```python
def set_tz()
```


## `load_time_zone()`

```python
def load_time_zone()
```


## `local_date_time()`

```python
def local_date_time(time=None)
```

Time to switch UTC time to a specific time zone.
[reference](https://docs.python.org/3/library/datetime.html)
:param time: Time to switch time zones
:return: local time.

# `calendar_bot.common.utils`

HTTP method providing authentication

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `refresh_token()`

```python
def refresh_token()
```


## `get_token()`

```python
def get_token()
```


## `replace_url_bot_no()`

```python
def replace_url_bot_no(url)
```


## `auth_post()`

```python
def auth_post(url, data=None, headers=None, files=None, params=None, json=None, refresh_token_flag=False)
```

Encapsulates the post method of adding token to headers.
Check also: calendar_bot/common/token.py
parameters and return values, refer to:
[reference](https://3.python-requests.org/user/advanced/#request-and-response-objects)

## `auth_get()`

```python
def auth_get(url, headers=None, refresh_token_flag=False)
```

Encapsulates the get method of adding token to headers.
Check also: calendar_bot/common/token.py
parameters and return values, refer to:
[reference](https://3.python-requests.org/user/advanced/#request-and-response-objects)

## `auth_del()`

```python
def auth_del(url, headers=None, refresh_token_flag=False)
```

Encapsulates the delete method of adding token to headers.
Check also: calendar_bot/common/token.py
parameters and return values, refer to:
[reference](https://3.python-requests.org/user/advanced/#request-and-response-objects)

## `auth_put()`

```python
def auth_put(url, data=None, headers=None, files=None, params=None, json=None, refresh_token_flag=False)
```

Encapsulates the put method of adding token to headers.
Check also: calendar_bot/common/token.py
parameters and return values, refer to:
[reference](https://3.python-requests.org/user/advanced/#request-and-response-objects)

# `calendar_bot.common.global_data`

This is a global variable cache.

## `set_value()`

```python
def set_value(key, value)
```

Sets a value into the global variable cache.
:param key: key
:param value: value
:return: no

## `get_value()`

```python
def get_value(key, def_value=None)
```

Gets a value from the global variable cache.
:param key: key
:param def_value: default value
:return: value, If the key does not exist, the default value.

# `calendar_bot.common.local_external_ke`

get a account external key.

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `get_external_key_from_remote()`

```python
def get_external_key_from_remote()
```

Get external key of account.
[reference](https://developers.worksmobile.com/kr/document/1006004/v1?lang=en)
If you fail to get external key,
log in to the development console to check your configuration.
[reference](https://auth.worksmobile.com/login/login?
accessUrl=https%3A%2F%2Fdevelopers.worksmobile.com
%3A443%2Fconsole%2Fopenapi%2Fmain)
:return: external key

## `get_external_key()`

```python
def get_external_key()
```


## `set_external_key()`

```python
def set_external_key()
```


## `load_external_key()`

```python
def load_external_key()
```

load external key.
:return: admin account's external key

# `calendar_bot.common.token`

Generate token according to JWT protocol

## `create_tmp_token()`

```python
def create_tmp_token(key_path, server_id)
```

This function use JWT protocol to creates a temporary token
for user authentication.

Focus on the "Server Token (ID Registration Style)" section of
the following documents.

[reference](https://developers.worksmobile.com/jp/document/1002002?lang=en)

## `generate_token()`

```python
def generate_token()
```

Using JWT protocol to create token.
Focus on the "Server Token (ID Registration Style)" section of
the following documents.

[reference](https://developers.worksmobile.com/jp/document/1002002?lang=en)

# `calendar_bot.router`

the url to handler route

## `getRouter()`

```python
def getRouter()
```

get the app with route info
[reference](https://www.tornadoweb.org/en/stable/web.html)

StaticFileHandler is a simple handler that can serve static content
from a directory.
[reference](https://www.tornadoweb.org/en/stable/web.html#tornado.web.StaticFileHandler)

# `calendar_bot.actions`


# `calendar_bot.actions.to_first`

!/bin/env python
-*- coding: utf-8 -*-

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `to_first()`

```python
@tornado.gen.coroutine
def to_first(account_id, _, __, ___)
```


# `calendar_bot.actions.confirm_out`

Deal confirm check-out

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `confirm_out_message()`

```python
def confirm_out_message(user_time, hours, min)
```


## `deal_confirm_out()`

```python
@tornado.gen.coroutine
def deal_confirm_out(account_id, create_time, callback)
```

will be linked with the calendar internally, Check out time of registered user.
Check also: calendar_bot/externals/calendar_req.py
:param account_id: user account id.
:param create_time: current date by local time.
:param callback: The message content of the callback,
    include the user's check-out time
:return: Prompt message of successful check out.

## `confirm_out()`

```python
@tornado.gen.coroutine
def confirm_out(account_id, current_date, create_time, callback)
```

This function is triggered when the user clicks confirm check-out.
will be linked with the calendar internally.
:param account_id: user account id.
:param current_date: current date by local time.
:param create_time: Time the request arrived at the server.
:param callback: User triggered callback.
:return: None

# `calendar_bot.actions.message`

common message

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `TimeStruct` Objects

```python
def __init__(self, sign_time)
```

to localize timestamp time

### `TimeStruct.__init__()`

```python
def __init__(self, sign_time)
```

Convert timestamp time to datetime time in a specific time zone.
And assign it to the corresponding member variable.
:param sign_time: A user time of timestamp value.

## `create_button_actions()`

```python
def create_button_actions(direct_sign_callback, manual_sign_callback)
```

Create the message body of the button template of two buttons.
Check also: calendar_bot/model/data.py
[reference](https://developers.worksmobile.com/jp/document/100500804?lang=en)
:param direct_sign_callback: callback string for the first button.
:param manual_sign_callback: callback string for the seconds button.

## `create_quick_replay_items()`

```python
def create_quick_replay_items(confirm_callback, previous_callback)
```

Building a quick reply floating window for messages.
Check also: calendar_bot/model/data.py
[reference](https://developers.worksmobile.com/jp/document/100500807?lang=en)
:param confirm_callback: callback string for the first button.
:param previous_callback: callback string for the seconds button.
:return:

## `prompt_input()`

```python
def prompt_input()
```

Format to remind users to enter time.
:return: text type message

## `number_message()`

```python
def number_message()
```

Non digital message entered.
:return: text type message

## `error_message()`

```python
def error_message()
```

Wrong data entered
:return: text type message

## `invalid_message()`

```python
def invalid_message()
```

Invalid input data reminder.
:return: text type message

## `reminder_message()`

```python
def reminder_message(process)
```

Illegal request reminder.
:param process: Current user's progress
:return: text type message

# `calendar_bot.actions.manual_sign_in`

Handle the user's manual check-in

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `manual_sign_in_message()`

```python
def manual_sign_in_message()
```

generate manual check-in message
:return: message content list

## `manual_sign_in_content()`

```python
@tornado.gen.coroutine
def manual_sign_in_content(account_id, current_date)
```

Update user status and generate manual check-in message.
:param account_id: user account id
:param current_date: current date by local time.
:return: message content list

## `manual_sign_in()`

```python
@tornado.gen.coroutine
def manual_sign_in(account_id, current_date, _, __)
```

Handle the user's manual check-in.
:param account_id: user account id.
:param current_date: current date by local time.
:param _: no use
:param __: no use

# `calendar_bot.actions.sign_in`

Handle the user's check-in

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `sign_in_message()`

```python
def sign_in_message()
```

generate check-in message
:return: button type message content

## `sign_in_content()`

```python
@tornado.gen.coroutine
def sign_in_content(account_id, current_date)
```

Update user status and generate check-in message.
:param account_id: user account id
:param current_date: current date by local time.
:return: button type message content

## `sign_in()`

```python
@tornado.gen.coroutine
def sign_in(account_id, current_date, _, __)
```

Handle the user's check-in.
:param account_id: user account id.
:param current_date: current date by local time.
:param _: no use
:param __: no use

# `calendar_bot.actions.direct_sign_out`

Handle the user's direct check-out

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `deal_sign_out_message()`

```python
def deal_sign_out_message(sign_time, manual_flag=False)
```

Generate a message returned to the user when checking out.
:param sign_time: The user's check-in time is a timestamp.
:param manual_flag: Boolean value. True is manually enters time.
:return: message content is a json.

## `deal_sign_out()`

```python
@tornado.gen.coroutine
def deal_sign_out(account_id, current_date, sign_time, manual_flag=False)
```


## `direct_sign_out()`

```python
@tornado.gen.coroutine
def direct_sign_out(account_id, current_date, sign_time, _)
```

Handle the user's direct check-out.
:param account_id: user account id.
:param current_date: current date by local time.
:param sign_time: Time when the user clicks to check-out.
:param _: no use

# `calendar_bot.actions.confirm_in`

Deal confirm check-in

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `deal_confirm_in()`

```python
@tornado.gen.coroutine
def deal_confirm_in(account_id, create_time, callback)
```

will be linked with the calendar internally, Check in time of registered user.
Check also: calendar_bot/externals/calendar_req.py
:param account_id: user account id.
:param create_time: current date by local time.
:param callback: The message content of the callback,
    include the user's check-in time
:return: Prompt message of successful check in.

## `confirm_in()`

```python
@tornado.gen.coroutine
def confirm_in(account_id, current_date, create_time, callback)
```

This function is triggered when the user clicks confirm check-in.
Update user's input reminder status, progress.
:param account_id: user account id.
:param current_date: current date by local time.
:param create_time: Time the request arrived at the server.
:param callback: User triggered callback.
:return: None

# `calendar_bot.actions.deal_message`

deal user input messages

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `deal_user_message()`

```python
@tornado.gen.coroutine
def deal_user_message(account_id, current_date, create_time, message)
```

Process messages entered by users,
Different scenarios need different processing functions.
Please see the internal implementation of the handler.
:param account_id: user account id.
:param current_date: current date by local time.
:param create_time: Time when the user requests to arrive at the BOT server.
:param message: User entered message.
:return: message content

## `deal_message()`

```python
@tornado.gen.coroutine
def deal_message(account_id, current_date, create_time, message)
```

Process messages manually entered by the user.
:param account_id: user account id.
:param current_date: current date by local time.
:param create_time: Time the request arrived at the server.
:param callback: User triggered callback.
:return: None

# `calendar_bot.actions.manual_sign_out`

Handle the user's manual check-out

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `manual_sign_out_message()`

```python
def manual_sign_out_message()
```

generate manual check-out message
:return: message content list

## `manual_sign_out_content()`

```python
@tornado.gen.coroutine
def manual_sign_out_content(account_id, current_date)
```

Update user status and generate manual check-out message.
:param account_id: user account id
:param current_date: current date by local time.
:return: message content list

## `manual_sign_out()`

```python
@tornado.gen.coroutine
def manual_sign_out(account_id, current_date, _, __)
```

Handle the user's manual check-out.
:param account_id: user account id.
:param current_date: current date by local time.
:param _: no use
:param __: no use

# `calendar_bot.actions.direct_sign_in`

Handle the user's direct check-in

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `deal_sign_in_message()`

```python
def deal_sign_in_message(sign_time, manual_flag)
```

Generate a message returned to the user when checking in.
:param sign_time: The user's check-in time is a timestamp.
:param manual_flag: Boolean value. True is manually enters time.
:return: message content is a json.

## `deal_sign_in()`

```python
@tornado.gen.coroutine
def deal_sign_in(account_id, current_date, sign_time, manual_flag=False)
```


## `direct_sign_in()`

```python
@tornado.gen.coroutine
def direct_sign_in(account_id, current_date, sign_time, _)
```

Handle the user's direct check-in.
:param account_id: user account id.
:param current_date: current date by local time.
:param sign_time: Time when the user clicks to check-in.
:param _: no use

# `calendar_bot.actions.start`

Start using robots

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `image_introduce()`

```python
def image_introduce()
```

This function constructs three image carousels for self introduction.
Check also: calendar_bot/model/data.py
[reference](https://developers.worksmobile.com/kr/document/100500809?lang=en)
:return: image carousels type message content.

## `sign()`

```python
@tornado.gen.coroutine
def sign(account_id)
```

Set up rich menu for chat with users.
Check also: calendar_bot/model/data.py
[reference](https://developers.worksmobile.com/jp/document/1005040?lang=en)
:param account_id: user account id

## `start_content()`

```python
@tornado.gen.coroutine
def start_content(account_id)
```


## `start()`

```python
@tornado.gen.coroutine
def start(account_id, _, __, ___)
```

Handle the user start using robots.
Send the robot's self introduction information,
and the chat room is bound with rich menu.
:param account_id: user account id.

# `calendar_bot.actions.sign_out`

Handle the user's check-out

## `LOGGER`

```python
LOGGER = logging.getLogger("calendar_bot")
```


## `sign_out_message()`

```python
def sign_out_message()
```

generate check-out message
:return: button type message content

## `sign_out_content()`

```python
@tornado.gen.coroutine
def sign_out_content(account_id, current_date)
```

Update user status and generate check-out message.
:param account_id: user account id
:param current_date: current date by local time.
:return: button type message content

## `sign_out()`

```python
@tornado.gen.coroutine
def sign_out(account_id, current_date, _, __)
```

Handle the user's check-out.
:param account_id: user account id.
:param current_date: current date by local time.
:param _: no use
:param __: no use

