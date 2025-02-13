# coding=utf-8
""""
---Logic file---

By BlockMaster
"""
import difflib
import db_manager


class NoCloseMatchException(Exception):
    pass


def calculate(private_km, community_km, food_type, at_home, at_restaurant, kilowatts):
    private_km_res = private_km * 200
    community_km_res = community_km * 50
    if food_type:  # vegan - true
        at_home_res = at_home * 2
        at_restaurant_res = at_restaurant * 2.5
    else:
        at_home_res = at_home * 4
        at_restaurant_res = at_restaurant * 6
    kilowatts_res = kilowatts * 500
    summ = private_km_res + community_km_res + at_home_res + at_restaurant_res + kilowatts_res
    private_km_per = private_km_res / summ * 100
    community_km_per = community_km_res / summ * 100
    at_home_per = at_home_res / summ * 100
    at_restaurant_per = at_restaurant / summ * 100
    kilowatts_per = kilowatts_res / summ * 100
    return {"private_km": private_km_res, "private_km_per": private_km_per, "community_km": community_km_res, "community_km_per": community_km_per, "at_home": at_home_res, "at_home_per": at_home_per,
            "at_restaurant": at_restaurant_res, "at_restaurant_per": at_restaurant_per, "kw": kilowatts_res, "kw_per": kilowatts_per, "all" : summ}


def find_match(text):
    db_controller = db_manager.DB()
    countries_list = db_controller.get_countries()
    match_ = difflib.get_close_matches(text, countries_list, n=1)
    if not match_:
        raise NoCloseMatchException("No matches")
    else:
        return match_[0]
