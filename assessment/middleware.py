from django.http import HttpResponse


class IshanDaiMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        HTTP_X_FORWARDED_FOR = request.META.get("HTTP_X_FORWARDED_FOR")
        if HTTP_X_FORWARDED_FOR:
            ip = HTTP_X_FORWARDED_FOR.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        print(ip)
        ishan_dai_ip = "192.168.2.19"
        if str(ip) == ishan_dai_ip:
            return HttpResponse("<h1>K cha Ishan dai</h1>")
        if str(ip) == "127.0.0.1":
            return HttpResponse("<h1>K cha Ishan dai</h1>")
        return HttpResponse("<h1>K cha Ishan dai</h1>")
