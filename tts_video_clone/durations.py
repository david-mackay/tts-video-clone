import json


def _get_intervals(data, total_length):
    intervals = []
    for i in range(len(data) - 1):
        interval = data[i + 1] - data[i]
        intervals.append(interval)
    intervals.append(total_length - data[-1])
    return intervals


def get_durations_from_speechmarks(filename: str, total_length):
    timestamps = []
    sentences = []
    with open(filename, 'r') as f:
        for i in f:
            data = json.loads(i)
            timestamps.append(data["time"])
            sentences.append(data["value"])
    return _get_intervals(timestamps, total_length), sentences
