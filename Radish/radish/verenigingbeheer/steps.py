from behave import given, when, then
from time import sleep

def split_and_strip(src, sep=None):
    return [token.strip() for token in src.split(sep)]

@given('ik ben niet op de pagina verenigingen')
def check_pagina(context):
    if context.browser.url == '%s/union/' % context.base_url:
        context.browser.find_link_by_partial_href('user').first.click()
    
@when('ik op de link Verenigingen druk')
def druk_op_link(context):
    context.browser.find_link_by_partial_href('union').first.click()
    
@then('zie ik de pagina vereniging-overzicht')
def check_pagina(context):
    assert context.browser.url == '%s/union/' % context.base_url
    
@then('zie ik een tabel met 2 kolommen "{columns}"')
def step_table(context, columns):
    tables = context.browser.find_by_css('table.table')
    assert len(tables) > 0, 'Geen datatable gevonden'
    table = tables.first
    row = table.find_by_tag('thead') or table.find_by_tag('tr')
    head = row.first.text
    for col in split_and_strip(columns, ','):
        assert col in head, 'Kolom "%s" niet gevonden in "%s"' % (col, head)
        
@given('ik ben op de pagina vereniging-overzicht')
def check_pagina(context):
    if context.browser.url == '%s/union/' % context.base_url:
        pass
    else:
        context.browser.visit('%s/union/' % context.base_url)

@when('ik op de knop voeg vereniging toe druk')
def druk_op_knop(context):
    context.browser.find_link_by_partial_href('vereniging/0').first.click()
    
@then('zie ik een pagina waar ik een vereniging kan toevoegen')
def check_pagina(context):
    assert context.browser.url == '%s/vereniging/0' % context.base_url
    assert context.browser.is_text_present('Vereniging bewerken')
    
@given('ik ben op de pagina waar ik een vereniging kan toevoegen')
def check_pagina(context):
    if context.browser.is_text_present('Vereniging bewerken'):
        pass
    else:
        context.browser.visit('%s/vereniging/0' % context.base_url)
        
@given('het veld afkorting is leeg')
def check_veld_afkorting(context):
    value = context.browser.find_by_id('afkorting').first.value
    if value == '':
        pass
        
#@when('ik op de knop verwerken druk')        wordt al in een andere stepfile(tochtenbeheer/steps.py) gedaan
    
@then('wordt er geen vereniging toegevoegd')
def check_pagina(context):
    assert context.browser.url == '%s/vereniging/0' % context.base_url
    assert context.browser.is_text_present('Vereniging bewerken')

@when('ik vul het veld afkorting in')
def vul_afk_in(context):
    context.afkorting_vereniging = 'VCRW'
    context.browser.find_by_id('afkorting').first.fill(context.afkorting_vereniging)
    
@when('ik vuld het veld naam in')
def vul_naam_in(context):
    context.naam_vereniging = 'Vereniging ter Controle van Ren%s\'s Werk' % '\xe9'
    context.browser.find_by_id('naam').first.fill(context.naam_vereniging)
    
@then('wordt de vereniging toegevoegd')
def check_toevoeging(context):
    rows = context.browser.find_by_tag('tr')
    row = rows[-1]
    cells = row.find_by_tag('td')
    assert cells[0].value == context.afkorting_vereniging, cells[0].value
    assert cells[1].value == context.naam_vereniging, cells[1].value

@then('verwijdert behave de vereniging voor volgende tests')
def verwijder_toegevoegde_vereniging(context):
    rows = context.browser.find_by_tag('tr')
    row = rows[-1]
    cells = row.find_by_tag('td')
    if cells[0].value == context.afkorting_vereniging:
        try:
            cell[0].click()
            context.browser.find_by_xpath('//a[@onclick="delete_item()"]').click()
        except:
            assert False, 'verwijderknop niet aanwezig'
# verenigingen kunnen niet verwijderd worden