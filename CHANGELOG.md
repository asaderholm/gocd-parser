# 1.2.1
* Permit anonymous commits - PR #2

# 1.2.0
* Fix: pipeline that is building, but previously failing, counts as a blocker
* StreamStatus object get_blocker_names() is deprecated, replaced by set_blockers()

# 1.1.5
* Update comparison page parser to handle new format in GoCD server 16.4
    * For good measure, we also test against 16.5
* Fix: pipelines that are building are not complete

# 1.1.4
* Fix incorrect ancestor groups
    * Was being set from ancestors of the base pipeline, not the blocker pipeline

# 1.1.3
* Fix broken pip install

# 1.1.2
* Handle stream and parser corner cases
* Switch to dashboard api to retrieve overall status
    * cctray did not include paused pipelines

# 1.1.1
* Switch to Python requests; handles non-api authentication for free!
* Handle corner case of cctray parser

# 1.1.0
* Realize I neglected the change log!
* Add unit tests with vcrpy, enabling major refactoring
* Refactor graph to instead use in-memory graph db: networkx
    * This simplifies and normalizes graph operations; try it!
    * Old method is still available, but subject to deprecation!
* Reduce URL hits on the GoCD server
    * Only look up failing pipelines; we chack this by hitting cctray.xml
* Parse code comparison and materials changes
    * When the value stream is blocked, now you know what caused it

# 1.0.0
* Initial public release
