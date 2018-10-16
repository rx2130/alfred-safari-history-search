Alfred Safari History Search
=================

Search Safari browse history from Alfred. Support Sierra, High Sierra adn Mojave. (Earlier os untested)

Demo
----

![][demo]

Note for MacOS 10.14 Mojave users
---------------------------------
If you got the `unable to open database file` error, go to `System Preferences > Security & Privacy > Privacy > Full Disk Access` and give `Alfred 3.app` permission to access Safari data :)

Download
--------

Get Alfred Safari History Search from [GitHub][gh-releases].


Usage
-----

- `hsi` — Show list of recent 20 Safari browse history
- `hsi <query>` — Search for history matching `<query>`
  - `↩` or `⌘+NUM` — Open URL in browser
  - `⇧` or `⌘+Y` — Show Quick Look preview of URL
  - `⌘+L` — Show full title, URL, browse date in Alfred's Large Type window
  - `⌘+C` - Copy link URL


Licensing, thanks etc.
----------------------

[MIT][mit].

It's heavily based on [Alfred-Workflow][alfred-workflow], also [MIT-licensed][mit].



[mit]: http://opensource.org/licenses/MIT
[alfred-workflow]: http://www.deanishe.net/alfred-workflow/
[gh-releases]: https://github.com/rx2130/alfred-safari-history-search/releases
[demo]: https://raw.githubusercontent.com/rx2130/alfred-safari-history-search/master/demo.gif
