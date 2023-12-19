# Integration-JSM-Odoo
Integration between JSM and Odoo that takes a JSM webrequest as input and fetches data from Odoo. Writes data into specific JSM ticket

Required data:
- Part 3:
  - Order Reference
  - Sent From Hapro
  - Sent From Flex
  - Sent From BGL
  - Customer ref:

# Tables and keys

## stock_move_line_model = odoo.env["stock.move.line"]
key: lot_name = Serial number
- product_id: list[int, str] ie: [22, '200-000005']
- picking ID: list[int, str] ie: [757, 'Torun/OUT/00429']

## picking_model = odoo.env["stock.picking"]

## 3 sale_order_model = odoo.env["sale.order"]
Key: sale_order_id
- Order Reference: Str [SO9999]
- Sent From Hapro: Date or False [2018-01-22 10:42:31]
- Sent From Flex: Date or False [2018-01-22 10:42:31]
- Sent From BGL: Date or False [2018-01-22 10:42:31]
- Customer Reference: Str[112217000176766 and 112217000176767]
- Tracking No: int|str or False
- Tracking No Flex: int|str or False
- Customer (partner_id): list[3133, 'Company name Inc, Person']

## order_line_model = odoo.env['sale.order.line']
Key: 




## 4 odoo.env["res.partner"]
key: id (int)
other identifier: email
fields_to_fetch = ["name", "street", "city", "zip", "state_id", "country_id", "ref", "is_company"]