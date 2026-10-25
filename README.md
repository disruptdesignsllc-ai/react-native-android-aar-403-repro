# React Native Android artifact HTTP-status reproduction

**Status: this new reproduction script has not been executed.** These local files have not been published, and no public reproducer URL exists yet. This is an artifact-access reproducer, not a complete React Native application or a claim to satisfy every issue-template requirement.

## Historical observation

On October 25, 2026, a separate earlier downloader attempted one HTTPS GET for each of the two public artifact URLs listed in `reproduce.py`. Both returned HTTP 403 Forbidden; zero artifact bytes were downloaded. The failure record was saved at 21:55:43 UTC; exact individual request timestamps were not retained. Response headers and error bodies are unavailable. The cause is unknown. No retries or alternate routes were attempted.

The expected sizes and SHA-256 values in the script come from published Gradle module metadata. They are not hashes of successfully downloaded artifacts.

## Scope and requirements

- Python 3 standard library only; no package installation.
- Exactly one GET per listed artifact, with a 30-second timeout per request.
- No retries, redirect following, mirrors, proxy configuration, custom request headers, authentication or version changes.
- The response is closed without reading or saving its body, even if it succeeds. Therefore this script does not verify artifact payload checksums, and it cannot establish zero transport-level buffering.
- Logs UTC request times, HTTP status and selected response headers to standard output. It excludes cookies, authentication fields and client-IP fields, and removes query strings from any redirect location.
- Does not build an app, inspect a project, run React Native CLI, or collect local usernames, paths, account information or credentials.

## Optional execution by an authorized maintainer

Review the code and obtain any required network approval first. The following command would make fresh requests; it has not been run as part of preparing this reproducer:

```sh
python3 reproduce.py --run
```

Review output before sharing. Do not interpret the historical 403 observations as a current availability check. Stop and seek guidance if access is denied; do not reroute or repeat requests to bypass a restriction.

## Expected versus observed

Expected: the public artifacts are accessible, or the host provides documented access requirements.

Historically observed: HTTP 403 for both URLs. Results from this new script: not available because it has not been executed.

## React Native CLI information

Actual `react-native info` output is unavailable. Local module-resolution checks found `@react-native-community/cli` missing from the project and checked global Node locations. The installed React Native launcher requires that separate package; its `@react-native/community-cli-plugin` dependency is not the Community CLI itself. No CLI was fetched or installed, and no environment summary is presented as CLI output.

## References

- [Sonatype: authoritative artifact redirects](https://central.sonatype.org/faq/429-operational-dependencies/)
- [React Native issue #58427](https://github.com/react/react-native/issues/58427): a closed iOS 404 issue with a later report of the same React Android URL returning 403. This does not establish a shared cause or a current outage.

## Publication boundary

Only `README.md` and `reproduce.py` are intended for possible publication after separate approval. No private application source or diagnostic logs are included. A public repository URL must be obtained after actual publication; these local files do not meet that form requirement by themselves.
