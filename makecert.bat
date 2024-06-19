@echo off
2>startup.log (
cd ssl
mkcert -install
mkcert localhost.com "*.localhost.com" localhost.test localhost 127.0.0.1 ::1
)