# smelly_app/tests/test_app.py
import unittest
from app import MegaApp, ReportGenerator   # ✅ FIXED IMPORT

class TestSmellyApp(unittest.TestCase):
    def setUp(self):
        self.app = MegaApp()
        self.app.register_user(
            name="Bob", age=28, email="bob@example.com", address="42 Street",
            city="Karachi", country="PK", postal_code="75500", phone="111-1111",
            subscribe_newsletter=False, referral_code="XYZ"
        )
        self.app.add_product("p1", "Bag", 150.0)
        self.app.add_product("p2", "Marker", 5.0)
        self.app.add_product("p3", "Bottle", 60.0)

    def test_register_user_and_duplicates(self):
        # user already exists should raise
        with self.assertRaises(ValueError):
            self.app.register_user(
                name="Bob", age=28, email="bob@example.com", address="42 Street",
                city="Karachi", country="PK", postal_code="75500", phone="111-1111",
                subscribe_newsletter=False, referral_code=None
            )

    def test_add_product_duplicate(self):
        with self.assertRaises(ValueError):
            self.app.add_product("p1", "Another Bag", 10.0)

    def test_process_order_basic_total(self):
        order = self.app.process_order("bob@example.com", ["p2", "p3"])  # 5 + 60 = 65
        # subtotal=65; discount>100? no; tax=0.07*65=4.55; shipping=42 (since <50? no, it's >=50 so 3.14)
        # taxable_amount=65; tax=4.55; shipping=3.14; total=72.69
        self.assertAlmostEqual(order.total, 72.69, places=2)

    def test_process_order_discount_tier(self):
        order = self.app.process_order("bob@example.com", ["p1"])  # 150
        # discount_a/b: >100 => +7.5; loyalty starts 0 => no extra
        # taxable_amount=142.5; tax=9.98; shipping=3.14; total=155.62
        self.assertAlmostEqual(order.total, 155.62, places=2)

    def test_loyalty_increase(self):
        # Big order to push loyalty
        order = self.app.process_order("bob@example.com", ["p1", "p3"])  # 150 + 60 = 210
        # discount>100; taxable_amount≈? 210 - 10.5 = 199.5 -> actually <=200 so loyalty +0? No, it's >100 so +1
        self.assertGreaterEqual(self.app.users["bob@example.com"]["loyalty"], 1)

    def test_report_feature_envy(self):
        order = self.app.process_order("bob@example.com", ["p2"])  # 5
        summary = ReportGenerator().summarize_order(order, self.app)
        self.assertIn("Marker", summary["products"])  # ReportGenerator pokes into order/app
        self.assertEqual(summary["user_name"], "Bob")


if __name__ == "__main__":
    unittest.main()
