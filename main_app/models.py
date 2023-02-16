from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

ITEM_STATUS=(
    ('1','Ready to Trade'),
    ('2','Traded')
)
TRADE_STATUS=(
    ('1','Proposed'),
    ('2','Approved'),
    ('3','Denied')
)
CATEGORY_STATUS=(
    ('Clothing', 'Clothing'),
    ('Electronics', 'Electronics'),
    ('Sporting Goods', 'Sporting Goods'),
    ('Jewelry', 'Jewelry'),
    ('Entertainment', 'Entertainment'),
    ('Other', 'Other')
)

# Create your models here.

class Item(models.Model):
    name=models.CharField(max_length=150)
    description=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.CharField(
        max_length=15,
        choices=CATEGORY_STATUS,
        default=CATEGORY_STATUS[0][0]
    )
    status=models.CharField(
        max_length=1,
        choices=ITEM_STATUS,
        default=ITEM_STATUS[0][0]
    )
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('item_detail',  kwargs={'pk': self.id})
    
class Trade(models.Model):
    item_primary=models.ForeignKey(Item, related_name="trade_primary", on_delete=models.CASCADE)
    item_proposed=models.ForeignKey(Item, related_name="trade_proposed", on_delete=models.CASCADE)
    comment=models.CharField(max_length=1000, blank=True)
    status=models.CharField(
        max_length=1,
        choices=TRADE_STATUS,
        default=TRADE_STATUS[0][0]
    )
    def __str__(self):
        return f"trade {self.item_primary} for {self.item_proposed}"
    def get_absolute_url(self):
        return reverse('trades_index')
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    def __str__(self):
        return f"Photo for item_id: {self.item_id} @{self.url}"
    
    


