Pixel Recognition

This Repository used to detect pattern of specific pixel values in image.
Currently works only for pink color and it's some of variations.


Sample CURL Request:

curl -X POST \
  http://127.0.0.1:8080/uploader \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'Postman-Token: ad510159-778f-440b-b247-bdeda7272321' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F file=undefined


Start Python Flask Server:

python3 mainServer.py 
