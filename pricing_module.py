class Pricing_Module():
    def pricing_module(self,gallons_amount,state,ordered_before):
        location_factor=0.02
        rate_history_factor=0.01
        gallons_requested_factor=0.02
        if state!='TX':
            location_factor=0.04
        if ordered_before != True:
            rate_history_factor=0.0
        if gallons_amount < 1000:
            gallons_requested_factor=0.03
        margin=1.50 * (location_factor - rate_history_factor + gallons_requested_factor + 0.10)
        suggested_price= 1.50 + margin
        total_amount_due=gallons_amount*suggested_price
        return suggested_price,total_amount_due