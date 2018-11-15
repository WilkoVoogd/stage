from behave import given, when, then
from time import sleep

def split_and_strip(src, sep=None):
    return [token.strip() for token in src.split(sep)]

#@given('ik ben ingelogd')                                                     #wordt al gedaan in andere stepfile(uitloggen)
#def ingelogd_check(context):
 #   loggedoff_url = '%s/login?next=%%2F' % context.base_url
  #  base_url = context.base_url
   # context.browser.visit(base_url)
    #if context.browser.url == loggedoff_url:                                
     #   context.browser.find_by_id('email').first.fill('admin')             #moet makkelijker kunnen
      #  context.browser.find_by_id('password').first.fill('nimda')          #
       # context.browser.find_by_id('submit').first.click()                  #
    #assert context.browser.url != loggedoff_url 
    
@given('ik ben op de pagina ledenoverzicht')
def check_pagina(context):
    if context.browser.url != '%s/lid/' % context.base_url:
        context.browser.visit('%s/lid/' % context.base_url)

@given('ik ben niet op de pagina ledenoverzicht')
def check_pagina_niet_ledenoverzicht(context):
    if context.browser.url == '%s/lid/' % context.base_url:
        context.browser.find_link_by_partial_href('user').first.click()    

@when('ik op de knop Leden druk')
def klik_leden(context):
    context.browser.find_link_by_partial_href('lid').first.click()
    
@then('kom ik op de pagina Lid-overzicht')
def lid_overzicht(context):
    assert context.browser.url == '%s/lid/' % context.base_url
    
@then('zie ik een tabel met kolommen "{columns}"')
def step_table(context, columns):
    tables = context.browser.find_by_id('lid')
    assert len(tables) > 0, 'Geen datatable gevonden'
    table = tables.first
    row = table.find_by_tag('thead') or table.find_by_tag('tr')
    head = row.first.text
    for col in split_and_strip(columns, ','):
        assert col in head, 'Kolom "%s" niet gevonden in "%s"' % (col, head)  #komt dit goed? check of er een tabel is
        
@when('ik in het zoekveld een achternaam invul')
def zoek_achternaam(context):
    context.lidzoektocht = 'Deelnemer'
    context.browser.find_by_xpath('//input[@type="search"]').first.fill(context.lidzoektocht)
    #sleep(2)
    
@then('zie ik alle leden met die achternaam')
def check_tabel_results(context):
    sleep(2)
    table = context.browser.find_by_tag('tbody')                  
    rows = table.find_by_tag('tr')                                
    values = [row.find_by_tag('td')[2].value for row in rows] 
    assert all(context.lidzoektocht in values for values in values), values