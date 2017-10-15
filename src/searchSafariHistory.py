#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow, ICON_WEB, ICON_WARNING

import sqlite3
from os.path import expanduser
from datetime import datetime

UPDATE_SETTINGS = {'github_slug': 'deanishe/alfred-reddit'}
HELP_URL = 'https://github.com/deanishe/alfred-reddit'

sql = '''
SELECT title, url, visit_time + 978307200
FROM history_visits AS v
INNER JOIN history_items AS i
ON v.history_item = i.id
WHERE title <> '' AND (title LIKE ? OR url LIKE ?)
ORDER BY visit_time DESC
LIMIT 20
'''


def searchSafariHistory(query):
    path = expanduser('~/Library/Safari/History.db')
    con = sqlite3.connect(path)

    keyword = '%' + query + '%'
    pattern = (keyword, keyword, )

    with con:
        cur = con.cursor()
        cur.execute(sql, pattern)
        return cur.fetchall()


def timeBeautify(time):
    res = None
    time = datetime.fromtimestamp(time)
    now = datetime.now()
    if time.date() == now.date():
        res = time.strftime('%-I:%M %p')
    else:
        res = time.strftime('%A,%B %-d,%Y')
    return '[{}] '.format(res)


def main(wf):
    args = wf.args[0]
    history = searchSafariHistory(args)

    if not history:
        wf.add_item('No history found', icon=ICON_WARNING)
        wf.send_feedback()
        return

    for r in history:
        title, url, time = r
        wf.add_item(
            title=title,
            subtitle=timeBeautify(time) + url,
            arg=url,
            valid=True,
            icon=ICON_WEB)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    sys.exit(wf.run(main))
