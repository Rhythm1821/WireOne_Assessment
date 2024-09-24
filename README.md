# WireOne_Assessment


### Objective

This project is a web application with a configurable pricing module that supports **differential pricing**. Built using **Django**, it stores and manages pricing configurations and calculates the final price for a service based on multiple factors like time, distance, and day of the week.

### Features

- **Flexible Pricing Configuration**: Admin can configure base prices, additional prices, time multiplier factors, and waiting charges, customizable by day of the week.
- **API for Price Calculation**: Exposes an API to compute the final cost based on dynamic pricing configurations.
- **Django Admin Interface**: Manage pricing configurations and log configuration changes using Django's built-in admin panel.
- **Logging**: Keeps track of configuration changes including who made the changes and when.
- **Validation & Custom Forms**: Built with validation in mind to ensure correct data entry.

### Pricing Formula

The pricing is calculated using the formula:

***Price = (DBP + (Dn * DAP)) + (Tn * TMF) + WC***

Where:
- `DBP` = Distance Base Price (up to a base limit)
- `Dn` = Additional distance traveled beyond base limit
- `DAP` = Distance Additional Price (per km beyond base limit)
- `Tn` = Time duration (hours)
- `TMF` = Time Multiplier Factor
- `WC` = Waiting Charges

### Models

#### PricingConfig Model
This model stores the pricing configuration for different days of the week:

```python
class PricingConfig(models.Model):
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
    base_distance_price = models.DecimalField(max_digits=6, decimal_places=2)
    base_distance_limit = models.DecimalField(max_digits=4, decimal_places=1)
    additional_price_per_km = models.DecimalField(max_digits=4, decimal_places=2)
    time_multiplier_factor = models.DecimalField(max_digits=3, decimal_places=2)
    waiting_charge_per_minute = models.DecimalField(max_digits=3, decimal_places=2)
    enabled = models.BooleanField(default=True)
```

### PricingConfigLog Model
#### Tracks changes to pricing configurations:

```python
class PricingConfigLog(models.Model):
    config = models.ForeignKey(PricingConfig, on_delete=models.SET_NULL, null=True)
    modified_by = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=255)
```

## API Endpoints

### 1. Create Pricing Configuration

- **URL**: `http://127.0.0.1:8000/pricing/`
- **Method**: `POST`
- **Description**: Allows creation of new pricing configurations.

### 2. Calculate Price

- **URL**: `http://127.0.0.1:8000/pricing/calculate_price/`
- **Method**: `POST`
- **Request Example**:

  ```json
  {
      "distance": 5.0,
      "time": 1.5,
      "waiting_time": 1,
      "day_of_week": "THU"
  }

- **Response Example**:

    ```json
    {
        "total_price": 250.00
    }
    ```

## How to Run
### Clone the repository:

```bash
git clone https://github.com/Rhythm1821/WireOne_Assessment.git
cd WireOne_Assessment
```

### Set up the virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


### Apply migrations:

```bash
python3 manage.py migrate
```

### Run the server:

```bash
python manage.py runserver
Access the application at http://127.0.0.1:8000/admin/
```
