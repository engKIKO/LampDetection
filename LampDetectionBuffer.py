from collections import Counter
from datetime import datetime, timedelta

class LampDetectionBuffer:
    def __init__(self, interval_seconds=60):
        self.interval = timedelta(seconds=interval_seconds)
        self.start_time = datetime.now()
        self.buffer = []

    def add_detection(self, label, confidence):
        self.buffer.append((datetime.now(), label.lower(), confidence))
        self._remove_old_entries()

    def _remove_old_entries(self):
        cutoff = datetime.now() - self.interval
        self.buffer = [(t, label, conf) for t, label, conf in self.buffer if t >= cutoff]

    def get_majority_label(self):
        self._remove_old_entries()
        
        confidence_sum = {
            "on": 0.0,
            "off": 0.0,
            "unknown": 0.0
        }
        
        for _, label, confidence in self.buffer:
            if label in confidence_sum:
                confidence_sum[label] += confidence
            else:
                confidence_sum["unknown"] += confidence

        # Decide based on maximum total confidence
        majority_label = max(confidence_sum, key=confidence_sum.get)
        return majority_label, confidence_sum

    def should_log_broken_lamp(self, is_night_time=True):
        majority_label, confidence_sum = self.get_majority_label()

        # Customizable logic
        if is_night_time:
            if majority_label == "off":
                return True
        else:
            if majority_label == "off":
                return True
        return False

    def clear(self):
        self.buffer.clear()
