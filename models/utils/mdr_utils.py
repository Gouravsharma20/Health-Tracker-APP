# MDR (Merchant Discount Rate) Dictionary
MDR_RATES = {
    "UPI": 0.00,             # 0% MDR
    "Visa Credit Card": 0.015,  # 1.5% MDR
    "Visa Debit Card": 0.01,    # 1% MDR
    "Mastercard Credit Card": 0.017,  # 1.7% MDR
    "Mastercard Debit Card": 0.012,   # 1.2% MDR
    "RuPay Credit Card": 0.01,   # 1% MDR
    "RuPay Debit Card": 0.005,   # 0.5% MDR
    "Amex Card": 0.02,        # 2% MDR
    "Paytm Wallet": 0.015,    # 1.5% MDR
    "Mobikwik Wallet": 0.02,  # 2% MDR
    "PayPal": 0.03,           # 3% MDR (International payments)
    "Cash": 0.00              # No MDR for cash transactions
}

def calculate_final_amount(amount, payment_method):
    """Calculates the final amount after applying MDR fees."""
    mdr = MDR_RATES.get(payment_method, 0)
    mdr_fee = amount * mdr
    final_amount = amount + mdr_fee
    return round(final_amount, 2), round(mdr_fee, 2)
