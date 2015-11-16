"""
a simple profile
"""
from datetime import datetime

class Profile:
    def __init__(self):
        self.reset()

    def reset(self):
        self.history_counters = [{} for i in range(60)]
        self.current_counter = {}
        self.last_min_slice = 0
        self.start_time = datetime.utcnow()

    def count_event(self, event_key, event_value):
        now = datetime.utcnow()
        if now.minute != self.last_min_slice:
            # reset counter
            self.history_counters[self.last_min_slice] = self.current_counter
            self.last_min_slice = now.minute
            self.current_counter = {}
        else:
            if event_key not in self.current_counter:
                self.current_counter[event_key] = 0
            self.current_counter[event_key] += event_value

    def get_min_slice_event_count(self, event_key):
        now = datetime.utcnow()
        min = (now.minute - 1 + 60) % 60
        if now.minute != self.last_min_slice:
            # reset counter
            self.history_counters[self.last_min_slice] = self.current_counter
            self.last_min_slice = now.minute
            self.current_counter = {}
        if event_key in self.history_counters[min]:
            return self.history_counters[min][event_key]
        else:
            return 0

    def get_hour_slice_event_count(self, event_key):
        now = datetime.utcnow()
        # skip first minuter and last minuter due to not complete record
        elapse_min = max(0, (now.minute - self.start_time.minute + 60) % 60 - 1)
        min_count = min(60, elapse_min)
        t = 0
        for i in range(min_count):
            c_min = (now.minute - 1 - i) % 60
            if event_key in self.history_counters[c_min]:
                t += self.history_counters[c_min][event_key]
        if min_count == 0:
            return 0
        return t * (60 / float(min_count))

    def query(self):
        self.count_event("query", 1)

    def success(self):
        self.count_event("success", 1)

    def retry(self):
        self.count_event("retry", 1)

    def error(self):
        self.count_event("error", 1)

    def min_qps(self):
        return self.get_min_slice_event_count("success") / float(60)

    def hour_qps(self):
        return self.get_hour_slice_event_count("success") / float(3600)

    def avg_retry_count(self):
        if self.get_hour_slice_event_count("query") == 0:
            return 0
        return self.get_hour_slice_event_count("retry") / self.get_hour_slice_event_count("query")

    def error_rate(self):
        if self.get_hour_slice_event_count("query") == 0:
            return 0
        return self.get_hour_slice_event_count("error") / self.get_hour_slice_event_count("query")
