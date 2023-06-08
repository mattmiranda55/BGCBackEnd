from django.db import models


class Regulation(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField()
    address = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)


class User(models.Model):
    username = models.CharField()
    first_name = models.CharField()
    last_name = models.CharField()
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Graft(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    regulation = models.ForeignKey(Regulation, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
