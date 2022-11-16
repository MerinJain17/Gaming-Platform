from django.db import models

# Create your models here.
class Review(models.Model):
    feedback=(
        ('verygood',"Very Good"),
        ('good',"Good"),
        ('mediocre',"Mediocre"),
        ('bad',"Bad"),
        ('verybad',"Very Bad")

    )
    feedback=models.CharField(max_length=10,choices=feedback)
    desc=models.TextField()
    date=models.DateField()
    
    
    def __str__(self) :
        return self.feedback