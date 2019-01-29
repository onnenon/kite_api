def register_blueprints(app):
    from forum_api.resources.auth import auth_bp
    from forum_api.resources.posts import posts_bp
    from forum_api.resources.topics import topics_bp
    from forum_api.resources.users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(topics_bp)
    app.register_blueprint(users_bp)
