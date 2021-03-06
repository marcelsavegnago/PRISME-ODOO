﻿from report import report_sxw
from osv import osv
import netsvc
from macpath import split
from datetime import datetime

class prisme_accounting_parser(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(prisme_accounting_parser, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            "get_back_prefix": self._get_back_prefix,
            "get_date": self._get_date,
            "sorts_lines": self._sorts_lines,
            })
        self.context = context
    
    #return prefix of stock picking out
    def _get_back_prefix(self):
        
        related_prefix = []
        obj_prefix = self.pool.get("ir.sequence")
        related_prefix_ids = obj_prefix.search(self.cr, self.uid,
                              [("code", "=", "stock.picking.out"),])
        if related_prefix_ids:
            related_prefix = obj_prefix.browse(self.cr, self.uid, \
                                                     related_prefix_ids)
        return related_prefix[0].prefix
    
    #return date of sale by id of line
    def _get_date(self, line):
        
        id = line.id
        id = str(id)
        self.cr.execute("SELECT order_line_id FROM sale_order_line_invoice_rel WHERE invoice_id = "+ id)
        orderId = self.cr.fetchone()[0]
        
        relard_Stock=[]
        obj_Stock = self.pool.get("stock.move")
        related_Stock_ids = obj_Stock.search(self.cr, self.uid,
                              [("sale_line_id", "=", orderId),])
        if related_Stock_ids:
            relard_Stock = obj_Stock.browse(self.cr, self.uid, \
                                             related_Stock_ids)
        return relard_Stock[0].date_expected
    
    #return a dictionary of lines
    #differentiate between standard line and line of a combined delivery bulltin
    def _sorts_lines(self, lines):
        
        #import pdb
        #pdb.set_trace() 
        
        list_lines = []
        #sort by name
        linesstored = sorted(lines, key=lambda lines: lines.sequence, reverse=False)
        lasthead =''
        for l in linesstored:
            dic_lines = {}
            dic_lines['name'] = l.name
            #dic_lines['name']= l.product_id.name + ' \n ' + l.name
            splitedline = l.name.split('-')
            #if line is start with 'stock picking out' (OUT/)
            if splitedline[0].startswith(self._get_back_prefix()):
                #if the head is NOT allready know
                if lasthead!=splitedline[0]:
                    lasthead=splitedline[0]
                    dic_head={}
                    d_date = datetime.strptime(self._get_date(l), '%Y-%m-%d %H:%M:%S')
                    s_day = d_date.strftime('%d.%m.%Y').strip()
                    dic_head['pick']=str(splitedline[0])
                    dic_head['pickdate']= s_day
                    #the fields 'note' is not in v7.0
                    #dic_head['note']=''
                    dic_head['page_break'] = ''
                    dic_head['name']=''
                    list_lines.append(dic_head)
                    dic_lines['name']= '- '+splitedline[1]
                    
                else:
                    dic_lines['name']= '- '+splitedline[1]
            dic_lines['tax'] = ' ,'.join([ lt.name or '' for lt in l.invoice_line_tax_id ])
            dic_lines['quantity'] = l.quantity
            if l.uos_id:
              dic_lines['uos_name'] = l.uos_id.name
            else:
              dic_lines['uos_name'] = ''
            dic_lines['price_unit'] = l.price_unit
            dic_lines['discount'] = l.discount
            dic_lines['discount_type'] = l.discount_type
            dic_lines['price_subtotal'] = l.price_subtotal
            #the fields 'note' is not in v7.0
            #dic_lines['note'] = l.note
            dic_lines['pick'] = ''
            dic_lines['page_break'] = l.page_break
            #add dictionary in line
            list_lines.append(dic_lines)
        return list_lines

# Change default print report to custom prisme report 
class account_invoice(osv.osv):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    
    def invoice_print(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'sent': True}, context=context)
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.invoice.email.prisme',
            'datas': datas,
            'nodestroy' : True
        }
account_invoice()



    
report_sxw.report_sxw(
        'report.account.invoice.paper.prisme',
        'account.invoice',
        rml='addons/prisme_outputs_accounting/report/invoice.rml',
        parser=prisme_accounting_parser
    )

report_sxw.report_sxw(
        'report.account.invoice.email.prisme',
        'account.invoice',
        rml='addons/prisme_outputs_accounting/report/invoice.rml',
        parser=prisme_accounting_parser
    )
