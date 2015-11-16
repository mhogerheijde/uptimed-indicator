=================
uptimed-indicator
=================

This is intended to become a Unity indicator that keeps track of how 
many hours your computer has been on today, with the goal of giving 
insight to how many hours you worked today.

This means that you should shut your computer down at the end of the 
day; if you leave your computer on 24/7, this indicator is not meant for
you.

Status
------

 - depends on `uptimed` to keep track of uptimes
 - only works as a console command and outputs to stdout

Install
-------

Clone this repository and from the directory you cloned it to, do

::

    $ sudo pip install -e .


Usage
-----

::

    $ uptimed-indicator
    2015-10-26 (Mon) (44): 8:55:43 / 8:25:43
    2015-10-27 (Tue) (44): 8:20:20 / 7:50:20
    2015-10-28 (Wed) (44): 9:07:55 / 8:37:55
    2015-10-29 (Thu) (44): 8:25:52 / 7:55:52
    2015-10-30 (Fri) (44): 8:28:50 / 7:58:50
     -> Week 44 (days: 5) | 43:18:40 | overtime: +00:48:40
    2015-11-02 (Mon) (45): 9:03:18 / 8:33:18
    2015-11-03 (Tue) (45): 9:06:52 / 8:36:52
    2015-11-04 (Wed) (45): 9:12:58 / 8:42:58
    2015-11-05 (Thu) (45): 8:21:51 / 7:51:51
    2015-11-06 (Fri) (45): 8:31:11 / 8:01:11
     -> Week 45 (days: 5) | 44:16:10 | overtime: +01:46:10
    2015-11-09 (Mon) (46): 9:43:30 / 9:13:30
    2015-11-10 (Tue) (46): 9:11:36 / 8:41:36
    2015-11-11 (Wed) (46): 9:02:32 / 8:32:32
    2015-11-12 (Thu) (46): 9:15:01 / 8:45:01
    2015-11-13 (Fri) (46): 8:21:53 / 7:51:53
     -> Week 46 (days: 5) | 45:34:32 | overtime: +03:04:32
    2015-11-16 (Mon) (47): 9:08:06 / 8:38:06
     -> Week 47 (days: 1) | 09:08:06 | overtime: +00:38:06

