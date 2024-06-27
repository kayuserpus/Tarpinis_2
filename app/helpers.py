def get_products_and_categories(selected_category=''):
    from app.models import Product
    from app import db
    
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]  # Extract category names from tuples
    
    if selected_category:
        products = Product.query.filter_by(category=selected_category).all()
    else:
        products = Product.query.all()
    
    return products, categories
