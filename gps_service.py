class GPSSignalLostError(Exception):
    """Ngoai le tuy chinh khi thiet bi mat tin hieu dinh vi GPS."""
    pass


def get_current_location():
    """
    Ham mo phong truy cap phan cung GPS dien thoai de lay toa do.
    Trong moi truong kiem thu tu dong, ham nay se duoc dong the (mock).
    """
    return (10.0, 105.0)
