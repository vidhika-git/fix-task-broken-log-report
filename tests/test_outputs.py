import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _compute_expected():
    """Independently recompute expected stats from the access log."""
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return total, len(ips), paths.most_common(1)[0][0]


def test_report_written_as_valid_json_with_exact_keys():
    """Criterion 1: report is written to /app/report.json as a JSON object
    with exactly total_requests, unique_ips, and top_path — no other keys."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    report = json.loads(REPORT_PATH.read_text())
    assert set(report.keys()) == {"total_requests", "unique_ips", "top_path"}


def test_total_requests_correct():
    """Criterion 2: total_requests equals the number of request lines in the log."""
    expected_total, _, _ = _compute_expected()
    report = json.loads(REPORT_PATH.read_text())
    assert report["total_requests"] == expected_total


def test_unique_ips_correct():
    """Criterion 3: unique_ips equals the number of distinct client IP addresses."""
    _, expected_ips, _ = _compute_expected()
    report = json.loads(REPORT_PATH.read_text())
    assert report["unique_ips"] == expected_ips


def test_top_path_correct():
    """Criterion 4: top_path is the single most frequently requested path."""
    _, _, expected_top = _compute_expected()
    report = json.loads(REPORT_PATH.read_text())
    assert report["top_path"] == expected_top