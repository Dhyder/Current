from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets  # For secure key generation

class CustomUser(AbstractUser):
    usb_secret = models.CharField(max_length=255, blank=True, null=True, unique=True)

    # Resolving conflicts with default Django fields
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",
        blank=True
    )

    def generate_usb_secret(self):
        """Generate a new USB secret, save it in DB, and write to USB."""
        self.usb_secret = f"SecretInfinityKey-{secrets.randbelow(99999)}-{secrets.randbelow(99999)}-{secrets.randbelow(99999)}"
        self.save()

        try:
            with open(USB_DRIVE_PATH, "w") as key_file:
                key_file.write(self.usb_secret)
        except Exception as e:
            print(f"⚠️ Error writing USB key: {e}")

        return self.usb_secret
    
