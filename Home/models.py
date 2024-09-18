from djongo import models

# Create your models here.
class ClientInfo(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=50)
    phoneNo = models.CharField(max_length=10)
    receiveDate = models.DateField()
    productName = models.CharField(max_length=50)
    productimage = models.ImageField(upload_to='product_images/')
    reportedIssue = models.CharField(max_length=50)
    clientNotes = models.CharField(max_length=50)
    assignedTechnician = models.CharField(max_length=50)
    estimatedAmount = models.DecimalField(max_digits=10, decimal_places=2)  # Changed to DecimalField
    deadline = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} - {self.productName}"
