import re

# Each FAQ: keywords that trigger it, and the answer
FAQS = [
    {
        'keywords': ['hello', 'hi', 'hey', 'good morning', 'good evening'],
        'answer': "Hello! Welcome to Coach Factory. I can help with shipping, "
                  "payments, orders, returns, and accounts. What would you like to know?"
    },
    {
        'keywords': ['first order', 'first purchase', 'first time', 'new customer',
                     'first delivery'],
        'answer': "Your first order ships FREE, no matter the total. After that, shipping "
                  "is free on orders over $200, otherwise a flat $15 applies."
    },
    {
        'keywords': ['shipping', 'delivery', 'deliver', 'how long', 'arrive',
                     'free shipping', 'ship'],
        'answer': "Shipping is FREE on your first order. After that, orders over $200 ship "
                  "free, and orders under $200 have a flat $15 fee. Delivery usually takes "
                  "5-10 business days."
    },
    {
        'keywords': ['payment', 'pay', 'bitcoin', 'btc', 'crypto', 'wallet'],
        'answer': "We accept Bitcoin only. At checkout you'll get our BTC address and "
                  "QR code. Send the exact amount, then click 'I have sent the payment'. "
                  "An admin will confirm your payment shortly."
    },
    {
        'keywords': ['tx hash', 'transaction hash', 'txhash', 'hash', 'transaction id'],
        'answer': "The transaction hash is optional, but it helps us verify your payment "
                  "faster. You can find it in your wallet's transaction history after sending."
    },
    {
        'keywords': ['order status', 'my order', 'track', 'tracking', 'confirmed', 'pending'],
        'answer': "You can see your order status in My Account under 'My Orders'. "
                  "Pending means we are verifying your payment. Confirmed means your "
                  "order is accepted and you can view your receipt."
    },
    {
        'keywords': ['receipt', 'invoice', 'e-receipt'],
        'answer': "Your e-receipt is available in My Account once your order is confirmed. "
                  "Click 'Receipt' next to the order to view or print it."
    },
    {
        'keywords': ['quantity', 'how many', 'multiple', 'more than one'],
        'answer': "You can choose how many of each bag you want in your bag or at checkout. "
                  "The total updates automatically as you change the quantity."
    },
    {
        'keywords': ['return', 'refund', 'exchange', 'send back'],
        'answer': "We offer 30-day hassle-free returns. Contact coachfactory360@gmail.com "
                  "with your order number to start a return."
    },
    {
        'keywords': ['authentic', 'genuine', 'real', 'fake', 'original'],
        'answer': "Every Coach Factory product is authentic and crafted with premium "
                  "full-grain leather and signature Coach hardware."
    },
    {
        'keywords': ['login', 'log in', 'sign in', 'password', 'forgot'],
        'answer': "Click LOGIN in the top menu and enter your email and password. "
                  "If you don't have an account, click REGISTER to create one for free."
    },
    {
        'keywords': ['register', 'sign up', 'create account', 'account'],
        'answer': "Click REGISTER in the top menu, fill in your name, email and password. "
                  "Your account is created instantly."
    },
    {
        'keywords': ['add to bag', 'cart', 'bag', 'buy', 'checkout', 'order'],
        'answer': "Log in first, then click ADD TO BAG on any product. When you're ready, "
                  "open your bag and click CHECKOUT WITH BITCOIN."
    },
    {
        'keywords': ['contact', 'email', 'phone', 'support', 'human', 'agent', 'help',
                     'whatsapp', 'tiktok'],
        'answer': "You can reach us at coachfactory360@gmail.com, WhatsApp +1 (636) 427-8021, "
                  "or on TikTok at @coach_factory."
    },
    {
        'keywords': ['price', 'cost', 'how much', 'discount', 'sale'],
        'answer': "Prices are listed on each product page. Your first order ships free. "
                  "After that, shipping is free on orders over $200, otherwise $15 applies."
    },
]

FALLBACK = ("I'm not sure about that one. Try asking about shipping, payments, "
            "orders, returns, or accounts, or contact coachfactory360@gmail.com "
            "for personal help.")


def get_answer(message):
    text = re.sub(r'[^a-z0-9 ]', ' ', message.lower())
    text = ' ' + re.sub(r'\s+', ' ', text).strip() + ' '
    best, best_score = None, 0
    for faq in FAQS:
        score = sum(1 for kw in faq['keywords'] if f' {kw} ' in text)
        if score > best_score:
            best, best_score = faq, score
    return best['answer'] if best else FALLBACK