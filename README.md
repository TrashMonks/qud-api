# qud-api

This is a Flask REST API designed to serve the [`haberdasher` project.](https://github.com/trashmonks/haberdasher). It uses [hagadias](https://github.com/trashmonks/hagadias) as its backend.

## Endpoints
All endpoints begin with `qud-api/`.

`anatomies`: Available creature anatomies.
```json
{
  "AirWell": [
    {
      "Name": "Upper Dome", 
      "Type": "Head"
    }, 
    {
      "Name": "Back", 
      "Type": "Back"
    }, 
...
```
`wearables`: All equipment that can be equipped to body slots. For the hand slots, this only includes melee weapons.
```json

```