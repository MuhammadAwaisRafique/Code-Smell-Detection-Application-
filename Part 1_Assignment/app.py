# smelly_app/app.py
# Intentionally written to contain common code smells for the assignment.
# Each smell is tagged inline with comments like:  # [SMELL: Long Method]

from __future__ import annotations
from typing import List, Dict, Any


class Order:
    """A very lightweight order container."""
    def __init__(self, user_email: str, items: List[Dict[str, Any]]):
        self.user_email = user_email
        self.items = items
        self.subtotal = 0.0
        self.tax = 0.0
        self.shipping_fee = 0.0
        self.total = 0.0


class MegaApp:  # [SMELL: God Class] — does too many things (users, products, orders, pricing, reporting, I/O)
    def __init__(self):
        self.users: Dict[str, Dict[str, Any]] = {}
        self.products: Dict[str, Dict[str, Any]] = {}
        self.orders: List[Order] = []
        self._audit_log: List[str] = []

    def register_user(self, name: str, age: int, email: str, address: str, city: str, country: str,
                      postal_code: str, phone: str, subscribe_newsletter: bool, referral_code: str | None = None):
        # [SMELL: Large Parameter List] — too many parameters; should be an object or dataclass
        if email in self.users:
            raise ValueError("User already exists")
        self.users[email] = {
            "name": name,
            "age": age,
            "email": email,
            "address": address,
            "city": city,
            "country": country,
            "postal_code": postal_code,
            "phone": phone,
            "subscribe_newsletter": subscribe_newsletter,
            "referral_code": referral_code,
            "loyalty": 0,
        }
        self._audit_log.append(f"Registered user {email}")
        return self.users[email]

    def add_product(self, pid: str, name: str, price: float):
        if pid in self.products:
            raise ValueError("Product already exists")
        self.products[pid] = {"id": pid, "name": name, "price": price}
        self._audit_log.append(f"Added product {pid}:{name}")
        return self.products[pid]

    def calculate_discount_a(self, order_total: float, user: Dict[str, Any]) -> float:
        # [SMELL: Duplicated Code] — almost the same as calculate_discount_b with tiny differences
        # [SMELL: Magic Numbers] — 100, 0.05, 500, 0.10, 3, 0.02 appear without named constants
        discount = 0.0
        if order_total > 100:  # threshold 1
            discount += order_total * 0.05  # 5%
        if order_total > 500:  # threshold 2
            discount += order_total * 0.10  # 10%
        if user.get("loyalty", 0) > 3:  # loyalty level
            discount += order_total * 0.02  # 2%
        return discount

    def calculate_discount_b(self, order_total: float, user: Dict[str, Any]) -> float:
        # [SMELL: Duplicated Code] — repeated logic; should be refactored to a single strategy/function
        discount = 0.0
        if order_total > 100:
            discount += order_total * 0.05
        if order_total > 500:
            discount += order_total * 0.10
        if user.get("loyalty", 0) >= 4:  # slight variation but fundamentally duplicated
            discount += order_total * 0.02
        return discount

    def process_order(self, user_email: str, product_ids: List[str]) -> Order:
        # [SMELL: Long Method] — too many steps, conditional branches, and responsibilities in one method
        if user_email not in self.users:
            raise ValueError("Unknown user")

        user = self.users[user_email]

        # Build line items
        items: List[Dict[str, Any]] = []
        for pid in product_ids:
            if pid not in self.products:
                raise ValueError(f"Unknown product id: {pid}")
            prod = self.products[pid]
            items.append({"id": prod["id"], "name": prod["name"], "price": prod["price"], "qty": 1})

        order = Order(user_email, items)

        # Compute subtotal
        s = 0.0
        for it in items:
            # artificial verbosity to lengthen method
            price = float(it["price"])  # could be validated elsewhere
            qty = int(it["qty"]) if isinstance(it["qty"], int) else 1
            s += price * qty
        order.subtotal = round(s, 2)

        # Apply two discount systems (duplicated logic indirectly used)
        discount1 = self.calculate_discount_a(order.subtotal, user)
        discount2 = self.calculate_discount_b(order.subtotal, user)
        discount = max(discount1, discount2)  # choose best offer

        # Tax calculation
        # [SMELL: Magic Numbers] — 0.07 is an unexplained constant (tax rate)
        tax_rate = 0.07
        taxable_amount = max(order.subtotal - discount, 0)
        order.tax = round(taxable_amount * tax_rate, 2)

        # Shipping fee rules (contrived & verbose to extend length)
        # [SMELL: Magic Numbers] — 42 is an unexplained flat fee; 3.14 is another quirky constant
        if taxable_amount == 0:
            shipping = 0.0
        elif taxable_amount < 50:
            shipping = 42.0
        else:
            shipping = 3.14  # because… reasons
        order.shipping_fee = round(shipping, 2)

        # Update loyalty in a way that arguably belongs elsewhere
        # (another responsibility crammed into this long method)
        if taxable_amount > 200:
            user["loyalty"] += 2
        elif taxable_amount > 100:
            user["loyalty"] += 1
        else:
            user["loyalty"] += 0

        # Compute total
        order.total = round(max(taxable_amount + order.tax + order.shipping_fee, 0), 2)

        # Rudimentary audit and persistence side-effects (I/O-ish responsibility)
        self._audit_log.append(
            f"ORDER user={user_email} items={len(items)} subtotal={order.subtotal} discount={round(discount,2)}"
        )
        self.orders.append(order)

        # Additional bloating: inline formatting, printing, and tiny helpers
        def _format_money(x: float) -> str:
            return f"$ {x:,.2f}"

        # Pretend printing a receipt (I/O during domain processing)
        receipt_lines = [
            "=== RECEIPT ===",
            f"Customer: {user['name']} <{user_email}>",
            "Items:" if items else "(no items)",
        ]
        for it in items:
            receipt_lines.append(f" - {it['name']} x{it['qty']} = {_format_money(it['price'] * it['qty'])}")
        receipt_lines.extend([
            f"Subtotal: {_format_money(order.subtotal)}",
            f"Tax: {_format_money(order.tax)}",
            f"Shipping: {_format_money(order.shipping_fee)}",
            f"Total: {_format_money(order.total)}",
            "==============",
        ])
        # (We keep the receipt but do nothing real with it.)
        self._audit_log.extend(receipt_lines)

        return order

    def get_audit_log(self) -> List[str]:
        return list(self._audit_log)


