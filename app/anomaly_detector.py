import numpy as np
from sklearn.ensemble import IsolationForest
from datetime import datetime
import re

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.05, random_state=42)
        self.vectorized_logs = []
        self.trained = False

    def preprocess(self, line):
        """
        Convert log line to a numeric vector for ML.
        Basic method: Convert length, word count, special chars, entropy.
        """
        length = len(line)
        word_count = len(line.split())
        digit_count = sum(c.isdigit() for c in line)
        symbol_count = len(re.findall(r'[^\w\s]', line))
        entropy = self.calculate_entropy(line)
        return [length, word_count, digit_count, symbol_count, entropy]

    def calculate_entropy(self, s):
        """
        Shannon entropy of a string.
        """
        from collections import Counter
        prob = [n / len(s) for n in Counter(s).values()]
        return -sum(p * np.log2(p) for p in prob if p > 0)

    def train(self, log_lines):
        """
        Train IsolationForest on recent normal logs.
        """
        vectors = [self.preprocess(line) for line in log_lines if line.strip()]
        if len(vectors) < 20:
            print("[ML] Not enough data to train anomaly model.")
            return

        self.vectorized_logs = vectors
        self.model.fit(vectors)
        self.trained = True
        print(f"[ML] Trained anomaly model on {len(vectors)} entries.")

    def is_anomalous(self, line):
        """
        Check if a log line is anomalous using the trained model.
        """
        if not self.trained:
            return False

        vector = np.array(self.preprocess(line)).reshape(1, -1)
        prediction = self.model.predict(vector)  # -1 means anomaly
        return prediction[0] == -1
