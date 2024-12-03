# FarmLand Backend API

REST API for managing farmer data, farms, and fertilizer schedules.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Application

```bash
docker-compose up --build
```

The server will start at `http://localhost:5000`

## API Endpoints

### Farmers

#### 1. Get All Farmers

```
GET /api/farmers
```

**Response**: `200 OK`

```json
[
  {
    "id": 1,
    "name": "John Doe",
    "phone_number": "1234567890",
    "language": "Hindi"
  }
]
```

#### 2. Get Farmers by Crop

```
GET /api/farmers/by-crop/<crop_name>
```

**Response**: `200 OK`

```json
[
  {
    "farmer_id": 1,
    "farmer_name": "John Doe"
  }
]
```

#### 3. Create Farmer

```
POST /api/farmers
```

**Body**:

```json
{
  "name": "John Doe",
  "phone_number": "1234567890",
  "language": "Hindi"
}
```

**Response**: `201 Created`

#### 4. Update Farmer

```
PUT /api/farmers/<farmer_id>
```

**Response**: `200 OK`

#### 5. Delete Farmer

```
DELETE /api/farmers/<farmer_id>
```

**Response**: `200 OK`

### Farms

#### 1. Get All Farms

```
GET /api/farms
```

**Response**: `200 OK`

```json
[
  {
    "id": 1,
    "area": 4.5,
    "village": "Gorakhpur",
    "crop_grown": "Wheat",
    "sowing_date": "2024-12-01",
    "farmer_id": 1
  }
]
```

#### 2. Create Farm

```
POST /api/farms
```

**Body**:

```json
{
  "area": 4.5,
  "village": "Gorakhpur",
  "crop_grown": "Wheat",
  "sowing_date": "2024-12-01",
  "farmer_id": 1
}
```

**Response**: `201 Created`

#### 3. Update Farm

```
PUT /api/farms/<farm_id>
```

**Response**: `200 OK`

#### 4. Delete Farm

```
DELETE /api/farms/<farm_id>
```

**Response**: `200 OK`

### Schedules

#### 1. Get All Schedules

```
GET /api/schedules
```

**Response**: `200 OK`

```json
[
  {
    "id": 1,
    "days_after_sowing": 30,
    "fertilizer_type": "Urea",
    "quantity": 50,
    "quantity_unit": "kg",
    "farm_id": 1
  }
]
```

#### 2. Get Due Schedules

```
GET /api/schedules/due
```

**Response**: `200 OK`

```json
[
  {
    "schedule_id": 1,
    "farm_id": 1,
    "farmer_id": 1,
    "farmer_name": "John Doe",
    "farm_village": "Gorakhpur",
    "farm_crop_grown": "Wheat",
    "due_date": "2024-12-31"
  }
]
```

#### 3. Create Schedule

```
POST /api/schedules
```

**Body**:

```json
{
  "days_after_sowing": 30,
  "fertilizer_type": "Urea",
  "quantity": 50,
  "quantity_unit": "kg",
  "farm_id": 1
}
```

**Response**: `201 Created`

#### 4. Update Schedule

```
PUT /api/schedules/<schedule_id>
```

**Response**: `200 OK`

#### 5. Delete Schedule

```
DELETE /api/schedules/<schedule_id>
```

**Response**: `200 OK`

## Error Responses

- `400 Bad Request`: Invalid input data
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Database Schema

### Farmer

- id (Primary Key)
- name (String)
- phone_number (String)
- language (String)

### Farm

- id (Primary Key)
- area (Float)
- village (String)
- crop_grown (String)
- sowing_date (DateTime)
- farmer_id (Foreign Key)

### Schedule

- id (Primary Key)
- days_after_sowing (Integer)
- fertilizer_type (String)
- quantity (Float)
- quantity_unit (Enum: 'ton', 'kg', 'g', 'L', 'mL')
- farm_id (Foreign Key)
