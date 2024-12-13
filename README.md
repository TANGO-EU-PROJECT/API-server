# Resource API
This API allows managing sensors, resources, and access permissions.

## Endpoints
### 1. http://api-server.testing1.k8s-cluster.tango.rid-intrasoft.eu/add_permission - Allows adding a new permission for a user, specifying their role and the resources they have access to.
**Method**: POST
**Body**: JSON
{
    "user_id": "user789",
    "role": "admin",
    "action": "GET",
    "resources": ["/temperature", "/humidity"]
}
### 2. http://api-server.testing1.k8s-cluster.tango.rid-intrasoft.eu/access_map - Returns the current access map with the assigned permissions.
**Method**: GET

### 3. http://api-server.testing1.k8s-cluster.tango.rid-intrasoft.eu/resource/<resource_type> - Returns the sensors of a specific type (e.g., temperature, humidity, pressure).
**Method**: GET
**Permissions**: User and role can be added in the query parameters to check permissions.
Example: /resource/temperature?id=user123&role=employee

### 4. http://api-server.testing1.k8s-cluster.tango.rid-intrasoft.eu/resource/<resource_type> - Adds a new sensor of a specific type, along with its values and unit of measurement.
**Method**: POST
**Body**: JSON
{
    "sensor": "sensor5",
    "unit": "Celsius",
    "measure": "temperature",
    "values": [
        {"value": 22.5, "timestamp": "2024-09-09T12:09:00Z"},
        {"value": 23, "timestamp": "2024-09-09T12:10:00Z"}
    ]
}
**Permissions**: User and role can be added in the query parameters to check permissions.
Example: /resource/temperature?id=user456&role=leader
