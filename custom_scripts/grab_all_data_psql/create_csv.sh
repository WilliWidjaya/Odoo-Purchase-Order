#!/bin/bash

echo "ESKETIIIIT"
psql -d "$2" -c "\copy ($1) TO '$3' WITH CSV HEADER"

# psql rd-user -c '\copy (
# SELECT 
#     po.po_number,
#     po.status,
#     po.name, 
#     po_vendor.name AS "vendor_name",
#     po.vendor_ref_no, 
#     po_contact.name AS "contact_name",
#     po.posting_date,
#     po.due_date,
#     po.payment_date,
#     po.sta_date,
#     po.total_before_disc,
#     po.discount_percentage,
#     po.discounted_value,
#     po.discount_amount,
#     po.tax,
#     po.taxed_amount,
#     po.total_amount,
#     po.payment_terms,
#     po.remarks,
#     po_shipping_location.shipping_location,
#     po_pay_accounts.payment_information,
#     po.ad_vessel_flight,
#     po.ad_container,
#     po.ad_awb,
#     po.ad_pesawat,
#     "ad_vendor_DO_no",
#     "ad_no_tanggal_PIB",
#     "ad_PIB_pesan",
#     po.ad_bank_name,
#     po.ad_pph,
#     po.ad_tgl_bbpcp,
#     po.ad_total_cf,
#     "ad_NDPBM",
#     po.ad_pi_date, 
#     po.ad_tgl_invoice 
# FROM purchase_order po
# LEFT JOIN po_shipping_location ON po.ship_to = po_shipping_location.id
# LEFT JOIN po_pay_accounts ON po.pay_to = po_pay_accounts.id
# LEFT JOIN po_vendor ON po.vendor = po_vendor.id
# LEFT JOIN po_contact ON po.contact_person = po_contact.id

# ) TO 'output.csv' WITH CSV HEADER'