class ReportGenerator:
    def summarize_order(self, order: Order, app: MegaApp) -> Dict[str, Any]:
        # [SMELL: Feature Envy] — This method pokes at Order and MegaApp internals
        # instead of using a cohesive API. It "envies" their data.
        user = app.users.get(order.user_email)  # reaches into app state
        product_names = [it["name"] for it in order.items]  # reaches into order internals
        line_count = len(app.get_audit_log())  # yet more peeking
        return {
            "user_name": user.get("name") if user else None,
            "loyalty": user.get("loyalty") if user else None,
            "products": product_names,
            "lines_in_audit": line_count,
            "grand_total": order.total,
        }


if __name__ == "__main__":
    # Tiny demo so the program "runs correctly"
    app = MegaApp()
    app.register_user(
        name="Alice", age=30, email="alice@example.com", address="123 Lane",
        city="Karachi", country="PK", postal_code="75500", phone="000-0000",
        subscribe_newsletter=True, referral_code=None
    )
    app.add_product("p1", "Notebook", 120.0)
    app.add_product("p2", "Pen", 10.0)

    order = app.process_order("alice@example.com", ["p1", "p2"])  # Long method in action
    summary = ReportGenerator().summarize_order(order, app)
    print("Order Total:", order.total)
    print("Summary:", summary)
