import flet as ft
from flet_route import Params, Basket
def reload(page,params,basket):
    print(params.page)
    if params.page=='self':
        page.go('/self')
    elif params.page=='ai':
        page.go('/ai')
    elif params.page=='record':
        page.go('/record')