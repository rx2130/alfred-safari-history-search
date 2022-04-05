import sys
import json
import sqlite3
import os
from datetime import datetime


PATH = os.path.expanduser("~/Library/Safari/History.db")
HISTORY_LIMIT = 40


def searchSafariHistory():
    query = ["%{}%".format(w) for w in sys.argv[1].split(" ") if w]

    sql = f"""
    SELECT title, url, visit_time + 978307200, title || ' ' || url AS s
    FROM history_visits AS v
    INNER JOIN history_items AS i
    ON v.history_item = i.id
    WHERE title <> ''
    {"AND s LIKE ? " * len(query)}
    ORDER BY visit_time DESC
    LIMIT {HISTORY_LIMIT}
    """

    with sqlite3.connect(PATH) as con:
        return con.execute(sql, query)


def timeBeautify(time):
    res = None
    time = datetime.fromtimestamp(time)
    now = datetime.now()
    if time.date() == now.date():
        res = time.strftime("%-I:%M %p")
    else:
        res = time.strftime("%A,%B %-d,%Y")
    return "[{}] ".format(res)


def main():
    items = []
    for r in searchSafariHistory():
        title, url, time, _ = r
        time = timeBeautify(time)
        items.append(
            {
                "title": title,
                "subtitle": time + url,
                "arg": url,
                "text": {
                    "copy": url,
                    "largetype": "{}\n{}\n{}".format(title, url, time),
                },
            }
        )
    print(json.dumps({"items": items}))


if __name__ == "__main__":
    main()
