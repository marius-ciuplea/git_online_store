from django.db import models

class TimestampedModel(models.Model):
    """
    Un model abstract care adaugă automat câmpuri de dată și oră pentru creare și actualizare.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        # Ordonează implicit după data creării, cel mai nou primul
        ordering = ['-created_at']
