def register_blueprints(app):

    from kite.auth import auth_bp

    app.register_blueprint(auth_bp)

    # v3 API Endpoints
    from kite.api.v3.posts import posts_bp_v3
    from kite.api.v3.replies import replies_bp_v3
    from kite.api.v3.topics import topics_bp_v3
    from kite.api.v3.users import users_bp_v3

    app.register_blueprint(replies_bp_v3)
    app.register_blueprint(posts_bp_v3)
    app.register_blueprint(topics_bp_v3)
    app.register_blueprint(users_bp_v3)
