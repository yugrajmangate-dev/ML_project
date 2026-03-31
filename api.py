from flask import Blueprint, current_app, jsonify, request
from extensions import cache, limiter

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200


@api_bp.route('/recommend/collab', methods=['GET'])
@limiter.limit("20 per minute")
@cache.cached(timeout=60, query_string=True)
def recommend_collab():
    """Return collaborative recommendations for a given customer_id.

    Query params:
    - customer_id: str or int
    - n: number of recommendations (default 5)
    """
    customer_id = request.args.get('customer_id')
    try:
        n = int(request.args.get('n', 5))
    except Exception:
        n = 5

    if not customer_id:
        return jsonify({'error': 'customer_id is required'}), 400

    recommender = current_app.recommender
    res = recommender.recommend_collaborative(customer_id, n)
    if 'error' in res:
        return jsonify(res), 400
    return jsonify(res)


@api_bp.route('/recommend/content', methods=['GET'])
@limiter.limit("40 per minute")
@cache.cached(timeout=60, query_string=True)
def recommend_content():
    """Return content-based recommendations for a product query.

    Query params:
    - q: product StockCode or a search string
    - n: number of recommendations (default 5)
    """
    q = request.args.get('q')
    try:
        n = int(request.args.get('n', 5))
    except Exception:
        n = 5

    if not q:
        return jsonify({'error': 'q (query) is required'}), 400

    recommender = current_app.recommender
    res = recommender.recommend_content(q, n)
    if 'error' in res:
        return jsonify(res), 400
    return jsonify(res)
