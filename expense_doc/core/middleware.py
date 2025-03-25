from django.conf import settings

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy
        csp_policies = [
            "default-src 'self'",
            "img-src 'self' data: https:",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
            "style-src 'self' 'unsafe-inline'",
            "font-src 'self' data:",
            "connect-src 'self'",
            "frame-ancestors 'none'",
            "form-action 'self'",
            "base-uri 'self'",
            "object-src 'none'"
        ]
        response['Content-Security-Policy'] = "; ".join(csp_policies)

        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=()'
        
        # HSTS (only in production)
        if not settings.DEBUG:
            response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'

        return response

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limits = {}

    def __call__(self, request):
        client_ip = self.get_client_ip(request)
        
        # Skip rate limiting for health checks from monitoring services
        if request.path == '/expense-doc/health' and self.is_monitoring_service(request):
            return self.get_response(request)

        # Implement basic rate limiting
        if not self.check_rate_limit(client_ip):
            from django.http import HttpResponseTooManyRequests
            return HttpResponseTooManyRequests("Rate limit exceeded")

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')

    def is_monitoring_service(self, request):
        monitoring_ips = getattr(settings, 'MONITORING_SERVICE_IPS', [])
        return self.get_client_ip(request) in monitoring_ips

    def check_rate_limit(self, client_ip):
        import time
        current_time = time.time()
        
        # Clean up old entries
        self.rate_limits = {ip: timestamps for ip, timestamps in self.rate_limits.items()
                          if timestamps[-1] > current_time - 3600}  # Keep last hour
        
        # Get or create timestamps list for client
        timestamps = self.rate_limits.get(client_ip, [])
        timestamps = [ts for ts in timestamps if ts > current_time - 60]  # Keep last minute
        
        # Check rate limit (100 requests per minute)
        if len(timestamps) >= 100:
            return False
        
        # Add current timestamp
        timestamps.append(current_time)
        self.rate_limits[client_ip] = timestamps
        
        return True 