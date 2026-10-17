import uuid

from django.db import models


class Product(models.Model):
    class PackageUnit(models.TextChoices):
        GRAM = "g", "Gram"
        MILLILITER = "ml", "Milliliter"
        PIECE = "pcs", "Piece"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    barcode = models.CharField(max_length=32, unique=True, null=True, blank=True)
    name = models.TextField()
    brand = models.TextField(blank=True, default="")
    package_quantity = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        null=True,
        blank=True,
    )
    package_unit = models.CharField(
        max_length=16,
        choices=PackageUnit,
        blank=True,
        default="",
    )
    image_url = models.URLField(max_length=500, blank=True, default="")
    source_updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.brand:
            return f"{self.brand} — {self.name}"
        return self.name


class ProductNutrition(models.Model):
    class BasisUnit(models.TextChoices):
        PER_100_GRAMS = "100g", "Per 100 grams"
        PER_100_MILLILITERS = "100ml", "Per 100 milliliters"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="nutrition",
    )
    basis_unit = models.CharField(max_length=8, choices=BasisUnit)
    energy_kcal = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    protein_g = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    fat_g = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    saturated_fat_g = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    carbohydrates_g = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    sugars_g = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    fiber_g = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    salt_g = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Nutrition for {self.product}"
