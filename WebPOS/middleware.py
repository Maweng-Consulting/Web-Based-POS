# middleware.py
class CashierMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        cashier_id = request.session.get('cashier_id')
        if cashier_id:
            request.current_cashier = cashier_id
        else:
            request.current_cashier = None

        response = self.get_response(request)
        return response
