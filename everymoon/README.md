MoonDate
========
A Python class for lunar phases, which can currently
- tell you the lunar phase in your hemisphere on a specific date (by default this is today's date)
- retrieve the appropriate moon emoji depending on the lunar phase

...yeah, not very exciting I know :) suggestions for further features welcome!

Installation
--------------
download the raw file [here]() and put it in the directory you want to work in. easy!

Usage
--------

```
from moondate import MoonDate
...
<your_var_name> = MoonDate([date][hemisphere])
```

`date` and `hemisphere` are optional. The first is a datetime object and the second is a string, which can be either "southern" or (by default) "northern".
If you don't specify a date, MoonDate defaults to today's date. 

for example usage of MoonDate take a look at everymoon.py, a twitterbot which tweets moon emoji based on the current lunar phase (that's what I wrote it for).
