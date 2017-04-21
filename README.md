[![Build Status](https://travis-ci.org/msurdi/cutepaste.svg?branch=master)](https://travis-ci.org/msurdi/cutepaste)

Cutepaste
=========

Web based file browser focused on copying/pasting
server side files.

![screenshot](http://i.imgur.com/z559VIb.png)


Trying it out
-------------

*Note*: Do not run as root


    docker run -d -v /path/to/your/files:/data -p 8080:8080 msurdi/cutepaste:1.0
 
 
To run it with custom settings, copy [this file](https://github.com/msurdi/cutepaste/blob/master/cutepaste/settings/prod.py) to
somewhere, modify it, and then add to the prvious command:

    -v /path/to/your/prod.py:/code/cutepaste/settings/prod.py
   

Development
-----------
Development server with live reload, etc:

    make run
    
Running tests:

    make test
    
Development environment shell:

    make shell
