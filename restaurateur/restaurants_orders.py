from restaurateur.restaurants_coordinates import calculate_distance


def add_restaurants_orders(restaurants_menu, orders, apikey):
    orders_restaurants = {}
    for order in orders:
        order_products = []
        for order_product in order.order_products.prefetch_related('product'):
            order_products.append(order_product.product.name)
        restaurant_matches_count = {}

        for restaurant_menu in restaurants_menu:
            if not restaurant_menu.product.name in order_products:
                continue
            matches_number = restaurant_matches_count.get(
                restaurant_menu.restaurant.name, 0)
            restaurant_matches_count[
                restaurant_menu.restaurant.name] = matches_number + 1
            if not restaurant_matches_count[restaurant_menu.restaurant.name] >= len(order_products):
                continue
            order.restaurant = restaurant_menu.restaurant
            order.save()
            calculated_distance = calculate_distance(
                restaurant_menu.restaurant, order.address, apikey)

            orders_restaurants[order.id] = sorted(
                orders_restaurants.get(order.id, []) + [
                    (restaurant_menu.restaurant.name, calculated_distance)],
                key=lambda restaurant: restaurant[1])
    return orders_restaurants
