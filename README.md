# API de Recursos

Esta API permite gestionar sensores, recursos y permisos de acceso.

## Endpoints

### 1. http://api-server.testing1.k8s-cluster.tango.rid-intrasoft.eu/access_map/add_permission - Permite agregar un nuevo permiso para un usuario, especificando su rol y recursos a los que tiene acceso.
**Método**: POST
**Body**: JSON
{
    "user_id": "user789",
    "role": "admin",
    "action": "GET",
    "resources": ["/temperature", "/humidity"]
}

### 2. http://api-server.testing1.k8s-cluster.tango.rid-intrasoft.eu/access_map/access_map - Devuelve el mapa de acceso actual con los permisos asignados.
**Método**: GET

### 3. http://api-server.testing1.k8s-cluster.tango.rid-intrasoft.eu/access_map/resource - Devuelve todos los recursos disponibles (sensores).
**Método**: GET

### 4. http://api-server.testing1.k8s-cluster.tango.rid-intrasoft.eu/access_map/resource/<resource_type> - Devuelve los sensores de un tipo específico (por ejemplo, temperature, humidity, pressure).
**Método**: GET
**Permisos**: Se puede añadir usuario y rol en los query parameters para comprobar permisos.
/resource/temperature?id=user123&role=employee

### 5. http://api-server.testing1.k8s-cluster.tango.rid-intrasoft.eu/access_map/resource/<resource_type> - Agregar un nuevo sensor de un tipo específico, junto con sus valores y unidad de medida.
**Método**: POST
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
**Permisos**: Se puede añadir usuario y rol en los query parameters para comprobar permisos.
/resource/temperature?id=user456&role=leader
