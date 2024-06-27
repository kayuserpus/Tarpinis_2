def get_products_and_categories(selected_category='', search_query=''):
    from app.models import Product
    from app import db
    
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories]
    
    query = Product.query
    
    if selected_category:
        query = query.filter_by(category=selected_category)
    
    if search_query:
        query = query.filter(Product.name.ilike(f'%{search_query}%'))
    
    products = query.all()
    
    return products, categories
