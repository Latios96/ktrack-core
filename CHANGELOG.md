# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).



## [Unreleased]
### Added
- Tests: added batch file which runs regular ktrack tests, kttk_widgets tests and maya tests (regular tests and maya tests)
- FileManagerWidget can now open and advance files
- Maya Engine: get qt_main_window
- we can run tests for Maya
### Changed
- renamed ktrack_command to ktrack
### Fixed
- Context step was not validated correctly, now only accepts not None not empty strings or unicode
- FileManager OpenManager: now correclty calls engine to open file
- Maya Engine: now correctly sets project
### Added
## 0.0.1 - 2017-07-24
### Added
- This CHANGELOG file to hopefully serve as an evolving example
- __version__ to kttk
