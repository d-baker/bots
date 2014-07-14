MoonDate
========
A Python class for lunar phases, which can currently
- tell you the lunar phase in your hemisphere on a specific date (by default this is today's date)
- retrieve the appropriate moon emoji depending on the lunar phase

...yeah, not very exciting I know :) suggestions for further features welcome!

Installation
--------------
download the raw file [here](https://raw.githubusercontent.com/d-baker/bots/master/everymoon/moondate.py) and put it in the directory you want to work in. easy!

Usage
--------

```
from moondate import MoonDate
from datetime import date
...
your_date = date(year, month, day)
<your_var_name> = MoonDate(hemisphere, [mdate=your_date])
```

`mdate` (stands for 'moondate', to avoid naming conflicts) is a date object and is optional - if you don't specify a date, it defaults to today's date.
`hemisphere` is a string, which can be either "southern" or "northern".

for example usage of MoonDate take a look at everymoon.py, a twitterbot which tweets moon emoji based on the current lunar phase (that's what I wrote it for).
