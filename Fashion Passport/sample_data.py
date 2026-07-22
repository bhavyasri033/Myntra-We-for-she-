"""
Sample Data and Mock Repository Module (Upgraded)
=================================================
Provides seed regional stores, regional fashion products (Product -> Store -> Region hierarchy),
and an in-memory repository store for simulating production persistence.
"""

from typing import Dict, List, Optional, Any
from models import Product, RegionalStore, UserPassport
from config import REGION_METADATA

# Seed Regional Fashion Icon Stores (Tier-2 & Tier-3 Regional Champions)
SAMPLE_STORES: List[RegionalStore] = [
    RegionalStore(
        store_id="STORE_HYD_01",
        store_name="Charminar Heritage Silks",
        region="Hyderabad",
        city="Hyderabad",
        state="Telangana",
        description="Famous for century-old regal Zardozi embroidery, Nizam bridal wear, and pure Hyderabad pearls.",
        rating=4.9,
        logo_icon="store_charminar_logo.png",
        banner_image="store_charminar_banner.jpg"
    ),
    RegionalStore(
        store_id="STORE_HYD_02",
        store_name="Pochampally Weaves Hub",
        region="Hyderabad",
        city="Hyderabad",
        state="Telangana",
        description="Authentic GI-tagged Pochampally Ikkat silk and Telia Rumal handcrafted garments.",
        rating=4.7,
        logo_icon="store_pochampally_logo.png",
        banner_image="store_pochampally_banner.jpg"
    ),
    RegionalStore(
        store_id="STORE_BLR_01",
        store_name="Indiranagar Sustainable Studio",
        region="Bengaluru",
        city="Bengaluru",
        state="Karnataka",
        description="Modern eco-conscious fashion label creating upcycled indie fusion wear.",
        rating=4.8,
        logo_icon="store_indiranagar_logo.png",
        banner_image="store_indiranagar_banner.jpg"
    ),
    RegionalStore(
        store_id="STORE_BLR_02",
        store_name="Garden City Artisans",
        region="Bengaluru",
        city="Bengaluru",
        state="Karnataka",
        description="Premier hub for contemporary Kanjeevaram fusion sarees and silk outerwear.",
        rating=4.6,
        logo_icon="store_gardencity_logo.png",
        banner_image="store_gardencity_banner.jpg"
    ),
    RegionalStore(
        store_id="STORE_VJA_01",
        store_name="Krishna River Loom Crafts",
        region="Vijayawada",
        city="Vijayawada",
        state="Andhra Pradesh",
        description="Heritage weaving cluster producing world-renowned Mangalagiri cottons and Kalamkari prints.",
        rating=4.8,
        logo_icon="store_krishna_logo.png",
        banner_image="store_krishna_banner.jpg"
    ),
    RegionalStore(
        store_id="STORE_VIZAG_01",
        store_name="Bayfront Artisan Boutique",
        region="Visakhapatnam",
        city="Visakhapatnam",
        state="Andhra Pradesh",
        description="Coastal breezy resortwear and handcrafted Etikoppaka wooden-beaded accessories.",
        rating=4.7,
        logo_icon="store_bayfront_logo.png",
        banner_image="store_bayfront_banner.jpg"
    ),
    RegionalStore(
        store_id="STORE_IND_01",
        store_name="Malwa Heritage Looms",
        region="Indore",
        city="Indore",
        state="Madhya Pradesh",
        description="Traditional weavers of tissue Maheshwari sarees and golden Chanderi festive apparel.",
        rating=4.9,
        logo_icon="store_malwa_logo.png",
        banner_image="store_malwa_banner.jpg"
    )
]

