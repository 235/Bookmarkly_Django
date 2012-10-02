This is a **Backbone.js** + **Django** testing application. This is the first alpha with a very crude API implementation. Ideally, the API it should be rewritten with [django-tastypie](http://django-tastypie.readthedocs.org/en/latest/index.html), but that will require changes of the front-end as well. Consider that this version was just a testbed. 

![Bookmarkly.com](http://bookmarkly.com/images/homeshot.png)

This repository contains a fork of the code behind [Bookmarkly](http://bookmarkly.com), a bookmark organizer built with [Backbone.js](http://backbonejs.org/).

Originally, the server side was buid with [Node.js](http://nodejs.org/), however, this fork replaces it with Python/[Django](https://www.djangoproject.com) (based on this [django template](https://github.com/lincolnloop/django-layout), you can borrow other scripts there).


Some features:

* Add bookmarks with a bookmarklet, Chrome extension or through the site
* Saves URL, title, description, tags with autosuggest and a screenshot
* Bookmark grid view resizes with the window and loads more bookmarks on scroll
* Can import bookmark files exported from IE, Chrome, Firefox and Delicious
* No page reloads at all, so moving between pages is near-instant and smooth
* Combines and minifies all the JS source and view templates automatically when the server starts

## Installation

1. Clone this repository

2. Run `bootstrap_venv.sh` to initialise a virtual environment

3. Configure your local settings in `app/settings/local.py`

4. Initialise database `./manage.py syncdb`

5. Run `./manage.py runserver` and browse to `http://localhost:8000`



## License
The backend in `app` by Oleksandr Pryymak, 2012. The frontend in `public` and the idea behind all API calls in `app` by (the original licence):

Copyright (c) 2012 Dan Grossman. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of the author nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.