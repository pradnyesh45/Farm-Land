## API Endpoints

### 1. Get all schedules due for today/tomorrow

```
GET http://localhost:5000/api/schedules/due
```

### 2. Get Farmers by Crop Name

Retrieve all farmers growing a specific crop

```
GET http://localhost:5000/api/farmers/by-crop/<crop_name>
```

### 3. Get Farmer's Bill

Calculate the bill of materials for a specific farmer

```
GET http://localhost:5000/api/farmers/<farmer_id>/bill
```
