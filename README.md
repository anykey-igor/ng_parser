# ng_parser
#Parser Nginx log

Using log format 

```python
log_format myformat '$remote_addr - - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
```
