from restaurateur.restaurants_coordinates import calculate_distance


def add_restaurants_orders(restaurants, orders):
    orders_restaurants = {}
    for order in orders:
        order_products = []
        for order_product in order.order_product.prefetch_related('product'):
            order_products.append(order_product.product.name)
        restaurant_matches_count = {}

        for restaurant in restaurants:
            if not restaurant.product.name in order_products:
                continue
            matches_number = restaurant_matches_count.get(
                restaurant.restaurant.name, 0)
            restaurant_matches_count[
                restaurant.restaurant.name] = matches_number + 1
            if not restaurant_matches_count[restaurant.restaurant.name] >= len(order_products):
                continue
            order.restaurant = restaurant.restaurant
            order.save()
            calculated_distance = calculate_distance(
                restaurant.restaurant, order.address)

            orders_restaurants[order.id] = sorted(
                orders_restaurants.get(order.id, []) + [
                    (restaurant.restaurant.name, calculated_distance)],
                key=lambda restaurant: restaurant[1])
    return orders_restaurants
