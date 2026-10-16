import gps_service

MENU = {
    "pho": 50000,
    "bun": 45000,
    "com": 30000,
}

PROMO_CODES = {
    "GIAM10": {"discount": 0.1, "min_os_version": 0},
    "NEW_OS_ONLY": {"discount": 0.2, "min_os_version": 15},
}

RESTAURANTS_BY_LOCATION = {
    "10.0,105.0": ["Nha hang Pho Ly Quoc Su", "Bun cha Huong Lien"],
}


class YummyApp:
    def __init__(self, network_status="online", os_version=15):
        self.network_status = network_status
        self.os_version = os_version

    def calculate_order_total(self, cart: dict) -> float:
        """Tinh tong gia tri don hang dua tren gio hang."""
        total = 0.0
        for item, quantity in cart.items():
            if item in MENU and quantity > 0:
                total += MENU[item] * quantity
        return total

    def apply_promo_code(self, total: float, code: str) -> float:
        """Kiem tra va ap dung ma khuyen mai."""
        if self.network_status == "offline":
            raise ConnectionError("Khong co ket noi mang de xac thuc ma.")
        if code not in PROMO_CODES:
            raise ValueError("Ma khuyen mai khong hop le.")
        promo = PROMO_CODES[code]
        if self.os_version < promo["min_os_version"]:
            raise ValueError(
                f"Ma nay yeu cau HDH phien ban {promo['min_os_version']} tro len."
            )
        return total * (1 - promo["discount"])

    def get_nearby_restaurants(self):
        """Goi dich vu GPS de de xuat nha hang lan can."""
        try:
            lat, lon = gps_service.get_current_location()
            location_key = f"{lat},{lon}"
            return RESTAURANTS_BY_LOCATION.get(location_key, [])
        except gps_service.GPSSignalLostError:
            return "Khong the xac dinh vi tri."
