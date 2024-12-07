# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [6.0.0]
### Changed
- delete 10 of the easiest problems
- select a subset of 25 to use as the competition problem set
- remove "best of 5" logic and instead just run each problem multiple times and
  sum the score
- refactor config.yaml

## [5.0.0]
### Added
- Count API calls

### Changed
- New rate limiting system
- Prompts changed to make it easier for stupider models

## [4.0.0]
### Fixed
- remove overly common words from verifications

## [3.0.0]
### Added
- Log more information about errors.
- Rate limiting
- Retry logic for Anthropic

### Fixed
- Many of the interrogees were broken.

## [2.0.0]
### Added
- record metrics to postgres for analysis

### Changed
- doubled the number of questions
 
