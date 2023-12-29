# Integration-JSM-Odoo

## Introduction
Integration for JSM and Odoo. Takes a JSM webrequest (POST) as input and fetches data from Odoo. Returns data to JSM automation to update ticket

### Usage

- POST request
  - Headers:
    - Authorization: Bearer [token]
  - Body:

	```json
	{"fields":{
	    "issue_type": "bug",
	    "email": "test@example.com",
	    "customfield_10408":"52129A0001,52132B0127"
	    }
	}
	```
	- "customfield_10408": \[serial number to search]
- Requires ID-token from SA:
  - odoo_trigger_stage
    or
  - odoo_trigger_prod

## Deploy
### PROD
>gcloud functions deploy odoo_prod \
 --gen2 \
 --region=europe-west1 \
 --source=. \
 --min-instances 0 \
 --max-instances 6 \
 --timeout 540 \
 --entry-point main \
 --runtime python311 \
 --trigger-http \
 --set-secrets= \
 --service-account odoo-function-prod@integration-jsm-odoo.iam.gserviceaccount.com \
 --project integration-jsm-odoo

>Failed.
ERROR: (gcloud.functions.deploy) OperationError: code=3, message=Build failed with status: FAILURE and message: *** Error compiling './product.py'...
  File "./product.py", line 22
    def _get_


# Needs restructure:
## Tables and keys

Required data:
- Part 3:
  - Order Reference
  - Sent From Hapro
  - Sent From Flex
  - Sent From BGL
  - Customer ref:

### stock_move_line_model = odoo.env["stock.move.line"]
key: lot_name = Serial number
- product_id: list[int, str] ie: [22, '200-000005']
- picking ID: list[int, str] ie: [757, 'Torun/OUT/00429']

### picking_model = odoo.env["stock.picking"]

### 3 sale_order_model = odoo.env["sale.order"]
Key: sale_order_id
- Order Reference: Str [SO9999]
- Sent From Hapro: Date or False [2018-01-22 10:42:31]
- Sent From Flex: Date or False [2018-01-22 10:42:31]
- Sent From BGL: Date or False [2018-01-22 10:42:31]
- Customer Reference: Str[112217000176766 and 112217000176767]
- Tracking No: int|str or False
- Tracking No Flex: int|str or False
- Customer (partner_id): list[3133, 'Company name Inc, Person']

### order_line_model = odoo.env['sale.order.line']
Key:




### 4 odoo.env["res.partner"]
key: id (int)
other identifier: email
fields_to_fetch = ["name", "street", "city", "zip", "state_id", "country_id", "ref", "is_company"]

