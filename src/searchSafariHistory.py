#!/usr/bin/python
# encoding: utf-8

import sys
from workflow import Workflow3, ICON_WEB, ICON_WARNING

import sqlite3
import os
from datetime import datetime

__author__ = 'rx2130'
__version__ = '1.0'

UPDATE_SETTINGS = {
    'github_slug': 'rx2130/alfred-safari-history-searchs',
    'version': __version__,
    'frequency': 7
}
HELP_URL = 'https://github.com/rx2130/alfred-safari-history-search'
ICON_UPDATE = os.path.join(os.path.dirname(__file__), 'update-available.png')
PATH = os.path.expanduser('~/Library/Safari/History.db')
HISTORY_LIMIT = 20


def searchSafariHistory(args):
    sql, query = searchPatternCmd(args)

    with sqlite3.connect(PATH) as con:
        for r in con.execute(sql, query):
            yield r


def searchPatternCmd(args):
    query = [u'%{}%'.format(w) for w in args.split(' ') if w]

    sql = '''
    SELECT title, url, visit_time + 978307200, title || ' ' || url AS s
    FROM history_visits AS v
    INNER JOIN history_items AS i
    ON v.history_item = i.id
    WHERE title <> '' {}
    ORDER BY visit_time DESC
    LIMIT {}
    '''.format('AND s LIKE ? ' * len(query), HISTORY_LIMIT)

    return sql, query


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
    # workflow update
    if wf.update_available:
        wf.add_item(
            'A newer version is available',
            '↩ to install update',
            autocomplete='workflow:update',
            icon=ICON_UPDATE)

    # search history
    args = wf.args[0]
    history = searchSafariHistory(args)

    r = None
    for r in history:
        title, url, time, _ = r
        time = timeBeautify(time)
        wf.add_item(
            title,
            time + url,
            arg=url,
            valid=True,
            icon=ICON_WEB,
            copytext=url,
            largetext=u'{}\n{}\n{}'.format(title, url, time))
    if r is None:
        wf.add_item('No history found', icon=ICON_WARNING)

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3(help_url=HELP_URL, update_settings=UPDATE_SETTINGS)
    sys.exit(wf.run(main))
