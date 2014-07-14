import calendar
from datetime import datetime

class MoonDate:
    HALF_WEEK = 7/2

    def __init__(self, day = None, hemisphere = None):

        # current day is default
        if day is None:
            self.month_day = datetime.today().day
        else:
            self.month_day = day

        self.month = datetime.today().month
        self.year = datetime.today().year
        self.last_month_day = calendar.monthrange(self.year, self.month)[1]

        # northern hemisphere is default
        self.emoji = [
            "\U0001f311", #new moon
            "\U0001f312", #waxing crescent
            "\U0001f313", #first quarter
            "\U0001f314", #waxing gibbous
            "\U0001f315", #full moon
            "\U0001f316", #waning gibbous
            "\U0001f317", #last quarter
            "\U0001f318", #waning crescent
        ]

        # change order of emoji for southern hemisphere
        if hemisphere == "southern":
            self.emoji = [
                "\U0001f311", #new moon
                "\U0001f318", #waxing crescent
                "\U0001f317", #first quarter
                "\U0001f316", #waxing gibbous
                "\U0001f315", #full moon
                "\U0001f314", #waning gibbous
                "\U0001f313", #last quarter
                "\U0001f312", #waning crescent
            ]


    def get_cur_phase(self):
        if self.new_moon():
            return "new moon"
        elif self.waning_cresc(): 
            return "waxing crescent"
        elif self.first_quart():
            return "first quarter"
        elif self.waxing_gibb():
            return "waxing gibbous"
        elif self.full_moon():
            return "full moon"
        elif self.waning_gibb():
            return "waning gibbous"
        elif self.last_quart():
            return "last quarter" 
        elif self.waning_cresc():
            return "waning crescent"

    def get_emoji(self):
        cur_phase = "oops, something went wrong"

        if self.new_moon():
            cur_phase = self.emoji[0]
        elif self.waxing_cresc():
            cur_phase = self.emoji[1]
        elif self.first_quart():
            cur_phase = self.emoji[2]
        elif self.waxing_gibb():
            cur_phase = self.emoji[3]
        elif self.full_moon():
            cur_phase = self.emoji[4]
        elif self.waning_gibb():
            cur_phase = self.emoji[5]
        elif self.last_quart():
            cur_phase = self.emoji[6] 
        elif self.waning_cresc():
            cur_phase = self.emoji[7]

        return cur_phase

    def day_between(self, lower, upper):
        if self.month_day >= lower and self.month_day < upper:
            return True
        else:
            return False

    def new_moon(self):
        if self.day_between(1, MoonDate.HALF_WEEK):
            return True
        return False

    def waxing_cresc(self):
        if self.day_between(MoonDate.HALF_WEEK, 7):
            return True
        return False

    def first_quart(self):
        if self.day_between(7, 7 + MoonDate.HALF_WEEK):
            return True
        return False

    def waxing_gibb(self):
        if self.day_between(7 + MoonDate.HALF_WEEK, 14):
            return True
        return False

    def full_moon(self):
        if self.day_between(14, 14 + MoonDate.HALF_WEEK):
            return True
        return False

    def waning_gibb(self):
        if self.day_between(14 + MoonDate.HALF_WEEK, 21):
            return True
        return False

    def last_quart(self):
        if self.day_between(21, 21 + MoonDate.HALF_WEEK):
            return True
        return False

    def waning_cresc(self):
        if self.day_between(21 + MoonDate.HALF_WEEK, self.last_month_day):
            return True
        return False

