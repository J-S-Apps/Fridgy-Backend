from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import Product, ProductNutrition


class ProductModelTests(TestCase):
    def test_product_can_be_created_with_barcode(self):
        product = Product.objects.create(
            barcode="4750000000000",
            name="Milk",
            brand="Fridgy",
            package_quantity=Decimal("1000"),
            package_unit=Product.PackageUnit.MILLILITER,
        )

        self.assertEqual(product.barcode, "4750000000000")
        self.assertEqual(str(product), "Fridgy — Milk")

    def test_multiple_products_can_have_null_barcode(self):
        first = Product.objects.create(name="Apple")
        second = Product.objects.create(name="Banana")

        self.assertIsNone(first.barcode)
        self.assertIsNone(second.barcode)

    def test_non_null_barcode_must_be_unique(self):
        Product.objects.create(barcode="4750000000000", name="Milk")

        with self.assertRaises(IntegrityError), transaction.atomic():
            Product.objects.create(barcode="4750000000000", name="Other milk")

    def test_name_must_not_be_blank(self):
        with self.assertRaises(ValidationError):
            Product(name="").full_clean()

    def test_product_string_without_brand_is_name(self):
        product = Product(name="Apple")

        self.assertEqual(str(product), "Apple")

    def test_package_unit_values(self):
        self.assertEqual(
            set(Product.PackageUnit.values),
            {"g", "ml", "pcs"},
        )


class ProductNutritionModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Milk")

    def test_nutrition_can_be_created_for_product(self):
        nutrition = ProductNutrition.objects.create(
            product=self.product,
            basis_unit=ProductNutrition.BasisUnit.PER_100_MILLILITERS,
            energy_kcal=Decimal("60"),
            protein_g=Decimal("3.2"),
        )

        self.assertEqual(self.product.nutrition, nutrition)
        self.assertEqual(str(nutrition), "Nutrition for Milk")

    def test_product_can_have_only_one_nutrition_record(self):
        ProductNutrition.objects.create(
            product=self.product,
            basis_unit=ProductNutrition.BasisUnit.PER_100_GRAMS,
            energy_kcal=Decimal("100"),
        )

        with self.assertRaises(IntegrityError), transaction.atomic():
            ProductNutrition.objects.create(
                product=self.product,
                basis_unit=ProductNutrition.BasisUnit.PER_100_GRAMS,
                energy_kcal=Decimal("101"),
            )

    def test_nutrition_can_be_created_without_known_values(self):
        nutrition = ProductNutrition.objects.create(
            product=self.product,
            basis_unit=ProductNutrition.BasisUnit.PER_100_GRAMS,
        )

        self.assertIsNone(nutrition.energy_kcal)

    def test_deleting_product_deletes_nutrition(self):
        nutrition = ProductNutrition.objects.create(
            product=self.product,
            basis_unit=ProductNutrition.BasisUnit.PER_100_GRAMS,
            energy_kcal=Decimal("100"),
        )

        self.product.delete()

        self.assertFalse(ProductNutrition.objects.filter(pk=nutrition.pk).exists())

    def test_basis_unit_values(self):
        self.assertEqual(
            set(ProductNutrition.BasisUnit.values),
            {"100g", "100ml"},
        )
