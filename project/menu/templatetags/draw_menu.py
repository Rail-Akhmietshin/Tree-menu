from django import template

from menu.models import Submenu, Menu

register = template.Library()


@register.simple_tag
def get_main_menu():
    return Menu.objects.all()


@register.inclusion_tag("menu/draw_menu.html", takes_context=True)
def draw_menu(context, menu):
    suitable_submenu = Submenu.objects.filter(menu__name=menu).values()

    main_submenus = list(suitable_submenu.filter(parent_submenu_id=None))  # main submenus of the main menu

    data = {
        'main_submenus': main_submenus,
        'menu': menu,
    }

    request_path = context.get('request').get_full_path()

    if '&' not in request_path:
        return data
    else:
        current_submenu_id = request_path.split("&").pop().split("=").pop()
        current_submenu = suitable_submenu.get(id=current_submenu_id)

        lower_draw_submenu = list(suitable_submenu.filter(parent_submenu_id=current_submenu['id']))

        if current_submenu in main_submenus:
            main_submenus[main_submenus.index(current_submenu)]["sub_submenu"] = lower_draw_submenu
        else:
            upper_draw_submenu = get_upper_draw_submenu(
                suitable_submenu, suitable_submenu.get(id=current_submenu['id']), main_submenus
            )
            current_submenu["sub_submenu"] = lower_draw_submenu
            draw_submenu = upper_draw_submenu + [current_submenu]

            data['main_submenus'] = get_undiscovered_roots(main_submenus, suitable_submenu, draw_submenu)

    return data


def get_upper_draw_submenu(suitable_submenus, current_submenu, main_submenus):
    suitable_submenu = []
    parent_submenu = current_submenu.get('parent_submenu_id')
    while parent_submenu:
        head_submenu = suitable_submenus.get(id=parent_submenu)
        if head_submenu not in main_submenus:
            suitable_submenu.append(head_submenu)
            parent_submenu = head_submenu.get('parent_submenu_id')
        else:
            break
    return suitable_submenu


def get_undiscovered_roots(main_submenus, suitable_submenu, draw_submenu):
    for submenu in draw_submenu:
        upper_draw_submenu_opened = suitable_submenu.exclude(id=submenu['id'])
        for collection in [main_submenus, draw_submenu]:
            submenus_main_submenus = list(filter(lambda x: x['id'] == submenu['parent_submenu_id'], collection))
            if submenus_main_submenus:
                upper_draw_submenu_opened = list(
                    upper_draw_submenu_opened.filter(parent_submenu_id=submenus_main_submenus[0]['id'])
                )
                submenus_found_submenus_id = collection.index(*submenus_main_submenus)
                collection[submenus_found_submenus_id]['sub_submenu'] = [submenu] + upper_draw_submenu_opened
    return main_submenus
