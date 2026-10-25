#!/usr/bin/env python3
"""Unexecuted, bounded HTTP-status reproducer. No artifact body is read or saved."""
import argparse
import datetime
import json
import urllib.error
import urllib.parse
import urllib.request

ARTIFACTS = [
    {
        "coordinate": "com.facebook.react:react-android:0.86.3:debug@aar",
        "url": "https://repo.reactnative.dev/maven2/com/facebook/react/react-android/0.86.3/react-android-0.86.3-debug.aar",
        "published_bytes": 279001319,
        "published_sha256": "21235cb3b34912f2c5042dfd293be3334735a7beafcf28c0c59f1ccbd13733e8",
    },
    {
        "coordinate": "com.facebook.hermes:hermes-android:250829098.0.17:debug@aar",
        "url": "https://repo.reactnative.dev/maven2/com/facebook/hermes/hermes-android/250829098.0.17/hermes-android-250829098.0.17-debug.aar",
        "published_bytes": 112345699,
        "published_sha256": "2a2f6431807d46cb6c5cd16e1f96c4a033dd76756b641e1901462bded6b1ed61",
    },
]

class DoNotFollowRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def safe_headers(headers):
    # Omit cookies, authentication data, client IP fields and signed query strings.
    result = {}
    for name in ["Date", "Server", "Content-Type", "Content-Length", "Retry-After"]:
        if headers.get(name) is not None:
            result[name] = headers.get(name)
    if headers.get("Location"):
        parsed = urllib.parse.urlsplit(headers.get("Location"))
        result["Location_without_query_or_fragment"] = urllib.parse.urlunsplit(
            (parsed.scheme, parsed.hostname or "", parsed.path, "", "")
        )
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Explicitly authorize two GET requests")
    args = parser.parse_args()
    if not args.run:
        parser.error("No requests made. Review the README before explicitly using --run.")
    opener = urllib.request.build_opener(DoNotFollowRedirects())
    results = []
    for artifact in ARTIFACTS:
        record = dict(artifact, request_started_utc=now(), method="GET",
                      artifact_body_bytes_read=0, redirects_followed=0, retries=0)
        response = None
        try:
            response = opener.open(urllib.request.Request(artifact["url"], method="GET"), timeout=30)
        except urllib.error.HTTPError as error:
            response = error
        except urllib.error.URLError:
            record["transport_error"] = "URLError (details omitted to avoid disclosing network information)"
        except TimeoutError:
            record["transport_error"] = "TimeoutError"
        if response is not None:
            try:
                record["http_status"] = response.code
                record["headers"] = safe_headers(response.headers)
            finally:
                response.close()  # Do not read or save the artifact or error body.
        record["request_finished_utc"] = now()
        results.append(record)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
