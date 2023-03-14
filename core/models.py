from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.core.exceptions import ValidationError
from .validators import validate_rut
