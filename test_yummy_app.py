import unittest
from unittest.mock import patch

from yummy_app import YummyApp
import gps_service


# CAP DO 1: Bo test co ban cho san.
class TestEasyLevel(unittest.TestCase):
    """Kiem thu chuc nang co ban tinh tien don hang."""

    def setUp(self):
        self.app = YummyApp()

    def test_calculate_total_for_single_item(self):
        cart = {"pho": 2}
        self.assertEqual(self.app.calculate_order_total(cart), 100000)

    def test_calculate_total_for_multiple_items(self):
        cart = {"pho": 1, "bun": 1}
        self.assertEqual(self.app.calculate_order_total(cart), 95000)

    def test_calculate_total_for_empty_cart(self):
        self.assertEqual(self.app.calculate_order_total({}), 0.0)

    def test_calculate_total_with_zero_quantity(self):
        cart = {"pho": 0}
        self.assertEqual(self.app.calculate_order_total(cart), 0.0)


# CAP DO 2: 4 kich ban ap dung ma khuyen mai theo de bai.
class TestMediumLevel(unittest.TestCase):
    def test_apply_valid_promo_online(self):
        app = YummyApp(network_status="online")
        self.assertEqual(app.apply_promo_code(100000, "GIAM10"), 90000)

    def test_apply_promo_offline_raises_connection_error(self):
        app = YummyApp(network_status="offline")
        with self.assertRaisesRegex(
            ConnectionError, "Khong co ket noi mang de xac thuc ma."
        ):
            app.apply_promo_code(100000, "GIAM10")

    def test_apply_special_promo_on_os_15(self):
        app = YummyApp(os_version=15)
        self.assertEqual(app.apply_promo_code(100000, "NEW_OS_ONLY"), 80000)

    def test_apply_special_promo_on_os_14_raises_value_error(self):
        app = YummyApp(os_version=14)
        with self.assertRaisesRegex(ValueError, "HDH phien ban 15 tro len"):
            app.apply_promo_code(100000, "NEW_OS_ONLY")


# CAP DO 2: 3 kich ban GPS, patch dung noi ham duoc su dung.
class TestHardLevel(unittest.TestCase):
    def setUp(self):
        self.app = YummyApp()

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_nearby_restaurants_in_supported_location(self, mock_gps):
        mock_gps.return_value = (10.0, 105.0)
        self.assertEqual(
            self.app.get_nearby_restaurants(),
            ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
        )
        mock_gps.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_nearby_restaurants_outside_supported_location(self, mock_gps):
        mock_gps.return_value = (20.0, 110.0)
        self.assertEqual(self.app.get_nearby_restaurants(), [])
        mock_gps.assert_called_once_with()

    @patch("yummy_app.gps_service.get_current_location")
    def test_get_nearby_restaurants_when_gps_signal_is_lost(self, mock_gps):
        mock_gps.side_effect = gps_service.GPSSignalLostError("Mat tin hieu GPS")
        self.assertEqual(
            self.app.get_nearby_restaurants(), "Khong the xac dinh vi tri."
        )
        mock_gps.assert_called_once_with()


# Bo sung de kiem tra nhanh ma khuyen mai khong hop le con thieu.
class TestAdditionalCases(unittest.TestCase):
    def test_unknown_item_does_not_change_total(self):
        cart = {"pho": 1, "mon_khong_co_trong_menu": 2}
        self.assertEqual(YummyApp().calculate_order_total(cart), 50000)

    def test_negative_quantity_does_not_reduce_total(self):
        cart = {"pho": -2, "bun": 1}
        self.assertEqual(YummyApp().calculate_order_total(cart), 45000)

    def test_invalid_promo_code_raises_value_error(self):
        with self.assertRaisesRegex(ValueError, "Ma khuyen mai khong hop le"):
            YummyApp().apply_promo_code(100000, "KHONG_TON_TAI")


if __name__ == "__main__":
    unittest.main()
