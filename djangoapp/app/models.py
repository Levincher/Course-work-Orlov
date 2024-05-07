from django.db import models

# Create your models here.


NULLABLE = {'blank': True, 'null': True}


# class BaseManager(models.Manager):
#    def get_queryset(self):
#        return super().get_queryset().filter(deleted_at=None)


class BaseModel(models.Model):
    # deleted_at = models.DateTimeField(editable=False, verbose_name=_('deleted_at'), **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, **NULLABLE)

    # objects = BaseManager()
    objects = models.Manager()

    class Meta:
        abstract = True

    # def delete(self, *args, **kwargs):
    #     self.deleted_at = datetime.datetime.now(datetime.timezone.utc)
    #     self.save()


class User(BaseModel):
    nickname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100, **NULLABLE)
    date_of_birth = models.DateField(**NULLABLE)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    company = models.CharField(max_length=100, **NULLABLE)
    profile_description = models.TextField(**NULLABLE)

    objects = models.Manager()

    def __str__(self):
        return self.nickname


class Customer(BaseModel):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE, related_query_name="Customer", default=1)

    objects = models.Manager()

    def __str__(self):
        return self.user.nickname


class Executor(BaseModel):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE, related_query_name="Executor", default=1)
    rating = models.DecimalField(max_digits=2, decimal_places=2, default=0.00)
    fields_of_work = models.CharField(max_length=200, **NULLABLE)

    objects = models.Manager()

    def __str__(self):
        return self.user.nickname


class Order(BaseModel):
    cust_id = models.OneToOneField(Customer, on_delete=models.CASCADE)
    exec_id = models.OneToOneField(Executor, on_delete=models.CASCADE, null=True)
    type_of_order = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    PROCESS_CHOICES = (
        ('In progress', 'In progress'),
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    )
    process = models.CharField(max_length=20, choices=PROCESS_CHOICES, default='Open')
    version = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return f"{self.pk} - Status: {self.process}"


class Payment(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    operation_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    objects = models.Manager()

    def __str__(self):
        return (f"Order: {self.order}, "
                f"Price: {self.price}, "
                f"Operation date: {self.operation_date}")


class Discuss(BaseModel):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    message_sender = Order.cust_id
    message_receiver = Order.exec_id
    message_content = models.TextField(**NULLABLE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Order: {self.order_id} - Content: {self.message_content}"


class Feedback(BaseModel):
    order_id = models.OneToOneField(Order, on_delete=models.CASCADE)
    MARKS = (
        ('1.0', '1.0'),
        ('1.5', '1.5'),
        ('2.0', '2.0'),
        ('2.5', '2.5'),
        ('3.0', '3.0'),
        ('3.5', '3.5'),
        ('4.0', '4.0'),
        ('4.5', '4.5'),
        ('5.0', '5.0'),
    )
    mark = models.CharField(choices=MARKS, max_length=3, default="0.0")
    description = models.TextField(**NULLABLE)

    objects = models.Manager()

    def __str__(self):
        return (f"Order: {self.order_id}, "
                f"Mark: {self.mark}")
