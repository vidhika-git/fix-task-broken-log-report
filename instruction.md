There is an Apache-style access log in your working directory at /app/access.log. Read it and write a JSON summary report describing the traffic.

Your solution must satisfy the following:

1. Write the report to /app/report.json as a single JSON object containing exactly three keys: total_requests, unique_ips, and top_path — no other keys.
2. total_requests must be an integer equal to the total number of request lines in the log.
3. unique_ips must be an integer equal to the number of distinct client IP addresses seen (the first field of each log line).
4. top_path must be a string containing the single most frequently requested path (the request target from the request line, e.g. /index.html) — the path with the highest request count.

Do not modify /app/access.log.