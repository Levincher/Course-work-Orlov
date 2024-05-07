from django.contrib import admin

# Register your models here.

from .models import User, Customer, Executor, Feedback, Payment, Order, Discuss
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Executor)
admin.site.register(Feedback)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(Discuss)