# Seed Products linked directly to Regional Stores & Regions
SAMPLE_PRODUCTS: List[Product] = [
    # Hyderabad Store Products
    Product(
        product_id="PROD_HYD_01",
        product_name="Royal Zardozi Silk Saree",
        store_id="STORE_HYD_01",
        store_name="Charminar Heritage Silks",
        region="Hyderabad",
        category="Ethnic Wear",
        price=12499.00
    ),
    Product(
        product_id="PROD_HYD_02",
        product_name="Handcrafted Pearl Nizam Sherwani",
        store_id="STORE_HYD_01",
        store_name="Charminar Heritage Silks",
        region="Hyderabad",
        category="Men's Festive",
        price=18999.00
    ),
    Product(
        product_id="PROD_HYD_03",
        product_name="Telia Rumal Designer Kurta",
        store_id="STORE_HYD_02",
        store_name="Pochampally Weaves Hub",
        region="Hyderabad",
        category="Fusion Wear",
        price=3499.00
    ),

    # Bengaluru Store Products
    Product(
        product_id="PROD_BLR_01",
        product_name="Eco-Linen Indie Trench Jacket",
        store_id="STORE_BLR_01",
        store_name="Indiranagar Sustainable Studio",
        region="Bengaluru",
        category="Western Fusion",
        price=5999.00
    ),
    Product(
        product_id="PROD_BLR_02",
        product_name="Kanjeevaram Fusion Crop Top Set",
        store_id="STORE_BLR_02",
        store_name="Garden City Artisans",
        region="Bengaluru",
        category="Modern Ethnic",
        price=7499.00
    ),

    # Vijayawada Store Products
    Product(
        product_id="PROD_VJA_01",
        product_name="Mangalagiri Cotton Handloom Saree",
        store_id="STORE_VJA_01",
        store_name="Krishna River Loom Crafts",
        region="Vijayawada",
        category="Traditional Weaves",
        price=4299.00
    ),
    Product(
        product_id="PROD_VJA_02",
        product_name="Kalamkari Hand-printed Dupatta",
        store_id="STORE_VJA_01",
        store_name="Krishna River Loom Crafts",
        region="Vijayawada",
        category="Accessories",
        price=1899.00
    ),

    # Visakhapatnam Store Products
    Product(
        product_id="PROD_VIZAG_01",
        product_name="Breezy Coastal Handloom Linen Dress",
        store_id="STORE_VIZAG_01",
        store_name="Bayfront Artisan Boutique",
        region="Visakhapatnam",
        category="Casual Resortwear",
        price=3799.00
    ),
    Product(
        product_id="PROD_VIZAG_02",
        product_name="Tribal Etikoppaka Beaded Jacket",
        store_id="STORE_VIZAG_01",
        store_name="Bayfront Artisan Boutique",
        region="Visakhapatnam",
        category="Craft Outerwear",
        price=4899.00
    ),

    # Indore Store Products
    Product(
        product_id="PROD_IND_01",
        product_name="Maheshwari Tissue Silk Dupatta",
        store_id="STORE_IND_01",
        store_name="Malwa Heritage Looms",
        region="Indore",
        category="Ethnic Wear",
        price=2999.00
    ),
    Product(
        product_id="PROD_IND_02",
        product_name="Chanderi Gold Thread Anarkali",
        store_id="STORE_IND_01",
        store_name="Malwa Heritage Looms",
        region="Indore",
        category="Festive Wear",
        price=8999.00
    )
]


class InMemoryRepository:
    """
    Mock In-Memory Repository simulating a Database layer (PostgreSQL/Redis).
    Exposes stores, products, regions, and user state persistence.
    """

    def __init__(self):
        self._users: Dict[str, UserPassport] = {}
        self._stores: Dict[str, RegionalStore] = {
            s.store_id: s for s in SAMPLE_STORES
        }
        self._products: Dict[str, Product] = {
            p.product_id: p for p in SAMPLE_PRODUCTS
        }
        self._region_metadata = REGION_METADATA

    def get_or_create_user(self, user_id: str) -> UserPassport:
        """Retrieves existing user passport or initializes a new user."""
        if user_id not in self._users:
            user = UserPassport(user_id=user_id)
            # Add initial timeline event
            user.timeline.append({
                "timeline_id": "TL_JOIN",
                "title": "Fashion Passport Joined",
                "description": "Began exploring regional fashion icon stores across India on Myntra!",
                "event_type": "MILESTONE",
                "icon": "passport_joined.png",
                "timestamp": user.joined_at
            })
            self._users[user_id] = user
        return self._users[user_id]

    def save_user(self, user_passport: UserPassport) -> None:
        """Saves user passport state."""
        self._users[user_passport.user_id] = user_passport

    def get_product(self, product_id: str) -> Optional[Product]:
        """Retrieves a product by ID."""
        return self._products.get(product_id)

    def get_store(self, store_id: str) -> Optional[RegionalStore]:
        """Retrieves a regional store by ID."""
        return self._stores.get(store_id)

    def get_store_by_name(self, store_name: str) -> Optional[RegionalStore]:
        """Finds a regional store by name."""
        for store in self._stores.values():
            if store.store_name.lower() == store_name.lower():
                return store
        return None

    def list_all_products(self) -> List[Product]:
        """Lists all seed products."""
        return list(self._products.values())

    def list_all_stores(self) -> List[RegionalStore]:
        """Lists all seed regional fashion stores."""
        return list(self._stores.values())

    def get_region_metadata(self, region: str) -> Optional[Dict[str, Any]]:
        """Returns metadata for a specific region."""
        return self._region_metadata.get(region)
