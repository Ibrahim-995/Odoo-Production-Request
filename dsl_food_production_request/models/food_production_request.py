# -*- coding: utf-8 -*-

import time
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta


class Storefood_production_request(models.Model):
    _name = "store.food_production_request"
    _description = "Store Food Production Request"

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    # department_id = fields.Many2one("hr.department", string="Department",
    #                                 default=lambda self: self.env.user.employee.department_id.id)
    employee = fields.Many2one('res.users', readonly="1", string="Employee Name", default=lambda self: self.env.user)
    department = fields.Many2one('hr.department',string="Department")
    requsition_line_ids = fields.One2many('store.food_production_request.line', 'store_food_production_request_id', string='Lines')
    approved_by = fields.Many2one("res.users", string="Approved by")
    approved_date = fields.Date("Approved On")
    confirmed_by = fields.Many2one("res.users", string="Accepted by")
    confirmed_date = fields.Date("Accepted On")
     
    delivered_by = fields.Many2one("res.users", string="Delivered by")
    delivered_date = fields.Date("Delivered On")

    requested_by = fields.Many2one("res.users", string="Requested by")
    requested_date = fields.Date("Requested On")
     
    received_by = fields.Many2one("res.users", string="Received by")
    received_date = fields.Date("Received On")

    rejected_by = fields.Many2one("res.users", string="Rejected by")
    rejected_date = fields.Date("Rejected On")
    state = fields.Selection([('draft', 'Draft'),
                              ('request', 'Request Sent'),
                              ('confirm', 'Request Accepted'),
                              ('approve', 'Approved'),
                              ('delivery', 'Delivered'),
                              ('receive', 'Received'),
                              ('reject', 'Rejected')], string="Status", default='draft')
    # company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    # def _compute_picking_ids(self):
    #     for item in self:
    #         item.picking_count = self.env['stock.picking'].search_count([('store_food_production_request_id', '=', self.id)])

    def request(self):
        self.state = "request"
        self.requested_by = self.env.user.id
        self.requested_date = date.today()

    def confirm(self):
        self.state = "confirm"
        self.confirmed_by = self.env.user.id
        self.confirmed_date = date.today()

    def approve(self):
        self.state = "approve"
        self.approved_by = self.env.user.id
        self.approved_date = date.today()

    def delivery(self):
        self.state = "delivery"
        self.delivered_by = self.env.user.id
        self.delivered_date = date.today()

    def receive(self):
        self.state = "receive"
        self.received_by = self.env.user.id
        self.received_date = date.today()

    def reject(self):
        self.state = "reject"
        self.rejected_by = self.env.user.id
        self.rejected_date = date.today()

    @api.model
    def create(self, values):
        if values.get('name', '/') == '/':
            values['name'] = self.env['ir.sequence'].next_by_code(
                'store.food_production_request')
        return super(Storefood_production_request, self).create(values)

    def unlink(self):
        if self.filtered(lambda r: r.state != 'draft'):
            raise UserError(_('Only requests on draft state can be unlinked'))
        return super(Storefood_production_request, self).unlink()

    @api.onchange('employee')
    def _onchange_employee(self):
        for dep in self:
          if dep.employee:
            dep.department = dep.employee.department_id.id

class Storefood_production_requestLine(models.Model):
    _name = "store.food_production_request.line"
    _description = "Store Food Production Request Line"

    product_id = fields.Many2one("product.product", string="Product")
    uom_id = fields.Many2one("uom.uom", string="Unit of Measure")
    quantity = fields.Integer("Request Quantity")
    store_food_production_request_id = fields.Many2one('store.food_production_request', string='Food Production Request')

#     def get_available_qty(self):
#         for item in self:
#             if item.product_id:
#                 item.available_qty = item.product_id.qty_available
    
#     def get_qty_done(self):
#         for line in self:
#             picking = self.env['stock.picking'].search([('store_food_production_request_id', '=', line.store_food_production_request_id.id)])
#             for item in picking.move_lines:
#                 if item.product_id.id == line.product_id.id:
#                     line.quantity_done = item.quantity_done
    @api.onchange('product_id')
    def onchange_product_id(self):
        for item in self:
            if item.product_id:
                item.uom_id = item.product_id.uom_id.id


# class StockPicking(models.Model):
#     _inherit = "stock.picking"

#     store_food_production_request_id = fields.Many2one('store.food_production_request', string='Food Production Request')
