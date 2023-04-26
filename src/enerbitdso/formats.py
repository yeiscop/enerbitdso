import csv
import io

import orjson

import enerbitdso.enerbit as enerbit


def as_json(records: list[enerbit.ScheduleUsageRecord]) -> io.BytesIO:
    content = orjson.dumps(records)
    res = io.BytesIO(content)
    return res


def as_csv(records: list[enerbit.ScheduleUsageRecord]) -> io.BytesIO:
    res = io.BytesIO()
    writer = csv.writer(res, dialect="excel", delimiter=",")
    writer.writerows(records)
    return res
